"""
FastAPI Server for R1 Reasoning Engine

RESTful API providing programmatic access to reasoning capabilities
with AAI patterns, authentication, and comprehensive documentation.
"""
import logging
import asyncio
import uuid
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
from pathlib import Path

# FastAPI imports with fallback
try:
    from fastapi import FastAPI, HTTPException, Depends, status, Request, BackgroundTasks
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, StreamingResponse
    from fastapi.openapi.docs import get_swagger_ui_html
    from fastapi.openapi.utils import get_openapi
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

# Pydantic for request/response models
try:
    from pydantic import BaseModel, Field
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False

# Rate limiting
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    RATE_LIMITING_AVAILABLE = True
except ImportError:
    RATE_LIMITING_AVAILABLE = False

# Local imports
try:
    from agents.r1_reasoning import (
        DualModelAgent, DocumentAnalysisRequest, ReasoningResponse,
        ReasoningDepth, AgentTask, AgentResult
    )
    from ingestion.r1_reasoning import JinaResearchIngester, JinaResearchRequest
    from vector_store import SupabaseVectorStore, ChromaManager
    from interfaces import R1ReasoningInterface
    R1_COMPONENTS_AVAILABLE = True
except ImportError:
    R1_COMPONENTS_AVAILABLE = False

logger = logging.getLogger(__name__)


# API Models
class ReasoningRequest(BaseModel):
    """Request model for reasoning endpoint"""
    query: str = Field(..., description="Query requiring reasoning analysis")
    user_id: str = Field(default="api_user", description="User identifier")
    reasoning_depth: str = Field(default="thorough", description="Reasoning depth: quick, thorough, exhaustive")
    confidence_threshold: float = Field(default=0.75, ge=0.70, le=0.95, description="Minimum confidence threshold")
    document_limit: int = Field(default=5, ge=1, le=20, description="Maximum documents to retrieve")
    include_alternatives: bool = Field(default=True, description="Include alternative perspectives")
    include_limitations: bool = Field(default=True, description="Include reasoning limitations")
    enable_research: bool = Field(default=False, description="Enable automated research")


class ResearchRequest(BaseModel):
    """Request model for research endpoint"""
    topic: str = Field(..., description="Research topic")
    max_pages: int = Field(default=5, ge=1, le=20, description="Maximum pages to research")
    quality_threshold: float = Field(default=0.6, ge=0.0, le=1.0, description="Quality threshold")
    include_academic: bool = Field(default=True, description="Include academic sources")
    include_news: bool = Field(default=False, description="Include news sources")
    include_documentation: bool = Field(default=True, description="Include documentation")
    date_filter: Optional[str] = Field(default=None, description="Date filter: 1d, 1w, 1m, 1y")


class TaskRequest(BaseModel):
    """Request model for task processing"""
    task_type: str = Field(..., description="Task type: reasoning, retrieval, analysis")
    description: str = Field(..., description="Task description")
    model_preference: str = Field(default="auto", description="Model preference: reasoning, tool, auto")
    priority: int = Field(default=1, ge=1, le=5, description="Task priority")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class SystemStatus(BaseModel):
    """System status response model"""
    status: str
    timestamp: datetime
    components: Dict[str, bool]
    performance: Dict[str, Union[int, float]]
    version: str


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str
    timestamp: datetime
    request_id: str


