from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import auth, users, resumes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Career Assistant API",
    description="Backend API for resume analysis and job matching.",
    version="1.0.0",
)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(resumes.router)


@app.get("/")
def root():
    return {
        "message": "AI Career Assistant API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }