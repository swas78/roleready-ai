import json
import os
import io
import time
import logging
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
logger = logging.getLogger(__name__)

# Structured Logger Helper
def log_event(event_name: str, **kwargs):
    logger.info(json.dumps({"event": event_name, **kwargs}))

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Configuration constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_TEXT_LENGTH = 50000  # Characters
ALLOWED_DOMAINS = {"tech", "ops", "shared"}
ALLOWED_MIME_TYPES = {"application/pdf", "text/plain"}
ALLOWED_FILE_EXTENSIONS = {".pdf", ".txt"}


def validate_domain(domain: str) -> str:
    """Validate and normalize domain parameter."""
    domain = domain.strip().lower()
    if domain not in ALLOWED_DOMAINS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid domain. Must be one of: {', '.join(ALLOWED_DOMAINS)}"
        )
    return domain


def validate_text_input(text: str, min_length: int = 30, max_length: int = MAX_TEXT_LENGTH) -> str:
    """Validate text input length."""
    if len(text) < min_length:
        raise HTTPException(
            status_code=400,
            detail=f"Text too short. Minimum {min_length} characters required."
        )
    if len(text) > max_length:
        raise HTTPException(
            status_code=400,
            detail=f"Text too long. Maximum {max_length} characters allowed."
        )
    return text.strip()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_profile(request: Request, payload: AnalyzeRequest):
    start_time = time.time()
    log_event("analyze_profile_start", domain=payload.domain)
    
    embedder = request.app.state.embedder
    if not embedder:
        log_event("analyze_profile_error", error="Embedder not loaded")
        raise HTTPException(status_code=500, detail="Embedder model not loaded")

    # Validate inputs
    payload.domain = validate_domain(payload.domain)
    payload.resume_text = validate_text_input(payload.resume_text, min_length=50)
    payload.jd_text = validate_text_input(payload.jd_text, min_length=30)

    # 1. Parse
    try:
        candidate_skills = await parse_resume(payload.resume_text)
        required_skills = await parse_jd(payload.jd_text)
        log_event("parse_success", candidate_skills_count=len(candidate_skills), required_skills_count=len(required_skills))
    except Exception as e:
        log_event("parse_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to parse text")

    # 2 & 3. Embed and classify gaps
    gap_object = classify_gaps(candidate_skills, required_skills, embedder)
    readiness_score = compute_readiness(gap_object)

    # 4. Graph sorting for missing/partial
    skills_to_learn = gap_object.missing + [s.name for s in gap_object.partial]
    ordered_skills = topological_sort(skills_to_learn)

    # 5. Planner
    roadmap = await build_roadmap(ordered_skills, embedder, payload.domain, gap_object)

    # 6. Tracer
    roadmap_with_reasons = attach_reasons(roadmap, gap_object, candidate_skills, required_skills)

    total_duration = sum(m.duration_hours for m in roadmap_with_reasons)

    # Extract initials from resume text naively (or prompt could do it)
    initials = "AC"
    words = payload.resume_text.split()
    if len(words) >= 2:
        initials = (words[0][0] + words[1][0]).upper()

    log_event("analyze_profile_complete", 
              duration_ms=round((time.time() - start_time) * 1000),
              readiness_score=readiness_score,
              modules_count=len(roadmap_with_reasons))

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
    # Validate domain
    domain = validate_domain(domain)

    # Validate JD text length
    jd_text = validate_text_input(jd_text, min_length=30)

    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_FILE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_FILE_EXTENSIONS)}"
        )

    # Read file with size limit
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024 * 1024)}MB"
        )

    resume_text = ""

    if file_ext == ".pdf":
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        resume_text += extracted + "\n"
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse PDF: {str(e)}"
            )
    else:
        # Text file
        try:
            resume_text = content.decode("utf-8", errors="ignore")
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail="Failed to decode text file"
            )

    resume_text = validate_text_input(resume_text, min_length=50)

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
    if domain:
        domain = validate_domain(domain)

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
    # Debug endpoint - validate inputs
    payload.domain = validate_domain(payload.domain)
    payload.resume_text = validate_text_input(payload.resume_text, min_length=50)
    payload.jd_text = validate_text_input(payload.jd_text, min_length=30)

    candidate_skills = await parse_resume(payload.resume_text)
    required_skills = await parse_jd(payload.jd_text)
    return {
        "candidate_skills": [s.model_dump() for s in candidate_skills],
        "required_skills": required_skills
    }
