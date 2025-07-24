from pydantic import BaseModel
from typing import Any, Optional

class StandardResponse(BaseModel):
    status: bool = True
    message: str = "Success"
    data: Optional[Any] = None
