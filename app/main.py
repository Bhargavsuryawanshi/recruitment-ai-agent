from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import os
from dotenv import load_dotenv

from .ai_processing import generate_jd, evaluate_resumes, generate_emails
from .text_extraction import extract_text_from_file
from .model import JobDescriptionInput, Candidate


load_dotenv()

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory storage (for simplicity in this example)
job_description_text = ""
candidates_data = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process-jd", response_class=HTMLResponse)
async def process_jd(
    request: Request,
    jd_file: Optional[UploadFile] = File(None),
    jd_text: Optional[str] = Form(None),
    job_title: Optional[str] = Form(None),
    experience: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    employment_type: Optional[str] = Form(None),
    industry: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
):
    global job_description_text

    if jd_file and jd_file.filename:
        job_description_text = await extract_text_from_file(jd_file)
    elif jd_text:
        job_description_text = jd_text
    elif job_title and skills:
        jd_input = JobDescriptionInput(
            job_title=job_title,
            experience=experience,
            skills=skills,
            company_name=company_name,
            employment_type=employment_type,
            industry=industry,
            location=location
        )
        job_description_text = await generate_jd(jd_input)

    return templates.TemplateResponse("index.html", {"request": request, "job_description": job_description_text})

@app.post("/evaluate-resumes", response_class=HTMLResponse)
async def evaluate_uploaded_resumes(request: Request, resumes: List[UploadFile] = File(...)):
    global candidates_data
    global job_description_text

    if not job_description_text:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Please provide a job description first."})

    resume_texts = []
    for resume in resumes:
        text = await extract_text_from_file(resume)
        resume_texts.append({"filename": resume.filename, "text": text})

    candidates_data = await evaluate_resumes(job_description_text, resume_texts)

    # Generate emails for the best and other candidates
    if candidates_data:
        best_candidate = max(candidates_data, key=lambda x: x.score)
        other_candidates = [c for c in candidates_data if c != best_candidate]
        
        emails = await generate_emails(job_description_text, best_candidate, other_candidates)
        
        for i, candidate in enumerate(candidates_data):
            if candidate == best_candidate:
                candidate.email = emails["interview_email"]
            else:
                candidate.email = emails["rejection_emails"][i] if i < len(emails["rejection_emails"]) else ""


    return templates.TemplateResponse("results.html", {"request": request, "candidates": candidates_data})