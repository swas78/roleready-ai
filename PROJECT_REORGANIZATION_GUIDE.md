# RoleReady AI - Project Reorganization Guide

**Goal:** Convert scattered codebase into production-ready architecture

---

## PHASE 1: DIRECTORY RESTRUCTURING

### Current State (Confusing):
```
roleready-ai/
├── api/backend.js              ← Purpose unclear
├── backend/                    ← Python, but mixed concerns
│   ├── api/routes.py           ← API endpoints
│   ├── core/*.py               ← Business logic (scattered)
│   ├── data/                   ← Static data
│   └── main.py                 ← Entry point
├── server.js                   ← Frontend server
├── routes/*.js                 ← Frontend routes
├── views/*.ejs                 ← Templates
├── public/                     ← Static assets
│   ├── js/                     ← Front-end logic
│   └── css/                    ← Styles
└── package.json                ← npm (but express server in root!)
```

**Problems:** Frontend and backend concepts mixed, unclear responsibilities

---

## PHASE 2: PROPOSED NEW STRUCTURE

```
roleready-ai/
│
├── 📁 frontend/                                    [NEW FOLDER]
│   ├── public/
│   │   ├── js/
│   │   │   ├── cursor.js          ← REMOVE THIS
│   │   │   ├── animations.js      ← REFACTOR
│   │   │   ├── form-handler.js    ← NEW: Form submission
│   │   │   ├── api-client.js      ← NEW: Backend calls
│   │   │   └── utils.js           ← NEW: Shared utilities
│   │   ├── css/
│   │   │   ├── reset.css          ← NEW: Normalize styles
│   │   │   ├── variables.css      ← NEW: Extract design tokens
│   │   │   ├── global.css         ← REFACTOR: Remove cursor
│   │   │   ├── layout.css         ← NEW: Separate from global
│   │   │   ├── landing.css        ← FIX: Z-index issues
│   │   │   ├── forms.css          ← NEW: Consolidate form styles
│   │   │   ├── responsive.css     ← NEW: Mobile breakpoints
│   │   │   └── accessibility.css  ← NEW: A11y improvements
│   │   └── images/                ← NEW: Store images locally
│   │
│   ├── views/
│   │   ├── layout.ejs             ← KEEP (but update refs)
│   │   ├── landing.ejs            ← KEEP
│   │   ├── analyze.ejs            ← KEEP
│   │   ├── results.ejs            ← KEEP
│   │   ├── catalog.ejs            ← KEEP
│   │   ├── components/            ← NEW: Reusable components
│   │   │   ├── navbar.ejs
│   │   │   ├── footer.ejs
│   │   │   ├── form-error.ejs
│   │   │   └── loading.ejs
│   │   └── partials/              ← NEW: Micro components
│   │       ├── skill-badge.ejs
│   │       ├── course-card.ejs
│   │       └── stat-card.ejs
│   │
│   ├── middleware/                ← NEW
│   │   ├── auth.js
│   │   ├── error-handler.js
│   │   ├── request-logger.js
│   │   └── csrf-protection.js
│   │
│   ├── routes/
│   │   ├── index.js
│   │   ├── analyze.js             ← REFACTOR API call
│   │   ├── results.js             ← FIX session handling
│   │   ├── catalog.js
│   │   └── api.js                 ← NEW: Consolidated API routes
│   │
│   ├── controllers/               ← NEW: Business logic
│   │   ├── analyze-controller.js
│   │   └── results-controller.js
│   │
│   ├── config/                    ← NEW
│   │   ├── constants.js
│   │   └── environment.js
│   │
│   ├── server.js                  ← RENAME to index.js
│   ├── package.json               ← MOVE here
│   └── .env.example               ← NEW
│
├── 📁 backend/                                     [REORGANIZE]
│   ├── app/
│   │   ├── main.py                ← Entry point (only)
│   │   └── config.py              ← NEW: Config management
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              ← Endpoints only
│   │   ├── schemas.py             ← Keep: Request/response models
│   │   └── middleware.py          ← NEW: CORS, logging, etc
│   │
│   ├── core/                      [KEEP BUT REFACTOR]
│   │   ├── __init__.py
│   │   ├── embedder.py            ← KEEP
│   │   ├── parser.py              ← FIX: Better prompts
│   │   ├── gap.py                 ← FIX: Logic errors
│   │   ├── graph.py               ← KEEP: Prerequisites
│   │   ├── planner.py             ← FIX: Matching algorithm
│   │   └── tracer.py              ← KEEP
│   │
│   ├── services/                  ← NEW: Extract utilities
│   │   ├── __init__.py
│   │   ├── skill_matcher.py       ← NEW: From planner
│   │   ├── course_recommender.py  ← NEW: Improved logic
│   │   ├── validator.py           ← NEW: Input validation
│   │   ├── pdf_extractor.py       ← NEW: From routes
│   │   └── llm_client.py          ← NEW: Groq wrapper
│   │
│   ├── models/                    ← NEW: Domain objects
│   │   ├── __init__.py
│   │   ├── skill.py
│   │   ├── course.py
│   │   ├── gap.py
│   │   └── recommendation.py
│   │
│   ├── utils/                     ← NEW: Helpers
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── cache.py
│   │   └── exceptions.py
│   │
│   ├── data/
│   │   ├── catalog.json           ← RESTRUCTURE with new fields
│   │   ├── demo_profiles/
│   │   └── prerequisites.json     ← NEW: Skill dependency graph
│   │
│   ├── tests/                     ← NEW: Test suite
│   │   ├── __init__.py
│   │   ├── test_parser.py
│   │   ├── test_gap.py
│   │   ├── test_planner.py
│   │   ├── fixtures.py            ← Example data
│   │   └── conftest.py            ← pytest config
│   │
│   ├── venv/                      ← LOCAL ONLY (not tracked)
│   ├── requirements.txt           ← KEEP
│   ├── requirements-dev.txt       ← NEW: Test deps
│   ├── .env.example               ← NEW: Template
│   └── pytest.ini                 ← NEW: Test config
│
├── 📁 shared/                                      [NEW]
│   ├── openapi.yaml               ← API spec (auto-generated)
│   ├── typescript-types.ts        ← NEW: Shared types
│   ├── constants.ts               ← Frontend/backend constants
│   └── domain-spec.md             ← Domain language definitions
│
├── 📁 docs/                                        [NEW]
│   ├── README.md                  ← Setup & overview
│   ├── ARCHITECTURE.md            ← System design decisions
│   ├── API.md                     ← Endpoint documentation
│   ├── DEPLOYMENT.md              ← Production guide
│   ├── CONTRIBUTING.md            ← Developer guide
│   ├── CHANGELOG.md               ← Version history
│   ├── diagrams/
│   │   ├── architecture.png
│   │   ├── data-flow.png
│   │   └── skill-graph.png
│   └── examples/
│       ├── sample-resume.pdf
│       ├── sample-jd.txt
│       └── api-usage.md
│
├── 📁 scripts/                                     [NEW]
│   ├── setup.sh                   ← Development setup
│   ├── migrate-db.py              ← Future: DB migrations
│   ├── seed-courses.py            ← Load course data
│   └── validate-catalog.py        ← Check catalog consistency
│
├── 📁 config/                                      [NEW]
│   ├── docker-compose.yml
│   ├── .dockerignore
│   └── nginx.conf                 ← Future: Production server
│
├── .gitignore                     ← FIX: Remove venv/ node_modules/
├── .env.example                   ← NEW: Root template
├── docker-compose.yml             ← NEW: Local dev
├── package-lock.json              ← (from npm install)
└── AUDIT_AND_IMPROVEMENTS.md      ← This document!
```

