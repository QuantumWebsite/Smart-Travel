from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.services import init_services
from app.core.logging_config import configure_logging
from app.middleware.cors_logger import CORSLoggerMiddleware

# Set up logging
configure_logging()
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENVIRONMENT} mode")
    logger.info("Initializing services...")
    await init_services.initialize_services()
    logger.info("All services initialized successfully")
    yield
    logger.info("Shutting down services...")
    await init_services.cleanup_services()
    logger.info("Shutdown complete")
    
    
# Initialize FastAPI app
app = FastAPI(
    title="Smart Travel Deals Planner API",
    description="API for finding the best travel deals with AI-powered recommendations",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS logger middleware first (before CORS middleware)
app.add_middleware(CORSLoggerMiddleware)
logger.info("Added CORS logger middleware")

# Configure CORS
if settings.BACKEND_CORS_ORIGINS:
    logger.info(f"Setting up CORS with origins: {settings.BACKEND_CORS_ORIGINS}")
    # Debug CORS settings
    cors_origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    logger.info(f"CORS origins after conversion: {cors_origins}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_origin_regex=None,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],  # Allow all headers to simplify debugging
        expose_headers=["Content-Length", "Content-Range"],
        max_age=600,  # Cache preflight requests for 10 minutes
    )

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    """
    Health check endpoint
    """
    logger.info("Health check endpoint accessed")
    return {
        "status": "ok", 
        "message": f"{settings.APP_NAME} is running",
        "environment": settings.APP_ENVIRONMENT,
        "version": "0.1.0"
    }

@app.options("/cors-test")
@app.get("/cors-test")
def test_cors():
    """
    Endpoint to test CORS configuration
    """
    logger.info("CORS test endpoint accessed")
    return {
        "cors_configured": True,
        "allowed_origins": settings.BACKEND_CORS_ORIGINS
    }