# 🧠 AI-Adaptive Onboarding Engine
> Built for **ARTPARK CodeForge Hackathon**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)
![spaCy](https://img.shields.io/badge/NLP-spaCy-09A3D5?logo=spacy)

---

## 🚀 The Problem

Corporate onboarding is broken. Every new hire gets the **same static curriculum** — regardless of what they already know.

- Senior engineers sit through beginner modules they mastered years ago
- Juniors get thrown into advanced content before they're ready
- Result: wasted time, poor retention, slow ramp-up to productivity

## 💡 Our Solution

Upload your **Resume** + **Job Description** → our AI does the rest.

1. Extracts your existing skills from your resume
2. Identifies what the role requires
3. Finds the exact gap between the two
4. Generates a **week-by-week personalised learning roadmap**
5. Explains **why** every skill is recommended

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 Smart Parsing | Extracts skills from PDF resumes and job descriptions |
| 🔍 NLP Extraction | spaCy-powered with alias normalization (JS → JavaScript) |
| 📊 Match Score | Shows your % alignment with the job requirements |
| 🗺️ Adaptive Roadmap | Graph-based BFS generates optimal learning sequence |
| 💡 Reasoning Trace | Explains WHY each skill is in your roadmap |
| 🔗 Resource Links | YouTube, Coursera, freeCodeCamp links per skill |
| 🌐 Cross-Domain | Works for tech AND non-tech job roles |
| 🐳 Dockerized | One command to run the entire app |

---

## 🎬 Demo
```
Resume Skills:     Python, HTML, CSS, Git
JD Requirements:   Python, React, SQL, HTML, CSS, Git, Docker

Match Score: 65%

Missing Skills: React · SQL · Docker

Roadmap:
  Week 1 → SQL       (Beginner)   "Required in JD, no prerequisites"
  Week 2 → React     (Intermediate) "Required in JD, JS already known"  
  Week 3 → Docker    (Intermediate) "Required in JD, best after core skills"
```

---

## 🏗️ Architecture
```
Resume (PDF) ─┐
              ├─→ Flask Backend ─→ NLP Engine ─→ Skill Gap Analyzer ─→ Adaptive Engine ─→ JSON
JD (PDF/TXT) ─┘                                                                              │
                                                                                             ↓
                                                                                     React Dashboard
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Tailwind CSS + React Router |
| Backend | Python Flask + Flask-CORS |
| NLP | spaCy en_core_web_sm + keyword matching |
| Adaptive Engine | Graph-based BFS topological sort |
| Containerization | Docker + Docker Compose |
| Version Control | GitHub |

---

## 📁 Project Structure
```
ai-onboarding-engine/
├── frontend/                  ← React app
│   └── src/
│       ├── pages/             ← Home, Upload, Result
│       ├── components/        ← UploadForm, Roadmap, SkillList
│       └── services/api.js    ← Backend connection
├── backend/                   ← Flask API
│   ├── app.py
│   ├── routes/analyze.py
│   └── services/
│       ├── parser.py          ← PDF text extraction
│       ├── skill_extractor.py ← NLP skill detection
│       ├── skill_gap.py       ← Gap calculator
│       ├── scorer.py          ← Match % calculator
│       └── recommender.py     ← BFS adaptive engine
├── data/
│   ├── skills.json            ← 80+ curated skills
│   └── courses.json           ← Resources per skill
├── Dockerfile.backend
├── Dockerfile.frontend
└── docker-compose.yml
```

---

## ⚡ Quick Start

### Option 1 — Docker (Recommended)
```bash
git clone https://github.com/ujjay2808/ai-onboarding-engine.git
cd ai-onboarding-engine
docker-compose up --build
```

- Frontend → http://localhost:5173
- Backend → http://localhost:5000

### Option 2 — Manual
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## 📡 API Reference

### `POST /analyze`

**Request:** `multipart/form-data`
| Field | Type | Description |
|---|---|---|
| `resume` | PDF file | Candidate's resume |
| `jd` | PDF or TXT | Target job description |

**Response:**
```json
{
  "match_score": 65,
  "resume_skills": ["Python", "HTML"],
  "jd_skills": ["Python", "React", "SQL"],
  "missing_skills": ["React", "SQL"],
  "roadmap": [
    {
      "skill": "SQL",
      "week": 1,
      "difficulty": "Beginner",
      "reason": "Required in JD. Not found in resume. No prerequisites needed. Confidence: High.",
      "resources": [
        {
          "title": "SQL Full Course",
          "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
          "platform": "YouTube",
          "duration": "4 hours"
        }
      ]
    }
  ]
}
```

---

## 🧮 How the Adaptive Engine Works

1. **Text Extraction** — PyPDF2 pulls raw text from uploaded PDFs
2. **NLP Processing** — spaCy tokenizes + lemmatizes, then matches against `skills.json`
3. **Alias Normalization** — Maps `JS → JavaScript`, `ML → Machine Learning` etc.
4. **Skill Gap** — `gap = set(jd_skills) - set(resume_skills)`
5. **Dependency Graph** — Each skill has prerequisites (e.g. React needs JavaScript)
6. **BFS Topological Sort** — Orders skills so prerequisites always come first
7. **Reasoning Trace** — Each item explained: why needed, why this week, confidence level
8. **Match Score** — `(matched / total_jd_skills) * 100`

---

## 📊 Datasets Used

- [O*NET Skills Database](https://www.onetcenter.org/db_releases.html) — occupational skill taxonomy
- [Kaggle Resume Dataset](https://kaggle.com/datasets/snehaanbhawal/resume-dataset) — real resume samples
- Custom `courses.json` — manually curated resource links per skill

---

## 👥 Team

| Name | Role |
|---|---|
| Ujjay | Frontend (React + Tailwind) + Docker |
| Vansh | Backend (Flask) + Core Logic + Adaptive Engine |
| Rutvi | AI/NLP Enhancement + Reasoning Trace + PPT |