---

## PHASE 3: FILE MIGRATION STEPS

### Step 1: Create New Folder Structure
```bash
# From /Users/hridey/hackathon/roleready-ai/

# Frontend folder
mkdir -p frontend/{public/{js,css,images},views/{components,partials},middleware,routes,controllers,config}

# Backend reorganization
mkdir -p backend/{app,services,models,utils,tests}

# Shared & docs
mkdir -p shared/{} docs/{diagrams,examples} scripts/
```

### Step 2: Move Frontend Files
```bash
# Move existing files
mv public/* frontend/public/
mv views/* frontend/views/
mv routes/* frontend/routes/
mv server.js frontend/

# Create new files (empty stubs)
touch frontend/middleware/{auth.js,error-handler.js,request-logger.js,csrf-protection.js}
touch frontend/controllers/{analyze-controller.js,results-controller.js}
touch frontend/routes/api.js
```

### Step 3: Reorganize Backend
```bash
# Backend already has structure, just needs extension
mkdir -p backend/{services,models,utils,tests}

# Create new files
touch backend/services/{skill_matcher.py,course_recommender.py,validator.py,pdf_extractor.py,llm_client.py}
touch backend/models/{skill.py,course.py,gap.py,recommendation.py}
touch backend/utils/{logger.py,cache.py,exceptions.py}
touch backend/tests/{test_parser.py,test_gap.py,test_planner.py,fixtures.py,conftest.py}
```

