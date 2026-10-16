import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load .env file from project root
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# ── Streamlit Cloud secrets fallback ──
# When deployed on Streamlit Cloud, .env is gitignored.
# Secrets set via the Streamlit Cloud UI are loaded here.
try:
    import streamlit as st
    for key in ("GROQ_API_KEY", "GROQ_MODEL", "PORTFOLIO_RESUME_PATH"):
        if key in st.secrets and not os.getenv(key):
            os.environ[key] = str(st.secrets[key])
except Exception:
    pass  # Not running inside Streamlit (e.g. FastAPI standalone)


class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()
    FALLBACK_MODEL: str = os.getenv("FALLBACK_MODEL", "llama-3.3-70b-versatile").strip()
    PORTFOLIO_RESUME_PATH: Path = ROOT_DIR / os.getenv(
        "PORTFOLIO_RESUME_PATH", "data/my_resume.pdf"
    )
    FASTAPI_HOST: str = os.getenv("FASTAPI_HOST", "127.0.0.1").strip()
    FASTAPI_PORT: int = int(os.getenv("FASTAPI_PORT", "8000"))
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

    @property
    def allowed_origins(self) -> List[str]:
        raw = os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:8501,http://127.0.0.1:8501,http://localhost:3000,http://127.0.0.1:3000"
        )
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

    @property
    def is_groq_ready(self) -> bool:
        return bool(self.GROQ_API_KEY and len(self.GROQ_API_KEY) > 10)


settings = Settings()
