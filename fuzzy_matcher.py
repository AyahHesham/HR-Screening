from rapidfuzz import process, fuzz
from typing import List

STANDARD_SKILLS = [
    "python", "java", "javascript", "sql", "react", "angular", "node.js", "typescript",
    "django", "flask", "spring boot", "tensorflow", "pytorch", "aws", "docker",
    "kubernetes", "git", "html", "css", "c++", "c#", "php", "go", "ruby"
]

def normalize_skill(skill: str) -> str:
    if not skill:
        return ""
    skill_lower = skill.lower().strip()
    match, score, _ = process.extractOne(skill_lower, STANDARD_SKILLS, scorer=fuzz.WRatio)
    return match if score > 72 else skill_lower

def normalize_skills(skills: List[str]) -> List[str]:
    return [normalize_skill(s) for s in skills if s]