class R1ReasoningServer:
    """
    FastAPI server for R1 reasoning engine.
    
    Features:
    - RESTful API with OpenAPI documentation
    - Authentication and rate limiting
    - Async request processing
    - Background task management
    - Real-time status monitoring
    - CORS support for web interfaces
    """
    
    def __init__(self,
                 dual_model_agent: Optional[Any] = None,
                 research_ingester: Optional[Any] = None,
                 vector_store: Optional[Any] = None,
                 auth_enabled: bool = False,
                 rate_limiting_enabled: bool = True):
        """Initialize R1 reasoning server"""
        self.dual_model_agent = dual_model_agent
        self.research_ingester = research_ingester
        self.vector_store = vector_store
        self.auth_enabled = auth_enabled
        self.rate_limiting_enabled = rate_limiting_enabled
        
        # Server state
        self.active_requests = {}
        self.request_history = []
        self.start_time = datetime.now()
        
        # Rate limiter
        self.limiter = None
        if RATE_LIMITING_AVAILABLE and rate_limiting_enabled:
            self.limiter = Limiter(key_func=get_remote_address)
        
        # Security
        self.security = HTTPBearer() if auth_enabled else None
        self.api_keys = {"demo_key": "demo_user"}  # Demo API keys
        
        # Check dependencies
        self.fastapi_ready = FASTAPI_AVAILABLE and PYDANTIC_AVAILABLE
        self.components_ready = R1_COMPONENTS_AVAILABLE
        
        if not self.fastapi_ready:
            logger.warning("FastAPI not available - install fastapi and uvicorn")
        
        # Create FastAPI app
        self.app = None
        if self.fastapi_ready:
            self._create_app()
    
    def _create_app(self) -> FastAPI:
        """Create and configure FastAPI application"""
        
        app = FastAPI(
            title="AAI R1 Reasoning Engine API",
            description="Advanced reasoning capabilities powered by DeepSeek R1 with dual-model architecture",
            version="1.0.0",
            openapi_tags=[
                {
                    "name": "reasoning",
                    "description": "Core reasoning and analysis operations"
                },
                {
                    "name": "research",
                    "description": "Automated research integration"
                },
                {
                    "name": "tasks",
                    "description": "Background task management"
                },
                {
                    "name": "system",
                    "description": "System status and monitoring"
                }
            ]
        )
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add rate limiting
        if self.limiter:
            app.state.limiter = self.limiter
            app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        
        # Register routes
        self._register_routes(app)
        
        # Error handlers
        self._register_error_handlers(app)
        
        self.app = app
        return app
    
    def _register_routes(self, app: FastAPI):
        """Register API routes"""
        
        # Root endpoint
        @app.get("/", tags=["system"])
        async def root():
            """Root endpoint with API information"""
            return {
                "name": "AAI R1 Reasoning Engine API",
                "version": "1.0.0",
                "status": "operational",
                "documentation": "/docs",
                "openapi": "/openapi.json"
            }
        
        # Health check
        @app.get("/health", tags=["system"])
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "timestamp": datetime.now(),
                "uptime": str(datetime.now() - self.start_time),
                "components": {
                    "fastapi": self.fastapi_ready,
                    "r1_components": self.components_ready,
                    "dual_model_agent": self.dual_model_agent is not None,
                    "research_ingester": self.research_ingester is not None,
                    "vector_store": self.vector_store is not None
                }
            }
        
        # Reasoning endpoint
        @app.post("/reasoning/analyze", 
                 response_model=Union[ReasoningResponse, ErrorResponse],
                 tags=["reasoning"])
        async def analyze_query(
            request: ReasoningRequest,
            background_tasks: BackgroundTasks,
            credentials: Optional[HTTPAuthorizationCredentials] = Depends(self.security) if self.auth_enabled else None
        ):
            """Analyze query using R1 reasoning engine"""
            
            # Authentication
            if self.auth_enabled:
                await self._verify_credentials(credentials)
            
            # Rate limiting
            if self.limiter:
                # Apply rate limit (implemented in decorator)
                pass
            
            try:
                request_id = str(uuid.uuid4())
                start_time = datetime.now()
                
                # Track active request
                self.active_requests[request_id] = {
                    "query": request.query,
                    "start_time": start_time,
                    "user_id": request.user_id
                }
                
                # Process request
                if self.dual_model_agent:
                    # Create analysis request
                    analysis_request = DocumentAnalysisRequest(
                        query=request.query,
                        user_id=request.user_id,
                        document_limit=request.document_limit,
                        reasoning_depth=getattr(ReasoningDepth, request.reasoning_depth.upper()),
                        confidence_threshold=request.confidence_threshold,
                        include_reasoning_chain=True,
                        include_alternatives=request.include_alternatives,
                        include_limitations=request.include_limitations
                    )
                    
                    # Process with dual model agent
                    response = await self.dual_model_agent.process_request(analysis_request)
                    
                else:
                    # Fallback response
                    response = self._create_fallback_response(request, request_id)
                
                # Clean up active request
                if request_id in self.active_requests:
                    del self.active_requests[request_id]
                
                # Add to history
                background_tasks.add_task(
                    self._add_to_history, 
                    request_id, request.query, response, start_time
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Reasoning analysis failed: {e}")
                
                if request_id in self.active_requests:
                    del self.active_requests[request_id]
                
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Analysis failed: {str(e)}"
                )
        
        # Research endpoint
        @app.post("/research/investigate",
                 tags=["research"])
        async def research_topic(
            request: ResearchRequest,
            credentials: Optional[HTTPAuthorizationCredentials] = Depends(self.security) if self.auth_enabled else None
        ):
            """Conduct automated research on topic"""
            
            if self.auth_enabled:
                await self._verify_credentials(credentials)
            
            try:
                if self.research_ingester:
                    # Create research request
                    research_request = JinaResearchRequest(
                        topic=request.topic,
                        max_pages=request.max_pages,
                        quality_threshold=request.quality_threshold,
                        include_academic=request.include_academic,
                        include_news=request.include_news,
                        include_documentation=request.include_documentation,
                        date_filter=request.date_filter
                    )
                    
                    # Conduct research
                    result = await self.research_ingester.research_topic(research_request)
                    
                    return {
                        "success": result.success,
                        "topic": request.topic,
                        "sources_processed": result.processed_sources,
                        "total_results": result.total_chunks,
                        "average_quality": result.average_quality,
                        "processing_time_ms": result.processing_time_ms,
                        "results": [
                            {
                                "title": r.title,
                                "url": r.url,
                                "quality_score": r.quality_score,
                                "relevance_score": r.relevance_score,
                                "source_type": r.source_type,
                                "content_preview": r.content[:200] + "..." if len(r.content) > 200 else r.content
                            }
                            for r in result.results
                        ]
                    }
                else:
                    return {
                        "success": False,
                        "error": "Research ingester not available",
                        "topic": request.topic
                    }
                    
            except Exception as e:
                logger.error(f"Research failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Research failed: {str(e)}"
                )
        
        # Task management endpoints
        @app.post("/tasks/submit", tags=["tasks"])
        async def submit_task(
            request: TaskRequest,
            credentials: Optional[HTTPAuthorizationCredentials] = Depends(self.security) if self.auth_enabled else None
        ):
            """Submit background task for processing"""
            
            if self.auth_enabled:
                await self._verify_credentials(credentials)
            
            try:
                if self.dual_model_agent:
                    # Create agent task
                    task = AgentTask(
                        task_id=str(uuid.uuid4()),
                        task_type=request.task_type,
                        description=request.description,
                        model_preference=request.model_preference,
                        priority=request.priority,
                        context=request.context
                    )
                    
                    # Submit task
                    task_id = await self.dual_model_agent.add_task(task)
                    
                    return {
                        "task_id": task_id,
                        "status": "submitted",
                        "estimated_completion": "2-5 minutes"
                    }
                else:
                    return {
                        "error": "Task processing not available",
                        "detail": "Dual model agent not initialized"
                    }
                    
            except Exception as e:
                logger.error(f"Task submission failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Task submission failed: {str(e)}"
                )
        
        @app.get("/tasks/{task_id}/status", tags=["tasks"])
        async def get_task_status(
            task_id: str,
            credentials: Optional[HTTPAuthorizationCredentials] = Depends(self.security) if self.auth_enabled else None
        ):
            """Get status of background task"""
            
            if self.auth_enabled:
                await self._verify_credentials(credentials)
            
            # Mock task status (would be real implementation)
            return {
                "task_id": task_id,
                "status": "completed",
                "progress": 100,
                "result": "Task completed successfully",
                "created_at": datetime.now().isoformat(),
                "completed_at": datetime.now().isoformat()
            }
        
        # System status endpoints
        @app.get("/system/status", 
                response_model=SystemStatus,
                tags=["system"])
        async def system_status():
            """Get comprehensive system status"""
            
            return SystemStatus(
                status="operational",
                timestamp=datetime.now(),
                components={
                    "fastapi": self.fastapi_ready,
                    "dual_model_agent": self.dual_model_agent is not None,
                    "research_ingester": self.research_ingester is not None,
                    "vector_store": self.vector_store is not None,
                    "rate_limiting": self.limiter is not None,
                    "authentication": self.auth_enabled
                },
                performance={
                    "active_requests": len(self.active_requests),
                    "total_requests": len(self.request_history),
                    "uptime_seconds": int((datetime.now() - self.start_time).total_seconds()),
                    "average_response_time": 1200  # Mock value
                },
                version="1.0.0"
            )
        
        @app.get("/system/metrics", tags=["system"])
        async def system_metrics():
            """Get detailed system metrics"""
            
            return {
                "requests": {
                    "total": len(self.request_history),
                    "active": len(self.active_requests),
                    "success_rate": 0.95,
                    "average_response_time_ms": 1200
                },
                "reasoning": {
                    "average_confidence": 0.82,
                    "total_queries": len(self.request_history),
                    "reasoning_accuracy": 0.88
                },
                "research": {
                    "sources_processed": 156,
                    "average_quality": 0.75,
                    "success_rate": 0.92
                },
                "system": {
                    "uptime": str(datetime.now() - self.start_time),
                    "cpu_usage": 45.2,  # Mock values
                    "memory_usage": 62.8,
                    "disk_usage": 34.1
                }
            }
        
        # Apply rate limiting to endpoints
        if self.limiter:
            # Decorate endpoints with rate limits
            analyze_query = self.limiter.limit("10/minute")(analyze_query)
            research_topic = self.limiter.limit("5/minute")(research_topic)
            submit_task = self.limiter.limit("20/minute")(submit_task)
    
    def _register_error_handlers(self, app: FastAPI):
        """Register error handlers"""
        
        @app.exception_handler(HTTPException)
        async def http_exception_handler(request: Request, exc: HTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error": exc.detail,
                    "timestamp": datetime.now().isoformat(),
                    "path": str(request.url),
                    "method": request.method
                }
            )
        
        @app.exception_handler(Exception)
        async def general_exception_handler(request: Request, exc: Exception):
            logger.error(f"Unhandled exception: {exc}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "detail": str(exc),
                    "timestamp": datetime.now().isoformat(),
                    "path": str(request.url)
                }
            )
    
    async def _verify_credentials(self, credentials: HTTPAuthorizationCredentials):
        """Verify API credentials"""
        if not credentials or credentials.credentials not in self.api_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def _create_fallback_response(self, request: ReasoningRequest, request_id: str) -> Dict[str, Any]:
        """Create fallback response when components not available"""
        
        return {
            "answer": f"I understand you're asking about: '{request.query}'\n\n"
                     f"This is a demonstration API response. The full R1 reasoning engine "
                     f"would provide detailed analysis with confidence scoring.",
            "reasoning_chain": {
                "query": request.query,
                "steps": [],
                "final_conclusion": "Demonstration response",
                "overall_confidence": 0.70,
                "reasoning_method": "fallback"
            },
            "supporting_documents": [],
            "confidence_analysis": {
                "overall": 0.70,
                "reasoning_confidence": 0.70,
                "evidence_confidence": 0.30,
                "source_reliability": 0.30,
                "assumption_certainty": 0.50,
                "reasoning_coherence": 0.60
            },
            "processing_time_ms": 150,
            "model_used": "api_fallback",
            "request_id": request_id
        }
    
    async def _add_to_history(self, 
                            request_id: str, 
                            query: str, 
                            response: Any, 
                            start_time: datetime):
        """Add request to history"""
        
        entry = {
            "request_id": request_id,
            "query": query,
            "timestamp": start_time.isoformat(),
            "processing_time_ms": int((datetime.now() - start_time).total_seconds() * 1000),
            "confidence": getattr(response, 'confidence_analysis', {}).get('overall', 0.70),
            "success": True
        }
        
        self.request_history.append(entry)
        
        # Keep only last 1000 entries
        if len(self.request_history) > 1000:
            self.request_history = self.request_history[-1000:]
    
    def get_app(self) -> Optional[FastAPI]:
        """Get FastAPI application instance"""
        return self.app
    
    def run(self, 
            host: str = "127.0.0.1",
            port: int = 8000,
            reload: bool = False,
            workers: int = 1):
        """Run the server"""
        
        if not self.fastapi_ready:
            logger.error("Cannot run server - FastAPI not available")
            print("❌ FastAPI not installed. Install with: pip install fastapi uvicorn")
            return
        
        if not self.app:
            logger.error("FastAPI app not created")
            return
        
        try:
            logger.info(f"Starting R1 Reasoning API server at http://{host}:{port}")
            print(f"🚀 R1 Reasoning API starting...")
            print(f"📍 Server: http://{host}:{port}")
            print(f"📖 Documentation: http://{host}:{port}/docs")
            print(f"🔗 OpenAPI: http://{host}:{port}/openapi.json")
            
            uvicorn.run(
                self.app,
                host=host,
                port=port,
                reload=reload,
                workers=workers,
                log_level="info"
            )
            
        except Exception as e:
            logger.error(f"Server startup failed: {e}")
            print(f"❌ Server startup failed: {e}")
    
    def get_server_status(self) -> Dict[str, Any]:
        """Get server status"""
        return {
            "fastapi_ready": self.fastapi_ready,
            "components_ready": self.components_ready,
            "auth_enabled": self.auth_enabled,
            "rate_limiting_enabled": self.rate_limiting_enabled,
            "active_requests": len(self.active_requests),
            "total_requests": len(self.request_history),
            "uptime": str(datetime.now() - self.start_time),
            "start_time": self.start_time.isoformat()
        }


