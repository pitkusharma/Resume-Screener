import os
import time
from fastapi import UploadFile, HTTPException, BackgroundTasks
from bson import ObjectId

# Internal Imports
from app.core.database import resumes_collection
from app.core.config import UPLOAD_DIR, MAX_FILE_SIZE_MB
from app.models.resume import Resume
from app.services.resume.resume_parse import extract_text_from_pdf
from app.services.vector_store.store_resume import add_resume
from app.services.llm.resume_llm_parser import extract_resume_metadata


async def handle_resume_upload(file: UploadFile, background_tasks: BackgroundTasks):
    """
    Handles resume upload, validates the file, saves it, inserts metadata into DB,
    and triggers background parsing + embedding.

    Args:
        file (UploadFile): PDF resume file.
        background_tasks (BackgroundTasks): FastAPI background task handler.

    Returns:
        dict: Contains `id` (resume ID) and `filename`.

    Raises:
        HTTPException: For invalid file, size limit exceeded, DB or file errors.
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Read file content
        content = await file.read()

        # Validate size
        file_size_mb = len(content) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            raise HTTPException(status_code=400, detail=f"File size exceeds {MAX_FILE_SIZE_MB} MB limit")

        # Save file
        timestamp = int(time.time())
        file_name = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        try:
            with open(file_path, "wb") as f:
                f.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

        # Create Resume object
        resume = Resume(filename=file_name, filepath=file_path)

        # Insert into DB
        try:
            result = await resumes_collection.insert_one(resume.model_dump())
            resume_id = str(result.inserted_id)
        except Exception as e:
            # Rollback file if DB insert fails
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        # Schedule background task
        background_tasks.add_task(parse_and_embed_resume, resume_id, file_path, file_name)

        return {
            "id": resume_id,
            "filename": file_name,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def parse_and_embed_resume(resume_id: str, file_path: str, file_name: str):
    """
    Background task: Extract text, parse metadata, and embed resume into vector DB.

    Args:
        resume_id (str): MongoDB ID of the resume.
        file_path (str): Path to the uploaded resume file.
        file_name (str): Name of the uploaded file.
    """
    try:
        # STEP 1: Extract text
        text = await extract_text_from_pdf(file_path)
        await resumes_collection.update_one(
            {"_id": ObjectId(resume_id)},
            {"$set": {"text": text, "step": "text-parsed"}}
        )

        # STEP 2: Extract metadata
        metadata = await extract_resume_metadata(text)
        await resumes_collection.update_one(
            {"_id": ObjectId(resume_id)},
            {"$set": {"metadata": metadata, "step": "metadata-parsed"}}
        )

        # STEP 3: Embed in Pinecone
        await add_resume(resume_id, text, {"filename": file_name, "filepath": file_path})

        await resumes_collection.update_one(
            {"_id": ObjectId(resume_id)},
            {"$set": {"step": "embedded", "status": True}}
        )

    except Exception as e:
        await resumes_collection.update_one(
            {"_id": ObjectId(resume_id)},
            {"$set": {"status": False, "reason": str(e)}}
        )
