import io
import json
import logging
from pathlib import Path
from typing import BinaryIO, Union

from groq import Groq
from pypdf import PdfReader

from backend.schemas import (
    Education,
    Experience,
    Project,
    Resume,
    SkillCategory,
)

logger = logging.getLogger("resume_parser")


class PDFExtractionError(Exception):
    """Raised when text cannot be extracted from a PDF."""
    pass


def read_pdf(file_input: Union[str, Path, bytes, BinaryIO]) -> str:
    """
    Extracts text from a PDF file path, bytes, or file-like object using pypdf.
    Validates that the file has non-empty extractable text.
    """
    try:
        if isinstance(file_input, (str, Path)):
            path = Path(file_input)
            if not path.exists():
                raise FileNotFoundError(f"PDF file not found at: {path}")
            if path.stat().st_size == 0:
                raise PDFExtractionError("The provided PDF file is empty (0 bytes).")
            reader = PdfReader(str(path))
        elif isinstance(file_input, bytes):
            if len(file_input) == 0:
                raise PDFExtractionError("Uploaded PDF content is empty.")
            reader = PdfReader(io.BytesIO(file_input))
        else:
            reader = PdfReader(file_input)

        if len(reader.pages) == 0:
            raise PDFExtractionError("PDF document contains no pages.")

        extracted_text = []
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text.strip())

        full_text = "\n\n".join(extracted_text).strip()
        if not full_text:
            raise PDFExtractionError(
                "PDF contains no extractable text. Scanned or image-only PDFs are not supported."
            )

        return full_text

    except (PDFExtractionError, FileNotFoundError):
        raise
    except Exception as e:
        logger.error(f"Failed to read PDF: {e}")
        raise PDFExtractionError(f"Could not read or parse PDF: {str(e)}")


