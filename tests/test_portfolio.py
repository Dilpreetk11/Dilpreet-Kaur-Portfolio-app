import pytest
from backend.resume_parser import get_verified_resume
from backend.chatbot import format_resume_context, ask_candidate
from backend.schemas import Resume
from frontend.app import PROJECTS


def test_verified_resume_contains_all_five_live_projects():
    resume = get_verified_resume()
    assert isinstance(resume, Resume)
    
    live_links = {
        proj.name: proj.live_url
        for proj in resume.projects
        if proj.live_url
    }
    
    # Check that all five deployed projects are represented with their live URLs
    assert any("Deep Packet Inspection" in name and "https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/" in url for name, url in live_links.items())
    assert any("Travel Planning Agent" in name and "https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/" in url for name, url in live_links.items())
    assert any("IT Support" in name and "https://enterprise-it-support-copilot.vercel.app/" in url for name, url in live_links.items())
    assert any("Resumind" in name and "https://resumind-cmdp.onrender.com/" in url for name, url in live_links.items())
    assert any("GridScan RL" in name and "https://rl-gridscan.onrender.com/" in url for name, url in live_links.items())
    assert any("Telco Customer Churn" in project.name for project in resume.projects)


def test_resume_context_includes_live_links():
    resume = get_verified_resume()
    context = format_resume_context(resume)
    
    assert "https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/" in context
    assert "https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/" in context
    assert "https://enterprise-it-support-copilot.vercel.app/" in context
    assert "https://rl-gridscan.onrender.com/" in context
    assert "91.7% recall" in context
    assert "Dilpreet Kaur Portfolio & AI Assistant" in context
    assert "https://resumind-cmdp.onrender.com/" in context


def test_chatbot_offline_fallback():
    resume = get_verified_resume()
    resp = ask_candidate("What projects has Dilpreet built?", resume, client=None)
    assert resp.grounded is True
    assert "Deep Packet Inspection" in resp.answer
    assert "IT Support" in resp.answer
    assert "Telco Customer Churn" in resp.answer


def test_chatbot_answers_personal_and_project_questions_offline():
    resume = get_verified_resume()
    about = ask_candidate("Tell me about Dilpreet.", resume, client=None)
    gridscan = ask_candidate("What is GridScan RL?", resume, client=None)
    nic = ask_candidate("What was her NIC internship about?", resume, client=None)

    assert "AI/ML Engineer" in about.answer
    assert "GTBIT" in about.answer
    assert "GirlScript Summer of Code" in about.answer
    assert "90.1% coverage" in gridscan.answer
    assert "82 of 91 free tiles" in gridscan.answer
    assert "National Informatics Centre" in nic.answer
    assert "0.91 ROUGE-1/ROUGE-L" in nic.answer


def test_frontend_projects_have_live_links():
    live_urls = [p["live"] for p in PROJECTS if p.get("live")]
    
    expected_links = [
        "https://ai-powered-deep-packet-inspection-threat-detection-elnk5rn8mqt.streamlit.app/",
        "https://ai-travel-agent-6ifdxlfvnddcdo9p9vkyjx.streamlit.app/",
        "https://enterprise-it-support-copilot.vercel.app/",
        "https://resumind-cmdp.onrender.com/",
        "https://rl-gridscan.onrender.com/"
    ]
    
    for link in expected_links:
        assert link in live_urls, f"Expected live link {link} not found in frontend PROJECTS"
    assert not any(p["github"] == "https://github.com/Dilpreetk11/Dilpreet-Kaur-Portfolio-app" for p in PROJECTS)


def test_scholarship_replaced_and_assets_exist():
    resume = get_verified_resume()
    assert not any("Scholarship" in p.name for p in resume.projects)
    assert not any("Scholarship" in p["name"] for p in PROJECTS)
    assert not any("Roomify" in p.name for p in resume.projects)
    assert not any("Roomify" in p["name"] for p in PROJECTS)
    
    # Existing project images are optional; projects without supplied screenshots have no preview image.
    for p in PROJECTS:
        if p.get("thumb"):
            thumb_path = p.get("thumb")
            assert thumb_path.exists(), f"Thumbnail file does not exist: {thumb_path}"
