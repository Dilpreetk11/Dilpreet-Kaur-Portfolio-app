import { Fragment, useEffect, useMemo, useState, type ReactNode } from "react";
import { AnimatePresence, motion, useReducedMotion } from "framer-motion";
import Lenis from "lenis";
import {
  ArrowDown,
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  Check,
  Code2,
  Github,
  Linkedin,
  Mail,
  Menu,
  MessageCircle,
  RotateCcw,
  Send,
  Sparkles,
  X,
} from "lucide-react";
import { askAssistant, fetchResume } from "./api";
import type { Project, Resume } from "./types";

const projectImages: Record<string, string> = {
  "GridScan RL": "/assets/gridscan-preview.png",
  "Deep Packet": "/assets/dpi-thumbnail.png",
  Travel: "/assets/travel-agent-thumbnail.png",
  "IT Support": "/assets/it-support-thumbnail.png",
  Resumind: "/assets/resumind-thumbnail.png",
};

const fallback: Resume = {
  name: "Dilpreet Kaur",
  headline: "AI/ML Engineer",
  email: "dilpreetk401@gmail.com",
  location: "New Delhi, India",
  github: "https://github.com/Dilpreetk11",
  linkedin: "https://www.linkedin.com/in/dilpreet-kaur-a71413317",
  summary:
    "B.Tech Information Technology student (2027) building AI/ML solutions. Former Machine Learning Intern at NIC with experience in end-to-end AI applications.",
  skills: [
    "Python",
    "C++",
    "SQL",
    "Supervised Learning",
    "Classification",
    "Random Forest",
    "LightGBM",
    "Scikit-learn",
    "Reinforcement Learning (Q-learning)",
    "Feature Engineering",
    "Hyperparameter Tuning",
    "Model Evaluation",
    "MLflow",
    "Neural Networks",
    "Hugging Face",
    "Fine-tuning",
    "Text Summarization",
    "Text Classification",
    "FastAPI",
    "Streamlit",
    "React",
    "TypeScript",
    "Git",
    "Pandas",
    "NumPy",
  ],
  skill_categories: [
    {
      category: "Machine Learning",
      skills: [
        "Supervised Learning",
        "Classification",
        "Random Forest",
        "LightGBM",
        "Scikit-learn",
        "Reinforcement Learning (Q-learning)",
        "Feature Engineering",
        "Hyperparameter Tuning",
        "Model Evaluation",
        "MLflow",
      ],
    },
    {
      category: "Deep Learning & NLP",
      skills: [
        "Neural Networks",
        "Transformers (T5, BERT)",
        "Hugging Face",
        "Fine-tuning",
        "Text Summarization",
        "Text Classification",
        "Embeddings",
      ],
    },
    {
      category: "LLM & Agents",
      skills: [
        "LLM Applications",
        "Prompt Engineering",
        "Multi-Agent Systems",
        "LangGraph",
        "LangChain",
      ],
    },
    {
      category: "Programming & data",
      skills: [
        "Python",
        "C++",
        "SQL",
        "Pandas",
        "NumPy",
        "PostgreSQL",
        "SQLite",
      ],
    },
    {
      category: "Backend & Deployment",
      skills: [
        "FastAPI",
        "REST APIs",
        "Streamlit",
        "Gradio",
        "Git",
        "GitHub",
        "React",
      ],
    },
  ],
  education: [
    {
      institution: "Guru Tegh Bahadur Institute of Technology, Delhi",
      degree: "B.Tech in Information Technology",
      duration: "2023 – 2027",
      score: "CGPA: 8.38",
      location: "Delhi, India",
    },
  ],
  experiences: [
    {
      role: "Machine Learning Intern",
      company: "National Informatics Centre (NIC)",
      duration: "Jun 2025 – Aug 2025",
      location: "New Delhi, India",
      responsibilities: [
        "Cleaned multi-gigabyte log datasets with Pandas and regex, and built a rule-based labeling system covering 7+ log categories (port scans, DDoS, failed SSH, malware) to bootstrap training labels at scale.",
        "Fine-tuned a T5-small transformer for security-log summarization on 500 labeled logs, reaching 0.91 ROUGE-1/ROUGE-L on validation.",
        "Built BERT-based classification pipelines to sort logs into 3 categories (Error, Warning, Information), streamlining triage for downstream analysis.",
        "Diagnosed a 0.91 to 0.45 ROUGE drop between validation and full-dataset inference and proposed GPT-4-assisted relabeling to improve generalization.",
      ],
      technologies: [
        "Python",
        "Pandas",
        "Hugging Face",
        "T5-small",
        "BERT",
        "ROUGE",
        "Streamlit",
        "Gradio",
      ],
    },
  ],
  projects: [
    {
      name: "Telco Customer Churn Prediction | End-to-End ML Pipeline",
      problem:
        "Identify telecom customers at risk of leaving so teams can target retention efforts.",
      description:
        "Built an end-to-end LightGBM pipeline on a 7,043-customer telecom dataset. Tracked experiments with MLflow, reached 91.7% recall for churn-prone customers, and deployed real-time inference through FastAPI and Gradio.",
      technologies: ["Python", "LightGBM", "MLflow", "FastAPI", "Gradio"],
      contributions: [
        "Built and tuned a churn model on 7,043 customer records.",
        "Reached 91.7% recall for churn-prone customers using MLflow-tracked experiments.",
        "Deployed an inference API and Gradio interface for real-time predictions.",
      ],
      github_url: "https://github.com/Dilpreetk11/ML-Churn-Prediction",
    },
    {
      name: "AI Travel Planning Agent | LangGraph with Long-Term Memory",
      problem:
        "Personalize trip itineraries from destination, duration, and budget while retaining conversation context.",
      description:
        "Built a LangGraph multi-agent planner using Tavily for travel research, Groq Llama 3.3 for reasoning, and PostgreSQL checkpointing for long-term conversation memory. Generated a seven-day Japan itinerary within a 2 lakh INR budget.",
      technologies: [
        "Python",
        "LangGraph",
        "LangChain",
        "PostgreSQL",
        "Groq Llama 3.3",
        "Tavily",
      ],
      contributions: [
        "Generated personalized travel plans from destination, duration, and budget.",
        "Retained conversation context across sessions with PostgreSQL checkpointing.",
        "Produced a seven-day Japan itinerary within a 2 lakh INR budget.",
      ],
      github_url: "https://github.com/Dilpreetk11/AI-Travel-Agent",
      live_url: "https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/",
    },
    {
      name: "GridScan RL | Reinforcement Learning Environment",
      problem:
        "Explore an obstacle grid efficiently while maximizing coverage of free tiles.",
      description:
        "Built a tabular Q-learning agent with Bellman updates and decaying epsilon-greedy exploration to scan a 10x10 obstacle grid. It reached 90.1% coverage (82 of 91 free tiles). Shaped rewards and cycle detection track coverage, collisions, and loops; a FastAPI and NumPy engine serves a React dashboard with live Q-values.",
      technologies: ["Python", "NumPy", "FastAPI", "React", "Q-learning"],
      contributions: [
        "Implemented tabular Q-learning with Bellman updates and exploration decay.",
        "Reached 90.1% coverage across 82 of 91 free tiles.",
        "Built a React dashboard showing live Q-values.",
      ],
      live_url: "https://rl-gridscan.onrender.com/",
    },
    {
      name: "Enterprise IT Support Agentic RAG Copilot",
      problem:
        "Enterprise support teams face repetitive tickets and scattered internal documentation.",
      description:
        "An IT support copilot that retrieves private knowledge, grades evidence, and can fall back to web search when a knowledge base cannot answer confidently.",
      technologies: [
        "Python",
        "LangGraph",
        "FastAPI",
        "Pinecone",
        "Groq",
        "Tavily",
        "Docker",
      ],
      contributions: [
        "Built evidence grading, query rewriting, and a guarded retrieval retry flow.",
        "Added a protected document upload pipeline and an interactive decision trace.",
      ],
      github_url:
        "https://github.com/Dilpreetk11/IT-Support-Agentic-RAG-Copilot",
      live_url: "https://enterprise-it-support-copilot.vercel.app/",
    },
    {
      name: "AI-Powered Deep Packet Inspection & Threat Detection",
      problem:
        "Network teams need to inspect traffic and identify suspicious behavior in PCAP data.",
      description:
        "A multithreaded C++ inspection engine that tracks network flows, extracts behavioral features, and classifies applications and threat patterns.",
      technologies: [
        "C++",
        "Python",
        "CMake",
        "Scikit-learn",
        "Random Forest",
        "Streamlit",
      ],
      contributions: [
        "Built PCAP parsing and five-tuple flow tracking.",
        "Engineered 32 flow features and trained models to classify application traffic and five threat classes.",
      ],
      github_url:
        "https://github.com/Dilpreetk11/AI-Powered-Deep-Packet-Inspection-Threat-Detection",
      live_url:
        "https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/",
    },
    {
      name: "Resumind | AI Resume Analyzer",
      problem:
        "Job seekers need actionable feedback on how a resume matches a specific role.",
      description:
        "An AI resume analyzer that scores a resume against a job description and returns practical, recruiter-style feedback.",
      technologies: [
        "React",
        "TypeScript",
        "Vite",
        "Tailwind CSS",
        "Zustand",
        "Puter.js",
      ],
      contributions: [
        "Built the React application and resume analysis flow.",
        "Added a demo mode to explore the dashboard without AI credits.",
      ],
      github_url: "https://github.com/Dilpreetk11/Resumind",
      live_url: "https://resumind-cmdp.onrender.com/",
    },
    {
      name: "Dilpreet Kaur Portfolio & AI Assistant",
      problem:
        "Recruiters need a clear way to explore Dilpreet’s background, projects, and technical work.",
      description:
        "A full-stack portfolio with a Streamlit frontend and FastAPI backend, featuring an AI assistant grounded in verified resume and project information.",
      technologies: [
        "Python",
        "Streamlit",
        "FastAPI",
        "Groq",
        "Pydantic",
        "Pytest",
      ],
      contributions: [
        "Connected a grounded portfolio assistant to a FastAPI backend.",
        "Created an interactive project and experience showcase.",
      ],
      github_url: "https://github.com/Dilpreetk11/Dilpreet-Kaur-Portfolio-app",
    },
  ],
  certifications: [
    "Microsoft Generative AI",
    "IBM Machine Learning with Python",
  ],
  achievements: [
    "Secured 1st Position at Perfect Pitch 2.0 Ideathon (E-Cell GTBIT x NASSCOM Foundation)",
    "Open-source contributor, GirlScript Summer of Code (GSSoC)",
  ],
};

