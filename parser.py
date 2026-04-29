import pymupdf4llm
import json
from candidate import Candidate
from fuzzy_matcher import normalize_skills
import ollama

def extract_text_from_cv(file_path: str) -> str:
    if file_path.lower().endswith(".pdf"):
        return pymupdf4llm.to_markdown(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def parse_cv_with_llm(file_path: str) -> Candidate:
    text = extract_text_from_cv(file_path)
    
    prompt = f"""Extract structured information from this resume. Return ONLY valid JSON.

Keys:
{{
  "name": "Full Name",
  "years_experience": number,
  "degree_level": "Bachelor/Master/PhD/None",
  "field_of_study": "string",
  "technical_skills": ["python", "java", ...],
  "soft_skills": ["communication", ...],
  "has_demonstrated_potential": true/false
}}

Resume:
{text[:13000]}
"""

    try:
        response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
        content = response['message']['content']
        
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1]
            
        data = json.loads(content.strip())
        candidate = Candidate(**data, raw_text=text)
        candidate.technical_skills = normalize_skills(candidate.technical_skills)
        return candidate
    except Exception as e:
        print("LLM Error:", e)
        return Candidate(name="Parse Error", raw_text=text)