from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    FILLED = "filled"

class ApplicationStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

# Job Seeker Models
class JobSeekerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    skills: List[str]
    experience_years: int

class JobSeekerCreate(JobSeekerBase):
    pass

class JobSeeker(JobSeekerBase):
    id: int
    created_at: datetime
    resume_url: Optional[str] = None

    class Config:
        from_attributes = True

# Employer Models
class EmployerBase(BaseModel):
    company_name: str
    email: EmailStr
    phone: str
    description: str
    website: Optional[str] = None

class EmployerCreate(EmployerBase):
    pass

class Employer(EmployerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Job Posting Models
class JobPostingBase(BaseModel):
    title: str
    description: str
    requirements: List[str]
    location: str
    salary_range: str
    job_type: str  # full-time, part-time, contract
    experience_required: int

class JobPostingCreate(JobPostingBase):
    employer_id: int

class JobPosting(JobPostingBase):
    id: int
    employer_id: int
    status: JobStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Application Models
class ApplicationBase(BaseModel):
    cover_letter: str

class ApplicationCreate(ApplicationBase):
    job_id: int
    seeker_id: int

class Application(ApplicationBase):
    id: int
    job_id: int
    seeker_id: int
    status: ApplicationStatus
    applied_at: datetime
    resume_url: Optional[str] = None

    class Config:
        from_attributes = True

# Response Models with HATEOAS links
class JobPostingWithLinks(JobPosting):
    links: dict = {}

class ApplicationWithLinks(Application):
    links: dict = {}
