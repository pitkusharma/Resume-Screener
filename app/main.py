from fastapi import FastAPI, HTTPException
from app.core.exceptions import http_exception_handler

# Middlewares
from app.core.middleware import IPWhitelistMiddleware

# Routers
from app.routes.resume_routes import resume_router

app = FastAPI(title="Resume Screener API")

# Include middlewares
app.add_middleware(IPWhitelistMiddleware)

@app.get("/")
def root():
    return {"message": "Resume Screener API is running"}

# Include routes
app.include_router(resume_router, prefix="/api", tags=["Resume Upload"])

# Exception handler
app.add_exception_handler(HTTPException, http_exception_handler)
