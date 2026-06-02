from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "projects.json"

app = FastAPI(title="AI Project Idea Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class RecommendationRequest(BaseModel):
    interests: str
    skill_level: str
    known_skills: str = ""
    duration_weeks: int = 4


def load_projects():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_words(text: str):
    words = re.findall(r"[a-zA-Z0-9+#]+", text.lower())
    stopwords = {
        "i", "am", "like", "want", "and", "or", "the", "a", "an", "to", "of",
        "in", "for", "with", "on", "my", "is", "using", "based"
    }
    return [w for w in words if w not in stopwords]


def difficulty_value(level: str):
    mapping = {"beginner": 1, "intermediate": 2, "advanced": 3}
    return mapping.get(level.lower(), 2)


def score_project(user_words, known_skills_words, skill_level, duration_weeks, project):
    title_words = normalize_words(project["title"])
    desc_words = normalize_words(project["description"])
    domain_words = [d.lower() for d in project["domains"]]
    project_skills = [s.lower() for s in project["skills"]]

    project_word_bank = set(title_words + desc_words + domain_words + project_skills)
    interest_overlap = len(set(user_words) & project_word_bank)
    skill_overlap = len(set(known_skills_words) & set(project_skills))

    project_diff = difficulty_value(project["difficulty"])
    user_diff = difficulty_value(skill_level)

    difficulty_penalty = 0
    if project_diff > user_diff:
        difficulty_penalty = (project_diff - user_diff) * 2

    duration_penalty = 0
    if project["time_weeks"] > duration_weeks:
        duration_penalty = project["time_weeks"] - duration_weeks

    score = (interest_overlap * 4) + (skill_overlap * 3) - difficulty_penalty - duration_penalty

    if any(word in domain_words for word in user_words):
        score += 2

    return score


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "ai-project-generator.html")


@app.get("/api/projects")
def get_projects():
    return load_projects()


@app.post("/api/recommend")
def recommend(req: RecommendationRequest):
    projects = load_projects()

    user_words = normalize_words(req.interests)
    known_skills_words = normalize_words(req.known_skills)

    scored = []
    for project in projects:
        score = score_project(
            user_words=user_words,
            known_skills_words=known_skills_words,
            skill_level=req.skill_level,
            duration_weeks=req.duration_weeks,
            project=project
        )

        reason_parts = []
        if any(w in [d.lower() for d in project["domains"]] for w in user_words):
            reason_parts.append("matches your interest domains")
        if any(s.lower() in known_skills_words for s in project["skills"]):
            reason_parts.append("fits your current skills")
        if project["difficulty"].lower() == req.skill_level.lower():
            reason_parts.append("matches your skill level")
        if project["time_weeks"] <= req.duration_weeks:
            reason_parts.append("fits your available time")

        if not reason_parts:
            reason_parts.append("is a useful nearby option for your profile")

        scored.append({
            **project,
            "score": score,
            "reason": ", ".join(reason_parts)
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    diversified = []
    used_clusters = set()

    for item in scored:
        if item["cluster"] not in used_clusters:
            diversified.append(item)
            used_clusters.add(item["cluster"])
        if len(diversified) == 4:
            break

    for item in scored:
        if len(diversified) >= 6:
            break
        if item not in diversified:
            diversified.append(item)

    return {
        "query": {
            "interests": req.interests,
            "skill_level": req.skill_level,
            "known_skills": req.known_skills,
            "duration_weeks": req.duration_weeks
        },
        "recommendations": diversified
    }
