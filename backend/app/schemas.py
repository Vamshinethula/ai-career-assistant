from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ResumeResponse(BaseModel):
    id: int
    original_filename: str
    user_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


class ResumeDetailResponse(ResumeResponse):
    resume_text: str | None


class ResumeSkillsResponse(BaseModel):
    resume_id: int
    method: Literal["rule_based"] = "rule_based"
    text_available: bool
    skills: list[str]

