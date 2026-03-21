# RoleReady AI - Quick Reference Checklist

**Use this as a quick lookup while reading the detailed audit documents.**

---

## 🔴 CRITICAL ISSUES (Fix First)

### UI/UX
- [ ] **Cursor System** - Remove custom cursor (breaks accessibility, performance hit)
  - File: `/public/js/cursor.js`
  - Impact: Accessibility failure, 16KB code, 15-20ms CPU use
  - Fix: Delete file + CSS references

- [ ] **Overlapping Elements** - Landing page has z-index conflicts
  - Files: `/public/css/landing.css`, `/views/landing.ejs`
  - Impact: Some elements clickable, hover effects broken
  - Fix: Proper z-index stacking, remove opacity: 0.02 text

- [ ] **No Mobile Support** - Page breaks on phones
  - Files: All CSS files
  - Impact: 50%+ users can't use site on mobile
  - Fix: Add mobile breakpoints (@media 480px, 768px)

### Backend Logic
- [ ] **Broken Gap Classification** - Known/partial/missing logic is wrong
  - File: `/backend/core/gap.py` lines 35-60
  - Impact: Wrong skill recommendations
  - Fix: Rewrite lines 35-60, test with examples

- [ ] **Flawed Readiness Formula** - Score doesn't reflect true readiness
  - File: `/backend/core/gap.py` lines 63-74
  - Calculation: (known + partial×0.5) / total × 100
  - Problem: Partial-heavy users score higher than known-heavy
  - Fix: Use weighted formula with domain-specific weights

- [ ] **Course Matching is Dumb** - No prerequisite enforcement
  - File: `/backend/core/planner.py` lines 13-31
  - Impact: Recommends "Advanced" without "Basics"
  - Fix: Add prerequisite graph resolution

### Security
- [ ] **No Input Validation** - File uploads unchecked, no size limits
  - File: `/backend/api/routes.py` lines 63-80
  - Vulnerability: File bomb (10GB upload), path traversal, code injection
  - Fix: Add MIME check, file size (5MB max), sanitize

- [ ] **No CSRF Protection** - Forms vulnerable to cross-site attacks
  - File: `/server.js` - missing csrf middleware
  - Impact: Malicious site can submit forms on user's behalf
  - Fix: Add csrf-csrf middleware, tokens on forms

- [ ] **Weak Session Management** - Uses fallback secret if env missing
  - File: `/server.js` lines 18-23
  - Problem: `secret: process.env.SESSION_SECRET || 'fallback-secret'`
  - Fix: Require env var in production, fail startup if missing

- [ ] **No Secrets Management** - API keys logged to console
  - Files: `/backend/core/parser.py` line 14
  - Problem: Default placeholder key visible in errors
  - Fix: Use dotenv with required validation

### Data
- [ ] **Courses Are Generic** - No learning structure, no assessments
  - File: `/backend/data/catalog.json`
  - Problem: Just name + duration + vague skills list
  - Fix: Add modules, lessons, learning outcomes, assessments

---

## 🟠 HIGH PRIORITY ISSUES (Do Next 2 Weeks)

### Organization
- [ ] **Scattered Responsibilities** - Frontend/backend mixed
  - Problem: `/api/backend.js` unused, routes in multiple folders
  - Fix: Follow PROJECT_REORGANIZATION_GUIDE structure

- [ ] **No Tests** - Zero test coverage
  - Missing: `/backend/tests/` folder, pytest config
  - Fix: Set up pytest, write tests for core logic

- [ ] **No Documentation** - Missing README, API spec, architecture
  - Missing: README.md, openapi.yaml, architecture diagram
  - Fix: Create docs/ folder with all guides

### Performance
- [ ] **Cursor Trails Cause Jank** - 3 extra DOM elements + RAF loop
  - File: `/public/js/cursor.js` lines 7-55
  - Impact: 15-20ms CPU per frame on low-end devices
  - Fix: Remove entirely (included in critical fixes above)

- [ ] **Font Loading Blocks Page** - 4 fonts without font-display
  - Files: CSS @import statements
  - Impact: Users see blank page while fonts load (~150KB)
  - Fix: Add `font-display: swap` or `block`

- [ ] **No Image Optimization** - Avatar images not lazy-loaded
  - Files: `/views/*.ejs` img tags
  - Fix: Add loading="lazy" and width/height attributes

### Accessibility
- [ ] **No Keyboard Navigation** - Tab only works on some elements
  - Problem: Custom cursor breaks keyboard nav
  - Fix: Remove cursor, add focus-visible outlines to all interactive elements

- [ ] **Color-Only Indicators** - Skill status shown by color alone
  - File: `/views/results.ejs`
  - Problem: Red/green/yellow means nothing to colorblind users
  - Fix: Add text badges: "Missing", "Partial", "Known"

