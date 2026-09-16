import shutil
from pathlib import Path
from uuid import uuid4
from app.services.resume_parser import extract_text_from_pdf, InvalidResumePDF, ResumePageLimitExceeded
from app.services.skill_extractor import extract_skills
from app.services.role_matcher import match_roles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.config import MAX_RESUME_BYTES, load_data_directory
from app.dependencies import get_db
from app.oauth2 import get_current_user


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)

UPLOAD_DIRECTORY = load_data_directory() / 'uploads'
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@router.get("", response_model=list[schemas.ResumeResponse])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Resume)
        .filter(models.Resume.user_id == current_user.id)
        .order_by(models.Resume.uploaded_at.desc(), models.Resume.id.desc())
        .all()
    )


def get_owned_resume(resume_id: int, db: Session, user_id: int) -> models.Resume:
    resume = db.query(models.Resume).filter(
        models.Resume.id == resume_id,
        models.Resume.user_id == user_id,
    ).first()
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.get("/{resume_id}", response_model=schemas.ResumeDetailResponse)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return get_owned_resume(resume_id, db, current_user.id)


@router.get("/{resume_id}/skills", response_model=schemas.ResumeSkillsResponse)
def get_resume_skills(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    resume = get_owned_resume(resume_id, db, current_user.id)
    return schemas.ResumeSkillsResponse(
        resume_id=resume.id,
        text_available=bool(resume.resume_text and resume.resume_text.strip()),
        skills=extract_skills(resume.resume_text),
    )


@router.get("/{resume_id}/matches", response_model=schemas.ResumeRoleMatchesResponse)
def get_resume_matches(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    resume = get_owned_resume(resume_id, db, current_user.id)
    skills = extract_skills(resume.resume_text)
    return schemas.ResumeRoleMatchesResponse(
        resume_id=resume.id,
        text_available=bool(resume.resume_text and resume.resume_text.strip()),
        extracted_skills=skills,
        matches=match_roles(skills),
    )


@router.post(
    "/upload",
    response_model=schemas.ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_resume(
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    original_filename = Path(resume_file.filename or "").name

    if not original_filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A filename is required",
        )

    file_extension = Path(original_filename).suffix.lower()

    if file_extension != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF resumes are allowed",
        )

    if resume_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file must be a PDF",
        )

    # Measure the actual spooled upload, not a client-supplied size header.
    resume_file.file.seek(0, 2)
    file_size = resume_file.file.tell()
    resume_file.file.seek(0)
    if file_size == 0 or file_size > MAX_RESUME_BYTES:
        resume_file.file.close()
        raise HTTPException(
            status_code=413 if file_size > MAX_RESUME_BYTES else 400,
            detail='Resume must be a nonempty PDF no larger than 5 MiB',
        )

    stored_filename = f"{uuid4()}.pdf"
    destination = UPLOAD_DIRECTORY / stored_filename

    try:
        with destination.open("wb") as output_file:
            shutil.copyfileobj(
                resume_file.file,
                output_file,
            )
    except OSError:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save the uploaded resume",
        )
    finally:
        resume_file.file.close()

    new_resume = models.Resume(
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=str(destination),
        user_id=current_user.id,
    )

    try:
        new_resume.resume_text = extract_text_from_pdf(str(destination))
        db.add(new_resume)
        # Populate generated fields and validate the response before committing.
        # A flush writes within the transaction; rollback can still undo it.
        db.flush()
        result = schemas.ResumeResponse.model_validate(new_resume)
        db.commit()
    except (InvalidResumePDF, ResumePageLimitExceeded) as error:
        db.rollback()
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=413 if isinstance(error, ResumePageLimitExceeded) else 400,
            detail=str(error),
        ) from error
    except Exception:
        # Parser, schema and database failures all require the same cleanup.
        db.rollback()

        if destination.exists():
            destination.unlink()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save resume information",
        )

    return result
