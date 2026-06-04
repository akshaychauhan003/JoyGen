# AI Project Idea Generator

> An intelligent recommendation system that suggests personalized project ideas to students based on their interests, skill level, known technologies, and available time.

---

## Table of Contents

1. [Project Summary](#project-summary)
2. [Key Features](#key-features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [Installation](#installation)
7. [How to Run](#how-to-run)
8. [Usage Guide](#usage-guide)
9. [API Endpoints](#api-endpoints)
10. [Use Cases](#use-cases)
11. [Screenshots](#screenshots)
12. [Future Enhancements](#future-enhancements)
13. [Troubleshooting](#troubleshooting)
14. [License](#license)

---

## Project Summary

Students often struggle to find meaningful project topics that align with their skills and career goals. Generic lists from Google do not account for individual differences in:
- Domain interests (NLP, Web Dev, Cybersecurity, etc.)
- Current skill level (Beginner / Intermediate / Advanced)
- Available technologies (Python, React, FastAPI, etc.)
- Time constraints (1 week to full semester)

**AI Project Idea Generator** solves this by using a scoring-based recommendation engine that:
- Matches user interests against project domains using keyword overlap
- Filters projects by skill compatibility and time feasibility
- Diversifies results across thematic clusters so recommendations are not repetitive
- Suggests missing skills the user may need to learn for each recommended project

This makes it a practical tool for:
- Final-year students looking for capstone ideas
- Beginners trying to build their first portfolio project
- Teachers who want to suggest relevant topics to different student profiles

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Interest-Based Matching** | Enter free-text interests; the system scores projects by domain and description overlap |
| **Skill Level Filtering** | Choose Beginner, Intermediate, or Advanced; only feasible projects are recommended |
| **Known Skills Input** | Add technologies you already know; projects requiring those skills are boosted |
| **Time Constraint Awareness** | Set available duration in weeks; projects exceeding your timeline are penalized |
| **Cluster-Based Diversification** | Recommendations are spread across different project clusters so you get variety, not clones |
| **Skill Gap Feedback** | Each recommendation shows which skills you are missing, helping you plan learning |
| **Dark Theme UI** | Black / Navy / White color scheme for a modern, clean interface |
| **FastAPI Backend** | Lightweight, high-performance Python API with CORS enabled |
| **Static File Serving** | Frontend HTML/CSS/JS served directly from the backend or any static host |

---

## Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** — modern, fast web framework for building APIs
- **Uvicorn** — ASGI server to run the application
- **Pydantic** — data validation and settings management

### Frontend
- **HTML5** — semantic markup
- **CSS3** — custom properties, flexbox, grid, fluid typography
- **Vanilla JavaScript** — no build step required, fetch API for async requests

### Data
- **JSON** — lightweight project dataset stored in `data/projects.json`

---

## Project Structure

```text
ai-project-generator/
│
├── main.py                          # FastAPI backend with recommendation logic
├── requirements.txt               # Python dependencies
├── README.md                      # This file
│
├── data/
│   └── projects.json              # Project ideas dataset (title, description,
│                                  #   difficulty, domains, skills, time, cluster)
│
├── static/                        # Frontend assets
│   ├── ai-project-generator.html  # Main UI page (also served at root)
│   ├── style.css                  # Black / Navy / White theme stylesheet
│   └── script.js                  # Frontend logic: form handling, API calls, rendering
│
└── assets/                        # Optional: images, logos, screenshots
```

---

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.10 or higher**
   - Check version: `python --version` or `python3 --version`
2. **pip** (Python package installer)
   - Usually included with Python
3. **Git** (optional, for cloning)

---

## Installation

### Step 1: Download or Clone the Project

```bash
# Option A: Extract the ZIP file
unzip ai-project-generator.zip
cd ai-project-generator

# Option B: If using Git
git clone <repository-url>
cd ai-project-generator
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `fastapi`
- `uvicorn[standard]`

---

## How to Run

### Development Mode (with auto-reload)

```bash
uvicorn main:app --reload
```

Then open your browser and navigate to:

```text
http://127.0.0.1:8000
```

The root route (`/`) automatically serves the frontend HTML file.

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

This makes the app accessible on your network. Use a process manager like **Gunicorn** with Uvicorn workers for production deployments:

```bash
pip install gunicorn
gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Static Hosting (Frontend Only)

If you only want to host the UI on a static site (Netlify, GitHub Pages, Vercel):

1. Copy `index.html` (or `static/ai-project-generator.html`) to the root
2. Ensure CSS and JS paths point to `./static/style.css` and `./static/script.js`
3. Update the API endpoint in `script.js` from `/api/recommend` to your deployed backend URL

---

## Usage Guide

### 1. Open the Application

Navigate to `http://127.0.0.1:8000` after starting the server.

### 2. Fill Your Profile

| Field | What to Enter | Example |
|-------|---------------|---------|
| **Interests** | Comma-separated topics you enjoy | `NLP, web development, finance` |
| **Skill Level** | Select from dropdown | `Intermediate` |
| **Available Time** | Number of weeks you have | `4` |
| **Known Skills** | Technologies you already know | `Python, FastAPI, HTML, CSS` |

### 3. Generate Ideas

Click the **"Generate Ideas"** button. The backend will:
1. Parse and normalize your inputs
2. Score all projects in the dataset against your profile
3. Filter out projects that are too hard or too long
4. Diversify results across different clusters
5. Return the top recommendations with explanations

### 4. Review Recommendations

Each result card shows:
- **Project title** and **description**
- **Difficulty badge** (Beginner / Intermediate / Advanced)
- **Domains** and **required skills**
- **Estimated time** in weeks
- **Why it was recommended**
- **Skills to learn** (if you are missing any required skills)

### 5. Iterate

Try different combinations of interests and skills to explore new domains. The scoring engine adapts dynamically.

---

## API Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/` | Serves the frontend HTML | — |
| `GET` | `/api/projects` | Returns all projects in the dataset | — |
| `POST` | `/api/recommend` | Returns personalized recommendations | `{"interests": "...", "skill_level": "...", "known_skills": "...", "duration_weeks": 4}` |

### Example API Request

```bash
curl -X POST "http://127.0.0.1:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "interests": "NLP, education",
    "skill_level": "intermediate",
    "known_skills": "Python, machine learning",
    "duration_weeks": 4
  }'
```

### Example Response

```json
{
  "query": {
    "interests": "NLP, education",
    "skill_level": "intermediate",
    "known_skills": "Python, machine learning",
    "duration_weeks": 4
  },
  "recommendations": [
    {
      "id": 4,
      "title": "Project Topic Recommender",
      "description": "Recommend project topics to students using interests and skill level.",
      "difficulty": "intermediate",
      "domains": ["recommendation", "education", "nlp"],
      "skills": ["python", "machine learning", "fastapi"],
      "time_weeks": 4,
      "cluster": "education-tools",
      "score": 18,
      "reason": "matches your interest domains, fits your current skills, matches your skill level, fits your available time",
      "missing_skills": ["fastapi"]
    }
  ]
}
```

---

## Use Cases

### For Students
- **Capstone Projects**: Find a topic that matches your branch and skills for final-year submissions
- **Skill Building**: Discover projects that teach you technologies you want to learn
- **Portfolio Development**: Build projects that are unique and relevant to your career goals
- **Hackathons**: Quickly find feasible ideas within a 24–48 hour time frame

### For Teachers / Mentors
- **Classroom Differentiation**: Suggest easier projects to struggling students and advanced ones to top performers
- **Curriculum Planning**: Identify which skills students commonly lack and add them to the syllabus
- **Project Fair Organization**: Ensure diversity of topics by using cluster-based recommendations

### For Self-Learners
- **Career Switchers**: Enter your target domain (e.g., "data science") and current skills to find a learning roadmap
- **Bootcamp Graduates**: Find intermediate projects that bridge the gap between tutorials and real work

---

## Screenshots

> Add screenshots of your application here for documentation and portfolio purposes.

### Suggested Screenshots to Capture:
1. **Homepage / Hero Section** — shows the tagline and input form
2. **Filled Form** — interests, skills, and time entered
3. **Recommendations Grid** — multiple project cards with badges
4. **Single Card Detail** — showing "Why recommended" and "Skills to learn"
5. **Mobile View** — responsive layout on a phone screen

Save screenshots to the `assets/` folder and reference them like:

```markdown

```

---

## Future Enhancements

| Enhancement | Benefit |
|-------------|---------|
| **Tag-Based Input** | Add interests/skills via `+ Add` buttons instead of free text to prevent typos |
| **Larger Dataset** | Expand `projects.json` to 50+ entries across more domains (CV, IoT, Blockchain, etc.) |
| **TF-IDF / Embeddings** | Replace keyword matching with semantic similarity using `sentence-transformers` |
| **User Accounts** | Save profiles and history; enable collaborative filtering over time |
| **LLM Integration** | Use a lightweight LLM to generate custom project briefs and milestones |
| **Feedback Loop** | Let users rate recommendations to improve future suggestions |
| **Deployment Guide** | Add Docker, Render, Railway, and Vercel deployment configs |

---

## Troubleshooting

### Issue: `uvicorn` command not found
**Fix:** Ensure your virtual environment is activated, then reinstall:
```bash
pip install uvicorn
```

### Issue: Port 8000 is already in use
**Fix:** Use a different port:
```bash
uvicorn main:app --reload --port 8080
```

### Issue: Frontend shows "Server error"
**Fix:** Check that the backend is running and that the API URL in `script.js` matches your server address.

### Issue: CSS/JS not loading on deployment
**Fix:** Verify that `static/` files are being served. If using static hosting, ensure paths are relative (`./static/...`).

### Issue: Recommendations feel repetitive
**Fix:** Add more diverse projects to `data/projects.json` and ensure clusters are distinct.

---

## License

This project is open-source and available under the **MIT License**.

Feel free to fork, modify, and use it for personal, academic, or commercial purposes.

---

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and modern web standards
- Inspired by research on student project recommendation systems and diversity in recommender systems
- Designed for students, by students

---

> **Need help?** Open an issue or reach out with questions about setup, deployment, or customization.