from pydantic import BaseModel
from typing import List, Optional, Dict

class Candidate(BaseModel):
    name: str = "Unknown Candidate"
    years_experience: float = 0.0
    degree_level: str = "None"
    field_of_study: str = ""
    technical_skills: List[str] = []
    soft_skills: List[str] = []
    has_demonstrated_potential: bool = False
    raw_text: Optional[str] = None

    # New fields from merged project
    status: str = "Hold"
    confidence: float = 0.0
    explanation: List[str] = []
    fired_rules: List[Dict] = []
    score_breakdown: Dict = {}
    reasoning_trace: List[Dict] = []