const navItems = [
  ["About", "about"],
  ["Skills", "skills"],
  ["Projects", "projects"],
  ["Experience", "experience"],
  ["Achievements", "achievements"],
  ["Contact", "contact"],
];
const suggestions = [
  "Tell me about Dilpreet.",
  "What projects has she built?",
  "What was her NIC internship about?",
  "What is GridScan RL?",
];
const projectOrder = [
  "AI Travel Planning Agent",
  "GridScan RL",
  "AI-Powered Deep Packet Inspection",
  "Enterprise IT Support",
  "Resumind",
  "Portfolio",
  "Telco Customer Churn",
];
const reveal = { hidden: { opacity: 0, y: 22 }, visible: { opacity: 1, y: 0 } };

function useSmoothScroll() {
  useEffect(() => {
    const reduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;
    if (reduced) return;
    const lenis = new Lenis({ duration: 1.05, wheelMultiplier: 0.9 });
    let frame = 0;
    const tick = (time: number) => {
      lenis.raf(time);
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(frame);
      lenis.destroy();
    };
  }, []);
}

function SectionTitle({
  eyebrow,
  title,
  note,
}: {
  eyebrow: string;
  title: ReactNode;
  note?: string;
}) {
  return (
    <div className="section-title">
      <span className="eyebrow">{eyebrow}</span>
      <div className="section-title-row">
        <h2>{title}</h2>
        {note && <p>{note}</p>}
      </div>
    </div>
  );
}

