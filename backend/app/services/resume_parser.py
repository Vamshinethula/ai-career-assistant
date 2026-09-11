import fitz
from pathlib import Path


def extract_text_from_pdf(file_path: str) -> str:
    # Close the filesystem handle before parsing, including malformed PDFs.
    # This allows upload cleanup to remove the file on Windows after an error.
    pdf_bytes = Path(file_path).read_bytes()
    with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
        return "".join(page.get_text() for page in document).strip()
