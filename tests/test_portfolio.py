import pytest
from backend.resume_parser import get_verified_resume
from backend.chatbot import format_resume_context, ask_candidate
from backend.schemas import Resume
from frontend.app import PROJECTS


def test_verified_resume_contains_all_four_live_projects():
    resume = get_verified_resume()
    assert isinstance(resume, Resume)
    
    live_links = {
        proj.name: proj.live_url
        for proj in resume.projects
        if proj.live_url
    }
    
    # Check that all 4 projects are represented with their live URLs
    assert any("Deep Packet Inspection" in name and "https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/" in url for name, url in live_links.items())
    assert any("Travel Agent" in name and "https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/" in url for name, url in live_links.items())
    assert any("IT Support" in name and "https://it-support-agentic-rag-copilot-brakzz3tuwuejuwhxmkkh8.streamlit.app/" in url for name, url in live_links.items())
    assert any("Resumind" in name and "https://resumind-cmdp.onrender.com/" in url for name, url in live_links.items())


def test_resume_context_includes_live_links():
    resume = get_verified_resume()
    context = format_resume_context(resume)
    
    assert "https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/" in context
    assert "https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/" in context
    assert "https://it-support-agentic-rag-copilot-brakzz3tuwuejuwhxmkkh8.streamlit.app/" in context
    assert "https://resumind-cmdp.onrender.com/" in context


def test_chatbot_offline_fallback():
    resume = get_verified_resume()
    resp = ask_candidate("What projects has Dilpreet built?", resume, client=None)
    assert resp.grounded is True
    assert "Deep Packet Inspection" in resp.answer
    assert "IT Support" in resp.answer


def test_frontend_projects_have_live_links():
    live_urls = [p["live"] for p in PROJECTS if p.get("live")]
    
    expected_links = [
        "https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/",
        "https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/",
        "https://it-support-agentic-rag-copilot-brakzz3tuwuejuwhxmkkh8.streamlit.app/",
        "https://resumind-cmdp.onrender.com/"
    ]
    
    for link in expected_links:
        assert link in live_urls, f"Expected live link {link} not found in frontend PROJECTS"


def test_scholarship_replaced_and_assets_exist():
    resume = get_verified_resume()
    assert not any("Scholarship" in p.name for p in resume.projects)
    assert not any("Scholarship" in p["name"] for p in PROJECTS)
    assert not any("Roomify" in p.name for p in resume.projects)
    assert not any("Roomify" in p["name"] for p in PROJECTS)
    
    # Check that each of the 4 live projects has a valid thumbnail
    for p in PROJECTS:
        if p.get("live"):
            thumb_path = p.get("thumb")
            assert thumb_path is not None, f"Thumbnail path missing for {p['name']}"
            assert thumb_path.exists(), f"Thumbnail file does not exist: {thumb_path}"
