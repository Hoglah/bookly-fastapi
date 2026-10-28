from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)
        processing_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port}- {request.method} -  {request.url} - {response.status_code} completed after {processing_time}s"

        print(message)

        return response

    @app.middleware("http")
    async def authorization(request: Request, call_next):
        # 1. Define all paths that should remain accessible without a login header
        open_endpoints = [
            "/api/v1/docs",
            "/api/v1/redoc",
            "/openapi.json",
            "/api/v1/auth/signup",  # Allow users to register
            "/api/v1/auth/login",  # Allow users to login
        ]

        # 2. Check if the current incoming request matches an open endpoint
        # Using .startswith handles any route variations or trailing slashes
        if any(request.url.path.startswith(path) for path in open_endpoints):
            return await call_next(request)

        # 3. Secure all other endpoints
        if "Authorization" not in request.headers:
            return JSONResponse(
                content={
                    "message": "Unauthorized",
                    "resolution": "Please provide right credentials",
                },
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        response = await call_next(request)
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])
