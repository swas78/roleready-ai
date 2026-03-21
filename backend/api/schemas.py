from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=50)
    jd_text: str = Field(..., min_length=30)
    domain: Literal["frontend", "backend", "fullstack", "devops", "cloud", "data", "ml", "ops", "tech", "shared"]

class ExtractedSkill(BaseModel):
    name: str
    years: Optional[int] = None
    confidence: int = Field(..., ge=0, le=100)
    context: Optional[str] = None

class GapObject(BaseModel):
    known: List[ExtractedSkill]
    partial: List[ExtractedSkill]
    missing: List[str]

class RoadmapModule(BaseModel):
    module_id: str
    title: str
    duration_hours: int
    type: str # e.g. "new", "refresher", "skip"
    order: int
    reason: str
    skills_covered: List[str]
    domain: str
    level: str
    difficulty: str = "medium"

class AnalyzeResponse(BaseModel):
    candidate_skills: List[ExtractedSkill]
    required_skills: List[str]
    gap_object: GapObject
    readiness_score: int = Field(..., ge=0, le=100)
    roadmap: List[RoadmapModule]
    time_saved_hours: int
    domain: str
    initials: str