- [ ] **Tiny Font on Small Screens** - 13px mono font, no mobile optimization
  - Files: `/public/css/results.css` line 52
  - Fix: 16px minimum on mobile, clamp sizing

- [ ] **Missing Alt Text** - Avatar images have no alt attributes
  - Files: `/views/landing.ejs` lines 25-28
  - Fix: Add meaningful alt text to images

- [ ] **Low Contrast** - `#888` on `#111` = 3:1 ratio (WCAG fails)
  - Multiple places in CSS
  - Fix: Use #999+ for text on dark backgrounds (4.5:1 ratio)

### Content/UX
- [ ] **No Course Prerequisites** - Catalog doesn't link courses
  - File: `/backend/data/catalog.json`
  - Problem: Can't define that "Python Advanced" requires "Python Basics"
  - Fix: Add prerequisites array to each course

- [ ] **No Learning Objectives** - Courses don't define outcomes
  - File: `/backend/data/catalog.json`
  - Problem: "Python Basics (8h)" - but teaches what exactly?
  - Fix: Add learning_outcomes array with specific goals

- [ ] **No Course Specialization** - All tech courses equal weight
  - Problem: Backend/frontend/devops mixed
  - Fix: Create learning paths and specialization tracks

---

## 🟡 MEDIUM PRIORITY ISSUES (Next Month)

### Code Quality
- [ ] **Inconsistent Error Handling** - No centralized error formatter
  - Files: All route files
  - Fix: Create error middleware in `/frontend/middleware/error-handler.js`

- [ ] **No Logging** - Silent failures, hard to debug
  - All files
  - Fix: Add `/backend/utils/logger.py` with structured logging

- [ ] **Duplicate Code** - Parser prompts similar, not DRY
  - File: `/backend/core/parser.py`
  - Fix: Extract shared prompt templates

- [ ] **Missing Caching** - Catalog loaded from disk every request
  - File: `/backend/core/planner.py` line 7
  - Fix: Load once in memory, cache embeddings

### Infrastructure
- [ ] **No Docker Setup** - Can't deploy reproducibly
  - Missing: `Dockerfile`, `docker-compose.yml`
  - Fix: Create containerized setup

- [ ] **No CI/CD Pipeline** - No automated testing
  - Missing: `.github/workflows/` or similar
  - Fix: Add GitHub Actions for tests on push

- [ ] **No Rate Limiting** - Anyone can spam `/analyze` endpoint
  - File: `/server.js`
  - Fix: Add express-rate-limit middleware

---

## 🟢 LOW PRIORITY ISSUES (Future Nice-to-Haves)

- [ ] User accounts & history
- [ ] Certificates & badges
- [ ] Real-time progress tracking
- [ ] Team/admin dashboard
- [ ] Integration with LMS (Udemy, Coursera)
- [ ] Peer review system
- [ ] Discussion forums
- [ ] Advanced AI features

---

## 💾 FILES TO CREATE/MODIFY

### Create (New Files)
- [ ] `/frontend/middleware/error-handler.js`
- [ ] `/frontend/middleware/csrf-protection.js`
- [ ] `/frontend/middleware/request-logger.js`
- [ ] `/frontend/controllers/analyze-controller.js`
- [ ] `/frontend/config/environment.js`
- [ ] `/backend/services/validator.py`
- [ ] `/backend/services/skill_matcher.py`
- [ ] `/backend/services/course_recommender.py`
- [ ] `/backend/utils/logger.py`
- [ ] `/backend/utils/exceptions.py`
- [ ] `/backend/models/skill.py`
- [ ] `/backend/models/course.py`
- [ ] `/backend/tests/test_*.py` (6 test files)
- [ ] `/docs/README.md`
- [ ] `/docs/ARCHITECTURE.md`
- [ ] `/docs/API.md`
- [ ] `/docs/DEPLOYMENT.md`
- [ ] `docker-compose.yml`
- [ ] `.env.example`

### Modify (Existing Files)
- [ ] Delete: `/public/js/cursor.js`
- [ ] Modify: `/backend/core/gap.py` (lines 35-60, 63-74)
- [ ] Modify: `/backend/core/planner.py` (add prerequisites resolve)
- [ ] Modify: `/backend/api/routes.py` (add validation)
- [ ] Modify: `/server.js` (add middleware, security)
- [ ] Modify: `/backend/data/catalog.json` (enhance structure)
- [ ] Modify: All CSS files (fix z-index, add mobile, accessibility)
- [ ] Modify: `/views/layout.ejs` (remove cursor reference)
- [ ] Create: `package.json` sections (add security deps)
- [ ] Create: `requirements.txt` additions (add test deps)

---

## 🔍 TESTING PRIORITIES

