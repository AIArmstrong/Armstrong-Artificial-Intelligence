#!/usr/bin/env python3
"""
FastAPI application for Enhanced Repository Analyzer
Provides async endpoints for real-time analysis and collaboration
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
from pydantic import BaseModel, Field

from ..core.cache_manager import CacheManager
from ..core.pattern_registry import PatternRegistry
from ..core.semantic_analyzer import SemanticAnalyzer
from ..core.streaming_walker import StreamingFileWalker
from ..agents.structure_agent import StructureAgent
from ..integrations.openrouter_integration import OpenRouterIntegration

logger = logging.getLogger(__name__)

# Global application state
app_state = {
    'cache_manager': None,
    'pattern_registry': None,
    'semantic_analyzer': None,
    'openrouter_client': None,
    'streaming_walker': None,
    'structure_agent': None,
    'active_connections': set()
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Enhanced Repository Analyzer API")
    
    # Initialize components
    cache_dir = Path('.cache/enhanced-analyzer')
    app_state['cache_manager'] = CacheManager(disk_cache_dir=cache_dir)
    app_state['pattern_registry'] = PatternRegistry()
    
    # Initialize OpenRouter if API key available
    if os.getenv('OPENROUTER_API_KEY'):
        app_state['openrouter_client'] = OpenRouterIntegration()
        app_state['semantic_analyzer'] = SemanticAnalyzer(app_state['openrouter_client'])
    else:
        logger.warning("OpenRouter API key not found - semantic analysis will use basic mode")
        app_state['semantic_analyzer'] = SemanticAnalyzer()
    
    # Initialize agents
    app_state['streaming_walker'] = StreamingFileWalker()
    app_state['structure_agent'] = StructureAgent(
        cache_manager=app_state['cache_manager'],
        pattern_registry=app_state['pattern_registry'],
        semantic_analyzer=app_state['semantic_analyzer']
    )
    
    # Register agents with walker
    app_state['streaming_walker'].register_agent('structure', app_state['structure_agent'])
    
    logger.info("Enhanced Repository Analyzer API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Enhanced Repository Analyzer API")
    
    # Clean up active connections
    for connection in app_state['active_connections']:
        try:
            await connection.close()
        except:
            pass
    
    logger.info("Enhanced Repository Analyzer API shutdown complete")

app = FastAPI(
    title="Enhanced Repository Analyzer",
    description="Intelligent code analysis platform with semantic understanding and real-time integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class AnalysisRequest(BaseModel):
    repository_path: str = Field(..., description="Path to repository")
    analysis_types: List[str] = Field(default=['structure'], description="Types of analysis to perform")
    use_semantic: bool = Field(default=True, description="Enable semantic analysis")
    use_cache: bool = Field(default=True, description="Use caching")
    performance_targets: Optional[Dict[str, float]] = Field(None, description="Performance targets")

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Source code to analyze")
    language: str = Field(..., description="Programming language")
    analysis_type: str = Field(default="semantic", description="Type of analysis")

class StreamingAnalysisRequest(BaseModel):
    repository_path: str = Field(..., description="Path to repository")
    batch_size: int = Field(default=50, description="Files per batch")
    max_concurrent: int = Field(default=4, description="Max concurrent processors")

# Response models
class AnalysisResponse(BaseModel):
    analysis_id: str
    repository_path: str
    success: bool
    execution_time: float
    results: Dict[str, any]
    performance_metrics: Dict[str, float]
    errors: List[str] = []

class HealthResponse(BaseModel):
    status: str
    version: str
    components: Dict[str, str]
    usage_stats: Optional[Dict[str, any]] = None

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Get API health status and component information"""
    components = {
        'cache_manager': 'healthy' if app_state['cache_manager'] else 'unavailable',
        'pattern_registry': 'healthy' if app_state['pattern_registry'] else 'unavailable',
        'semantic_analyzer': 'healthy' if app_state['semantic_analyzer'] else 'unavailable',
        'openrouter_integration': 'healthy' if app_state['openrouter_client'] else 'unavailable'
    }
    
    usage_stats = None
    if app_state['openrouter_client']:
        usage_stats = app_state['openrouter_client'].get_usage_stats()
    
    return HealthResponse(
        status='healthy',
        version='1.0.0',
        components=components,
        usage_stats=usage_stats
    )

# Repository analysis endpoint
@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_repository(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Analyze a repository with specified analysis types"""
    import time
    import uuid
    
    analysis_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        repo_path = Path(request.repository_path)
        if not repo_path.exists():
            raise HTTPException(status_code=404, detail="Repository path not found")
        
        results = {}
        
        # Structure analysis
        if 'structure' in request.analysis_types:
            structure_result = await app_state['structure_agent'].analyze(repo_path)
            results['structure'] = {
                'success': structure_result.success,
                'data': structure_result.data,
                'execution_time': structure_result.execution_time,
                'errors': structure_result.errors
            }
        
        # Additional analysis types can be added here
        
        execution_time = time.time() - start_time
        
        # Calculate performance metrics
        performance_metrics = {
            'total_execution_time': execution_time,
            'cache_hit_rate': 0.0,  # Will be calculated from agents
            'files_per_second': 0.0,
            'memory_usage_mb': 0.0
        }
        
        if app_state['cache_manager']:
            cache_stats = await app_state['cache_manager'].get_statistics()
            performance_metrics['cache_hit_rate'] = cache_stats['performance']['overall_hit_rate']
        
        return AnalysisResponse(
            analysis_id=analysis_id,
            repository_path=str(repo_path),
            success=True,
            execution_time=execution_time,
            results=results,
            performance_metrics=performance_metrics
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return AnalysisResponse(
            analysis_id=analysis_id,
            repository_path=request.repository_path,
            success=False,
            execution_time=time.time() - start_time,
            results={},
            performance_metrics={},
            errors=[str(e)]
        )

# Code analysis endpoint
@app.post("/api/v1/analyze-code")
async def analyze_code(request: CodeAnalysisRequest):
    """Analyze a code snippet"""
    try:
        if not app_state['semantic_analyzer']:
            raise HTTPException(status_code=503, detail="Semantic analyzer not available")
        
        # Analyze with semantic analyzer
        features = await app_state['semantic_analyzer'].analyze_code(
            code=request.code,
            language=request.language,
            use_llm=bool(app_state['openrouter_client'])
        )
        
        # Convert features to dict for JSON response
        feature_dicts = [
            {
                'name': f.name,
                'type': f.type,
                'intent': f.intent,
                'confidence': f.confidence,
                'complexity': f.complexity_score,
                'line_range': f.line_range,
                'dependencies': f.dependencies
            }
            for f in features
        ]
        
        return {
            'success': True,
            'analysis_type': request.analysis_type,
            'language': request.language,
            'features': feature_dicts,
            'feature_count': len(features)
        }
        
    except Exception as e:
        logger.error(f"Code analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Streaming analysis endpoint
@app.post("/api/v1/analyze-streaming")
async def analyze_streaming(request: StreamingAnalysisRequest):
    """Start streaming analysis of repository"""
    try:
        repo_path = Path(request.repository_path)
        if not repo_path.exists():
            raise HTTPException(status_code=404, detail="Repository path not found")
        
        async def generate_results():
            try:
                async for batch_result in app_state['streaming_walker'].walk_repository(repo_path):
                    yield f"data: {batch_result.json()}\n\n"
            except Exception as e:
                yield f"data: {{'error': '{str(e)}'}}\n\n"
        
        return StreamingResponse(
            generate_results(),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache"}
        )
        
    except Exception as e:
        logger.error(f"Streaming analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time updates
@app.websocket("/ws/analysis")
async def websocket_analysis(websocket: WebSocket):
    """WebSocket endpoint for real-time analysis updates"""
    await websocket.accept()
    app_state['active_connections'].add(websocket)
    
    try:
        while True:
            # Wait for analysis requests
            data = await websocket.receive_json()
            
            if data.get('type') == 'analyze_repo':
                repo_path = Path(data['repository_path'])
                
                if not repo_path.exists():
                    await websocket.send_json({
                        'type': 'error',
                        'message': 'Repository path not found'
                    })
                    continue
                
                # Send progress updates
                await websocket.send_json({
                    'type': 'progress',
                    'message': 'Starting analysis...',
                    'progress': 0
                })
                
                # Perform analysis with progress updates
                async for batch_result in app_state['streaming_walker'].walk_repository(repo_path):
                    await websocket.send_json({
                        'type': 'batch_result',
                        'data': {
                            'file_type': batch_result.file_type,
                            'files_processed': batch_result.files_processed,
                            'processing_time': batch_result.processing_time,
                            'success': len(batch_result.errors) == 0
                        }
                    })
                
                await websocket.send_json({
                    'type': 'complete',
                    'message': 'Analysis completed'
                })
                
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({
            'type': 'error',
            'message': str(e)
        })
    finally:
        app_state['active_connections'].discard(websocket)

# Statistics endpoint
@app.get("/api/v1/stats")
async def get_statistics():
    """Get system statistics and performance metrics"""
    stats = {
        'cache': None,
        'patterns': None,
        'agents': {},
        'openrouter': None
    }
    
    # Cache statistics
    if app_state['cache_manager']:
        stats['cache'] = await app_state['cache_manager'].get_statistics()
    
    # Pattern statistics
    if app_state['pattern_registry']:
        stats['patterns'] = app_state['pattern_registry'].get_pattern_statistics()
    
    # Agent statistics
    if app_state['structure_agent']:
        stats['agents']['structure'] = app_state['structure_agent'].get_statistics()
    
    # OpenRouter statistics
    if app_state['openrouter_client']:
        stats['openrouter'] = app_state['openrouter_client'].get_usage_stats()
    
    return stats

def create_app() -> FastAPI:
    """Factory function to create FastAPI app"""
    return app

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )