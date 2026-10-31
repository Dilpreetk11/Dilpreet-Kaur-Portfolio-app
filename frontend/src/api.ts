import type { ChatResponse, Resume } from "./types";

const configuredBase = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "");
const apiBase =
  configuredBase ||
  (import.meta.env.PROD
    ? "https://dilpreet-kaur-portfolio-app.onrender.com"
    : "/api");

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    throw new Error(payload?.detail || `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export const fetchResume = () => request<Resume>("/resume");
export const askAssistant = (question: string) =>
  request<ChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify({ question }),
  });
