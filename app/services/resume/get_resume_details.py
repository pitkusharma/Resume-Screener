from bson import ObjectId
from fastapi import HTTPException

# Custom imports
from app.core.database import resumes_collection


async def get_resume_by_id(resume_id: str) -> dict:
    """
    Fetch resume details by its ID from MongoDB.

    Args:
        resume_id (str): The unique resume identifier (MongoDB ObjectId as string).

    Returns:
        dict: Resume details with 'id' as string (ObjectId converted).

    Raises:
        HTTPException:
            - 400: If the resume_id is invalid.
            - 404: If no resume is found for the given ID.
            - 500: For unexpected database or server errors.
    """
    try:
        # Validate ObjectId
        if not ObjectId.is_valid(resume_id):
            raise HTTPException(status_code=400, detail="Invalid resume ID format")

        resume = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")

        # Convert MongoDB ObjectId to string
        resume["id"] = str(resume["_id"])
        del resume["_id"]
        return resume

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching resume: {str(e)}")
