export type Project = {
  name: string;
  problem?: string | null;
  description: string;
  technologies: string[];
  contributions: string[];
  github_url?: string | null;
  live_url?: string | null;
};

export type Resume = {
  name: string;
  headline?: string | null;
  email?: string | null;
  location?: string | null;
  github?: string | null;
  linkedin?: string | null;
  summary?: string | null;
  skills: string[];
  skill_categories: { category: string; skills: string[] }[];
  experiences: {
    role: string;
    company: string;
    duration?: string | null;
    location?: string | null;
    responsibilities: string[];
    technologies: string[];
  }[];
  education: {
    institution: string;
    degree: string;
    duration?: string | null;
    score?: string | null;
    location?: string | null;
  }[];
  projects: Project[];
  certifications: string[];
  achievements: string[];
};

export type ChatResponse = {
  answer: string;
  grounded: boolean;
  sources: string[];
};
