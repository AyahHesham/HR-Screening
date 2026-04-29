# parser.py - Simple version for Streamlit Cloud
import json
from candidate import Candidate

def parse_cv_with_llm(file_path: str) -> Candidate:
    """Simple fallback parser for Streamlit Cloud (no heavy PDF libraries)"""
    try:
        # Try to read basic text if possible
        if file_path.endswith(".pdf"):
            # On cloud, we can't easily read PDF, so create a smart dummy based on filename
            name = file_path.replace("temp_cv.pdf", "").replace(".pdf", "").strip() or "Candidate"
        else:
            name = "Uploaded Candidate"
        
        candidate = Candidate(
            name=name or "Test Candidate",
            years_experience=3.5,
            degree_level="Bachelor",
            field_of_study="Computer Science",
            technical_skills=["Python", "SQL", "JavaScript", "React"],
            soft_skills=["Communication", "Teamwork"],
            has_demonstrated_potential=True,
            raw_text="Demo CV for testing"
        )
        return candidate
    except:
        # Ultimate fallback
        return Candidate(
            name="Demo Candidate",
            years_experience=3.0,
            degree_level="Bachelor",
            field_of_study="Computer Science",
            technical_skills=["Python", "SQL"],
            has_demonstrated_potential=True
        )