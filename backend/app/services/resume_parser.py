import fitz
from pathlib import Path
from app.config import MAX_RESUME_PAGES


class InvalidResumePDF(ValueError):
    pass


class ResumePageLimitExceeded(ValueError):
    pass


def extract_text_from_pdf(file_path: str) -> str:
    # Close the filesystem handle before parsing, including malformed PDFs.
    # This allows upload cleanup to remove the file on Windows after an error.
    pdf_bytes = Path(file_path).read_bytes()
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            if not document.is_pdf or document.needs_pass:
                raise InvalidResumePDF('Upload a readable PDF without password protection')
            if document.page_count > MAX_RESUME_PAGES:
                raise ResumePageLimitExceeded(f'Resumes may contain at most {MAX_RESUME_PAGES} pages')
            if document.page_count == 0:
                raise InvalidResumePDF('The PDF has no pages')
            return "".join(page.get_text() for page in document).strip()
    except fitz.FileDataError as error:
        raise InvalidResumePDF('The uploaded PDF is empty or unreadable') from error
