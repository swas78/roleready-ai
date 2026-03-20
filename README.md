# RoleReady AI
### Adaptive Onboarding Engine — IISc Bangalore Hackathon 2025

> Stop giving every new hire the same 40-hour course.  
> RoleReady AI reads their resume, reads the job description, and builds a learning path for exactly what they're missing.

---

## What It Does

RoleReady AI is an end-to-end adaptive onboarding system. It takes a candidate's resume and a job description, identifies the exact skill gap between them using semantic AI, and generates a personalized learning roadmap — with every recommendation explained in plain language.

**The problem it solves:** Most companies give every new hire identical onboarding. A 10-year veteran sits through the same beginner modules as a fresh graduate. RoleReady AI eliminates that waste.

---

## Live Demo

| Profile | Readiness | Modules | Hours Saved |
|---|---|---|---|
| Senior Engineer | 72% | 4 modules | 28h saved |
| Fresh Graduate | 22% | 7 modules | 18h saved |
| Operations Worker | 45% | 4 modules | 22h saved |

Try the demo at `/demo` — no resume upload needed.

---

## Key Features

- **Semantic Skill Matching** — SBERT embeddings, not keyword search. "ML experience" matches "machine learning" correctly.
- **Zero Hallucinations** — AI picks only from a fixed 30-course catalog. It never invents a course name.
- **Reasoning Trace** — Every module shows exactly why it was recommended. Not hidden in logs — shown in the UI.
- **Prerequisite Graph** — NetworkX topological sort ensures you learn Linux before Docker, Python before FastAPI.
- **Cross-Domain** — Works for tech roles (engineers) and ops roles (warehouse, supply chain) equally.
- **Readiness Score** — Live percentage that updates as you complete modules.

---

## Architecture
```
Resume + JD (text)
       │
       ▼
┌─────────────────┐
│   LLM Parser    │  LLaMA 3.1 via Groq — extracts skills + confidence scores
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SBERT Embedder  │  all-MiniLM-L6-v2 — semantic similarity matching
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gap Classifier │  Known / Partial / Missing buckets (cosine similarity)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Prerequisite    │  NetworkX DiGraph — topological sort of missing skills
│ Graph Sort      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Catalog Planner │  Matches skills → fixed 30-course catalog (no hallucinations)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Reasoning Tracer│  Generates plain-language explanation per module
└────────┬────────┘
         │
         ▼
  Personalized Roadmap
  with readiness score + reasoning trace
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM Parsing | LLaMA 3.1 8B via Groq API |
| Semantic Matching | Sentence-BERT (all-MiniLM-L6-v2) |
| Prerequisite Graph | NetworkX (topological sort) |
| Backend API | Python FastAPI + Uvicorn |
| Frontend | Node.js + Express + EJS |
| Session Management | express-session |
| Skill Grounding | Fixed catalog.json (30 courses, zero hallucinations) |
| Containerisation | Docker |

---

## Project Structure
```
roleready-ai/
├── backend/                 # Python FastAPI backend
│   ├── core/
│   │   ├── parser.py        # LLM-based resume + JD parsing
│   │   ├── embedder.py      # SBERT semantic embeddings
│   │   ├── gap.py           # Skill gap classification
│   │   ├── graph.py         # Prerequisite graph + topological sort
│   │   ├── planner.py       # Catalog matching (zero hallucinations)
│   │   └── tracer.py        # Reasoning trace generation
│   ├── api/
│   │   ├── routes.py        # FastAPI endpoints
│   │   └── schemas.py       # Pydantic data models
│   ├── data/
│   │   ├── catalog.json     # Fixed 30-course catalog
│   │   ├── skill_graph.json # Prerequisite dependency graph
│   │   └── demo_profiles/   # Pre-built senior/fresher/ops personas
│   ├── main.py              # FastAPI app + SBERT preload
│   └── requirements.txt
├── views/                   # EJS templates
│   ├── index.ejs            # Landing page
│   ├── analyze.ejs          # Upload page
│   ├── analyzing.ejs        # Loading screen
│   ├── results.ejs          # Bento dashboard
│   ├── demo.ejs             # 3-persona comparison
│   ├── skills.ejs           # Knowledge graph
│   ├── catalog.ejs          # Course catalog
│   └── about.ejs            # About page
├── public/                  # Static assets
├── routes/                  # Express route handlers
├── api/backend.js           # Node → Python bridge
├── server.js                # Express app entry point
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API key (free at console.groq.com)

### 1. Clone and install
```bash
git clone https://github.com/YOUR_USERNAME/roleready-ai.git
cd roleready-ai
```

### 2. Backend setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add your GROQ_API_KEY to backend/.env
```

### 3. Frontend setup
```bash
cd ..
npm install
cp .env.example .env
# PYTHON_API=http://localhost:8000 is already set
```

### 4. Run both servers
```bash
# Terminal 1 — Python backend
cd backend && python3 -m uvicorn main:app --reload --port 8000

# Terminal 2 — Node frontend
npm run dev
```

### 5. Open in browser
```
http://localhost:3000
```

### Docker (single command)
```bash
docker-compose up --build
```

---

## How the Skill Gap Algorithm Works

1. **Parse** — LLaMA 3.1 extracts skills from resume with confidence scores (0–100) and years of experience. Same for job description requirements.

2. **Embed** — Each skill name is encoded into a 384-dimensional vector using Sentence-BERT. Cached per unique string for performance.

3. **Classify** — Cosine similarity between candidate skills and required skills:
   - Score ≥ 0.75 → **Known** (skip)
   - Score 0.42–0.75 → **Partial** (refresher module)
   - Score < 0.42 → **Missing** (full module)

4. **Sort** — Missing and partial skills are passed through a NetworkX prerequisite graph. Topological sort ensures correct learning order (e.g. Linux CLI → Docker → Kubernetes).

5. **Match** — Each ordered skill is matched against the fixed 30-course catalog using cosine similarity. Below 0.45 threshold → placeholder, never an invented course name.

6. **Trace** — Every matched module gets a plain-language reason: what the resume showed, what the JD requires, and why this module appears at this position.

---

## What Makes RoleReady AI Different

| Feature | Most teams | RoleReady AI |
|---|---|---|
| Skill matching | Keyword exact match | SBERT semantic similarity |
| Course names | LLM generates freely | Fixed catalog only |
| Reasoning | Hidden in backend | Shown in UI per module |
| Learning order | Random list | Prerequisite graph sort |
| Domain coverage | Tech only | Tech + Operations |
| Readiness score | Static | Updates live as you complete modules |

---

## Datasets Used

- **O*NET** — Standardised occupational skills database
- **Kaggle Resume Dataset** — Resume parsing training reference
- **Kaggle Job Descriptions Dataset** — JD parsing reference
- Custom 30-course catalog built from industry skill frameworks

---

Built for IISc Bangalore Hackathon 2025 — Adaptive Onboarding Challenge
