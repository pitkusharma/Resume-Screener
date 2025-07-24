import os
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Custom import
from app.core.config import WHITELISTED_IPS


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    """
    Middleware that allows requests only from whitelisted IPs.

    Checks the client IP (or X-Forwarded-For if present) against WHITELISTED_IPS.
    Blocks requests with a 403 status if the IP is not allowed.
    """
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host

        # If behind proxy
        real_ip = request.headers.get("X-Forwarded-For", client_ip)

        if real_ip not in WHITELISTED_IPS:
            return JSONResponse(status_code=403, content={
                "message": "Access denied: IP not allowed",
                "status": False,
                "data": None
            })

        return await call_next(request)