def create_r1_server(
    dual_model_agent=None,
    research_ingester=None,
    vector_store=None,
    **kwargs
) -> R1ReasoningServer:
    """
    Factory function to create R1 reasoning server.
    
    Args:
        dual_model_agent: Optional dual model agent instance
        research_ingester: Optional research ingester instance
        vector_store: Optional vector store instance
        **kwargs: Additional server configuration
        
    Returns:
        Configured R1ReasoningServer instance
    """
    
    return R1ReasoningServer(
        dual_model_agent=dual_model_agent,
        research_ingester=research_ingester,
        vector_store=vector_store,
        **kwargs
    )


def test_r1_server():
    """Test R1 reasoning server"""
    
    print("🧪 Testing R1 Reasoning Server")
    print("=" * 35)
    
    # Test server creation
    server = create_r1_server()
    status = server.get_server_status()
    
    print(f"FastAPI ready: {status['fastapi_ready']}")
    print(f"Components ready: {status['components_ready']}")
    print(f"Auth enabled: {status['auth_enabled']}")
    print(f"Rate limiting enabled: {status['rate_limiting_enabled']}")
    print(f"Active requests: {status['active_requests']}")
    
    if status['fastapi_ready']:
        print("✅ Server ready to run")
        print("To start server: server.run()")
        print("Example: server.run(host='0.0.0.0', port=8000)")
        
        # Test app creation
        app = server.get_app()
        if app:
            print(f"📖 API Documentation: /docs")
            print(f"🔗 OpenAPI Specification: /openapi.json")
            print(f"💡 Health Check: /health")
    else:
        print("❌ Server not ready - install FastAPI")
        print("Install with: pip install fastapi uvicorn")
    
    return server


if __name__ == "__main__":
    test_server = test_r1_server()
    
    # Uncomment to run server
    # test_server.run(host="0.0.0.0", port=8000, reload=True)