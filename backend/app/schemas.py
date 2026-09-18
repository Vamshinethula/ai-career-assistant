from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value or '\x00' in value or len(value.encode('utf-8')) > 72:
            raise ValueError('Password must be 1–72 UTF-8 bytes and contain no null characters')
        return value


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


class RoleMatchResponse(BaseModel):
    role_id: str
    title: str
    skill_overlap_percent: float = Field(ge=0, le=100)
    matched_skills: list[str]
    not_detected_skills: list[str]


class ResumeRoleMatchesResponse(BaseModel):
    resume_id: int
    method: Literal["skill_overlap"] = "skill_overlap"
    catalog: Literal["illustrative_v1"] = "illustrative_v1"
    text_available: bool
    extracted_skills: list[str]
    matches: list[RoleMatchResponse]


class JobComparisonRequest(BaseModel):
    job_description: str = Field(min_length=1, max_length=10000)

    @field_validator('job_description')
    @classmethod
    def reject_blank_description(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Job description must contain non-whitespace text')
        return value.strip()


RequirementCategory = Literal['required', 'optional', 'not_required', 'uncertain']


class RequirementEvidence(BaseModel):
    text: str = Field(min_length=1, max_length=10000)
    category: RequirementCategory


class JobRequirementResponse(BaseModel):
    skill: str = Field(min_length=1)
    category: RequirementCategory
    evidence: list[RequirementEvidence] = Field(min_length=1)


class JobComparisonResponse(BaseModel):
    resume_id: int
    method: Literal['keyword_overlap'] = 'keyword_overlap'
    text_available: bool
    job_skills: list[str]
    matched_skills: list[str]
    not_detected_skills: list[str]
    skill_overlap_percent: float | None = Field(default=None, ge=0, le=100)
    requirements: list[JobRequirementResponse]

