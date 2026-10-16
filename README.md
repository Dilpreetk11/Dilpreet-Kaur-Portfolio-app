# Dilpreet Kaur · AI Portfolio & Interactive AI Assistant ✦

An interactive, full-stack AI engineering portfolio and candidate copilot built with **FastAPI**, **Streamlit**, and **Groq LLM inference**. Demonstrates live deployed applications in agentic RAG, multi-agent systems, network threat detection, and ATS resume intelligence.

---

## 🌟 Key Features

- **Segmented Interactive UI**: Responsive Streamlit frontend with glassmorphism aesthetics, live project showcase, interactive resume viewers, and certificate downloads.
- **Grounded AI Resume Assistant**: Groq-powered assistant answering recruiter, hiring manager, and engineer queries with zero hallucinations, strictly grounded in verified resume data.
- **FastAPI REST Backend**: High-performance backend providing health checks, structured chat endpoints, in-memory candidate resume caching, and isolated PDF upload sessions.
- **Dual Runtime Resilience**: Standalone and microservices modes — seamlessly functions with or without the FastAPI server running.
- **Automated Test Suite**: Pytest test suite validating ground-truth schemas, live links, and offline fallback mechanisms.

---

## 🚀 Featured Live Projects

| Project | Tech Stack | Live Demo | Repository |
| :--- | :--- | :--- | :--- |
| **Enterprise IT Support Agentic RAG Copilot** | LangGraph, FastAPI, Pinecone, Groq, Tavily, Docker | [Live Demo ↗](https://it-support-agentic-rag-copilot-brakzz3tuwuejuwhxmkkh8.streamlit.app/) | [GitHub →](https://github.com/Dilpreetk11/IT-Support-Agentic-RAG-Copilot) |
| **AI Travel Agent (Multi-Agent System)** | LangGraph, LangChain, Groq, PostgreSQL, Tavily | [Live Demo ↗](https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/) | [GitHub →](https://github.com/Dilpreetk11/AI-Travel-Agent) |
| **AI-Powered Deep Packet Inspection & Threat Detection** | C++, Python, CMake, Scikit-learn, Random Forest | [Live Demo ↗](https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/) | [GitHub →](https://github.com/Dilpreetk11/AI-Powered-Deep-Packet-Inspection-Threat-Detection) |
| **Resumind (AI Resume Analyzer)** | React, TypeScript, Vite, Tailwind CSS, Puter.js | [Live Demo ↗](https://resumind-cmdp.onrender.com/) | [GitHub →](https://github.com/Dilpreetk11/Resumind) |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Custom Modern Vanilla CSS / Glassmorphism Design System
- **Backend**: FastAPI, Uvicorn, Pydantic v2
- **LLM & Inference**: Groq API (`openai/gpt-oss-120b`, fallback `llama-3.3-70b-versatile`)
- **Document Processing**: PyPDF, Structured JSON validation
- **Testing**: Pytest

---

## 💻 Local Setup & Execution

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/Dilpreetk11/Dilpreet-Kaur-Portfolio-app.git
cd Dilpreet-Kaur-Portfolio-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Add your Groq API key in `.env`:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

### 3. Run the Services

**Terminal 1 — FastAPI Backend**:
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 — Streamlit Frontend**:
```bash
python -m streamlit run frontend/app.py
```

Open your browser at `http://localhost:8501`.

---

## 🧪 Running Tests

```bash
python -m pytest
```

---

## 📬 Contact & Links

- **LinkedIn**: [linkedin.com/in/dilpreet-kaur-a71413317](https://www.linkedin.com/in/dilpreet-kaur-a71413317)
- **GitHub**: [github.com/Dilpreetk11](https://github.com/Dilpreetk11)
- **Email**: dilpreetk401@gmail.com
