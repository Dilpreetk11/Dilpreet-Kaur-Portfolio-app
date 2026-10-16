import base64
import os
import sys
from pathlib import Path

# ── Ensure repo root is on sys.path so `backend` package is importable ──
# This is required when Streamlit Cloud runs `frontend/app.py` as the entry point.
_REPO_ROOT = str(Path(__file__).resolve().parent.parent)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import requests
import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BACKEND_URL: str = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT: int = 30  # seconds per request

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RESUME_PDF = DATA_DIR / "my_resume.pdf"
PROFILE_PHOTO = ASSETS_DIR / "profile-photo.jpg"
DPI_THUMB = ASSETS_DIR / "dpi-thumbnail.png"
TRAVEL_THUMB = ASSETS_DIR / "travel-agent-thumbnail.png"
IT_SUPPORT_THUMB = ASSETS_DIR / "it-support-thumbnail.png"
RESUMIND_THUMB = ASSETS_DIR / "resumind-thumbnail.png"

PROFILE = {
    "name": "Dilpreet Kaur",
    "headline": "B.Tech IT Student @ GTBIT · AI/ML & Agentic Systems | Building Smart Solutions",
    "github": "https://github.com/Dilpreetk11",
    "linkedin": "https://www.linkedin.com/in/dilpreet-kaur-a71413317",
    "email": "dilpreetk401@gmail.com",
    "location": "New Delhi, India",
    "bio": (
        "B.Tech IT student building and deploying AI/ML applications, including multi-agent systems, "
        "agentic RAG and NLP pipelines, with live demos for each project. Completed an ML internship at NIC "
        "working on transformer-based log analysis. Looking for AI, ML and AI engineering roles.\n\n"
        "At the National Informatics Centre (NIC), I built an end-to-end transformer-based security-log analysis "
        "workflow: cleaned and organized multi-gigabyte log datasets into 7+ labeled attack categories, fine-tuned "
        "T5-small reaching 0.91 ROUGE-1/ROUGE-L on validation, built BERT pipelines for triage classification, "
        "and deployed Gradio and Streamlit demos for non-technical stakeholders.\n\n"
        "Outside my internship, I built the Enterprise IT Support Agentic RAG Copilot (LangGraph, FastAPI, Pinecone, "
        "Groq, Tavily) with self-corrective retrieval and evidence grading, an AI Travel Agent multi-agent planner "
        "with PostgreSQL memory, a deep packet inspection and threat detection system with a multithreaded C++ engine "
        "and Random Forest models, and Resumind, an ATS resume analyzer."
    ),
}

SKILLS = [
    {"category": "AI & LLM Engineering", "items": ["Agentic RAG", "Multi-Agent Systems", "LLM Applications", "Prompt Engineering", "LangGraph", "LangChain", "Pinecone (Vector DB)", "Embeddings", "Groq API", "Tavily API"]},
    {"category": "Machine Learning & NLP", "items": ["Machine Learning", "NLP", "Transformers (T5, BERT)", "Hugging Face", "Random Forest", "LightGBM", "Scikit-learn", "Feature Engineering", "Model Evaluation (ROUGE)"]},
    {"category": "Backend & Deployment", "items": ["FastAPI", "REST APIs", "Streamlit", "Gradio", "Docker", "Git", "GitHub", "MLflow"]},
    {"category": "Programming & Data", "items": ["Python", "C++", "SQL", "PostgreSQL", "SQLite", "Pandas", "NumPy"]},
    {"category": "Core CS", "items": ["Data Structures", "DBMS", "Operating Systems", "Computer Networks", "OOP"]},
]

EXPERIENCE = [
    {
        "role": "Machine Learning Intern",
        "company": "National Informatics Centre (NIC)",
        "duration": "Jun 2025 – Aug 2025",
        "location": "New Delhi, India",
        "points": [
            "Built Gradio and Streamlit interfaces that present model outputs clearly for users without coding expertise.",
            "Used T5 and BERT to summarize and classify cybersecurity logs, turning dense technical data into short, readable summaries for faster triage.",
            "Cleaned and organized large log datasets (Pandas, regex) into a labeled structure covering 7+ security event categories.",
            "Fine-tuned a T5-small model for security-log summarization on 500 labeled logs, reaching **0.91 ROUGE-1/ROUGE-L** on validation.",
            "Evaluated model performance, identified data-quality and generalization issues, and explored improvements.",
            "Delivered an end-to-end transformer-based log analysis workflow, from raw data preprocessing to model evaluation and a user-facing interface.",
        ],
        "tech": ["Python", "Pandas", "Regex", "T5-small", "BERT", "ROUGE", "Streamlit", "Gradio", "Hugging Face"],
        "certificate": ASSETS_DIR / "nic-certificate.pdf",
    },
]

