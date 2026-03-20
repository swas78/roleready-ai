import json
import os
import io
import pdfplumber
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from typing import Optional, List

from .schemas import AnalyzeRequest, AnalyzeResponse, ExtractedSkill
# We will create these core modules next
from core.parser import parse_resume, parse_jd
from core.gap import classify_gaps, compute_readiness
from core.graph import get_prereq_chain, topological_sort
from core.planner import build_roadmap
from core.tracer import attach_reasons

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_profile(request: Request, payload: AnalyzeRequest):
    embedder = request.app.state.embedder
    if not embedder:
        raise HTTPException(status_code=500, detail="Embedder model not loaded")
        
    # 1. Parse
    candidate_skills = await parse_resume(payload.resume_text)
    required_skills = await parse_jd(payload.jd_text)
    
    # 2 & 3. Embed and classify gaps
    gap_object = classify_gaps(candidate_skills, required_skills, embedder)
    readiness_score = compute_readiness(gap_object)
    
    # 4. Graph sorting for missing/partial
    skills_to_learn = gap_object.missing + [s.name for s in gap_object.partial]
    ordered_skills = topological_sort(skills_to_learn)
    
    # 5. Planner
    roadmap = build_roadmap(ordered_skills, embedder, payload.domain, gap_object)
    
    # 6. Tracer
    roadmap_with_reasons = attach_reasons(roadmap, gap_object, candidate_skills, required_skills)
    
    total_duration = sum(m.duration_hours for m in roadmap_with_reasons)
    
    # Extract initials from resume text naively (or prompt could do it)
    initials = "AC"
    words = payload.resume_text.split()
    if len(words) >= 2:
        initials = (words[0][0] + words[1][0]).upper()
        
    return AnalyzeResponse(
        candidate_skills=candidate_skills,
        required_skills=required_skills,
        gap_object=gap_object,
        readiness_score=readiness_score,
        roadmap=roadmap_with_reasons,
        time_saved_hours=max(0, 120 - total_duration), # arbitrary metric
        domain=payload.domain,
        initials=initials
    )

@router.post("/analyze/upload", response_model=AnalyzeResponse)
async def analyze_upload(
    request: Request,
    file: UploadFile = File(...),
    jd_text: str = Form(..., min_length=30),
    domain: str = Form(...)
):
    content = await file.read()
    resume_text = ""
    
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    resume_text += extracted + "\n"
    else:
        # Fallback for txt
        resume_text = content.decode("utf-8", errors="ignore")
        
    if len(resume_text) < 50:
        raise HTTPException(status_code=400, detail="Could not extract enough text from file.")
        
    payload = AnalyzeRequest(
        resume_text=resume_text,
        jd_text=jd_text,
        domain=domain
    )
    return await analyze_profile(request, payload)

@router.get("/demo/{profile}")
async def get_demo(profile: str):
    allowed = ["senior", "fresher", "ops"]
    if profile not in allowed:
        raise HTTPException(status_code=404, detail="Profile not found")
        
    path = os.path.join(DATA_DIR, "demo_profiles", f"{profile}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="JSON Data not found")
        
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/catalog")
async def get_catalog(domain: Optional[str] = None):
    path = os.path.join(DATA_DIR, "catalog.json")
    if not os.path.exists(path):
        return {"courses": [], "total": 0}
        
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
        
    courses = []
    if isinstance(raw, dict) and "courses" in raw:
        courses = raw["courses"]
    elif isinstance(raw, list):
        courses = raw
        
    if domain:
        courses = [c for c in courses if c.get("domain") in (domain, "both", "shared")]
        
    return {"courses": courses, "total": len(courses)}

@router.post("/parse-only")
async def parse_only(payload: AnalyzeRequest):
    # Debug endpoint
    candidate_skills = await parse_resume(payload.resume_text)
    required_skills = await parse_jd(payload.jd_text)
    return {
        "candidate_skills": [s.model_dump() for s in candidate_skills],
        "required_skills": required_skills
    }
