from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException

# Models
from app.models.resume import ResumeSearchRequest, ResumeDetailResponse
from app.models.generic import StandardResponse

# Services
from app.services.resume.resume_upload import handle_resume_upload
from app.services.vector_store.search_resumes import perform_resume_search
from app.services.resume.get_resume_details import get_resume_by_id


resume_router = APIRouter()

@resume_router.post("/upload-resume", response_model=StandardResponse)
async def upload_resume(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    upload_response = await handle_resume_upload(file, background_tasks)

    return StandardResponse(
        status=True,
        message="Resume uploaded and processing started.",
        data=upload_response
    )

@resume_router.post("/search", response_model=StandardResponse)
async def search_resume(payload: ResumeSearchRequest):
    resume_list = await perform_resume_search(payload.description, payload.top_k)

    return StandardResponse(
        status=True,
        message="Similar resumes fetched successfully.",
        data=resume_list
    )

@resume_router.get("/resumes/{resume_id}", response_model=StandardResponse)
async def get_resume(resume_id: str):
    resume_details = await get_resume_by_id(resume_id)
    response_data = ResumeDetailResponse.model_validate(resume_details)

    return StandardResponse(
        status=True,
        message="Resume details fetched successfully.",
        data=response_data
    )
