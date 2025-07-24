import fitz
import os
from fastapi import HTTPException

async def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file using PyMuPDF (fitz).

    Args:
        file_path (str): The absolute path of the PDF file.

    Returns:
        str: Extracted text from the PDF.

    Raises:
        HTTPException:
            - 404: If the file does not exist.
            - 500: If the PDF cannot be opened or parsed.
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {str(e)}")

    return text.strip()
