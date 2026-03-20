import asyncio
from core.parser import parse_resume, parse_jd
from core.embedder import Embedder
from core.gap import classify_gaps, compute_readiness
from core.graph import topological_sort
from core.planner import build_roadmap
from core.tracer import attach_reasons

async def run_final_test():
    try:
        print("Loading Embedder...")
        embedder = Embedder()
        embedder.load()

        resume_text = "4 years Python Docker SQL Git REST APIs. Worked extensively in container automation."
        jd_text = "FastAPI Kubernetes CI/CD System Design Python Advanced"
        domain = "tech"

        print("Parsing...")
        candidate_skills = await parse_resume(resume_text)
        required_skills = await parse_jd(jd_text)
        
        print(f"Candidates: {len(candidate_skills)} | Required: {len(required_skills)}")

        print("Gapping...")
        gap_object = classify_gaps(candidate_skills, required_skills, embedder)
        readiness = compute_readiness(gap_object)
        
        print(f"Readiness: {readiness}%")
        print(f"Known: {len(gap_object.known)} | Partial: {len(gap_object.partial)} | Missing: {len(gap_object.missing)}")

        print("Graph sorting...")
        skills_to_learn = gap_object.missing + [s.name for s in gap_object.partial]
        ordered_skills = topological_sort(skills_to_learn)
        
        print("Planning...")
        roadmap = build_roadmap(ordered_skills, embedder, domain, gap_object)
        
        print("Tracing...")
        roadmap = attach_reasons(roadmap, gap_object, candidate_skills, required_skills)
        
        if len(candidate_skills) >= 3 and len(required_skills) >= 3 and len(roadmap) >= 1 and 10 <= readiness <= 90:
            if all(m.reason for m in roadmap):
                print("ALL TESTS PASSED")
                return
                
        print("FAILED Criteria.")
    except Exception as e:
        print("Pipeline Failed:", e)

if __name__ == "__main__":
    asyncio.run(run_final_test())