PROJECTS = [
    {
        "name": "AI-Powered Deep Packet Inspection & Threat Detection",
        "tag": "C++ · Systems · ML / Data Science",
        "summary": "Multithreaded network traffic analysis engine with Random Forest threat scoring.",
        "description": (
            "Built a C++ multithreaded DPI engine that parses PCAP captures, tracks five-tuple flows, "
            "and extracts TLS SNI / HTTP Host fields for application identification. Engineered 32 behavioral "
            "flow features (packet timing, payload entropy, TCP flag statistics) and trained two Random Forest "
            "models on 8,000 synthetic flows — one for application classification and one for detecting 5 "
            "threat classes (benign, SYN flood, tunneling, exfiltration, C2 beaconing). Results are presented "
            "on an interactive Streamlit dashboard with 0–100 threat scoring."
        ),
        "tech": ["C++", "Python", "CMake", "Scikit-learn", "Random Forest", "Pandas", "Streamlit"],
        "github": "https://github.com/Dilpreetk11/AI-Powered-Deep-Packet-Inspection-Threat-Detection",
        "live": "https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/",
        "thumb": DPI_THUMB,
    },
    {
        "name": "AI Travel Agent — Multi-Agent Planning System",
        "tag": "LangGraph · Groq · PostgreSQL",
        "summary": "Orchestrated 4-agent LangGraph system for flight, hotel, and itinerary planning.",
        "description": (
            "Multi-agent travel planner built with LangGraph and Groq GPT-OSS 120B, orchestrating four "
            "specialized sub-agents (flights, hotels, itinerary, final response) with Tavily real-time web search. "
            "Implemented persistent multi-turn conversation memory using LangGraph's PostgreSQL checkpointer; "
            "deployed an interactive Streamlit Cloud interface."
        ),
        "tech": ["Python", "LangGraph", "LangChain", "Groq", "PostgreSQL", "Tavily", "Streamlit"],
        "github": "https://github.com/Dilpreetk11/AI-Travel-Agent",
        "live": "https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/",
        "thumb": TRAVEL_THUMB,
    },
    {
        "name": "Enterprise IT Support Agentic RAG Copilot",
        "tag": "LangGraph · Pinecone · Groq · Tavily",
        "summary": "Built a deployable Agentic RAG copilot that decides between private knowledge and web search, grades its own evidence, and shows its reasoning path to users.",
        "description": (
            "Built an agentic RAG IT-support copilot (LangGraph, FastAPI, Pinecone, Groq, Tavily) that grades retrieved "
            "evidence and falls back from a private knowledge base to web search, with query rewriting and a retry guard. "
            "Delivered the full stack: FastAPI REST APIs, an admin-protected document-upload pipeline for PDF/DOCX/TXT/MD, "
            "an interactive frontend showing the decision trace, SQLite audit logs and Docker deployment. "
            "Framed as a forward-deployed engineering project translating customer problems (repetitive tickets, "
            "scattered documents, hallucination risk) into a reliable enterprise assistant."
        ),
        "tech": ["Python", "LangGraph", "FastAPI", "Pinecone", "Groq", "Tavily", "Docker", "Streamlit"],
        "github": "https://github.com/Dilpreetk11/IT-Support-Agentic-RAG-Copilot",
        "live": "https://it-support-agentic-rag-copilot-brakzz3tuwuejuwhxmkkh8.streamlit.app/",
        "thumb": IT_SUPPORT_THUMB,
    },
    {
        "name": "Resumind — AI Resume Analyzer",
        "tag": "React · TypeScript · Puter.js",
        "summary": "Serverless ATS resume scoring platform with recruiter-style feedback.",
        "description": (
            "AI-powered resume analyzer that evaluates resumes against job descriptions and returns ATS scores "
            "with actionable, recruiter-style feedback. Built with React Router v7, TypeScript, Tailwind CSS, "
            "and Zustand; uses Puter.js for browser-based auth, secure PDF storage, and serverless AI inference. "
            "Includes a full demo mode enabling dashboard exploration without API credits."
        ),
        "tech": ["React", "TypeScript", "Vite", "Tailwind CSS", "Zustand", "Puter.js"],
        "github": "https://github.com/Dilpreetk11/Resumind",
        "live": "https://resumind-cmdp.onrender.com/",
        "thumb": RESUMIND_THUMB,
    },
    {
        "name": "Telco Customer Churn Prediction",
        "tag": "ML · FastAPI · Gradio",
        "summary": "End-to-end ML pipeline predicting churn on 7,043 telecom customers with 91.7% recall.",
        "description": (
            "Built an end-to-end machine learning pipeline using LightGBM to predict telecom customer churn "
            "on a dataset of 7,043 customers. Included feature engineering, missing value handling, and "
            "hyperparameter tuning tracked with MLflow — achieving 91.7% recall for churn-prone customers. "
            "Deployed a FastAPI inference service with an interactive Gradio UI."
        ),
        "tech": ["Python", "LightGBM", "Scikit-learn", "Pandas", "MLflow", "FastAPI", "Gradio"],
        "github": "https://github.com/Dilpreetk11/ML-Churn-Prediction",
        "live": None,
        "thumb": None,
    },
]

EDUCATION = [
    {
        "institution": "Guru Tegh Bahadur Institute of Technology (GTBIT), Delhi",
        "degree": "B.Tech – Information Technology",
        "duration": "2023 – 2027",
        "score": "CGPA: 8.38",
    },
    {
        "institution": "SS Mota Singh School, Delhi",
        "degree": "Class X & XII",
        "duration": "2011 – 2023",
        "score": "Class X: 86% · Class XII: 80%",
    },
]

CERTIFICATIONS = [
    {"name": "Microsoft Generative AI", "issuer": "Microsoft"},
    {"name": "IBM Machine Learning with Python", "issuer": "IBM"},
    {"name": "AWS APAC Architecture", "issuer": "AWS"},
]

ACHIEVEMENTS = [
    "🏆  1st Position — Perfect Pitch 2.0 Ideathon (E-Cell GTBIT × NASSCOM Foundation)",
]

