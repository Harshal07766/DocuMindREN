"""
DocuMind AI - Simple Version for Render Deployment
This version runs without external dependencies to avoid early exit errors
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
            "health": "/health",
            "status": "running"
        }
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "system": "documind_ai",
            "message": "Service is running",
            "version": "2.0.0"
        }
    
    # Basic API endpoints
    @app.get("/api/")
    async def api_root():
        return {
            "message": "DocuMind AI API",
            "status": "running",
            "endpoints": {
                "health": "/api/health",
                "test": "/api/test",
                "upload": "/api/upload",
                "query": "/api/query"
            }
        }
    
    @app.get("/api/health")
    async def api_health():
        return {
            "status": "healthy",
            "message": "API is running",
            "mode": "basic"
        }
    
    @app.get("/api/test")
    async def test_endpoint():
        return {
            "message": "DocuMind AI is working!",
            "status": "success",
            "note": "Running in basic mode - full services require API keys"
        }
    
    @app.post("/api/upload")
    async def upload_endpoint():
        return {
            "message": "Upload endpoint ready",
            "status": "basic_mode",
            "note": "Full upload functionality requires API keys configuration"
        }
    
    @app.post("/api/query")
    async def query_endpoint():
        return {
            "message": "Query endpoint ready",
            "status": "basic_mode",
            "note": "Full query functionality requires API keys configuration"
        }
    
    # Mount frontend
    try:
        app.mount("/api", StaticFiles(directory="frontend", html=True), name="frontend")
        print("✅ Frontend mounted successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not mount frontend: {e}")
    
    return app

# Create the DocuMind AI application
app = create_app()
print("🏆 Starting DocuMind AI - Simple Version")

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    print(f"🌐 Server starting on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔗 DocuMind Frontend: http://{host}:{port}/api/")
    print(f"❤️ Health Check: http://{host}:{port}/health")
    
    try:
        uvicorn.run(
            "simple_main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        exit(1)
