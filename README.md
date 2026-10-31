# Dilpreet Kaur · AI Portfolio & Interactive AI Assistant

A recruiter-focused portfolio with a modern **React + TypeScript** frontend and a **FastAPI** backend. The frontend uses Vite, Tailwind CSS, Framer Motion, Lucide, and Lenis. FastAPI serves verified portfolio data and the existing Groq-powered, grounded AI assistant. The original Streamlit portfolio is retained as a legacy frontend.

---

## 🌟 Key Features

- **Modern React portfolio**: Responsive sections for background, skills, featured projects, experience, certifications, and contact.
- **Grounded AI Resume Assistant**: Groq-powered assistant answering recruiter, hiring manager, and engineer queries with zero hallucinations, strictly grounded in verified resume data.
- **FastAPI REST Backend**: Health checks, public resume endpoint, structured chat endpoint, in-memory candidate resume caching, and isolated PDF upload sessions.
- **Legacy Streamlit UI**: Existing Python portfolio remains available and continues to use the same backend and assistant logic.
- **Automated Test Suite**: Pytest test suite validating ground-truth schemas, live links, and offline fallback mechanisms.

---

## 🚀 Featured Live Projects

| Project | Tech Stack | Live Demo | Repository |
| :--- | :--- | :--- | :--- |
| **Enterprise IT Support Agentic RAG Copilot** | LangGraph, FastAPI, Pinecone, Groq, Tavily, Docker | [Live Demo ↗](https://enterprise-it-support-copilot.vercel.app/) | [GitHub →](https://github.com/Dilpreetk11/IT-Support-Agentic-RAG-Copilot) |
| **AI Travel Planning Agent (LangGraph with Long-Term Memory)** | LangGraph, LangChain, Groq Llama 3.3, PostgreSQL, Tavily | [Live Demo ↗](https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/) | [GitHub →](https://github.com/Dilpreetk11/AI-Travel-Agent) |
| **GridScan RL (Reinforcement Learning Environment)** | Python, NumPy, FastAPI, React, Q-learning | [Live Demo ↗](https://rl-gridscan.onrender.com/) | — |
| **AI-Powered Deep Packet Inspection & Threat Detection** | C++, Python, CMake, Scikit-learn, Random Forest | [Live Demo ↗](https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/) | [GitHub →](https://github.com/Dilpreetk11/AI-Powered-Deep-Packet-Inspection-Threat-Detection) |
| **Resumind (AI Resume Analyzer)** | React, TypeScript, Vite, Tailwind CSS, Puter.js | [Live Demo ↗](https://resumind-cmdp.onrender.com/) | [GitHub →](https://github.com/Dilpreetk11/Resumind) |
| **Telco Customer Churn Prediction** | Python, LightGBM, MLflow, FastAPI, Gradio | — | [GitHub →](https://github.com/Dilpreetk11/ML-Churn-Prediction) |

---

## 🛠️ Tech Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Framer Motion, Lucide React, Lenis
- **Backend**: FastAPI, Uvicorn, Pydantic v2
- **LLM & Inference**: Groq API (`openai/gpt-oss-120b`, fallback `llama-3.3-70b-versatile`)
- **Document Processing**: PyPDF, Structured JSON validation
- **Testing**: Pytest

---

## 💻 Local Setup & Execution

### 1. Install backend dependencies

```bash
git clone https://github.com/Dilpreetk11/Dilpreet-Kaur-Portfolio-app.git
cd Dilpreet-Kaur-Portfolio-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

Install the React dependencies in a second terminal:

```bash
cd frontend
npm install
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

For local Vite development, the `/api` path is proxied to FastAPI at port `8000` by default. For a deployed frontend, set `VITE_API_BASE_URL` in the Vercel project settings to the public FastAPI origin.

### 3. Run the services

**Terminal 1 — FastAPI Backend**:
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 — React frontend**:
```bash
cd frontend
npm run dev
```

Open the React site at `http://localhost:5173`. Vite proxies `/api` requests to FastAPI at `http://127.0.0.1:8000`.

To run the retained Streamlit frontend instead, use:

```bash
python -m streamlit run frontend/app.py
```

### Build the React frontend

```bash
cd frontend
npm run build
npm run preview
```

The static production files are written to `frontend/dist`.

## 🚀 Deployment

### Vercel frontend

Create a Vercel project with `frontend` as its Root Directory. Use `npm run build` as the build command and `dist` as the output directory. The frontend defaults to the deployed Render API and accepts `VITE_API_BASE_URL` as an override (without a trailing slash). This value is a public API URL; never put model keys in `VITE_*` variables.

### Render FastAPI backend

Deploy the repository as a Python web service. Use `pip install -r requirements.txt` as the build command and `uvicorn main:app --host 0.0.0.0 --port $PORT` as the start command. Configure `GROQ_API_KEY`, `GROQ_MODEL`, `PORTFOLIO_RESUME_PATH=data/my_resume.pdf`, and `ADDITIONAL_ALLOWED_ORIGINS` with the deployed Vercel origin. Keep the Groq key only in the backend environment. The health endpoint is `/health`.

---

## 🧪 Running Tests

```bash
python -m pytest
```

The React production build is checked separately with `cd frontend && npm run build`.

---

## 📬 Contact & Links

- **LinkedIn**: [linkedin.com/in/dilpreet-kaur-a71413317](https://www.linkedin.com/in/dilpreet-kaur-a71413317)
- **GitHub**: [github.com/Dilpreetk11](https://github.com/Dilpreetk11)
- **Email**: dilpreetk401@gmail.com
