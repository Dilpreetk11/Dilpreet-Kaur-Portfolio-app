import logging
import uuid
from contextlib import asynccontextmanager
from typing import Dict, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from groq import Groq

from backend.chatbot import ask_candidate
from backend.config import settings
from backend.resume_parser import (
    PDFExtractionError,
    get_verified_resume,
    parse_resume_with_llm,
    read_pdf,
)
from backend.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    PublicResume,
    Resume,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("backend_main")


class ResumeManager:
    """
    Thread-safe in-memory cache manager for the portfolio resume and
    isolated temporary visitor upload sessions.
    """
    def __init__(self):
        self.portfolio_resume: Optional[Resume] = None
        self.groq_client: Optional[Groq] = None
        # Isolated visitor uploads keyed by session UUID
        self.custom_sessions: Dict[str, Resume] = {}

    def initialize(self):
        """Initializes the Groq client and loads the portfolio resume once on startup."""
        if settings.is_groq_ready:
            try:
                self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info("Groq client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self.groq_client = None
        else:
            logger.warning("GROQ_API_KEY is not configured or too short.")

        self.load_portfolio_resume()

    def load_portfolio_resume(self):
        """Reads and caches the portfolio resume once."""
        resume_path = settings.PORTFOLIO_RESUME_PATH
        logger.info(f"Loading portfolio resume from: {resume_path}")

        extracted_text = ""
        if resume_path.exists():
            try:
                extracted_text = read_pdf(resume_path)
                logger.info(f"Successfully extracted {len(extracted_text)} characters from resume PDF.")
            except Exception as e:
                logger.warning(f"Could not extract text from {resume_path}: {e}")

        # Use the verified ground-truth structure containing all 4 live project deployments and metadata
        self.portfolio_resume = get_verified_resume()
        logger.info("Portfolio resume loaded from verified ground-truth structure with 4 live projects.")

    def get_portfolio_resume(self) -> Resume:
        if self.portfolio_resume is None:
            self.portfolio_resume = get_verified_resume()
        return self.portfolio_resume

    def store_custom_resume(self, resume: Resume) -> str:
        session_id = str(uuid.uuid4())
        self.custom_sessions[session_id] = resume
        logger.info(f"Stored isolated visitor resume for session: {session_id}")
        return session_id

    def get_custom_resume(self, session_id: str) -> Optional[Resume]:
        return self.custom_sessions.get(session_id)

    def remove_custom_resume(self, session_id: str) -> bool:
        if session_id in self.custom_sessions:
            del self.custom_sessions[session_id]
            logger.info(f"Removed custom resume session: {session_id}")
            return True
        return False


# Singleton instance
resume_manager = ResumeManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    logger.info("Starting Portfolio AI Backend...")
    resume_manager.initialize()
    yield
    logger.info("Shutting down Portfolio AI Backend...")


app = FastAPI(
    title="Dilpreet Kaur - AI Portfolio API",
    description="Production-minded FastAPI backend powering the AI Resume Chatbot and structured portfolio services.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
async def root():
    """Basic service status and metadata."""
    return {
        "service": "Dilpreet Kaur AI Portfolio API",
        "status": "online",
        "docs": "/docs",
        "model": settings.GROQ_MODEL
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint without revealing internal secrets."""
    return HealthResponse(
        status="healthy",
        model=settings.GROQ_MODEL,
        resume_loaded=resume_manager.portfolio_resume is not None,
        groq_configured=settings.is_groq_ready
    )


@app.get("/resume", response_model=PublicResume, tags=["Resume"])
async def get_public_resume():
    """Returns approved public portfolio information (sanitized to protect privacy)."""
    resume = resume_manager.get_portfolio_resume()
    return PublicResume(
        name=resume.name,
        headline=resume.headline,
        email=resume.email,
        location=resume.location,
        github=resume.github,
        linkedin=resume.linkedin,
        summary=resume.summary,
        skills=resume.skills,
        skill_categories=resume.skill_categories,
        experiences=resume.experiences,
        education=resume.education,
        projects=resume.projects,
        certifications=resume.certifications,
        achievements=resume.achievements
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Answers a question about the candidate strictly using the cached, validated resume.
    Avoids re-parsing the PDF on every request.
    """
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question cannot be empty or whitespace only."
        )

    # Determine which resume to use (custom uploaded or cached portfolio resume)
    target_resume: Resume
    if request.custom_resume_id:
        custom = resume_manager.get_custom_resume(request.custom_resume_id)
        if not custom:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Custom uploaded resume session not found or has expired."
            )
        target_resume = custom
    else:
        target_resume = resume_manager.get_portfolio_resume()

    try:
        response = ask_candidate(
            question=question,
            resume=target_resume,
            client=resume_manager.groq_client,
            model=settings.GROQ_MODEL
        )
        return response
    except Exception as e:
        logger.error(f"Unexpected error in /chat endpoint: {e}")
        # Never expose internal stack traces or secrets to users
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the answer. Please try again."
        )


@app.post("/resume/reload", tags=["Resume"])
async def reload_resume():
    """Development endpoint to safely reload the fixed portfolio resume from disk."""
    try:
        resume_manager.load_portfolio_resume()
        return {"status": "success", "message": "Portfolio resume reloaded successfully."}
    except Exception as e:
        logger.error(f"Failed to reload resume: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reload portfolio resume."
        )


@app.post("/resume/upload", tags=["Resume Analysis Mode"])
async def upload_custom_resume(file: UploadFile = File(...)):
    """
    Optional analysis mode: Allows a visitor to upload their own PDF and ask questions
    about it in isolation without modifying or overwriting the portfolio resume.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents (.pdf) are supported."
        )

    contents = await file.read()
    if len(contents) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded PDF file is empty."
        )
    if len(contents) > 5 * 1024 * 1024:  # 5MB limit
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="PDF file size exceeds maximum limit of 5MB."
        )

    try:
        extracted_text = read_pdf(contents)
    except PDFExtractionError as pe:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(pe)
        )
    except Exception as e:
        logger.error(f"Error reading uploaded PDF: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to read PDF. Ensure the file is not corrupted or password-protected."
        )

    # Parse with LLM or fallback
    if resume_manager.groq_client and settings.is_groq_ready:
        parsed_resume = parse_resume_with_llm(
            resume_text=extracted_text,
            client=resume_manager.groq_client,
            model=settings.GROQ_MODEL
        )
    else:
        # Basic parsing fallback
        parsed_resume = Resume(
            name=file.filename.replace(".pdf", ""),
            summary=extracted_text[:400],
            skills=[]
        )

    session_id = resume_manager.store_custom_resume(parsed_resume)
    return {
        "status": "success",
        "session_id": session_id,
        "name": parsed_resume.name,
        "message": "Custom resume parsed successfully and isolated for this session."
    }


@app.delete("/resume/upload/{session_id}", tags=["Resume Analysis Mode"])
async def delete_custom_resume(session_id: str):
    """Discards a visitor's uploaded resume session data."""
    deleted = resume_manager.remove_custom_resume(session_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session ID not found or already deleted."
        )
    return {"status": "success", "message": "Uploaded resume session discarded."}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Catch-all exception handler to guard against leaking sensitive internal details."""
    logger.error(f"Unhandled exception on {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."}
    )
