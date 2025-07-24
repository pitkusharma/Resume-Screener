from typing import List, Optional
from pydantic import BaseModel

class ExperienceItem(BaseModel):
    company: str
    role: str
    duration: str

class EducationItem(BaseModel):
    degree: str
    institution: str
    year: Optional[str]

class ParsedResume(BaseModel):
    name: str
    email: str
    phone: str
    skills: List[str]
    experience: List[ExperienceItem]
    education: List[EducationItem]
