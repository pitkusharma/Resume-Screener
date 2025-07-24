from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from app.services.vector_store.vector_store import vector_store


async def perform_resume_search(job_desc: str, top_k: int = 5):
    """
    Perform a similarity search on stored resumes based on job description.

    Args:
        job_desc (str): The job description text.
        top_k (int, optional): Number of top matching resumes to return. Default is 5.

    Returns:
        List[Dict]: A list of matching resumes with `resume_id`, `filename`, and `score`.

    Raises:
        HTTPException: If vector store is not initialized, request is invalid, or search fails.
    """
    if vector_store is None:
        raise HTTPException(status_code=503, detail="Vector store not initialized")

    try:
        results = await run_in_threadpool(
            vector_store.similarity_search_with_score,
            job_desc,
            k=top_k
        )

        return [
            {
                "resume_id": doc.metadata.get("resume_id") or doc.id,
                "filename": doc.metadata.get("filename"),
                "score": round(score * 100, 2)
            }
            for doc, score in results
        ]

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid search request: {str(ve)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error during resume search: {str(e)}")
