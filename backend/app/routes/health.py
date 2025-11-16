from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is running successfully"
    }

@router.get("/")
def root():
    """Root endpoint"""
    return {
        "name": "Immobilier API",
        "version": "0.0.1",
        "description": "API for managing real estate properties"
    }