function Header({ active, onOpenAssistant }: { active: string; onOpenAssistant: () => void }) {
  const [open, setOpen] = useState(false);
  return (
    <header className="site-header">
      <a className="wordmark" href="#home" aria-label="Dilpreet Kaur home">
        <span className="wordmark-mark">dk</span>
        <span>DILPREET KAUR</span>
      </a>
      <button
        className="mobile-menu"
        aria-label={open ? "Close menu" : "Open menu"}
        onClick={() => setOpen(!open)}
      >
        {open ? <X /> : <Menu />}
      </button>
      <nav
        className={open ? "nav-links is-open" : "nav-links"}
        aria-label="Main navigation"
      >
        {navItems.map(([label, id]) => (
          <Fragment key={id}>
            <a
              className={active === id ? "active" : ""}
              href={`#${id}`}
              onClick={() => setOpen(false)}
            >
              {label}
            </a>
            {id === "projects" && (
              <button
                className="nav-assistant"
                onClick={() => {
                  setOpen(false);
                  onOpenAssistant();
                }}
              >
                <Sparkles size={13} /> Assistant
              </button>
            )}
          </Fragment>
        ))}
        <a
          className="nav-contact"
          href="#contact"
          onClick={() => setOpen(false)}
        >
          Let’s talk <ArrowUpRight size={14} />
        </a>
      </nav>
    </header>
  );
}