SUGGESTED_QUESTIONS = [
    "Tell me about the IT Support Agentic RAG Copilot.",
    "Tell me about the Travel Agent project.",
    "Tell me about Deep Packet Inspection threat detection.",
    "Tell me about Resumind.",
    "Explain your internship at NIC.",
    "What are your core technical skills?",
    "What LLM and AI frameworks have you worked with?",
    "Tell me about yourself.",
    "What certifications and achievements do you have?",
]


# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dilpreet Kaur · AI Portfolio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ──────────────────────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────────────────────
def load_css() -> None:
    st.markdown("""
<style>
/* ── Import Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global Reset ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: radial-gradient(ellipse at 20% 20%, rgba(88,28,135,0.18) 0%, #080b14 55%) !important;
    color: #d4d8e8 !important;
}

/* Remove top padding */
.main .block-container { padding-top: 1.5rem; max-width: 920px; }

/* ── Section Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid rgba(168,85,247,0.12);
    margin: 2.5rem 0;
}

/* ── Top Brand Header & Navigation ── */
.brand-logo {
    font-family: 'Inter', -apple-system, sans-serif !important;
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    background: linear-gradient(90deg, #a855f7, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Streamlit Pills / Segmented Navigation Styling ── */
[data-testid="stPills"] {
    justify-content: center;
    gap: 0.35rem !important;
}
[data-testid="stPills"] button {
    background: rgba(168, 85, 247, 0.04) !important;
    border: 1px solid rgba(168, 85, 247, 0.15) !important;
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 0.42rem 0.9rem !important;
    transition: all 0.22s ease !important;
}
[data-testid="stPills"] button:hover {
    background: rgba(168, 85, 247, 0.12) !important;
    color: #e2d4f7 !important;
    border-color: rgba(168, 85, 247, 0.4) !important;
}
[data-testid="stPills"] button[aria-selected="true"] {
    background: rgba(168, 85, 247, 0.22) !important;
    color: #f0e6ff !important;
    border-color: rgba(192, 132, 252, 0.7) !important;
    box-shadow: 0 0 18px rgba(168, 85, 247, 0.38) !important;
}

/* ── Hero — Cosmic Glass Card ── */
.hero-block {
    background: radial-gradient(circle at 50% 0%, rgba(99,45,140,0.38) 0%, rgba(12,9,28,0.96) 72%);
    border: 1.5px solid rgba(192,132,252,0.55);
    border-radius: 20px;
    padding: 2.8rem 2.6rem 2rem;
    margin-bottom: 0.5rem;
    display: flex;
    gap: 2.4rem;
    align-items: center;
    box-shadow: 0 0 40px rgba(168,85,247,0.28), 0 2px 60px rgba(0,0,0,0.55), inset 0 0 30px rgba(168,85,247,0.08);
    position: relative;
    overflow: hidden;
}
.hero-block::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(168,85,247,0.22) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-block::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(0,229,153,0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-text { flex: 1; min-width: 0; position: relative; z-index: 1; }
.hero-name {
    font-size: 2.3rem;
    font-weight: 800;
    color: #f0ecff;
    margin: 0 0 0.4rem;
    line-height: 1.15;
    letter-spacing: -0.01em;
}
.hero-headline {
    font-size: 0.93rem;
    color: #c084fc;
    font-weight: 500;
    margin-bottom: 1rem;
    letter-spacing: 0.02em;
}
.hero-bio {
    font-size: 0.87rem;
    color: #9ca3be;
    line-height: 1.75;
    max-width: 560px;
    margin-bottom: 1.4rem;
}
.hero-links { display: flex; gap: 0.55rem; flex-wrap: wrap; }
.hero-link {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.78rem;
    font-weight: 500;
    color: #a0aec0 !important;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 7px;
    padding: 0.36rem 0.82rem;
    text-decoration: none !important;
    transition: all 0.22s;
    backdrop-filter: blur(4px);
}
.hero-link:hover {
    color: #e2d4f7 !important;
    border-color: rgba(192,132,252,0.45);
    background: rgba(168,85,247,0.12);
    box-shadow: 0 0 12px rgba(168,85,247,0.2);
}

/* ── Hero CTA Button Row ── */
.hero-cta-row {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-top: 1.2rem;
    margin-bottom: 1.5rem;
}

/* ── Profile Photo ── */
.profile-photo-wrap {
    flex-shrink: 0;
    width: 128px;
    height: 128px;
    border-radius: 50%;
    overflow: hidden;
    border: 2px solid rgba(192,132,252,0.5);
    box-shadow: 0 0 0 5px rgba(168,85,247,0.12), 0 0 25px rgba(168,85,247,0.22);
    position: relative;
    z-index: 1;
}
.profile-photo-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* ── Section Heading ── */
.section-heading {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7c5fa0;
    margin: 0 0 1.2rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(168,85,247,0.18);
}

/* ── Skill Tag ── */
.skill-tag {
    display: inline-block;
    font-size: 0.73rem;
    font-weight: 500;
    color: #b8a4d8;
    background: rgba(168,85,247,0.07);
    border: 1px solid rgba(168,85,247,0.18);
    border-radius: 6px;
    padding: 0.24rem 0.62rem;
    margin: 0.2rem;
    transition: all 0.18s;
}
.skill-tag:hover {
    border-color: rgba(192,132,252,0.45);
    background: rgba(168,85,247,0.14);
    color: #e2d4f7;
}
.skill-category-label {
    font-size: 0.71rem;
    font-weight: 700;
    color: #7c5fa0;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 1rem 0 0.35rem;
}

/* ── Experience Timeline ── */
.exp-card {
    background: rgba(168,85,247,0.04);
    border: 1px solid rgba(168,85,247,0.18);
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.exp-card:hover {
    border-color: rgba(192,132,252,0.35);
    box-shadow: 0 0 18px rgba(168,85,247,0.12);
}
.exp-card::before {
    content: '';
    position: absolute;
    left: 0; top: 1.5rem; bottom: 1.5rem;
    width: 2px;
    background: linear-gradient(180deg, #a855f7 0%, transparent 100%);
    border-radius: 1px;
}
.exp-role {
    font-size: 0.95rem;
    font-weight: 600;
    color: #e2d4f7;
    margin-bottom: 0.15rem;
}
.exp-company { font-size: 0.83rem; color: #c084fc; font-weight: 500; }
.exp-meta { font-size: 0.75rem; color: #7c5fa0; margin: 0.3rem 0 0.8rem; }
.exp-point {
    font-size: 0.82rem;
    color: #9ca3be;
    line-height: 1.65;
    padding-left: 1rem;
    position: relative;
    margin-bottom: 0.4rem;
}
.exp-point::before {
    content: '–';
    position: absolute;
    left: 0;
    color: #7c5fa0;
}

/* ── Project Card ── */
.project-card {
    background: radial-gradient(circle at 0% 0%, rgba(99,45,140,0.15) 0%, rgba(12,9,28,0.7) 65%);
    border: 1px solid rgba(168,85,247,0.2);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.25s, box-shadow 0.25s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
.project-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(192,132,252,0.5), transparent);
}
.project-card:hover {
    border-color: rgba(192,132,252,0.42);
    box-shadow: 0 4px 28px rgba(168,85,247,0.18);
    transform: translateY(-2px);
}
.project-tag {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #00c47a;
    background: rgba(0,229,153,0.08);
    border: 1px solid rgba(0,229,153,0.2);
    border-radius: 5px;
    padding: 0.17rem 0.55rem;
    margin-bottom: 0.6rem;
}
.project-name {
    font-size: 0.97rem;
    font-weight: 700;
    color: #e8e0f8;
    margin-bottom: 0.3rem;
}
.project-summary { font-size: 0.82rem; color: #9ca3be; margin-bottom: 0.7rem; }
.project-desc { font-size: 0.8rem; color: #8899aa; line-height: 1.65; margin-bottom: 0.8rem; }
.project-links { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.project-link {
    font-size: 0.74rem;
    font-weight: 600;
    color: #c084fc !important;
    background: rgba(168,85,247,0.08);
    border: 1px solid rgba(168,85,247,0.25);
    border-radius: 6px;
    padding: 0.26rem 0.78rem;
    text-decoration: none !important;
    transition: all 0.18s;
}
.project-link:hover {
    background: rgba(168,85,247,0.18);
    border-color: rgba(192,132,252,0.5);
    color: #e2d4f7 !important;
    box-shadow: 0 0 10px rgba(168,85,247,0.2);
}

/* ── Education Card ── */
.edu-card {
    background: rgba(168,85,247,0.04);
    border: 1px solid rgba(168,85,247,0.15);
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.edu-card:hover { border-color: rgba(192,132,252,0.3); }
.edu-degree { font-size: 0.9rem; font-weight: 600; color: #e2d4f7; }
.edu-inst { font-size: 0.82rem; color: #c084fc; margin: 0.2rem 0 0.3rem; }
.edu-meta { font-size: 0.76rem; color: #7c5fa0; }

/* ── Cert Card ── */
.cert-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    font-weight: 500;
    color: #b8a4d8;
    background: rgba(168,85,247,0.06);
    border: 1px solid rgba(168,85,247,0.18);
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin: 0.3rem;
    transition: all 0.18s;
}
.cert-chip:hover {
    border-color: rgba(192,132,252,0.35);
    background: rgba(168,85,247,0.12);
}

/* ── Chat Bubbles ── */
.chat-container { max-height: 480px; overflow-y: auto; padding: 0.5rem 0; }
.chat-msg { margin-bottom: 0.9rem; display: flex; align-items: flex-start; gap: 0.6rem; }
.chat-msg.user { flex-direction: row-reverse; }
.chat-avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    font-weight: 700;
    flex-shrink: 0;
}
.chat-avatar.user { background: rgba(168,85,247,0.2); color: #c084fc; border: 1px solid rgba(168,85,247,0.35); }
.chat-avatar.bot { background: rgba(0,229,153,0.12); color: #00e599; border: 1px solid rgba(0,229,153,0.3); }
.chat-bubble {
    max-width: 80%;
    font-size: 0.82rem;
    line-height: 1.65;
    padding: 0.7rem 0.95rem;
    border-radius: 10px;
    word-break: break-word;
}
.chat-bubble.user {
    background: rgba(168,85,247,0.1);
    border: 1px solid rgba(168,85,247,0.25);
    color: #e2d4f7;
    border-radius: 10px 2px 10px 10px;
}
.chat-bubble.bot {
    background: rgba(0,229,153,0.05);
    border: 1px solid rgba(0,229,153,0.15);
    color: #b8d8c8;
    border-radius: 2px 10px 10px 10px;
}
.chat-welcome {
    background: radial-gradient(circle at 50% 0%, rgba(99,45,140,0.25) 0%, rgba(12,9,28,0.9) 80%);
    border: 1px solid rgba(192,132,252,0.35);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 0 20px rgba(168,85,247,0.1);
}
.chat-welcome-title { font-size: 0.9rem; font-weight: 700; color: #e2d4f7; margin-bottom: 0.4rem; }
.chat-welcome-sub { font-size: 0.8rem; color: #9ca3be; line-height: 1.6; }
.chat-grounding-note {
    font-size: 0.73rem;
    color: #7c5fa0;
    background: rgba(168,85,247,0.04);
    border: 1px solid rgba(168,85,247,0.12);
    border-radius: 6px;
    padding: 0.4rem 0.75rem;
    margin-top: 0.5rem;
}

/* ── Contact ── */
.contact-card {
    background: radial-gradient(circle at 50% 0%, rgba(99,45,140,0.28) 0%, rgba(12,9,28,0.95) 75%);
    border: 1.5px solid rgba(192,132,252,0.35);
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 0 30px rgba(168,85,247,0.12);
}
.contact-card a {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    color: #c084fc !important;
    text-decoration: none !important;
    font-size: 0.85rem;
    font-weight: 500;
    margin: 0.3rem 0.5rem;
    transition: color 0.15s;
}
.contact-card a:hover { color: #e2d4f7 !important; }
.contact-sub { font-size: 0.8rem; color: #7c5fa0; margin-top: 0.5rem; }

/* Streamlit button overrides */
[data-testid="baseButton-secondary"] {
    border: 1px solid rgba(255,255,255,0.18) !important;
    background: rgba(255,255,255,0.04) !important;
    color: #b0bcd4 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    border-radius: 9px !important;
    transition: all 0.22s !important;
    backdrop-filter: blur(6px) !important;
}
[data-testid="baseButton-secondary"]:hover {
    background: rgba(168,85,247,0.1) !important;
    border-color: rgba(192,132,252,0.45) !important;
    color: #e2d4f7 !important;
    box-shadow: 0 0 14px rgba(168,85,247,0.2) !important;
}
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #00e599, #00c47a) !important;
    border: none !important;
    color: #041b12 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.83rem !important;
    font-weight: 700 !important;
    border-radius: 9px !important;
    box-shadow: 0 0 22px rgba(0,229,153,0.42), 0 2px 8px rgba(0,0,0,0.3) !important;
    transition: all 0.22s !important;
}
[data-testid="baseButton-primary"]:hover {
    background: linear-gradient(135deg, #00f5a8, #00e599) !important;
    box-shadow: 0 0 32px rgba(0,229,153,0.58), 0 2px 12px rgba(0,0,0,0.3) !important;
    transform: translateY(-1px) !important;
}
/* Download button special style */
[data-testid="stDownloadButton"] button {
    border: 1px solid rgba(255,255,255,0.18) !important;
    background: rgba(255,255,255,0.04) !important;
    color: #b0bcd4 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    border-radius: 9px !important;
    transition: all 0.22s !important;
    backdrop-filter: blur(6px) !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(168,85,247,0.1) !important;
    border-color: rgba(192,132,252,0.45) !important;
    color: #e2d4f7 !important;
    box-shadow: 0 0 14px rgba(168,85,247,0.2) !important;
}

/* Streamlit input override */
[data-testid="stTextInput"] input {
    background: rgba(168,85,247,0.05) !important;
    border: 1px solid rgba(168,85,247,0.22) !important;
    color: #e2d4f7 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(192,132,252,0.55) !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(168,85,247,0.12) !important;
}

/* Streamlit expander */
details > summary {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #9ca3be !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #080b14 !important;
    border-right: 1px solid rgba(168,85,247,0.12) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 1px dashed rgba(168,85,247,0.2) !important;
    border-radius: 10px !important;
    background: rgba(168,85,247,0.03) !important;
}

/* Spinner and alerts */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border: 1px solid rgba(168,85,247,0.2) !important;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def get_image_b64(path: Path) -> str | None:
    """Return base64-encoded image for embedding in HTML."""
    try:
        if path and path.exists():
            return base64.b64encode(path.read_bytes()).decode()
    except Exception:
        pass
    return None


def backend_chat(question: str, custom_session_id: str | None = None) -> dict:
    """Calls the FastAPI /chat endpoint, or falls back to direct inference so chat always functions without errors."""
    try:
        payload = {"question": question}
        if custom_session_id:
            payload["custom_resume_id"] = custom_session_id
        resp = requests.post(
            f"{BACKEND_URL}/chat", json=payload, timeout=TIMEOUT
        )
        if resp.status_code == 200:
            return {"ok": True, "data": resp.json()}
    except Exception:
        pass

    # Seamless fallback ensuring all chat buttons work even in standalone mode
    try:
        from backend.chatbot import ask_candidate
        from backend.resume_parser import get_verified_resume
        from backend.config import settings
        from groq import Groq

        client = None
        if settings.is_groq_ready:
            try:
                client = Groq(api_key=settings.GROQ_API_KEY)
            except Exception:
                client = None

        resume = get_verified_resume()
        chat_resp = ask_candidate(question, resume, client=client)
        return {
            "ok": True,
            "data": {
                "answer": chat_resp.answer,
                "grounded": chat_resp.grounded,
                "sources": chat_resp.sources
            }
        }
    except Exception as e:
        return {"ok": False, "error": f"Error: {str(e)[:200]}"}


def check_backend() -> dict:
    """Calls the /health endpoint and returns server status with automatic standalone readiness."""
    try:
        resp = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if resp.status_code == 200:
            return {"ok": True, "data": resp.json()}
    except Exception:
        pass
    # In standalone mode, local inference is ready
    return {"ok": True, "data": {"resume_loaded": True, "model": "Standalone Mode (Local / Groq)", "standalone": True}}


def render_html(html_str: str) -> None:
    """
    Renders HTML cleanly without leading spaces on each line so that
    Streamlit's markdown parser never treats HTML elements as 4-space code blocks.
    """
    cleaned = "\n".join(line.strip() for line in html_str.strip().splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def render_tech_tags(tech_list: list[str]) -> str:
    return "".join(f'<span class="skill-tag">{t}</span>' for t in tech_list)


def get_resume_bytes() -> bytes | None:
    try:
        if RESUME_PDF.exists():
            return RESUME_PDF.read_bytes()
    except Exception:
        pass
    return None


# ──────────────────────────────────────────────────────────────────────────────
# SECTION RENDERERS
# ──────────────────────────────────────────────────────────────────────────────
def go_to_chat():
    """Navigate to chat page AND sync the pills widget key."""
    target = "AI Resume Assistant ✦"
    st.session_state["current_page"] = target
    st.session_state["nav_selection"] = target
    if "chat_history" not in st.session_state or len(st.session_state.chat_history) == 0:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 I am Dilpreet Kaur's AI Portfolio Assistant.\n\n"
                    "I can answer questions about her background in AI/ML & Data Science, "
                    "her ML internship at the National Informatics Centre (NIC), "
                    "or her 4 live deployed applications:\n"
                    "- Enterprise IT Support Agentic RAG Copilot (LangGraph, Pinecone, Groq, Tavily)\n"
                    "- AI Travel Agent (LangGraph, Groq, PostgreSQL)\n"
                    "- Deep Packet Inspection (C++, Random Forest Threat Detection)\n"
                    "- Resumind (React, TypeScript, Puter.js ATS Scanner)\n\n"
                    "Click any suggested topic below or type your question!"
                )
            }
        ]


def go_to_projects():
    """Navigate to projects page AND sync the pills widget key."""
    target = "Projects (4 Live)"
    st.session_state["current_page"] = target
    st.session_state["nav_selection"] = target


def render_hero():
    photo_b64 = get_image_b64(PROFILE_PHOTO)
    photo_html = ""
    candidate_name = PROFILE["name"]
    if photo_b64:
        photo_html = f'<div class="profile-photo-wrap"><img src="data:image/jpeg;base64,{photo_b64}" alt="{candidate_name}"></div>'

    render_html(f"""
<div class="hero-block">
{photo_html}
<div class="hero-text">
<div class="hero-name">{PROFILE['name']}</div>
<div class="hero-headline">{PROFILE['headline']}</div>
<div class="hero-bio">
B.Tech IT student at GTBIT, Delhi (2027) building AI projects and deploying them as live demos. Former ML Intern at the <strong>National Informatics Centre (NIC)</strong>. Open to AI/ML and Data Science internships.
</div>
<div class="hero-links">
<a class="hero-link" href="{PROFILE['github']}" target="_blank">⌥ GitHub</a>
<a class="hero-link" href="{PROFILE['linkedin']}" target="_blank">in LinkedIn</a>
<a class="hero-link" href="mailto:{PROFILE['email']}">✉ Email</a>
<a class="hero-link" href="#" onclick="return false;">📍 {PROFILE['location']}</a>
</div>
</div>
</div>
""")

    col1, col2, col3 = st.columns([1.2, 1.2, 1.4])
    with col1:
        st.button("✦ Chat With My Resume", type="primary", key="hero_chat", on_click=go_to_chat, use_container_width=True)
    with col2:
        st.button("🚀 Explore Live Projects (4)", key="hero_explore", on_click=go_to_projects, use_container_width=True)
    with col3:
        resume_bytes = get_resume_bytes()
        if resume_bytes:
            st.download_button(
                label="⬇ Download Resume",
                data=resume_bytes,
                file_name="Dilpreet_Kaur_Resume.pdf",
                mime="application/pdf",
                key="hero_dl",
                use_container_width=True
            )


def render_about():
    render_html('<div class="section-heading">About Me</div>')
    for para in PROFILE["bio"].split("\n\n"):
        render_html(f'<p style="font-size:0.86rem; color:#8899bb; line-height:1.75;">{para}</p>')


def render_skills():
    render_html('<div class="section-heading">Technical Skills</div>')
    for cat in SKILLS:
        render_html(f'<div class="skill-category-label">{cat["category"]}</div>')
        tags = "".join(f'<span class="skill-tag">{item}</span>' for item in cat["items"])
        render_html(f'<div style="margin-bottom:0.5rem;">{tags}</div>')


def render_experience():
    render_html('<div class="section-heading">Experience & Internships</div>')
    for exp in EXPERIENCE:
        points_html = "".join(f'<div class="exp-point">{p}</div>' for p in exp["points"])
        tech_html = render_tech_tags(exp["tech"])

        render_html(f"""
<div class="exp-card">
<div class="exp-role">{exp['role']}</div>
<div class="exp-company">{exp['company']}</div>
<div class="exp-meta">{exp['duration']} · {exp['location']}</div>
{points_html}
<div style="margin-top:0.8rem;">{tech_html}</div>
</div>
""")

        if exp.get("certificate") and Path(str(exp["certificate"])).exists():
            cert_path = Path(str(exp["certificate"]))
            cert_bytes = cert_path.read_bytes()
            st.download_button(
                label="↓ View Internship Certificate",
                data=cert_bytes,
                file_name="NIC_Internship_Certificate.pdf",
                mime="application/pdf",
                key=f"cert_{exp['company'].replace(' ', '_')}",
            )


def render_projects():
    render_html('<div class="section-heading">Projects</div>')
    for idx, proj in enumerate(PROJECTS):
        links_html = ""
        if proj.get("github"):
            links_html += f'<a class="project-link" href="{proj["github"]}" target="_blank">GitHub →</a>'
        if proj.get("live"):
            links_html += f'<a class="project-link" href="{proj["live"]}" target="_blank">Live Demo ↗</a>'

        tech_html = render_tech_tags(proj["tech"])

        thumb_html = ""
        if proj.get("thumb") and Path(str(proj["thumb"])).exists():
            b64 = get_image_b64(Path(str(proj["thumb"])))
            if b64:
                thumb_html = f'<img src="data:image/png;base64,{b64}" style="width:100%;border-radius:6px;margin-bottom:0.8rem;opacity:0.85;" alt="{proj["name"]}">'

        render_html(f"""
<div class="project-card">
{thumb_html}
<div class="project-tag">{proj['tag']}</div>
<div class="project-name">{proj['name']}</div>
<div class="project-summary">{proj['summary']}</div>
<div class="project-desc">{proj['description']}</div>
<div style="margin-bottom:0.8rem;">{tech_html}</div>
<div class="project-links">{links_html}</div>
</div>
""")


def render_education():
    render_html('<div class="section-heading">Education</div>')
    for edu in EDUCATION:
        render_html(f"""
<div class="edu-card">
<div class="edu-degree">{edu['degree']}</div>
<div class="edu-inst">{edu['institution']}</div>
<div class="edu-meta">{edu['duration']} · {edu['score']}</div>
</div>
""")

    render_html('<div class="section-heading" style="margin-top:1.5rem;">Certifications</div>')
    cert_html = "".join(
        f'<span class="cert-chip">🏅 {c["name"]} <span style="color:#3a5060;">· {c["issuer"]}</span></span>'
        for c in CERTIFICATIONS
    )
    render_html(f'<div style="display:flex;flex-wrap:wrap;gap:0.3rem;">{cert_html}</div>')

    render_html('<div class="section-heading" style="margin-top:1.5rem;">Achievements</div>')
    for ach in ACHIEVEMENTS:
        render_html(
            f'<div class="edu-card" style="padding:0.9rem 1.2rem;">'
            f'<span style="font-size:0.85rem; color:#c8d4ea; font-weight:500;">{ach}</span></div>'
        )


def render_chat():
    """Full AI Resume Chatbot UI."""
    # Init session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "custom_session_id" not in st.session_state:
        st.session_state.custom_session_id = None
    if "custom_resume_name" not in st.session_state:
        st.session_state.custom_resume_name = None

    # Backend status indicator
    health = check_backend()
    if health.get("ok"):
        hd = health.get("data", {})
        status_dot = "🟢" if hd.get("resume_loaded") else "🟡"
        model_name = hd.get("model", "openai/gpt-oss-120b")
        render_html(
            f'<div style="font-size:0.73rem; color:#3a5060; margin-bottom:0.8rem;">'
            f'{status_dot} Backend online · Model: <code style="color:#5a7090;">{model_name}</code></div>'
        )
    else:
        st.error("⚠️ Cannot reach the backend. Make sure FastAPI is running on port 8000.")
        return

    # Welcome card
    render_html("""
<div class="chat-welcome">
<div class="chat-welcome-title">✦ AI Resume Assistant</div>
<div class="chat-welcome-sub">
Ask me anything about Dilpreet's background, skills, internship, or projects.
Answers are grounded strictly in the verified resume and will clearly indicate
when information is not available.
</div>
</div>
""")

    # Suggested questions
    render_html('<div style="font-size:0.73rem; color:#4a6080; margin-bottom:0.5rem; font-weight:600; letter-spacing:0.06em;">SUGGESTED QUESTIONS</div>')
    sq_cols = st.columns(3)
    for i, q in enumerate(SUGGESTED_QUESTIONS):
        if sq_cols[i % 3].button(q, key=f"sq_{i}", use_container_width=True):
            _submit_question(q)

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Chat history
    if st.session_state.chat_history:
        chat_html = ['<div class="chat-container">']
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html.append(f"""
<div class="chat-msg user">
<div class="chat-avatar user">You</div>
<div class="chat-bubble user">{msg['content']}</div>
</div>""")
            else:
                chat_html.append(f"""
<div class="chat-msg">
<div class="chat-avatar bot">AI</div>
<div class="chat-bubble bot">{msg['content']}</div>
</div>""")
        chat_html.append("</div>")
        render_html("".join(chat_html))
        render_html('<div class="chat-grounding-note">ⓘ Answers are grounded in the verified resume. Information not present in the resume will be stated clearly.</div>')

    # Input area
    st.markdown("<br>", unsafe_allow_html=True)
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Ask a question:",
            placeholder="Ask about Dilpreet's experience, skills, or projects…",
            key="chat_input",
            label_visibility="collapsed"
        )
    with col_btn:
        send = st.button("Send", type="primary", key="send_btn", use_container_width=True)

    if send and user_input.strip():
        _submit_question(user_input.strip())

    # Clear chat
    if st.session_state.chat_history:
        if st.button("Clear conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    # ── Optional: Upload Your Own Resume ──────────────────────────────────────
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    with st.expander("📂 Upload Your Own Resume (optional analysis mode)"):
        render_html(
            '<div style="font-size:0.78rem; color:#4a6080; margin-bottom:0.8rem;">'
            'Upload your PDF to ask questions about <em>your own</em> resume. '
            'Your document is processed in memory only, isolated from the portfolio resume, '
            'and is not permanently stored.</div>'
        )

        if st.session_state.custom_session_id:
            render_html(
                f'<div style="font-size:0.78rem; color:#4aba70; margin-bottom:0.6rem;">'
                f'✓ Uploaded: <strong>{st.session_state.custom_resume_name}</strong></div>'
            )
            if st.button("Discard uploaded resume", key="discard_custom"):
                try:
                    requests.delete(
                        f"{BACKEND_URL}/resume/upload/{st.session_state.custom_session_id}",
                        timeout=6
                    )
                except Exception:
                    pass
                st.session_state.custom_session_id = None
                st.session_state.custom_resume_name = None
                st.rerun()
        else:
            uploaded_file = st.file_uploader(
                "Choose a PDF", type=["pdf"], key="resume_upload"
            )
            if uploaded_file:
                if uploaded_file.size > 5 * 1024 * 1024:
                    st.error("File too large. Maximum size is 5MB.")
                else:
                    with st.spinner("Parsing uploaded resume…"):
                        try:
                            resp = requests.post(
                                f"{BACKEND_URL}/resume/upload",
                                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                                timeout=60
                            )
                            if resp.status_code == 200:
                                data = resp.json()
                                st.session_state.custom_session_id = data.get("session_id")
                                st.session_state.custom_resume_name = data.get("name", uploaded_file.name)
                                st.success(f"Resume parsed for: {data.get('name', 'Unknown')}")
                                st.rerun()
                            else:
                                st.error(f"Upload failed: {resp.json().get('detail', 'Unknown error')}")
                        except Exception as e:
                            st.error(f"Could not upload resume: {str(e)[:200]}")


def _submit_question(question: str):
    """Sends the question to the backend and appends results to chat history."""
    st.session_state.chat_history.append({"role": "user", "content": question})
    with st.spinner("Thinking…"):
        result = backend_chat(question, st.session_state.get("custom_session_id"))
    if result["ok"]:
        answer = result["data"].get("answer", "No answer returned.")
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"⚠️ {result['error']}"
        })
    st.rerun()


def render_contact():
    render_html('<div class="section-heading">Get In Touch</div>')
    resume_bytes = get_resume_bytes()
    render_html(f"""
<div class="contact-card">
<div style="font-size:0.92rem; font-weight:600; color:#c8d4ea; margin-bottom:0.5rem;">Dilpreet Kaur</div>
<div style="font-size:0.8rem; color:#4a6080; margin-bottom:1.2rem;">New Delhi, India · Open to internships and entry-level roles</div>
<div>
<a href="mailto:{PROFILE['email']}">✉ {PROFILE['email']}</a>
<a href="{PROFILE['linkedin']}" target="_blank">in LinkedIn</a>
<a href="{PROFILE['github']}" target="_blank">⌥ GitHub</a>
</div>
<div class="contact-sub">Feel free to reach out for collaboration, internships, or just to connect.</div>
</div>
""")
    if resume_bytes:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇ Download Resume PDF",
            data=resume_bytes,
            file_name="Dilpreet_Kaur_Resume.pdf",
            mime="application/pdf",
            key="contact_dl",
        )


# ──────────────────────────────────────────────────────────────────────────────
# MAIN APP
# ──────────────────────────────────────────────────────────────────────────────
def main():
    load_css()
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Overview"

    # Top Brand Header & Segmented Navbar
    col_brand, col_nav, col_cta = st.columns([1.6, 4.0, 1.2], vertical_alignment="center")
    with col_brand:
        render_html('<div class="brand-logo">✦ DILPREET KAUR</div>')
    with col_nav:
        nav_options = [
            "Overview",
            "Projects (4 Live)",
            "AI Resume Assistant ✦",
            "Experience & Skills",
            "Contact"
        ]
        if st.session_state.current_page not in nav_options:
            st.session_state.current_page = "Overview"

        def on_nav_change():
            chosen = st.session_state.get("nav_selection")
            if chosen:
                st.session_state.current_page = chosen
            else:
                st.session_state.nav_selection = st.session_state.current_page

        if "nav_selection" not in st.session_state:
            st.session_state.nav_selection = st.session_state.current_page

        selected = st.pills(
            "Navigation",
            options=nav_options,
            label_visibility="collapsed",
            key="nav_selection",
            on_change=on_nav_change
        )
        if selected and selected != st.session_state.current_page:
            st.session_state.current_page = selected
            st.rerun()

    with col_cta:
        resume_bytes = get_resume_bytes()
        if resume_bytes:
            st.download_button(
                label="⬇ Resume PDF",
                data=resume_bytes,
                file_name="Dilpreet_Kaur_Resume.pdf",
                mime="application/pdf",
                key="top_nav_resume_btn",
                use_container_width=True
            )

    render_html("<div class='section-divider' style='margin: 1.2rem 0 2rem;'></div>")

    # Render Active Section dynamically
    if st.session_state.current_page == "Overview":
        render_hero()
        render_about()
        render_html("<div class='section-divider' style='margin: 2.2rem 0 1.8rem;'></div>")
        render_projects()
        
    elif st.session_state.current_page == "Projects (4 Live)":
        render_projects()
        
    elif st.session_state.current_page == "AI Resume Assistant ✦":
        render_chat()
        
    elif st.session_state.current_page == "Experience & Skills":
        render_skills()
        render_html("<div class='section-divider' style='margin: 1.8rem 0;'></div>")
        render_experience()
        render_html("<div class='section-divider' style='margin: 1.8rem 0;'></div>")
        render_education()
        
    elif st.session_state.current_page == "Contact":
        render_contact()


if __name__ == "__main__":
    main()
