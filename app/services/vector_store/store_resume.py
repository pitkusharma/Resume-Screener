from fastapi.concurrency import run_in_threadpool
from app.services.vector_store.vector_store import vector_store


async def add_resume(resume_id: str, text: str, metadata: dict):
    """
    Add resume text and metadata to the vector store (Pinecone) asynchronously.

    Args:
        resume_id (str): Unique identifier for the resume.
        text (str): Extracted resume text.
        metadata (dict): Metadata for the resume (e.g., filename, filepath).

    Returns:
        bool: True if insertion succeeds, False otherwise.

    Raises:
        HTTPException: If vector store is uninitialized or an error occurs during insertion.
    """
    await run_in_threadpool(
        vector_store.add_texts,
        texts=[text],
        metadatas=[metadata],
        ids=[resume_id]
    )