def get_verified_resume() -> Resume:
    """
    Returns the grounded, verified structured Resume representation for Dilpreet Kaur,
    derived directly from the verified resume PDF and public project links.
    """
    return Resume(
        name="Dilpreet Kaur",
        headline="B.Tech IT Student @ GTBIT · AI/ML / Data Science & LLM Developer",
        email="dilpreetk401@gmail.com",
        phone=None,  # Intentionally kept private for portfolio
        location="New Delhi, India",
        github="https://github.com/Dilpreetk11",
        linkedin="https://www.linkedin.com/in/dilpreet-kaur-a71413317",
        summary=(
            "B.Tech IT student building and deploying AI/ML applications, including multi-agent systems, "
            "agentic RAG and NLP pipelines, with live demos for each project. Completed an ML internship at NIC "
            "working on transformer-based log analysis. Looking for AI, ML and AI engineering roles."
        ),
        skills=[
            "Python", "C++", "SQL", "PostgreSQL", "SQLite",
            "Agentic RAG", "Multi-Agent Systems", "LLM Applications", "Prompt Engineering", "LangGraph", "LangChain", "Pinecone (Vector DB)", "Embeddings", "Groq API", "Tavily API",
            "Machine Learning", "NLP", "Transformers (T5, BERT)", "Hugging Face", "Random Forest", "LightGBM", "Scikit-learn", "Feature Engineering", "Model Evaluation (ROUGE)",
            "FastAPI", "REST APIs", "Streamlit", "Gradio", "Docker", "Git", "GitHub", "MLflow", "Pandas", "NumPy",
            "Data Structures", "DBMS", "Operating Systems", "Computer Networks", "OOP"
        ],
        skill_categories=[
            SkillCategory(
                category="AI & LLM Engineering",
                skills=["Agentic RAG", "Multi-Agent Systems", "LLM Applications", "Prompt Engineering", "LangGraph", "LangChain", "Pinecone (Vector DB)", "Embeddings", "Groq API", "Tavily API"]
            ),
            SkillCategory(
                category="Machine Learning & NLP",
                skills=["Machine Learning", "NLP", "Transformers (T5, BERT)", "Hugging Face", "Random Forest", "LightGBM", "Scikit-learn", "Feature Engineering", "Model Evaluation (ROUGE)"]
            ),
            SkillCategory(
                category="Backend & Deployment",
                skills=["FastAPI", "REST APIs", "Streamlit", "Gradio", "Docker", "Git", "GitHub", "MLflow"]
            ),
            SkillCategory(
                category="Programming & Data",
                skills=["Python", "C++", "SQL", "PostgreSQL", "SQLite", "Pandas", "NumPy"]
            ),
            SkillCategory(
                category="Core CS",
                skills=["Data Structures", "DBMS", "Operating Systems", "Computer Networks", "OOP"]
            )
        ],
        experiences=[
            Experience(
                role="Machine Learning Intern",
                company="National Informatics Centre (NIC)",
                duration="Jun 2025 – Aug 2025",
                location="New Delhi, India",
                responsibilities=[
                    "Cleaned multi-gigabyte log datasets with Pandas and regex, and built a rule-based labeling system covering 7+ log categories (port scans, DDoS, failed SSH, malware) to bootstrap training labels at scale.",
                    "Fine-tuned a T5-small transformer for automated security-log summarization on 500 labeled logs, reaching 0.91 ROUGE-1/ROUGE-L on validation.",
                    "Built BERT-based classification pipelines to sort logs into 3 categories (Error, Warning, Information), streamlining triage for downstream analysis.",
                    "Diagnosed a 0.91 to 0.45 ROUGE drop between validation and full-dataset inference; proposed GPT-4-assisted relabeling to improve generalization.",
                    "Deployed Gradio and Streamlit demos for real-time log summarization, letting stakeholders test the model without writing code."
                ],
                technologies=[
                    "Python", "Pandas", "Regex", "Hugging Face Transformers", "T5-small",
                    "BERT", "ROUGE", "Streamlit", "Gradio"
                ]
            )
        ],
        education=[
            Education(
                institution="Guru Tegh Bahadur Institute of Technology, Delhi",
                degree="B.Tech in Information Technology",
                duration="2023 – 2027",
                score="CGPA: 8.38",
                location="Delhi, India"
            ),
            Education(
                institution="SS Mota Singh School, Delhi",
                degree="High School (Class X & XII)",
                duration="2011 – 2023",
                score="Class X: 86%, Class XII: 80%",
                location="Delhi, India"
            )
        ],
        projects=[
            Project(
                name="AI-Powered Deep Packet Inspection & Threat Detection",
                problem="Real-time network traffic inspection and behavioural threat detection on PCAP data.",
                description=(
                    "Built a multithreaded C++ Deep Packet Inspection engine that parses PCAP traffic, tracks "
                    "five-tuple flows, and extracts TLS SNI and HTTP Host fields to identify applications. "
                    "Engineered 32 behavioral flow features (packet timing, payload entropy, TCP flag statistics) "
                    "and trained two Random Forest models on 8,000 synthetic flows for application classification and "
                    "detection of 5 traffic classes (benign, SYN flood, tunneling, data exfiltration, C2 beaconing), "
                    "with 0–100 threat scoring and an interactive Streamlit dashboard."
                ),
                technologies=["C++", "Python", "Random Forest", "Scikit-learn", "Pandas", "Streamlit", "CMake"],
                contributions=[
                    "Multithreaded C++ PCAP parsing engine with flow state tracking",
                    "32 behavioral flow features extracted (timing, payload entropy, TCP flags)",
                    "Random Forest model for 5-class network threat classification",
                    "Interactive Streamlit dashboard displaying 0-100 real-time threat scores"
                ],
                github_url="https://github.com/Dilpreetk11/AI-Powered-Deep-Packet-Inspection-Threat-Detection",
                live_url="https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/"
            ),
            Project(
                name="AI Travel Agent | Multi-Agent Travel Planning System",
                problem="Coordinating flight search, hotel accommodations, and daily itinerary planning into a cohesive plan.",
                description=(
                    "Built a multi-agent travel planner with LangGraph, Tavily web search, and Groq-hosted GPT-OSS 120B, "
                    "orchestrating four agents (flights, hotels, itinerary, final response) to create day-wise plans. "
                    "Implemented persistent conversation memory using LangGraph's PostgreSQL checkpointer, enabling multi-turn "
                    "planning across sessions; deployed a Streamlit interface on Streamlit Cloud."
                ),
                technologies=["Python", "LangGraph", "LangChain", "Groq", "PostgreSQL", "Tavily", "Streamlit"],
                contributions=[
                    "Orchestrated 4 distinct specialized sub-agents with LangGraph",
                    "Integrated Tavily real-time web search for current flight and lodging data",
                    "PostgreSQL persistent conversation checkpointer for multi-turn planning",
                    "Streamlit Cloud UI deployment for interactive user interaction"
                ],
                github_url="https://github.com/Dilpreetk11/AI-Travel-Agent",
                live_url="https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/"
            ),
            Project(
                name="Enterprise IT Support Agentic RAG Copilot",
                problem="Repetitive enterprise IT support tickets, scattered internal documentation, and hallucination risks in standard retrieval bots.",
                description=(
                    "Built an agentic RAG IT-support copilot (LangGraph, FastAPI, Pinecone, Groq, Tavily) that grades "
                    "retrieved evidence and falls back from a private knowledge base to web search, with query rewriting "
                    "and a retry guard. Delivered the full stack: FastAPI REST APIs, an admin-protected document-upload "
                    "pipeline for PDF/DOCX/TXT/MD, an interactive UI showing the decision trace, SQLite audit logs and Docker deployment. "
                    "Framed as a forward-deployed engineering project translating customer problems into a reliable product."
                ),
                technologies=["Python", "LangGraph", "FastAPI", "Pinecone", "Groq", "Tavily", "Docker", "Streamlit"],
                contributions=[
                    "Engineered LangGraph agentic workflow with query rewriting, document retrieval, and LLM evidence grading",
                    "Self-corrective fallback from private Pinecone knowledge base to Tavily web search with retry guard",
                    "Admin-protected document-upload pipeline for PDF/DOCX/TXT/MD with FastAPI REST endpoints",
                    "Interactive decision trace UI, SQLite audit logging, and production Docker containerization"
                ],
                github_url="https://github.com/Dilpreetk11/IT-Support-Agentic-RAG-Copilot",
                live_url="https://it-support-agentic-rag-copilot-brakzz3tuwuejuwhxmkkh8.streamlit.app/"
            ),
            Project(
                name="Resumind | AI Resume Analyzer",
                problem="Job applicants need instant, actionable ATS compatibility scoring against target job descriptions.",
                description=(
                    "Developed a resume analyzer that scores resumes against job descriptions and returns ATS-style "
                    "ratings with actionable feedback, using React Router v7, TypeScript, Tailwind CSS, and Zustand. "
                    "Integrated Puter.js for browser-based auth, PDF storage, and AI inference (Claude 3.7); added a demo mode "
                    "so the full dashboard works without AI credits."
                ),
                technologies=["React", "React Router v7", "TypeScript", "Vite", "Tailwind CSS", "Zustand", "Puter.js"],
                contributions=[
                    "Frontend SPA architecture using React Router v7 and Zustand state management",
                    "Serverless browser-based authentication and secure PDF storage via Puter.js",
                    "ATS rating and gap analysis prompt pipelines",
                    "Offline demo mode enabling full dashboard exploration without API credits"
                ],
                github_url="https://github.com/Dilpreetk11/Resumind",
                live_url="https://resumind-cmdp.onrender.com/"
            )
        ],
        certifications=[
            "Microsoft Generative AI",
            "IBM Machine Learning with Python"
        ],
        achievements=[
            "Secured 1st Position at Perfect Pitch 2.0 Ideathon (E-Cell GTBIT x NASSCOM Foundation)"
        ]
    )


