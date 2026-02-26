from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.core.redis import init_redis, close_redis
from app.api.v1.endpoints.certificate import router as certificate_router
from app.api.v1.endpoints.template import router as template_router
from app.api.v1.endpoints.certificate_type import router as certificate_type_router
from app.core.exceptions import CertificateNotFoundError
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware


# Static Origin Value
origin = [
    "http://localhost:3000",  # React/Next.js default
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Vite default
    "https://hrd-center.com",  # Your production domain
    "https://verify.kshrd.app",
]

# Configure logging to see errors in your terminal/logs
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for initializing Redis connections on application startup
    and closing them on application shutdown.
    """
    # Startup
    print("Starting up...")
    await init_redis()

    from app.core.redis import redis_client

    await redis_client.set("connection_test", "ready")  # Force a write
    val = await redis_client.get("connection_test")
    print(f"✅ Redis Test: {val}")  # Should print 'ready'

    yield

    # Shutdown
    print("Shutting down...")
    await close_redis()


app = FastAPI(
    title="KSHRD Certificate Verify Service",
    version="0.0.1",
    description="A FastAPI-based certificate service for verifying KSHRD certificate",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.exception_handler(CertificateNotFoundError)
async def certificate_not_found_handler(
    request: Request, exc: CertificateNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": exc.message,
            "code": exc.code,
        },
    )


app.include_router(
    certificate_router, prefix="/api/v1/certificate", tags=["Certificates"]
)

app.include_router(
    template_router, prefix="/api/v1/templates", tags=["Templates"]
)

app.include_router(
    certificate_type_router, prefix="/api/v1/certificate-types", tags=["Certificate Types"]
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    # 1. Log the actual error for the developer
    logger.error(f"Unhandled error: {exc}", exc_info=True)

    # 2. Return a clean, consistent JSON to the client
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )