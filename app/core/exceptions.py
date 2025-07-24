from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler for FastAPI HTTPException.

    Returns a JSON response with a consistent structure:
    {
        "status": False,
        "message": <error detail>,
        "data": None
    }

    Args:
        request (Request): Incoming HTTP request.
        exc (HTTPException): The raised HTTP exception.

    Returns:
        JSONResponse: Formatted error response with the original status code.
    """
    return JSONResponse(
        content={
            "status": False,
            "message": exc.detail,
            "data": None
        },
        status_code=exc.status_code
    )
