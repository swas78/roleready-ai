# RoleReady AI
### Adaptive Onboarding Engine — IISc Bangalore Hackathon 2025

> **Stop giving every new hire the same 40-hour course.**  
> RoleReady AI analyzes their resume against the job description and builds a dynamic, personalized learning path for exactly what they're missing.

---

## 🚀 What It Does

**RoleReady AI** is an end-to-end adaptive onboarding system. It takes a candidate's resume and a target job description, identifies the exact skill gap using semantic AI, and generates a personalized learning roadmap.

**The problem:** Most companies give every new hire identical onboarding. A 10-year veteran sits through the same beginner modules as a fresh graduate. 
**The solution:** RoleReady AI eliminates that waste by targeting only the missing skills.

---

## ⚡ Live Demo

| Profile | Readiness | Modules | Efficiency |
|---|---|---|---|
| **Senior Engineer** | 72% | 4 modules | 28h saved |
| **Fresh Graduate** | 22% | 7 modules | 18h saved |
| **Operations Worker** | 45% | 4 modules | 22h saved |

Try the demo at `/demo` — no resume upload needed.

---

## ✨ Key Features

- **🧠 Semantic Skill Matching** — Uses SBERT embeddings, not keyword search. "ML experience" matches "machine learning" correctly.
- **🚫 Zero Hallucinations** — AI picks only from a fixed, curated catalog. It never invents a course name.
- **🔍 Reasoning Trace** — Every module shows exactly *why* it was recommended. Not hidden in logs — shown in the UI.
- **mj Prerequisite Graph** — NetworkX topological sort ensures you learn dependencies in order (e.g., Linux before Docker).
- **🌐 Cross-Domain** — Works for tech roles (engineers) and ops roles (warehouse, supply chain) equally.
- **📈 Dynamic Readiness** — Live readiness score that updates as you complete modules.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Resume + JD Text] -->|LLM Parser (LLaMA 3.1)| B(Extracted Skills & Confidence)
    B -->|SBERT Embedder| C{Gap Classifier}
    C -->|Score >= 0.75| D[Known - Skip]
    C -->|Score 0.42-0.75| E[Partial - Refresher]
    C -->|Score < 0.42| F[Missing - Full Module]
    E & F -->|NetworkX DiGraph| G[Prerequisite Sort]
    G -->|Catalog Matcher| H[Course Catalog]
    H -->|Reasoning Tracer| I[Personalized Roadmap]
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM Parsing** | LLaMA 3.1 8B via Groq API |
| **Semantic Matching** | Sentence-BERT (all-MiniLM-L6-v2) |
| **Graph Logic** | NetworkX (topological sort) |
| **Backend** | Python FastAPI + Uvicorn |
| **Frontend** | Node.js + Express + EJS |
| **Styling** | Custom CSS (Glassmorphism) |
| **Deployment** | Docker Containers |

---

## 📂 Project Structure

```bash
roleready-ai/
├── backend/                 # Python FastAPI backend
│   ├── core/                # Core AI logic (Parser, Embedder, Gap, Graph)
│   ├── api/                 # API Routes & Schemas
│   ├── data/                # Catalog & Graph JSONs
│   └── main.py              # App Entry Point
├── views/                   # EJS Templates (Frontend)
├── public/                  # Static Assets (CSS/JS)
├── routes/                  # Express Routes
└── server.js                # Node.js Server
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API key

### 1. Clone
```bash
git clone https://github.com/YOUR_USERNAME/roleready-ai.git
cd roleready-ai
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt
# Create .env with GROQ_API_KEY=your_key
python3 -m uvicorn main:app --reload --port 8000
```

### 3. Frontend
```bash
# In a new terminal
cd ..
npm install
npm run dev
```

### 4. Access
Open `http://localhost:3000`

---

## 🔮 Future Scope

1.  **LMS Integration:** Export learning paths to SCORM/xAPI for Moodle or Canvas.
2.  **Assessment Generation:** AI-generated quizzes based on the specific skill gaps.
3.  **Peer Matching:** Connect new hires with mentors who have the skills they are missing.
4.  **Multi-Language Support:** Localized content for global teams.

---

## 🏆 Hackathon Details

**Event:** IISc Bangalore Hackathon 2025  
**Track:** Adaptive Onboarding Challenge  
**Status:** Completed Prototype

---