def parse_resume_with_llm(resume_text: str, client: Groq, model: str) -> Resume:
    """
    Parses resume text using Groq LLM with structured JSON output and validates
    with Pydantic. If parsing or validation fails, gracefully falls back to the verified resume.
    """
    system_prompt = (
        "You are an expert resume parsing engine. Analyze the following resume text and extract "
        "accurate, structured information. Return ONLY valid JSON adhering strictly to this schema:\n"
        "{\n"
        '  "name": "Full Name",\n'
        '  "headline": "Professional Title / Headline",\n'
        '  "email": "Email address",\n'
        '  "location": "City, Country",\n'
        '  "github": "GitHub URL",\n'
        '  "linkedin": "LinkedIn URL",\n'
        '  "summary": "Brief summary",\n'
        '  "skills": ["skill1", "skill2"],\n'
        '  "skill_categories": [{"category": "Category Name", "skills": ["skill1"]}],\n'
        '  "experiences": [{"role": "Role", "company": "Company", "duration": "Dates", "responsibilities": ["bullet"], "technologies": ["tech"]}],\n'
        '  "education": [{"institution": "College", "degree": "Degree", "duration": "Dates", "score": "CGPA"}],\n'
        '  "projects": [{"name": "Project", "problem": "Problem", "description": "Desc", "technologies": ["tech"], "contributions": ["item"], "github_url": "url", "live_url": "url"}],\n'
        '  "certifications": ["Cert 1"],\n'
        '  "achievements": ["Achievement 1"]\n'
        "}\n"
        "Rules:\n"
        "- Do not invent missing facts. Use null or empty lists for missing details.\n"
        "- Include internships under experiences.\n"
        "- Extract all project details accurately."
    )

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract structured data from this resume text:\n\n{resume_text}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=4000
        )
        content = completion.choices[0].message.content
        data = json.loads(content)
        parsed = Resume.model_validate(data)
        return parsed
    except Exception as e:
        logger.warning(f"LLM resume parsing failed or returned invalid schema ({e}). Falling back to verified resume data.")
        return get_verified_resume()
