#!/usr/bin/env python3
"""
MCP Server for Research Engine
Provides Model Context Protocol interface for research delegation
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

# Add research modules to path
sys.path.append(str(Path(__file__).parent.parent))
from _map.openrouter_integration import OpenRouterResearchAgent
from _map.pattern_detector import CrossProjectPatternDetector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class MCPRequest:
    """MCP request structure"""
    method: str
    params: Dict[str, Any]
    id: Optional[str] = None

@dataclass
class MCPResponse:
    """MCP response structure"""
    result: Any
    error: Optional[str] = None
    id: Optional[str] = None

class ResearchRequest(BaseModel):
    """Research request model"""
    technology: str
    type: str  # 'general', 'project', 'analysis', 'pattern'
    project: Optional[str] = None
    content: Optional[str] = None
    sources: Optional[List[str]] = None

class ResearchResponse(BaseModel):
    """Research response model"""
    success: bool
    data: Dict[str, Any]
    message: str
    task_id: Optional[str] = None

class ResearchMCPServer:
    """MCP Server for research engine operations"""
    
    def __init__(self, research_dir: str):
        self.research_dir = Path(research_dir)
        self.app = FastAPI(title="Research Engine MCP Server", version="1.0.0")
        self.setup_middleware()
        self.setup_routes()
        
        # Initialize components
        self.openrouter_agent = None
        self.pattern_detector = None
        self.active_tasks = {}
        
        # Initialize OpenRouter if API key available
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            self.openrouter_agent = OpenRouterResearchAgent(openrouter_key, research_dir)
            logger.info("OpenRouter agent initialized")
        
        # Initialize pattern detector
        self.pattern_detector = CrossProjectPatternDetector(research_dir)
        logger.info("Pattern detector initialized")
        
        # MCP server registry
        self.mcp_servers = {
            "filesystem": {"host": "mcp-filesystem", "port": 3001},
            "git": {"host": "mcp-git", "port": 3002},
            "puppeteer": {"host": "mcp-puppeteer", "port": 3003},
            "brave-search": {"host": "mcp-brave-search", "port": 3004}
        }
        
        logger.info(f"Research MCP Server initialized with directory: {research_dir}")
    
    def setup_middleware(self):
        """Setup FastAPI middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "research_dir": str(self.research_dir),
                "openrouter_available": self.openrouter_agent is not None,
                "mcp_servers": list(self.mcp_servers.keys())
            }
        
        @self.app.post("/mcp/request")
        async def handle_mcp_request(request: MCPRequest):
            """Handle MCP protocol requests"""
            try:
                result = await self.process_mcp_request(request.method, request.params)
                return MCPResponse(result=result, id=request.id)
            except Exception as e:
                logger.error(f"MCP request error: {e}")
                return MCPResponse(
                    result=None,
                    error=str(e),
                    id=request.id
                )
        
        @self.app.post("/research/general")
        async def create_general_research(request: ResearchRequest, background_tasks: BackgroundTasks):
            """Create general research"""
            task_id = f"general_{request.technology}_{len(self.active_tasks)}"
            
            background_tasks.add_task(
                self.execute_general_research,
                task_id,
                request.technology,
                request.content
            )
            
            return ResearchResponse(
                success=True,
                data={"task_id": task_id},
                message=f"General research started for {request.technology}",
                task_id=task_id
            )
        
        @self.app.post("/research/project")
        async def create_project_research(request: ResearchRequest, background_tasks: BackgroundTasks):
            """Create project-specific research"""
            if not request.project:
                raise HTTPException(status_code=400, detail="Project name required")
            
            task_id = f"project_{request.project}_{request.technology}_{len(self.active_tasks)}"
            
            background_tasks.add_task(
                self.execute_project_research,
                task_id,
                request.project,
                request.technology,
                request.content
            )
            
            return ResearchResponse(
                success=True,
                data={"task_id": task_id},
                message=f"Project research started for {request.project}/{request.technology}",
                task_id=task_id
            )
        
        @self.app.post("/research/analyze")
        async def analyze_research(request: ResearchRequest, background_tasks: BackgroundTasks):
            """Analyze research content"""
            if not self.openrouter_agent:
                raise HTTPException(status_code=503, detail="OpenRouter agent not available")
            
            task_id = f"analyze_{request.technology}_{len(self.active_tasks)}"
            
            background_tasks.add_task(
                self.execute_research_analysis,
                task_id,
                request.technology,
                request.content
            )
            
            return ResearchResponse(
                success=True,
                data={"task_id": task_id},
                message=f"Research analysis started for {request.technology}",
                task_id=task_id
            )
        
        @self.app.post("/research/patterns")
        async def detect_patterns(background_tasks: BackgroundTasks):
            """Detect cross-project patterns"""
            task_id = f"patterns_{len(self.active_tasks)}"
            
            background_tasks.add_task(
                self.execute_pattern_detection,
                task_id
            )
            
            return ResearchResponse(
                success=True,
                data={"task_id": task_id},
                message="Pattern detection started",
                task_id=task_id
            )
        
        @self.app.get("/research/task/{task_id}")
        async def get_task_status(task_id: str):
            """Get task status"""
            if task_id not in self.active_tasks:
                raise HTTPException(status_code=404, detail="Task not found")
            
            return self.active_tasks[task_id]
        
        @self.app.get("/research/mcp/servers")
        async def list_mcp_servers():
            """List available MCP servers"""
            servers = []
            for name, config in self.mcp_servers.items():
                status = await self.check_mcp_server_status(config)
                servers.append({
                    "name": name,
                    "host": config["host"],
                    "port": config["port"],
                    "status": status
                })
            return {"servers": servers}
        
        @self.app.post("/research/mcp/delegate")
        async def delegate_to_mcp(request: Dict[str, Any]):
            """Delegate request to MCP server"""
            server_name = request.get("server")
            if server_name not in self.mcp_servers:
                raise HTTPException(status_code=404, detail="MCP server not found")
            
            result = await self.delegate_to_mcp_server(server_name, request)
            return {"result": result}
    
    async def process_mcp_request(self, method: str, params: Dict[str, Any]) -> Any:
        """Process MCP protocol request"""
        if method == "research/general":
            return await self.mcp_create_general_research(params)
        elif method == "research/project":
            return await self.mcp_create_project_research(params)
        elif method == "research/analyze":
            return await self.mcp_analyze_research(params)
        elif method == "research/patterns":
            return await self.mcp_detect_patterns(params)
        elif method == "research/delegate":
            return await self.mcp_delegate_request(params)
        else:
            raise ValueError(f"Unknown MCP method: {method}")
    
    async def mcp_create_general_research(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """MCP method for creating general research"""
        technology = params.get("technology")
        content = params.get("content")
        
        if not technology:
            raise ValueError("Technology parameter required")
        
        # Delegate to filesystem MCP for file operations
        if "filesystem" in self.mcp_servers:
            file_path = self.research_dir / "_knowledge-base" / technology / f"{technology}-general.md"
            await self.delegate_to_mcp_server("filesystem", {
                "method": "create_file",
                "path": str(file_path),
                "content": content or f"# {technology.title()} - General Research\n\n## Overview\n\nGeneral research for {technology}."
            })
        
        return {
            "success": True,
            "technology": technology,
            "file_path": str(file_path)
        }
    
    async def mcp_create_project_research(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """MCP method for creating project research"""
        project = params.get("project")
        technology = params.get("technology")
        content = params.get("content")
        
        if not project or not technology:
            raise ValueError("Project and technology parameters required")
        
        # Delegate to filesystem MCP for file operations
        if "filesystem" in self.mcp_servers:
            file_path = self.research_dir / "_knowledge-base" / technology / f"{technology}-{project}.md"
            await self.delegate_to_mcp_server("filesystem", {
                "method": "create_file",
                "path": str(file_path),
                "content": content or f"# {technology.title()} - {project.title()} Research\n\n## Project Context\n\nProject-specific research for {technology} in {project}."
            })
        
        return {
            "success": True,
            "project": project,
            "technology": technology,
            "file_path": str(file_path)
        }
    
    async def mcp_analyze_research(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """MCP method for research analysis"""
        if not self.openrouter_agent:
            raise ValueError("OpenRouter agent not available")
        
        technology = params.get("technology")
        content = params.get("content")
        
        if not technology or not content:
            raise ValueError("Technology and content parameters required")
        
        analysis = self.openrouter_agent.analyze_research_content(content, technology)
        
        return {
            "success": True,
            "analysis": asdict(analysis) if analysis else None
        }
    
    async def mcp_detect_patterns(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """MCP method for pattern detection"""
        analysis = self.pattern_detector.analyze_patterns()
        
        return {
            "success": True,
            "patterns": len(analysis.candidates),
            "recommendations": analysis.recommendations
        }
    
    async def mcp_delegate_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """MCP method for delegating to other MCP servers"""
        server_name = params.get("server")
        request = params.get("request")
        
        if not server_name or not request:
            raise ValueError("Server and request parameters required")
        
        result = await self.delegate_to_mcp_server(server_name, request)
        
        return {
            "success": True,
            "server": server_name,
            "result": result
        }
    
    async def execute_general_research(self, task_id: str, technology: str, content: Optional[str]):
        """Execute general research task"""
        self.active_tasks[task_id] = {
            "status": "running",
            "progress": 0,
            "message": f"Creating general research for {technology}"
        }
        
        try:
            # Create research file
            file_path = self.research_dir / "_knowledge-base" / technology / f"{technology}-general.md"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if content:
                file_path.write_text(content)
            else:
                # Generate basic template
                template = f"""# {technology.title()} - General Research

## Overview
General research for {technology} technology.

## Key Concepts
- Core concepts that apply across projects
- Universal patterns and best practices
- Common gotchas and solutions

## Implementation Patterns
### Basic Setup
[Setup instructions]

### Common Configurations
[Configuration examples]

### Integration Patterns
[Integration approaches]

## Quality Score: 0.85
**Inheritance**: Base knowledge for all projects
**Source Quality**: Template generated
**Completeness**: Basic coverage
**Reusability**: High

## Tags
#general #{technology} #template
"""
                file_path.write_text(template)
            
            # Update symlinks
            await self.update_symlinks()
            
            self.active_tasks[task_id] = {
                "status": "completed",
                "progress": 100,
                "message": f"General research created for {technology}",
                "result": {
                    "file_path": str(file_path),
                    "technology": technology
                }
            }
            
        except Exception as e:
            logger.error(f"Error in general research task {task_id}: {e}")
            self.active_tasks[task_id] = {
                "status": "failed",
                "progress": 0,
                "message": f"Error creating general research: {str(e)}"
            }
    
    async def execute_project_research(self, task_id: str, project: str, technology: str, content: Optional[str]):
        """Execute project research task"""
        self.active_tasks[task_id] = {
            "status": "running",
            "progress": 0,
            "message": f"Creating project research for {project}/{technology}"
        }
        
        try:
            # Create research file
            file_path = self.research_dir / "_knowledge-base" / technology / f"{technology}-{project}.md"
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if content:
                file_path.write_text(content)
            else:
                # Generate basic template
                template = f"""# {technology.title()} - {project.title()} Research

## Project Context
Project-specific research for {technology} in {project}.

## Inheritance
**Inherits from**: `general/{technology}/{technology}.md`
**Override reason**: Project-specific implementation requirements
**Inheritance type**: extension
**Confidence**: 0.75

## Project-Specific Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Deviations from General Research
### Configuration Differences
- [Difference 1 and reason]

### Implementation Adaptations
- [Adaptation 1 and context]

## Quality Score: 0.75
**Inheritance**: Extends general/{technology}
**Project Context**: High relevance to {project}
**Implementation Ready**: Yes

## Tags
#project-specific #{project} #{technology} #template
"""
                file_path.write_text(template)
            
            # Update symlinks
            await self.update_symlinks()
            
            self.active_tasks[task_id] = {
                "status": "completed",
                "progress": 100,
                "message": f"Project research created for {project}/{technology}",
                "result": {
                    "file_path": str(file_path),
                    "project": project,
                    "technology": technology
                }
            }
            
        except Exception as e:
            logger.error(f"Error in project research task {task_id}: {e}")
            self.active_tasks[task_id] = {
                "status": "failed",
                "progress": 0,
                "message": f"Error creating project research: {str(e)}"
            }
    
    async def execute_research_analysis(self, task_id: str, technology: str, content: str):
        """Execute research analysis task"""
        self.active_tasks[task_id] = {
            "status": "running",
            "progress": 0,
            "message": f"Analyzing research for {technology}"
        }
        
        try:
            if not self.openrouter_agent:
                raise ValueError("OpenRouter agent not available")
            
            analysis = self.openrouter_agent.analyze_research_content(content, technology)
            
            self.active_tasks[task_id] = {
                "status": "completed",
                "progress": 100,
                "message": f"Research analysis completed for {technology}",
                "result": asdict(analysis) if analysis else None
            }
            
        except Exception as e:
            logger.error(f"Error in research analysis task {task_id}: {e}")
            self.active_tasks[task_id] = {
                "status": "failed",
                "progress": 0,
                "message": f"Error analyzing research: {str(e)}"
            }
    
    async def execute_pattern_detection(self, task_id: str):
        """Execute pattern detection task"""
        self.active_tasks[task_id] = {
            "status": "running",
            "progress": 0,
            "message": "Detecting cross-project patterns"
        }
        
        try:
            analysis = self.pattern_detector.analyze_patterns()
            
            self.active_tasks[task_id] = {
                "status": "completed",
                "progress": 100,
                "message": f"Pattern detection completed - found {len(analysis.candidates)} candidates",
                "result": {
                    "candidates": len(analysis.candidates),
                    "recommendations": analysis.recommendations
                }
            }
            
        except Exception as e:
            logger.error(f"Error in pattern detection task {task_id}: {e}")
            self.active_tasks[task_id] = {
                "status": "failed",
                "progress": 0,
                "message": f"Error detecting patterns: {str(e)}"
            }
    
    async def update_symlinks(self):
        """Update symbolic links after file changes"""
        try:
            import subprocess
            script_path = self.research_dir / "scripts" / "create-symlinks.sh"
            if script_path.exists():
                subprocess.run([str(script_path)], check=True)
            logger.info("Symlinks updated successfully")
        except Exception as e:
            logger.error(f"Error updating symlinks: {e}")
    
    async def check_mcp_server_status(self, config: Dict[str, Any]) -> str:
        """Check MCP server status"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://{config['host']}:{config['port']}/health", timeout=5) as response:
                    if response.status == 200:
                        return "healthy"
                    else:
                        return "unhealthy"
        except:
            return "unreachable"
    
    async def delegate_to_mcp_server(self, server_name: str, request: Dict[str, Any]) -> Any:
        """Delegate request to MCP server"""
        if server_name not in self.mcp_servers:
            raise ValueError(f"MCP server {server_name} not found")
        
        config = self.mcp_servers[server_name]
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"http://{config['host']}:{config['port']}/mcp/request",
                    json=request,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise ValueError(f"MCP server error: {response.status}")
        except Exception as e:
            logger.error(f"Error delegating to MCP server {server_name}: {e}")
            raise

def main():
    """Main server startup"""
    research_dir = os.getenv("RESEARCH_DIR", "/app/research")
    
    # Ensure research directory exists
    Path(research_dir).mkdir(parents=True, exist_ok=True)
    
    # Initialize server
    server = ResearchMCPServer(research_dir)
    
    # Start server
    uvicorn.run(
        server.app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=False
    )

if __name__ == "__main__":
    main()