from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from PyPDF2 import PdfReader
import spacy

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load NLP model
nlp = spacy.load("en_core_web_sm")


@app.get("/")
def home():
    return {"message": "Resume Analyzer Backend Running"}


# Skill Database
skills_db = [
    "python", "java", "c++", "javascript", "react", "node",
    "machine learning", "deep learning", "ai", "data science",
    "nlp", "tensorflow", "pytorch", "sql", "mongodb",
    "html", "css", "flask", "fastapi", "django",
    "aws", "azure", "docker", "git", "github",
    "pandas", "numpy", "tableau", "power bi"
]


# Resume Score
def calculate_score(skills, text):

    score = 0

    score += len(skills) * 5

    if len(text) > 1000:
        score += 20
    elif len(text) > 500:
        score += 10

    keywords = ["project", "experience", "internship", "education"]

    for keyword in keywords:
        if keyword in text.lower():
            score += 5

    if score > 100:
        score = 100

    return score


# Job Role Prediction
def predict_job_role(text):

    roles = {
        "Data Scientist": [
            "machine learning", "data science",
            "statistics", "pandas", "numpy"
        ],
        "AI Engineer": [
            "deep learning", "tensorflow",
            "pytorch", "nlp"
        ],
        "Web Developer": [
            "html", "css", "javascript",
            "react", "frontend"
        ],
        "Backend Developer": [
            "api", "database",
            "django", "flask", "fastapi"
        ],
        "Data Analyst": [
            "excel", "sql",
            "power bi", "tableau"
        ]
    }

    text = text.lower()

    role_scores = {}

    for role, keywords in roles.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        role_scores[role] = score

    predicted_role = max(role_scores, key=role_scores.get)

    return predicted_role


# Suggestions
def generate_suggestions(skills, text, score):

    suggestions = []

    if len(skills) < 5:
        suggestions.append("Add more technical skills")

    if "project" not in text.lower():
        suggestions.append("Add projects section")

    if "experience" not in text.lower():
        suggestions.append("Add experience section")

    if "certification" not in text.lower():
        suggestions.append("Add certifications")

    if score < 50:
        suggestions.append("Improve resume content")

    if len(suggestions) == 0:
        suggestions.append("Resume looks strong")

    return suggestions


# Match Score
def calculate_match_score(resume_text, job_description):

    resume_text = resume_text.lower()
    job_description = job_description.lower()

    job_words = job_description.split()

    match_count = 0

    for word in job_words:
        if word in resume_text:
            match_count += 1

    match_score = int((match_count / len(job_words)) * 100)

    if match_score > 100:
        match_score = 100

    return match_score


# Match Feedback
def match_feedback(score):

    if score >= 80:
        return "Excellent match for this job"
    elif score >= 60:
        return "Good match"
    elif score >= 40:
        return "Average match"
    else:
        return "Poor match - Improve resume"


# Upload API
@app.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = ""
    reader = PdfReader(file_path)

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    text_lower = text.lower()

    # Skill Detection
    found_skills = []

    for skill in skills_db:
        if skill in text_lower:
            found_skills.append(skill)

    # Score
    score = calculate_score(found_skills, text)

    # Job Role
    job_role = predict_job_role(text)

    # Suggestions
    suggestions = generate_suggestions(found_skills, text, score)

    # Match Score
    match_score = calculate_match_score(text, job_description)

    # Feedback
    feedback = match_feedback(match_score)

    return {
        "filename": file.filename,
        "skills": found_skills,
        "score": score,
        "job_role": job_role,
        "match_score": match_score,
        "match_feedback": feedback,
        "suggestions": suggestions
    }