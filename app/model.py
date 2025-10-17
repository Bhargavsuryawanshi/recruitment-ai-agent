from pydantic import BaseModel
from typing import List, Optional

class JobDescriptionInput(BaseModel):
    job_title: str
    experience: str
    skills: str
    company_name: str
    employment_type: str
    industry: str
    location: str

class Candidate(BaseModel):
    filename: str
    score: int
    missing_skills: List[str]
    remarks: str
    email: Optional[str] = None