### Step 4: Create Documentation Structure
```bash
# Empty stub files
touch docs/{ARCHITECTURE.md,API.md,DEPLOYMENT.md,CONTRIBUTING.md,CHANGELOG.md}
touch docs/examples/{api-usage.md}
mkdir -p docs/diagrams
```

---

## PHASE 4: CODE REORGANIZATION (What Goes Where)

### Frontend: `frontend/middleware/error-handler.js`
**Extract from:** `server.js` lines 46-49
```javascript
// Current: In server.js
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('<h1>500 Internal Server Error</h1>');
});

// Move to: error-handler.js
module.exports = (err, req, res, next) => { ... }
```

### Backend: `backend/services/validator.py`
**Extract from:** `routes.py` line 65-68
```python
# Validation logic scattered in routes
# Move to central validator
class FileValidator:
    @staticmethod
    def validate_upload(file, max_size_mb=5):
        # Check MIME type
        # Check file size
        # Validate content
        pass
```

### Backend: `backend/models/skill.py`
**Extract from:** `schemas.py`
```python
# Move domain classes here
class SkillGap:
    known: List[str]
    partial: List[str]
    missing: List[str]
```

### Frontend: `frontend/public/css/variables.css`
**Extract from:** `global.css` lines 3-20
```css
:root {
  --bg: #0A0A0A;
  --surface: #111111;
  /* ... all vars ... */
}
```

---

## PHASE 5: DEPENDENCY UPDATES

### Frontend `package.json` (move to `frontend/`)
```json
{
  "name": "roleready-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "nodemon index.js",
    "start": "node index.js",
    "lint": "eslint public/js",
    "format": "prettier --write public/"
  },
  "dependencies": {
    "dotenv": "^16.4.5",
    "ejs": "^3.1.9",
    "express": "^4.19.2",
    "express-ejs-layouts": "^2.5.1",
    "express-session": "^1.18.0",
    "multer": "^1.4.5-lts.1",
    "node-fetch": "^2.7.0",
    "helmet": "^8.0.0",                    // NEW: Security headers
    "express-rate-limit": "^9.0.0"         // NEW: Rate limiting
  },
  "devDependencies": {
    "nodemon": "^3.1.14",
    "eslint": "^9.0.0",                   // NEW: Linting
    "prettier": "^4.0.0"                   // NEW: Formatting
  }
}
```

### Backend `requirements.txt`
```
fastapi==0.135.1
uvicorn[standard]==0.42.0
pydantic==2.12.5
python-multipart==0.0.22
sentence-transformers==5.3.0
scikit-learn==1.8.0
numpy==2.4.3
networkx==3.6.1
pdfplumber==0.11.9
python-docx==1.2.0
groq==1.1.1
python-dotenv==1.2.2
httpx==0.28.1
pydantic-settings==2.0.0          # NEW: Config management
pytest==8.0.0                      # NEW: Testing
pytest-asyncio==0.23.0             # NEW: Async tests
```

---

## PHASE 6: CONFIGURATION SEPARATION

### Frontend: `frontend/config/environment.js`
```javascript
module.exports = {
  NODE_ENV: process.env.NODE_ENV || 'development',
  PORT: process.env.PORT || 3000,
  API_BASE_URL: process.env.API_BASE_URL || 'http://localhost:8000',
  SESSION_SECRET: process.env.SESSION_SECRET,
  DEBUG: process.env.DEBUG === 'true'
};
```

### Backend: `backend/app/config.py`
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_PORT: int = 8000
    GROQ_API_KEY: str
    LLM_MODEL: str = "llama-3.1-8b-instant"
    SIMILARITY_THRESHOLD: float = 0.75
    PARTIAL_THRESHOLD: float = 0.42
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## PHASE 7: IMPORT PATH UPDATES

### After reorganization, update imports:

**Frontend:**
```javascript
// OLD: const routes = require('./routes/index');
// NEW:
const routes = require('./routes');
const middleware = require('./middleware');
```

**Backend:**
```python
# OLD: from core.parser import parse_resume
# NEW:
from services.parser import parse_resume
from utils.logger import get_logger
from models.skill import SkillGap
```

---

## PHASE 8: TESTING FRAMEWORK SETUP

### Backend: `backend/tests/conftest.py`
```python
import pytest
from app.config import Settings

@pytest.fixture
def test_settings():
    return Settings(GROQ_API_KEY="test_key")

@pytest.fixture
def embedder():
    # Mock embedder for testing
    pass
```

### Backend: `backend/pytest.ini`
```ini
[pytest]
testpaths = tests
asyncio_mode = auto
```

---

## PHASE 9: SHARED TYPES & CONSTANTS

### Frontend/Backend: `shared/constants.ts`
```typescript
export const DOMAINS = {
  TECH: 'tech',
  OPS: 'ops',
  SHARED: 'shared'
} as const;

export const SKILL_TYPES = {
  KNOWN: 'known',
  PARTIAL: 'partial',
  MISSING: 'missing'
} as const;
```

### Shared: `shared/openapi.yaml`
```yaml
openapi: 3.0.0
info:
  title: RoleReady AI API
  version: 1.0.0
paths:
  /analyze:
    post:
      summary: Analyze skill gaps
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AnalyzeRequest'
```

---

## PHASE 10: DOCUMENTATION STRUCTURE

### `docs/README.md`
- Project overview
- Quick start guide
- Architecture overview
- Feature list

### `docs/ARCHITECTURE.md`
- System design decisions
- Data flow diagrams
- Component interactions
- Technology choices

### `docs/API.md`
- All endpoints documented
- Request/response examples
- Error codes
- Rate limiting info

### `docs/DEPLOYMENT.md`
- Docker setup
- Environment variables
- Database setup (future)
- Scaling considerations

### `docs/CONTRIBUTING.md`
- Development setup
- Code style guide
- PR process
- Testing requirements

---

## PHASE 11: CLEANUP FILES

### `.gitignore` updates
```gitignore
# Environment
.env
.env.local
.env.*.local

# Node
node_modules/
npm-debug.log
dist/
build/

# Python
__pycache__/
*.py[cod]
*$py.class
venv/
*.egg-info/
.pytest_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build
/frontend/dist/
/backend/build/

# Uploads
/uploads/*
!uploads/.gitkeep
```

### Remove old files
```bash
rm api/backend.js      # Purpose was unclear, not used
rm *.pdf               # Move to docs/examples if needed
```

---

## PHASE 12: MIGRATION VALIDATION

### Checklist:
- [ ] All imports updated and working
- [ ] No circular dependencies
- [ ] Tests pass
- [ ] No orphaned files
- [ ] Documentation complete
- [ ] .env.example covers all vars
- [ ] Docker compose starts both servers
- [ ] API still works at 8000
- [ ] Frontend still works at 3000

---

## PHASE 13: CI/CD READY

### `package.json` scripts (frontend)
```json
"scripts": {
  "dev": "nodemon index.js",
  "start": "node index.js",
  "lint": "eslint public/js",
  "format": "prettier --write public/",
  "test": "echo 'No tests yet'"
}
```

### `Makefile` (optional but helpful)
```makefile
.PHONY: setup dev test lint

setup:
	cd frontend && npm install
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

dev:
	cd frontend && npm run dev &
	cd backend && source venv/bin/activate && python app/main.py

test:
	cd backend && python -m pytest

lint:
	cd frontend && npm run lint
	cd backend && python -m pylint backend/
```

---

## COMPLETED STRUCTURE BENEFITS

After reorganization:

✅ **Clear Separation**: Frontend code in `frontend/`, backend in `backend/`
✅ **Scalability**: New features go in predictable locations
✅ **Testing**: Organized `tests/` folder for both
✅ **Documentation**: Centralized `docs/` with everything
✅ **Configuration**: Centralized config management
✅ **Reusability**: Shared utilities extracted
✅ **Maintainability**: Clear responsibilities
✅ **Deployment**: Docker-ready structure
✅ **Team Ready**: New developers understand layout

---

## ESTIMATED TIME

- Phase 1-3: File moves - 30 minutes
- Phase 4-5: Code refactoring - 2-3 hours
- Phase 6-7: Config setup - 1 hour
- Phase 8-9: Testing framework - 1.5 hours
- Phase 10-13: Documentation & validation - 2 hours

**Total: ~8-9 hours of work**

Worth it? Absolutely. The codebase becomes:
- Easier to navigate
- Easier to test
- Easier to deploy
- Easier to hand off to others

---

**End of Reorganization Guide**
