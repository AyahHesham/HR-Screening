# expert_system.py - Merged Rich Rules + Scoring + Forward Chaining

from candidate import Candidate
from typing import List, Dict

class ForwardChainingEngine:
    def __init__(self):
        self.rules = self._define_rules()
        self.reasoning_trace: List[Dict] = []
        self.fired_rules: List[Dict] = []

    def _define_rules(self):
        return [
            {"id": "R1", "name": "Ideal Match", "category": "Qualified", "priority": 1,
             "conditions": [
                 {"slot": "years_experience", "op": ">=", "value": 3},
                 {"slot": "has_degree", "op": "==", "value": True},
                 {"slot": "field_related", "op": "==", "value": True},
                 {"slot": "tech_skill_level", "op": ">=", "value": 3},
             ],
             "action": "QUALIFIED",
             "explanation": "Rule R1 (Ideal Match) fired: ≥3 years experience, related degree, and strong technical skills."},

            {"id": "R2", "name": "Senior Expert", "category": "Qualified", "priority": 2,
             "conditions": [
                 {"slot": "years_experience", "op": ">=", "value": 5},
                 {"slot": "has_degree", "op": "==", "value": True},
                 {"slot": "tech_skill_level", "op": ">=", "value": 2},
             ],
             "action": "QUALIFIED",
             "explanation": "Rule R2 (Senior Expert) fired: Senior-level experience with degree."},

            {"id": "R3", "name": "Rising Star / Promising Graduate", "category": "Hold", "priority": 3,
             "conditions": [
                 {"slot": "years_experience", "op": "<", "value": 1},
                 {"slot": "high_potential", "op": "==", "value": True},
                 {"slot": "has_degree", "op": "==", "value": True},
                 {"slot": "field_related", "op": "==", "value": True},
                 {"slot": "tech_skill_level", "op": ">=", "value": 2},
             ],
             "action": "HOLD",
             "explanation": "Rule R3 (Rising Star) fired: High-potential fresh graduate → Talent Pool."},

            {"id": "R4", "name": "Skilled But Inexperienced", "category": "Hold", "priority": 4,
             "conditions": [
                 {"slot": "years_experience", "op": ">=", "value": 1},
                 {"slot": "years_experience", "op": "<", "value": 3},
                 {"slot": "tech_skill_level", "op": ">=", "value": 3},
                 {"slot": "has_degree", "op": "==", "value": True},
             ],
             "action": "HOLD",
             "explanation": "Rule R4 fired: Strong technical skills but limited experience."},

            {"id": "R5", "name": "Skills Gap", "category": "Rejected", "priority": 5,
             "conditions": [{"slot": "tech_skill_level", "op": "<=", "value": 1}],
             "action": "REJECTED",
             "explanation": "Rule R5 (Skills Gap) fired: Insufficient technical skills."},

            {"id": "R7", "name": "Education Mismatch", "category": "Rejected", "priority": 6,
             "conditions": [
                 {"slot": "has_degree", "op": "==", "value": False},
                 {"slot": "field_related", "op": "==", "value": False},
             ],
             "action": "REJECTED",
             "explanation": "Rule R7 (Education Mismatch) fired: No degree and unrelated field."},

            {"id": "R6", "name": "Entry Level", "category": "Rejected", "priority": 7,
             "conditions": [{"slot": "years_experience", "op": "<", "value": 1}],
             "action": "REJECTED",
             "explanation": "Rule R6 (Entry Level) fired: Below minimum experience."},
        ]

    def evaluate_condition(self, fact_value, condition):
        op = condition["op"]
        val = condition["value"]
        if op == "==": return fact_value == val
        if op == ">=": return fact_value >= val
        if op == "<=": return fact_value <= val
        if op == ">":  return fact_value > val
        if op == "<":  return fact_value < val
        return False

    def run(self, facts: dict) -> dict:
        self.reasoning_trace = [{"step": 0, "type": "LOAD", "description": "Candidate facts loaded"}]
        self.fired_rules = []

        sorted_rules = sorted(self.rules, key=lambda r: r["priority"])

        for rule in sorted_rules:
            matched = all(self.evaluate_condition(facts.get(c["slot"]), c) for c in rule["conditions"])
            if matched:
                self.fired_rules.append(rule)
                self.reasoning_trace.append({
                    "step": len(self.reasoning_trace),
                    "type": "FIRE",
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "action": rule["action"],
                    "explanation": rule["explanation"]
                })
                verdict = rule["action"]
                break
        else:
            verdict = "UNDETERMINED"

        self.reasoning_trace.append({
            "step": len(self.reasoning_trace),
            "type": "HALT",
            "description": f"Inference completed. Final verdict: {verdict}"
        })

        return {
            "verdict": verdict,
            "fired_rules": self.fired_rules,
            "reasoning_trace": self.reasoning_trace
        }


def compute_score(facts: dict) -> dict:
    exp_score = min(30, facts.get("years_experience", 0) * 6)
    edu_score = (15 if facts.get("has_degree", False) else 0) + (10 if facts.get("field_related", False) else 0)
    tech_score = min(25, facts.get("tech_skill_level", 0) * 8)
    soft_score = min(10, facts.get("soft_skill_level", 0) * 3)
    pot_score = 5 if facts.get("high_potential", False) else 0
    bonuses = min(5, facts.get("certifications", 0) * 2) + (3 if facts.get("has_references", False) else 0)

    total = min(100, exp_score + edu_score + tech_score + soft_score + pot_score + bonuses)

    return {
        "total": total,
        "experience": exp_score,
        "education": edu_score,
        "tech_skills": tech_score,
        "soft_skills": soft_score,
        "potential": pot_score,
        "bonuses": bonuses
    }


def screen_candidate(candidate: Candidate) -> Candidate:
    facts = {
        "years_experience": candidate.years_experience,
        "has_degree": candidate.degree_level in ["Bachelor", "Master", "PhD"],
        "field_related": any(f in candidate.field_of_study.lower() for f in ["computer science", "software engineering", "it", "informatics", "data science"]),
        "tech_skill_level": min(4, len([s for s in candidate.technical_skills if s])),
        "soft_skill_level": min(3, len(candidate.soft_skills)),
        "high_potential": candidate.has_demonstrated_potential,
        "certifications": 2,
        "has_references": True,
        "location_ok": True
    }

    engine = ForwardChainingEngine()
    result = engine.run(facts)
    score = compute_score(facts)

    candidate.status = result["verdict"]
    candidate.confidence = score["total"] / 100.0
    candidate.explanation = [r["explanation"] for r in result.get("fired_rules", [])]
    candidate.fired_rules = [{"rule": r["id"], "name": r["name"], "explanation": r["explanation"]} for r in result.get("fired_rules", [])]
    candidate.score_breakdown = score
    candidate.reasoning_trace = result["reasoning_trace"]

    return candidate