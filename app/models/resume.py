from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime


class Resume(BaseModel):
    filename: str
    filepath: str
    text: Optional[str] = None  # Extracted text after parsing
    metadata: Optional[Dict[str, Any]] = None  # Extracted resume metadata
    step: Literal["uploaded", "text-parsed", "metadata-parsed", "embedded"] = "uploaded"
    status: bool = True  # True = success, False = failure
    reason: Optional[str] = None  # Reason for failure, if any
    uploaded_at: datetime = Field(default_factory=datetime.now)

class ResumeSearchRequest(BaseModel):
    description: str
    top_k: int = 5

class ResumeDetailResponse(BaseModel):
    id: str
    filename: str
    metadata: Optional[Dict[str, Any]] = None  # Extracted resume metadata
    uploaded_at: datetime = Field(default_factory=datetime.now)
    model_config = {
        "json_encoders": {datetime: lambda v: v.isoformat()},
    }
