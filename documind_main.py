"""
DocuMind AI - Advanced Document Intelligence System
Advanced Document Intelligence System with cloud vector database, reranking, and citations
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    """Create the DocuMind AI application"""
    app = FastAPI(
        title="DocuMind AI - Advanced Document Intelligence",
        description="Advanced Document Intelligence System with cloud vector database, reranking, and citations",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "DocuMind AI - Advanced Document Intelligence System",
            "frontend": "/api/",
            "docs": "/docs",
            "health": "/health"
        }
    
    # Simple health check that doesn't depend on services
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "system": "documind_ai",
            "message": "Service is running"
        }
    
    # Try to include API routes, but don't fail if services aren't available
    try:
        from services.routes import router as api_router
        app.include_router(api_router)
        print("✅ API routes loaded successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not load API routes: {e}")
        print("📝 Running in basic mode - some features may be unavailable")
        
        # Add a basic API endpoint for testing
        @app.get("/api/test")
        async def test_endpoint():
            return {"message": "Basic API mode - full services not available"}
    
    # Mount frontend
    try:
        app.mount("/api", StaticFiles(directory="frontend", html=True), name="frontend")
        print("✅ Frontend mounted successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not mount frontend: {e}")
    
    return app

# Create the DocuMind AI application
app = create_app()
print("🏆 Starting DocuMind AI - Advanced Document Intelligence System")

if __name__ == "__main__":
    # Get configuration from environment (Railway-compliant)
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    # Railway-specific environment detection
    is_railway = os.getenv("RAILWAY_ENVIRONMENT") is not None
    if is_railway:
        print("🚂 Running on Railway")
        # Disable reload in production
        reload = False
    
    print(f"🌐 Server starting on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔗 DocuMind Frontend: http://{host}:{port}/api/")
    print(f"❤️ Health Check: http://{host}:{port}/health")
    
    try:
        uvicorn.run(
            "documind_main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        # Exit with error code for Railway
        exit(1)
