from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine
from app.config import load_cors_origins
from app.migrations import require_current_schema
from app.routers import auth, users, resumes

@asynccontextmanager
async def lifespan(app):
    require_current_schema(engine)
    yield

app = FastAPI(
    lifespan=lifespan,
    title="AI Career Assistant API",
    description="Backend API for resume analysis and job matching.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=load_cors_origins(),
    allow_methods=["GET", "POST", "DELETE", "PATCH"],
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