function ProjectCard({
  project,
  index,
  total,
  onSelect,
}: {
  project: Project;
  index: number;
  total: number;
  onSelect: (project: Project) => void;
}) {
  const reduceMotion = useReducedMotion();
  const image = Object.entries(projectImages).find(([key]) =>
    project.name.includes(key),
  )?.[1];
  return (
    <motion.article
      className={`project-card project-card-${index + 1}`}
      variants={reveal}
      whileHover={reduceMotion ? undefined : { y: -6 }}
      transition={{ duration: reduceMotion ? 0 : 0.24 }}
    >
      {image && (
        <button
          className="project-image"
          onClick={() => onSelect(project)}
          aria-label={`View details for ${project.name}`}
        >
          <img loading="lazy" src={image} alt={`${project.name} preview`} />
          <span className="image-index">
            0{index + 1} / 0{total}
          </span>
          <span className="project-open">
            <ArrowUpRight size={20} />
          </span>
        </button>
      )}
      <div className="project-card-body">
        <div className="project-kicker">
          {project.technologies.slice(0, 3).join(" · ")}
        </div>
        <button
          className="project-title-button"
          onClick={() => onSelect(project)}
        >
          <h3>{project.name}</h3>
          <ArrowUpRight size={18} />
        </button>
        <p>{project.problem || project.description}</p>
        <div className="project-card-footer">
          <div className="project-quick-links">
            {project.github_url && (
              <a href={project.github_url} target="_blank" rel="noreferrer">
                GitHub <ArrowUpRight size={14} />
              </a>
            )}
            {project.live_url && (
              <a href={project.live_url} target="_blank" rel="noreferrer">
                Live project <ArrowUpRight size={14} />
              </a>
            )}
          </div>
          <button className="text-button" onClick={() => onSelect(project)}>
            Explore project <ArrowRight size={15} />
          </button>
        </div>
      </div>
    </motion.article>
  );
}

