from typing import List, Optional
from pydantic import BaseModel, Field


class Experience(BaseModel):
    role: str = Field(..., description="Job or internship title")
    company: str = Field(..., description="Organization name")
    duration: Optional[str] = Field(None, description="Start and end dates or duration")
    location: Optional[str] = Field(None, description="Work location")
    responsibilities: List[str] = Field(
        default_factory=list, description="Key bullet points and responsibilities"
    )
    technologies: List[str] = Field(
        default_factory=list, description="Technologies and tools used"
    )


class Education(BaseModel):
    institution: str = Field(..., description="School or university name")
    degree: str = Field(..., description="Degree, major, or board")
    duration: Optional[str] = Field(None, description="Duration or graduation year")
    score: Optional[str] = Field(None, description="CGPA or percentage")
    location: Optional[str] = Field(None, description="Location of the institution")


class Project(BaseModel):
    name: str = Field(..., description="Project name")
    problem: Optional[str] = Field(None, description="Problem statement")
    description: str = Field(..., description="What the project does and how it works")
    technologies: List[str] = Field(
        default_factory=list, description="Key tools and languages used"
    )
    contributions: List[str] = Field(
        default_factory=list, description="Specific contributions or features built"
    )
    github_url: Optional[str] = Field(None, description="GitHub repository URL")
    live_url: Optional[str] = Field(None, description="Live demo or deployment URL")


class SkillCategory(BaseModel):
    category: str = Field(..., description="Category name (e.g. Programming Languages)")
    skills: List[str] = Field(
        default_factory=list, description="List of individual skills"
    )


class Resume(BaseModel):
    name: str = Field(..., description="Candidate's full name")
    headline: Optional[str] = Field(None, description="Professional headline or title")
    email: Optional[str] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    location: Optional[str] = Field(None, description="City, Country")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    summary: Optional[str] = Field(None, description="Short background summary")
    skills: List[str] = Field(
        default_factory=list, description="Flat list of all skills"
    )
    skill_categories: List[SkillCategory] = Field(
        default_factory=list, description="Skills grouped by category"
    )
    experiences: List[Experience] = Field(
        default_factory=list, description="Internship and professional experience"
    )
    education: List[Education] = Field(
        default_factory=list, description="Education history"
    )
    projects: List[Project] = Field(
        default_factory=list, description="Academic and personal projects"
    )
    certifications: List[str] = Field(
        default_factory=list, description="Completed certifications"
    )
    achievements: List[str] = Field(
        default_factory=list, description="Honors, ideathons, and awards"
    )


class PublicResume(BaseModel):
    """Sanitized resume representation for public API access (excludes phone number)."""
    name: str
    headline: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    summary: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    skill_categories: List[SkillCategory] = Field(default_factory=list)
    experiences: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User question to ask the resume assistant",
        examples=["What was Dilpreet's role at the National Informatics Centre?"]
    )
    session_id: Optional[str] = Field(
        None,
        description="Session identifier for multi-turn or visitor context"
    )
    custom_resume_id: Optional[str] = Field(
        None,
        description="Session ID for an uploaded custom resume, if in analysis mode"
    )


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Grounded answer to the question")
    grounded: bool = Field(
        True,
        description="Whether the answer is grounded in the candidate's resume"
    )
    sources: List[str] = Field(
        default_factory=list,
        description="Resume sections referenced in the answer"
    )


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    model: str = Field(..., description="Configured Groq LLM model")
    resume_loaded: bool = Field(..., description="Whether the portfolio resume is cached")
    groq_configured: bool = Field(..., description="Whether the Groq API key is set")
