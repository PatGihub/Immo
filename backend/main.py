from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.config import settings
from app.database import engine, Base
from app.routes import health, auth
from app.routes import properties
from app.middleware import LoggingMiddleware
from app.logging_config import logger, setup_logging

# Setup logging
setup_logging()
logger.info("=" * 50)
logger.info("Starting Immobilier API")
logger.info("=" * 50)

# Create tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created/verified")

# Initialize app
app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug
)

# Add CORS middleware FIRST (must be added first)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Accept", "Origin"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(properties.router)

logger.info(f"CORS allowed origins: {settings.allowed_origins}")
logger.info("All routers included")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        reload_excludes=["logs", "*.log", "__pycache__"]
    )
