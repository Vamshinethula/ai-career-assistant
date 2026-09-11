from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.database import engine
from app.routers import auth, users, resumes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Career Assistant API",
    description="Backend API for resume analysis and job matching.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
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