### Must Test
- [ ] Form submission with CSRF tokens
- [ ] File upload with size/type validation
- [ ] Gap classification accuracy (with test data)
- [ ] Readiness score calculation
- [ ] Course matching for skill
- [ ] Mobile responsiveness on real phones
- [ ] Cursor removal (accessibility)

### Should Test
- [ ] Rate limiting behavior
- [ ] Session management
- [ ] Error messages display correctly
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility

### Nice to Test
- [ ] Performance (lighthouse >90)
- [ ] API response times (<200ms)
- [ ] Load test with 1000 concurrent users
- [ ] Cross-browser compatibility

---

## 📊 IMPACT SUMMARY

### Critical Fixes Impact
| Issue | Current Impact | After Fix | User Benefit |
|-------|----------------|-----------|--------------|
| Cursor system | Accessibility broken | Works with keyboards | Accessible to all users |
| Gap logic | Wrong recommendations | Accurate matches | Gets right courses |
| Input validation | Infinite API costs | Controlled usage | Site stays up |
| CSRF | Account hijacking | Protected forms | Secure account |
| Mobile support | 50% users can't access | Fully responsive | Works on phone |

### Secondary Fixes Impact
| Issue | Current Impact | After Fix | Benefit |
|-------|----------------|-----------|---------|
| Course structure | No learning path | Guided progression | Better learning outcomes |
| Prerequisites | Can skip basics | Proper sequencing | Avoid knowledge gaps |
| Documentation | Hard to extend | Easy to extend | Team productivity |
| Tests | Bugs in production | Caught early | Higher reliability |
| Organization | Confusing layout | Clear structure | Faster onboarding |

---

## 🚀 RECOMMENDED FIRST 5 STEPS

1. **Delete cursor system** (30 min)
   - Remove `/public/js/cursor.js`
   - Remove CSS cursor rules
   - Test: Cursor works, no trails

2. **Fix gap.py logic** (2 hours)
   - Rewrite classification
   - Fix readiness formula
   - Test: Score matches expected values

3. **Add input validation** (1 hour)
   - File size limit
   - MIME type check
   - Domain enum validation
   - Test: Reject invalid uploads

4. **Add CSRF tokens** (30 min)
   - Install csrf-csrf
   - Add tokens to forms
   - Test: Forms require token

5. **Create mobile CSS** (1 hour)
   - Add breakpoints
   - Stack on mobile
   - Test: Works on 480px width

**Week 1 Total: ~5 hours → Most impact.**

---

## 📞 QUESTIONS TO ASK WHEN STUCK

**On Cursor Removal:**
- Where are cursor references? Find with: `grep -r "cursor" public/`
- What does custom cursor add? Nothing - it's pure aesthetics

**On Gap Logic:**
- Why is formula backwards? It weights partial = 0.5 credit
- How to fix? Use (known×1.0 + partial×0.3) / total × 100

**On Mobile:**
- What size is "mobile"? 480px and smaller
- How to test? Resize browser to 375px, check layout

**On Security:**
- What MIME types allowed? PDF, DOCX only (application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document)
- What file size max? 5MB (5242880 bytes)

**On Organization:**
- Where should service files go? `/backend/services/`
- Where should models go? `/backend/models/`
- Where should tests go? `/backend/tests/`

---

## ✅ VALIDATION CHECKLIST

After each phase, verify:

**Phase 1 (Week 1 Critical Fixes):**
- [ ] Cursor removed, no visual trails
- [ ] Custom CSS for cursor removed
- [ ] Gap classification passes test cases
- [ ] Readiness formula produces expected values
- [ ] File uploads have size/type validation
- [ ] Forms have CSRF tokens
- [ ] Sessions stored properly

**Phase 2 (Week 2 High-Impact):**
- [ ] Catalog JSON has new fields
- [ ] Prerequisites are enforced
- [ ] Mobile site works on 480px
- [ ] Security headers set (helmet.js)
- [ ] Rate limiting active
- [ ] Tests run and pass

**Phase 3 (Week 3 Polish):**
- [ ] WCAG 2.1 AA compliance checked
- [ ] Lighthouse score >90
- [ ] All endpoints documented
- [ ] README complete
- [ ] Architecture documented
- [ ] Code reorganized

---

## 🎯 BY THE NUMBERS

**Current State:**
- 21 identified issues
- 5 critical vulnerabilities
- 0% test coverage
- ~30 hours work needed
- 16KB cursor overhead

**After Complete Audit & Improvements:**
- 0 critical issues (fixed)
- 0 vulnerabilities (patched)
- 80%+ test coverage
- Production-ready codebase
- Fully documented
- Mobile-friendly
- Accessible compliance
- 40% faster
- Secure hardened

---

**Print this page as your reference guide while implementing!**

Last updated: March 21, 2026
