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
        headline="AI/ML Engineer",
        email="dilpreetk401@gmail.com",
        phone=None,  # Intentionally kept private for portfolio
        location="New Delhi, India",
        github="https://github.com/Dilpreetk11",
        linkedin="https://www.linkedin.com/in/dilpreet-kaur-a71413317",
        summary=(
            "B.Tech Information Technology student (2027) building AI/ML solutions. Former Machine Learning Intern "
            "at NIC with experience in end-to-end AI applications."
        ),
        skills=[
            "Supervised Learning", "Classification", "Random Forest", "LightGBM", "Scikit-learn",
            "Reinforcement Learning (Q-learning)", "Feature Engineering", "Hyperparameter Tuning", "Model Evaluation", "MLflow",
            "Neural Networks", "Transformers (T5, BERT)", "Hugging Face", "Fine-tuning", "Text Summarization", "Text Classification", "Embeddings",
            "LLM Applications", "Prompt Engineering", "Multi-Agent Systems", "LangGraph", "LangChain",
            "Python", "C++", "SQL", "PostgreSQL", "SQLite", "Pandas", "NumPy",
            "FastAPI", "REST APIs", "Streamlit", "Gradio", "Git", "GitHub", "React"
        ],
        skill_categories=[
            SkillCategory(
                category="Machine Learning",
                skills=["Supervised Learning", "Classification", "Random Forest", "LightGBM", "Scikit-learn", "Reinforcement Learning (Q-learning)", "Feature Engineering", "Hyperparameter Tuning", "Model Evaluation", "MLflow"]
            ),
            SkillCategory(
                category="Deep Learning & NLP",
                skills=["Neural Networks", "Transformers (T5, BERT)", "Hugging Face", "Fine-tuning", "Text Summarization", "Text Classification", "Embeddings"]
            ),
            SkillCategory(
                category="LLM & Agents",
                skills=["LLM Applications", "Prompt Engineering", "Multi-Agent Systems", "LangGraph", "LangChain"]
            ),
            SkillCategory(
                category="Programming & Data",
                skills=["Python", "C++", "SQL", "PostgreSQL", "SQLite", "Pandas", "NumPy"]
            ),
            SkillCategory(
                category="Backend & Deployment",
                skills=["FastAPI", "REST APIs", "Streamlit", "Gradio", "Git", "GitHub", "React"]
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
                    "Diagnosed a 0.91 to 0.45 ROUGE drop between validation and full-dataset inference and proposed GPT-4-assisted relabeling to improve generalization."
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
                name="Telco Customer Churn Prediction | End-to-End ML Pipeline",
                problem="Identify telecom customers at risk of leaving so teams can target retention efforts.",
                description=(
                    "Built an end-to-end LightGBM machine-learning pipeline on a 7,043-customer telecom dataset. "
                    "Tracked experiments with MLflow and reached 91.7% recall for churn-prone customers, then "
                    "deployed inference through FastAPI with a Gradio interface for real-time predictions."
                ),
                technologies=["Python", "LightGBM", "MLflow", "FastAPI", "Gradio"],
                contributions=[
                    "Built and tuned a churn prediction pipeline on 7,043 customer records",
                    "Tracked experiments with MLflow and achieved 91.7% recall for churn-prone customers",
                    "Deployed an inference API and interactive Gradio prediction interface"
                ],
                github_url="https://github.com/Dilpreetk11/ML-Churn-Prediction"
            ),
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
                name="AI Travel Planning Agent | LangGraph with Long-Term Memory",
                problem="Coordinating flight search, hotel accommodations, and daily itinerary planning into a cohesive plan.",
                description=(
                    "Built a LangGraph multi-agent planner that creates personalized itineraries from destination, duration, and budget. "
                    "Integrated Tavily travel research, Groq Llama 3.3 reasoning, and PostgreSQL checkpointing to retain conversation "
                    "context across sessions. The coordinated workflow generated a seven-day Japan itinerary within a 2 lakh INR budget."
                ),
                technologies=["Python", "LangGraph", "LangChain", "Groq", "PostgreSQL", "Tavily", "Streamlit"],
                contributions=[
                    "Orchestrated travel planning agents with LangGraph around the traveler's destination, duration, and budget",
                    "Integrated Tavily research and Groq Llama 3.3 for itinerary planning",
                    "Added PostgreSQL checkpointing to retain conversation context across sessions",
                    "Generated a seven-day Japan itinerary within a 2 lakh INR budget"
                ],
                github_url="https://github.com/Dilpreetk11/AI-Travel-Agent",
                live_url="https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/"
            ),
            Project(
                name="GridScan RL | Reinforcement Learning Environment",
                problem="Explore an obstacle grid efficiently while maximizing coverage of the available free tiles.",
                description=(
                    "Built a tabular Q-learning agent using Bellman updates and epsilon-greedy exploration with decay to scan a 10x10 obstacle grid. "
                    "The agent reached 90.1% coverage (82 of 91 free tiles). Shaped rewards and cycle detection track coverage, collisions, and loops; "
                    "a FastAPI and NumPy engine serves a React dashboard with live Q-values."
                ),
                technologies=["Python", "NumPy", "FastAPI", "React", "Q-learning"],
                contributions=[
                    "Implemented tabular Q-learning with Bellman updates and decaying epsilon-greedy exploration",
                    "Reached 90.1% coverage across 82 of 91 free tiles in a 10x10 obstacle grid",
                    "Added shaped rewards and cycle detection with coverage, collision, and loop tracking",
                    "Built a FastAPI and NumPy engine with a React dashboard showing live Q-values"
                ],
                live_url="https://rl-gridscan.onrender.com/"
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
                live_url="https://enterprise-it-support-copilot.vercel.app/"
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
            ),
            Project(
                name="Dilpreet Kaur Portfolio & AI Assistant",
                problem="Recruiters need a clear way to explore Dilpreet's background, projects, and technical work.",
                description=(
                    "Built a full-stack portfolio with a Streamlit frontend and FastAPI backend, featuring an AI assistant "
                    "grounded in verified resume and project information, plus an interactive project showcase."
                ),
                technologies=["Python", "Streamlit", "FastAPI", "Groq", "Pydantic", "Pytest"],
                contributions=[
                    "Created an interactive portfolio for skills, experience, and project exploration",
                    "Connected a grounded AI portfolio assistant to a FastAPI backend",
                    "Added verified resume context and automated tests for key portfolio details"
                ],
                github_url="https://github.com/Dilpreetk11/Dilpreet-Kaur-Portfolio-app"
            )
        ],
        certifications=[
            "Microsoft Generative AI",
            "IBM Machine Learning with Python"
        ],
        achievements=[
            "Secured 1st Position at Perfect Pitch 2.0 Ideathon (E-Cell GTBIT x NASSCOM Foundation)",
            "Open-source contributor, GirlScript Summer of Code (GSSoC)"
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