function ProjectDialog({
  project,
  onClose,
}: {
  project: Project | null;
  onClose: () => void;
}) {
  const reduceMotion = useReducedMotion();
  useEffect(() => {
    if (!project) return;
    const handle = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handle);
    document.body.classList.add("dialog-open");
    return () => {
      window.removeEventListener("keydown", handle);
      document.body.classList.remove("dialog-open");
    };
  }, [project, onClose]);
  return (
    <AnimatePresence>
      {project && (
        <motion.div
          className="dialog-backdrop"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onMouseDown={(e) => {
            if (e.target === e.currentTarget) onClose();
          }}
        >
          <motion.section
            className="project-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="dialog-title"
            initial={reduceMotion ? false : { opacity: 0, y: 24, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={reduceMotion ? undefined : { opacity: 0, y: 18, scale: 0.98 }}
            transition={reduceMotion ? { duration: 0 } : undefined}
          >
            <button
              className="dialog-close"
              onClick={onClose}
              aria-label="Close project details"
            >
              <X size={19} />
            </button>
            <span className="eyebrow">PROJECT NOTES</span>
            <h2 id="dialog-title">{project.name}</h2>
            <p className="dialog-description">{project.description}</p>
            <div className="dialog-tech">
              {project.technologies.map((tech) => (
                <span className="skill-pill" key={tech}>
                  {tech}
                </span>
              ))}
            </div>
            {project.contributions.length > 0 && (
              <div className="dialog-contributions">
                <h3>What I built</h3>
                {project.contributions.map((item) => (
                  <p key={item}>
                    <Check size={15} />
                    {item}
                  </p>
                ))}
              </div>
            )}
            <div className="dialog-links">
              {project.github_url && (
                <a
                  className="button button-dark"
                  href={project.github_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  View repository <Github size={16} />
                </a>
              )}
              {project.live_url && (
                <a
                  className="button button-lime"
                  href={project.live_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  Open live project <ArrowUpRight size={16} />
                </a>
              )}
            </div>
          </motion.section>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

type ChatMessage = { role: "assistant" | "user"; content: string };

function AnswerContent({ text }: { text: string }) {
  const renderInline = (value: string) =>
    value
      .split(/(\*\*[^*]+\*\*|https?:\/\/[^\s]+)/g)
      .filter(Boolean)
      .map((part, index) => {
        if (part.startsWith("**") && part.endsWith("**")) {
          return <strong key={index}>{part.slice(2, -2)}</strong>;
        }
        if (/^https?:\/\//.test(part)) {
          const cleanUrl = part.replace(/[.,;!?]+$/, "");
          const trailing = part.slice(cleanUrl.length);
          return (
            <span key={index}>
              <a href={cleanUrl} target="_blank" rel="noreferrer">
                {cleanUrl}
              </a>
              {trailing}
            </span>
          );
        }
        return part;
      });

  return (
    <div className="answer-content">
      {text.split(/\r?\n/).map((line, index) => {
        const content = line.trim();
        if (!content) return null;
        if (content.startsWith("- ")) {
          return (
            <p className="answer-bullet" key={index}>
              <span aria-hidden="true">·</span>
              {renderInline(content.slice(2))}
            </p>
          );
        }
        return (
          <p key={index}>{renderInline(content.replace(/^#{1,3}\s+/, ""))}</p>
        );
      })}
    </div>
  );
}

function Assistant({ open, onOpenChange }: { open: boolean; onOpenChange: (open: boolean) => void }) {
  const reduceMotion = useReducedMotion();
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Hi, I’m Dilpreet’s AI portfolio assistant. Ask me about her background, NIC internship, projects, skills, or achievements.",
    },
  ]);
  const reset = () => {
    setMessages([
      {
        role: "assistant",
        content:
          "Hi, I’m Dilpreet’s AI portfolio assistant. Ask me about her background, NIC internship, projects, skills, or achievements.",
      },
    ]);
    setError("");
    setInput("");
  };
  const send = async (value = input) => {
    const question = value.trim();
    if (!question || busy) return;
    setInput("");
    setError("");
    setMessages((current) => [...current, { role: "user", content: question }]);
    setBusy(true);
    try {
      const result = await askAssistant(question);
      setMessages((current) => [
        ...current,
        { role: "assistant", content: result.answer },
      ]);
    } catch {
      setError(
        "The assistant is unavailable right now. Please try again in a moment.",
      );
    } finally {
      setBusy(false);
    }
  };
  return (
    <div className="assistant-wrap">
      <AnimatePresence>
        {open && (
          <motion.aside
            className="assistant-panel"
            initial={reduceMotion ? false : { opacity: 0, y: 18, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={reduceMotion ? undefined : { opacity: 0, y: 18, scale: 0.97 }}
            transition={reduceMotion ? { duration: 0 } : undefined}
            role="dialog"
            aria-label="Portfolio assistant"
          >
            <div className="assistant-head">
              <div className="assistant-avatar">
                <Sparkles size={17} />
              </div>
              <div>
                <strong>Dilpreet’s AI assistant</strong>
                <span>
                  <i /> Grounded in verified details
                </span>
              </div>
              <button
                onClick={reset}
                aria-label="Start a new conversation"
                title="Start a new conversation"
              >
                <RotateCcw size={16} />
              </button>
              <button
                onClick={() => onOpenChange(false)}
                aria-label="Close assistant"
              >
                <X size={18} />
              </button>
            </div>
            <div className="assistant-messages" aria-live="polite">
              {messages.map((message, index) => (
                <motion.div
                  key={index}
                  initial={reduceMotion ? false : { opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={reduceMotion ? { duration: 0 } : undefined}
                  className={`chat-message ${message.role}`}
                >
                  {message.role === "assistant" ? (
                    <AnswerContent text={message.content} />
                  ) : (
                    message.content
                  )}
                </motion.div>
              ))}
              {busy && (
                <div className="typing">
                  <i />
                  <i />
                  <i />
                </div>
              )}
              {error && <p className="chat-error">{error}</p>}
              {messages.length === 1 && (
                <div className="suggestions">
                  {suggestions.map((question) => (
                    <button key={question} onClick={() => void send(question)}>
                      {question}
                      <ArrowUpRight size={12} />
                    </button>
                  ))}
                </div>
              )}
            </div>
            <form
              className="assistant-form"
              onSubmit={(e) => {
                e.preventDefault();
                void send();
              }}
            >
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about projects or experience…"
                aria-label="Your question"
                maxLength={1000}
              />
              <button
                aria-label="Send question"
                disabled={!input.trim() || busy}
              >
                <Send size={16} />
              </button>
            </form>
          </motion.aside>
        )}
      </AnimatePresence>
      <button
        className={`assistant-launcher ${open ? "is-open" : ""}`}
        onClick={() => onOpenChange(!open)}
        aria-label={
          open ? "Close portfolio assistant" : "Ask the portfolio assistant"
        }
      >
        {open ? (
          <X size={21} />
        ) : (
          <>
            <MessageCircle size={20} />
            <span>Ask my AI</span>
            <span className="launcher-spark">
              <Sparkles size={13} />
            </span>
          </>
        )}
      </button>
    </div>
  );
}

export default function App() {
  useSmoothScroll();
  const [resume, setResume] = useState<Resume>(fallback);
  const [active, setActive] = useState("home");
  const [selected, setSelected] = useState<Project | null>(null);
  const [assistantOpen, setAssistantOpen] = useState(false);
  const [apiAvailable, setApiAvailable] = useState<boolean | null>(null);
  const reduceMotion = useReducedMotion();
  const projects = useMemo(
    () =>
      resume.projects
        .filter((project) => !project.name.toLowerCase().includes("portfolio"))
        .slice()
        .sort((left, right) => {
        const leftIndex = projectOrder.findIndex((name) =>
          left.name.includes(name),
        );
        const rightIndex = projectOrder.findIndex((name) =>
          right.name.includes(name),
        );
        return (
          (leftIndex < 0 ? projectOrder.length : leftIndex) -
          (rightIndex < 0 ? projectOrder.length : rightIndex)
        );
      }),
    [resume.projects],
  );

  useEffect(() => {
    let alive = true;
    fetchResume()
      .then((data) => {
        if (alive) {
          setResume(data);
          setApiAvailable(true);
        }
      })
      .catch(() => {
        if (alive) setApiAvailable(false);
      });
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) setActive(visible.target.id);
      },
      { rootMargin: "-22% 0px -58% 0px", threshold: [0, 0.2, 0.5] },
    );
    document
      .querySelectorAll("main section[id]")
      .forEach((section) => observer.observe(section));
    return () => {
      alive = false;
      observer.disconnect();
    };
  }, []);

  const motionProps = reduceMotion
    ? {}
    : {
        initial: "hidden",
        whileInView: "visible",
        viewport: { once: true, amount: 0.16 },
        variants: reveal,
        transition: { duration: 0.65, ease: [0.22, 1, 0.36, 1] as const },
      };
  return (
    <>
      <Header active={active} onOpenAssistant={() => setAssistantOpen(true)} />
      {apiAvailable === false && (
        <div className="api-notice">
          <span /> Showing the saved portfolio profile. The assistant reconnects
          when the API is available.
        </div>
      )}
      <main>
        <section id="home" className="hero section-shell">
          <div className="hero-grid" aria-hidden="true">
            <span />
            <span />
            <span />
            <span />
            <span />
            <span />
          </div>
          <div className="hero-copy">
            <motion.div
              initial={reduceMotion ? false : { opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7 }}
              className="availability"
            >
              <span className="availability-dot" /> AI/ML ENGINEER · NEW DELHI,
              INDIA <ArrowDownRight size={14} />
            </motion.div>
            <motion.p
              className="hero-overline"
              initial={reduceMotion ? false : { opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.15 }}
            >
              AI / ML · SOFTWARE · INTELLIGENT SYSTEMS
            </motion.p>
            <motion.h1
              initial={reduceMotion ? false : { opacity: 0, y: 22 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.75, delay: 0.12 }}
            >
              Building ideas
              <br />
              into <em>useful</em> systems<span className="hero-period">.</span>
            </motion.h1>
            <motion.p
              className="hero-intro"
              initial={reduceMotion ? false : { opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.28 }}
            >
              {resume.name} is an AI/ML Engineer and B.Tech Information
              Technology student at GTBIT, building practical AI/ML solutions
              and end-to-end applications.
            </motion.p>
            <motion.div
              className="hero-actions"
              initial={reduceMotion ? false : { opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <a className="button button-dark" href="#projects">
                View selected work <ArrowDownRight size={16} />
              </a>
              <a
                className="button button-outline"
                href="/downloads/Dilpreet_Kaur_Resume.pdf?v=20261101-126334"
                download="Dilpreet_Kaur_Resume.pdf"
              >
                Download résumé <ArrowDown size={15} />
              </a>
            </motion.div>
            <motion.div
              className="hero-socials"
              initial={reduceMotion ? false : { opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.55 }}
            >
              {resume.linkedin && (
                <a href={resume.linkedin} target="_blank" rel="noreferrer">
                  <Linkedin size={15} /> LinkedIn <ArrowUpRight size={12} />
                </a>
              )}
              {resume.github && (
                <a href={resume.github} target="_blank" rel="noreferrer">
                  <Github size={15} /> GitHub <ArrowUpRight size={12} />
                </a>
              )}
            </motion.div>
          </div>
          <motion.div
            className="hero-visual"
            initial={reduceMotion ? false : { opacity: 0, scale: 0.97 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.85, delay: 0.18 }}
          >
            <div className="portrait-frame">
              <img
                src="/assets/profile-photo.jpg"
                alt="Dilpreet Kaur"
                fetchPriority="high"
              />
              <div className="portrait-label">
                <span>DELHI, INDIA</span>
                <span>BASED IN DELHI</span>
              </div>
            </div>
            <div className="hero-stamp">
              <span>
                CURIOUS
                <br />
                BY NATURE
              </span>
              <Sparkles size={22} />
            </div>
            <div className="visual-note">
              <span className="note-line" />
              <span>
                LEARNING BY BUILDING
                <br />
                B.TECH IT · GTBIT
              </span>
            </div>
          </motion.div>
          <a href="#about" className="scroll-cue">
            <span>SCROLL TO EXPLORE</span>
            <span className="scroll-cue-line">
              <i />
            </span>
          </a>
          <div className="hero-side-index">PORTFOLIO · 2026</div>
        </section>

        <section id="about" className="about section-shell section-pad">
          <motion.div {...motionProps}>
            <SectionTitle
              eyebrow="01 — A LITTLE ABOUT ME"
              title={
                <>
                  Curiosity, with
                  <br />
                  <em>follow-through.</em>
                </>
              }
              note="I like understanding the problem first, then building something people can actually use."
            />
          </motion.div>
          <div className="about-grid">
            <motion.div className="about-main" {...motionProps}>
              <span className="big-quote">“</span>
              <p>{resume.summary}</p>
              <p>
                My work spans machine learning, natural language processing, and
                full-stack applications. I care about useful details: reliable
                data, clear interfaces, and systems that explain what they’re
                doing.
              </p>
              <a className="inline-link" href="#experience">
                More about my path <ArrowDownRight size={16} />
              </a>
            </motion.div>
            <motion.div className="about-facts" {...motionProps}>
              <div className="fact-card fact-card-lime">
                <span className="fact-label">CURRENTLY</span>
                <strong>
                  Building at the intersection of AI and software.
                </strong>
                <span className="fact-icon">
                  <Sparkles size={18} />
                </span>
              </div>
              <div className="fact-card">
                <span className="fact-label">EDUCATION</span>
                {resume.education.slice(0, 1).map((item) => (
                  <div key={item.institution}>
                    <strong>{item.degree}</strong>
                    <span>{item.institution}</span>
                    <small>
                      {item.duration} {item.score ? `· ${item.score}` : ""}
                    </small>
                  </div>
                ))}
                <span className="fact-icon">
                  <Code2 size={18} />
                </span>
              </div>
              <div className="fact-note">
                <span className="note-line" />
                <p>
                  From log analysis to agentic systems, I enjoy turning
                  technical ideas into clear, useful experiences.
                </p>
              </div>
            </motion.div>
          </div>
        </section>

        <section id="skills" className="skills-section section-pad">
          <div className="section-shell">
            <motion.div {...motionProps}>
              <SectionTitle
                eyebrow="02 — THE TOOLKIT"
                title={
                  <>
                    Things I work
                    <br />
                    <em>with.</em>
                  </>
                }
                note="A practical toolkit, growing with every project."
              />
            </motion.div>
            <motion.div className="skills-grid" {...motionProps}>
              {resume.skill_categories.map((group, index) => (
                <article className="skill-group" key={group.category}>
                  <div className="skill-group-head">
                    <span>0{index + 1}</span>
                    <ArrowUpRight size={16} />
                  </div>
                  <h3>{group.category}</h3>
                  <div className="skill-pills">
                    {group.skills.map((skill) => (
                      <span className="skill-pill" key={skill}>
                        {skill}
                      </span>
                    ))}
                  </div>
                </article>
              ))}
            </motion.div>
            <div className="skills-footer">
              <span>ALWAYS LEARNING</span>
              <span className="skills-footer-line" />
              <span>PYTHON · AI · SOFTWARE</span>
            </div>
          </div>
        </section>

        <section id="projects" className="projects section-shell section-pad">
          <motion.div {...motionProps}>
            <SectionTitle
              eyebrow="03 — SELECTED WORK"
              title={
                <>
                  Built to make
                  <br />
                  <em>an impact.</em>
                </>
              }
              note="A selection of projects where I’ve explored a problem, built a system, and learned something along the way."
            />
          </motion.div>
          <motion.div
            className="project-grid"
            initial={reduceMotion ? false : "hidden"}
            whileInView={reduceMotion ? undefined : "visible"}
            viewport={{ once: true, amount: 0.08 }}
            variants={{ visible: { transition: { staggerChildren: 0.1 } } }}
          >
            {projects.map((project, index) => (
              <ProjectCard
                key={project.name}
                project={project}
                index={index}
                total={projects.length}
                onSelect={setSelected}
              />
            ))}
          </motion.div>
          <div className="projects-bottom">
            <span>
              {String(projects.length).padStart(2, "0")} PROJECTS ·{" "}
              {projects.filter((project) => project.live_url).length} LIVE DEMOS
            </span>
            <a
              href={resume.github || fallback.github || "#"}
              target="_blank"
              rel="noreferrer"
              className="inline-link"
            >
              More on GitHub <ArrowUpRight size={15} />
            </a>
          </div>
        </section>

        <section id="experience" className="experience-section section-pad">
          <div className="section-shell">
            <motion.div {...motionProps}>
              <SectionTitle
                eyebrow="04 — EXPERIENCE & EDUCATION"
                title={
                  <>
                    Learning through
                    <br />
                    <em>real work.</em>
                  </>
                }
                note="Applying research, engineering, and clear communication to practical challenges."
              />
            </motion.div>
            <div className="experience-layout">
              <div className="timeline-label">
                <span className="timeline-dot" /> EXPERIENCE
              </div>
              <div className="timeline-items">
                {resume.experiences.map((experience) => (
                  <motion.article
                    className="timeline-card"
                    key={experience.company}
                    {...motionProps}
                  >
                    <div className="timeline-meta">
                      <span>{experience.duration}</span>
                      <span>{experience.location}</span>
                    </div>
                    <h3>{experience.role}</h3>
                    <p className="timeline-company">{experience.company}</p>
                    <div className="timeline-copy">
                      {experience.responsibilities.map((item) => (
                        <p key={item}>
                          <span>↳</span>
                          {item}
                        </p>
                      ))}
                    </div>
                    <div className="skill-pills timeline-pills">
                      {experience.technologies.map((skill) => (
                        <span className="skill-pill" key={skill}>
                          {skill}
                        </span>
                      ))}
                    </div>
                    <a
                      className="inline-link"
                      href="/downloads/NIC_Internship_Certificate.pdf"
                      target="_blank"
                      rel="noreferrer"
                    >
                      View internship certificate <ArrowUpRight size={15} />
                    </a>
                  </motion.article>
                ))}
                {resume.education.map((education) => (
                  <motion.article
                    className="timeline-card education-card"
                    key={education.institution}
                    {...motionProps}
                  >
                    <div className="timeline-meta">
                      <span>{education.duration}</span>
                      <span>{education.location}</span>
                    </div>
                    <h3>{education.degree}</h3>
                    <p className="timeline-company">{education.institution}</p>
                    <p className="education-score">{education.score}</p>
                  </motion.article>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section
          id="achievements"
          className="achievements section-shell section-pad"
        >
          <motion.div {...motionProps}>
            <SectionTitle
              eyebrow="06 — CONTINUOUS LEARNING"
              title={
                <>
                  Foundations for
                  <br />
                  <em>what’s next.</em>
                </>
              }
              note="Learning beyond the classroom, one new capability at a time."
            />
          </motion.div>
          <div className="achievement-grid">
            <motion.article className="achievement-lead" {...motionProps}>
              <span className="fact-label">CERTIFICATIONS</span>
              <h3>
                Knowledge is a<br />
                <em>practice.</em>
              </h3>
              <p>
                Focused learning in generative AI and applied machine learning.
              </p>
              <div className="achievement-orbit">
                <span>LEARN</span>
                <ArrowDownRight size={24} />
              </div>
            </motion.article>
            <div className="cert-list">
              {resume.certifications.map((certification, index) => (
                <motion.div
                  className="cert-row"
                  key={certification}
                  {...motionProps}
                >
                  <span className="cert-index">0{index + 1}</span>
                  <span>{certification}</span>
                  <Check size={16} />
                </motion.div>
              ))}
              {resume.achievements.map((achievement, index) => (
                <motion.div
                  className="cert-row"
                  key={achievement}
                  {...motionProps}
                >
                  <span className="cert-index">A{index + 1}</span>
                  <span>{achievement}</span>
                  <Check size={16} />
                </motion.div>
              ))}
              {resume.certifications.length === 0 &&
                resume.achievements.length === 0 && (
                  <p className="no-achievements">
                    More milestones will be added as they’re earned.
                  </p>
                )}
              <a
                className="certificate-link"
                href="/downloads/NIC_Internship_Certificate.pdf"
                target="_blank"
                rel="noreferrer"
              >
                <span>
                  National Informatics Centre · Internship certificate
                </span>
                <ArrowUpRight size={17} />
              </a>
            </div>
          </div>
        </section>

        <section id="contact" className="contact-section">
          <div className="contact-orbit" aria-hidden="true">
            <span />
            <span />
            <span />
          </div>
          <div className="section-shell contact-content">
            <motion.div {...motionProps}>
              <span className="eyebrow">07 — SAY HELLO</span>
              <h2>
                Have a good
                <br />
                problem to <em>solve?</em>
              </h2>
              <p>
                I’d love to hear about it. Reach out to talk about AI, software,
                or an opportunity to build something useful.
              </p>
              <a
                className="button button-lime contact-cta"
                href={`mailto:${resume.email}`}
              >
                Start a conversation <ArrowUpRight size={17} />
              </a>
            </motion.div>
            <div className="contact-links">
              {resume.email && (
                <a href={`mailto:${resume.email}`}>
                  <span>
                    <Mail size={17} /> Email
                  </span>
                  <ArrowUpRight size={17} />
                </a>
              )}
              {resume.linkedin && (
                <a href={resume.linkedin} target="_blank" rel="noreferrer">
                  <span>
                    <Linkedin size={17} /> LinkedIn
                  </span>
                  <ArrowUpRight size={17} />
                </a>
              )}
              {resume.github && (
                <a href={resume.github} target="_blank" rel="noreferrer">
                  <span>
                    <Github size={17} /> GitHub
                  </span>
                  <ArrowUpRight size={17} />
                </a>
              )}
              <a
                href="/downloads/Dilpreet_Kaur_Resume.pdf?v=20261101-126334"
                download="Dilpreet_Kaur_Resume.pdf"
              >
                <span>
                  <ArrowDown size={17} /> Download résumé
                </span>
                <ArrowDown size={17} />
              </a>
            </div>
          </div>
          <footer className="site-footer section-shell">
            <a href="#home" className="wordmark">
              <span className="wordmark-mark">dk</span>
              <span>DILPREET KAUR</span>
            </a>
            <span>MADE WITH CURIOSITY · NEW DELHI, INDIA</span>
            <a href="#home" className="back-top">
              BACK TO TOP <ArrowUpRight size={13} />
            </a>
          </footer>
        </section>
      </main>
      <ProjectDialog project={selected} onClose={() => setSelected(null)} />
      <Assistant open={assistantOpen} onOpenChange={setAssistantOpen} />
    </>
  );
}
