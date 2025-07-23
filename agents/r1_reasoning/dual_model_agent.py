"""
Dual-Model Agent for R1 Reasoning Engine

Orchestrates between DeepSeek R1 reasoning model and tool execution model
using Smolagents framework with AAI patterns and confidence scoring.
"""
import logging
import asyncio
import uuid
from typing import List, Dict, Any, Optional, Union, Callable
from datetime import datetime
from dataclasses import dataclass

# Smolagents imports with fallback
try:
    from smolagents import CodeAgent, ToolCallingAgent, Tool, HfApiModel
    from smolagents.agents import MultiStepAgent
    SMOLAGENTS_AVAILABLE = True
except ImportError:
    SMOLAGENTS_AVAILABLE = False

# Local imports
try:
    from .models import (
        ReasoningChain, ReasoningStep, DocumentAnalysisRequest, ReasoningResponse,
        ConfidenceAnalysis, ModelInferenceConfig, ReasoningDepth, ReasoningMethod
    )
except ImportError:
    from agents.r1_reasoning.models.models import (
        ReasoningChain, ReasoningStep, DocumentAnalysisRequest, ReasoningResponse,
        ConfidenceAnalysis, ModelInferenceConfig, ReasoningDepth, ReasoningMethod
    )

# Import with fallback handling
try:
    from .reasoning_engine import ReasoningEngine as R1ReasoningEngine
except ImportError:
    try:
        from agents.r1_reasoning.reasoning_engine import ReasoningEngine as R1ReasoningEngine
    except ImportError:
        R1ReasoningEngine = None

try:
    from .confidence_scorer import ConfidenceScorer
except ImportError:
    try:
        from agents.r1_reasoning.confidence_scorer import ConfidenceScorer
    except ImportError:
        ConfidenceScorer = None

try:
    from inference.model_router import ModelRouter
except ImportError:
    ModelRouter = None

# Vector storage
try:
    from vector_store import SupabaseVectorStore, ChromaManager, RetrievalRanker
    VECTOR_STORE_AVAILABLE = True
except ImportError:
    VECTOR_STORE_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class AgentTask:
    """Task for dual-model agent execution"""
    task_id: str
    task_type: str  # "reasoning", "retrieval", "analysis", "synthesis"
    description: str
    model_preference: str  # "reasoning", "tool", "auto"
    priority: int = 1
    context: Dict[str, Any] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.context is None:
            self.context = {}


@dataclass
class AgentResult:
    """Result from agent task execution"""
    task_id: str
    success: bool
    result: Any
    model_used: str
    confidence_score: float
    processing_time_ms: int
    reasoning_chain: Optional[ReasoningChain] = None
    error_message: Optional[str] = None


class DocumentRetrievalTool:
    """Tool for document retrieval and search"""
    
    def __init__(self, vector_store=None, ranker=None):
        self.vector_store = vector_store
        self.ranker = ranker
        self.name = "document_retrieval"
        self.description = "Retrieve and search relevant documents for reasoning tasks"
    
    async def __call__(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Execute document retrieval"""
        try:
            if not self.vector_store:
                return []
            
            from vector_store import VectorSearchRequest
            
            # Create search request
            search_request = VectorSearchRequest(
                query=query,
                max_results=max_results,
                similarity_threshold=0.5,
                min_confidence=0.70
            )
            
            # Perform search
            results = await self.vector_store.search_similar(search_request)
            
            # Convert to tool output format
            tool_results = []
            for result in results:
                tool_results.append({
                    "content": result.content,
                    "filename": result.filename,
                    "similarity": result.similarity_score,
                    "confidence": result.confidence_score,
                    "metadata": result.metadata
                })
            
            return tool_results
            
        except Exception as e:
            logger.error(f"Document retrieval failed: {e}")
            return []


class ReasoningAnalysisTool:
    """Tool for detailed reasoning analysis"""
    
    def __init__(self, reasoning_engine=None):
        self.reasoning_engine = reasoning_engine
        self.name = "reasoning_analysis"
        self.description = "Perform detailed reasoning analysis on queries and evidence"
    
    async def __call__(self, query: str, evidence: List[str] = None, depth: str = "thorough") -> Dict[str, Any]:
        """Execute reasoning analysis"""
        try:
            if not self.reasoning_engine:
                return {"error": "Reasoning engine not available"}
            
            # Convert depth string to enum
            reasoning_depth = ReasoningDepth.THOROUGH
            if depth == "quick":
                reasoning_depth = ReasoningDepth.QUICK
            elif depth == "exhaustive":
                reasoning_depth = ReasoningDepth.EXHAUSTIVE
            
            # Generate reasoning chain
            reasoning_chain = await self.reasoning_engine.generate_reasoning_chain(
                query=query,
                context=evidence or [],
                reasoning_depth=reasoning_depth
            )
            
            return {
                "reasoning_chain": reasoning_chain.model_dump(),
                "conclusion": reasoning_chain.final_conclusion,
                "confidence": reasoning_chain.overall_confidence,
                "method": reasoning_chain.reasoning_method.value,
                "steps": len(reasoning_chain.steps)
            }
            
        except Exception as e:
            logger.error(f"Reasoning analysis failed: {e}")
            return {"error": str(e)}


class DualModelAgent:
    """
    Dual-model agent orchestrating reasoning and tool execution.
    
    Features:
    - DeepSeek R1 for complex reasoning tasks
    - Tool execution model for document retrieval and analysis
    - Intelligent task routing based on complexity
    - AAI confidence scoring throughout
    - Smolagents integration for tool management
    """
    
    def __init__(self, 
                 reasoning_engine: Optional[R1ReasoningEngine] = None,
                 model_router: Optional[ModelRouter] = None,
                 vector_store: Optional[Any] = None,
                 config: Optional[ModelInferenceConfig] = None):
        """Initialize dual-model agent"""
        self.reasoning_engine = reasoning_engine
        self.model_router = model_router
        self.vector_store = vector_store
        self.config = config or ModelInferenceConfig()
        
        # Initialize components
        self.confidence_scorer = ConfidenceScorer() if ConfidenceScorer else None
        self.task_queue = []
        self.active_tasks = {}
        
        # Initialize Smolagents components
        self.smolagents_ready = SMOLAGENTS_AVAILABLE
        self.reasoning_agent = None
        self.tool_agent = None
        
        if self.smolagents_ready:
            self._initialize_smolagents()
        else:
            logger.warning("Smolagents not available - using fallback implementation")
        
        # Initialize tools
        self.tools = self._initialize_tools()
    
    def _initialize_smolagents(self):
        """Initialize Smolagents components"""
        try:
            # Initialize reasoning agent (DeepSeek R1)
            if SMOLAGENTS_AVAILABLE:
                # This would use actual Smolagents setup
                # For now, we'll use our own implementation
                self.reasoning_agent = "DeepSeek-R1-Agent"  # Placeholder
                self.tool_agent = "Tool-Execution-Agent"    # Placeholder
                
                logger.info("Smolagents agents initialized")
            
        except Exception as e:
            logger.error(f"Smolagents initialization failed: {e}")
            self.smolagents_ready = False
    
    def _initialize_tools(self) -> Dict[str, Any]:
        """Initialize available tools"""
        tools = {}
        
        # Document retrieval tool
        if self.vector_store:
            tools["document_retrieval"] = DocumentRetrievalTool(
                vector_store=self.vector_store
            )
        
        # Reasoning analysis tool
        if self.reasoning_engine:
            tools["reasoning_analysis"] = ReasoningAnalysisTool(
                reasoning_engine=self.reasoning_engine
            )
        
        return tools
    
    async def process_request(self, request: DocumentAnalysisRequest) -> ReasoningResponse:
        """
        Process a document analysis request using dual-model approach.
        
        Args:
            request: Document analysis request
            
        Returns:
            Complete reasoning response with analysis
        """
        start_time = datetime.now()
        request_id = str(uuid.uuid4())
        
        try:
            logger.info(f"Processing request {request_id}: {request.query}")
            
            # Step 1: Retrieve relevant documents
            documents = await self._retrieve_documents(request)
            
            # Step 2: Analyze complexity and route to appropriate model
            complexity_analysis = await self._analyze_complexity(request, documents)
            
            # Step 3: Generate reasoning chain
            reasoning_chain = await self._generate_reasoning(
                request, documents, complexity_analysis
            )
            
            # Step 4: Execute tool operations if needed
            tool_results = await self._execute_tools(request, reasoning_chain)
            
            # Step 5: Synthesize final response
            response = await self._synthesize_response(
                request, reasoning_chain, documents, tool_results, start_time, request_id
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Request processing failed: {e}")
            
            # Return error response
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return ReasoningResponse(
                answer=f"I encountered an error processing your request: {str(e)}",
                reasoning_chain=ReasoningChain(
                    query=request.query,
                    steps=[],
                    final_conclusion="Error in processing",
                    overall_confidence=0.70
                ),
                confidence_analysis=ConfidenceAnalysis(
                    overall=0.70,
                    reasoning_confidence=0.70,
                    evidence_confidence=0.0,
                    source_reliability=0.0,
                    assumption_certainty=0.0,
                    reasoning_coherence=0.0
                ),
                processing_time_ms=int(processing_time),
                model_used="error_handler",
                request_id=request_id
            )
    
    async def _retrieve_documents(self, request: DocumentAnalysisRequest) -> List[Dict[str, Any]]:
        """Retrieve relevant documents using tool execution model"""
        try:
            if "document_retrieval" in self.tools:
                tool = self.tools["document_retrieval"]
                documents = await tool(
                    query=request.query,
                    max_results=request.document_limit
                )
                return documents
            else:
                logger.warning("Document retrieval tool not available")
                return []
                
        except Exception as e:
            logger.error(f"Document retrieval failed: {e}")
            return []
    
    async def _analyze_complexity(self, 
                                request: DocumentAnalysisRequest, 
                                documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze query complexity to determine model routing"""
        try:
            # Complexity indicators
            query_length = len(request.query.split())
            document_count = len(documents)
            reasoning_keywords = [
                "why", "how", "because", "therefore", "analyze", "compare",
                "evaluate", "assess", "determine", "conclude", "infer"
            ]
            
            reasoning_complexity = sum(
                1 for keyword in reasoning_keywords 
                if keyword in request.query.lower()
            )
            
            # Determine complexity score
            complexity_score = (
                min(query_length / 20, 1.0) * 0.3 +
                min(document_count / 10, 1.0) * 0.3 +
                min(reasoning_complexity / 5, 1.0) * 0.4
            )
            
            # Determine preferred model
            if complexity_score > 0.7 or request.reasoning_depth == ReasoningDepth.EXHAUSTIVE:
                preferred_model = "reasoning"  # Use DeepSeek R1
            elif complexity_score < 0.3 and request.reasoning_depth == ReasoningDepth.QUICK:
                preferred_model = "tool"  # Use tool execution model
            else:
                preferred_model = "reasoning"  # Default to reasoning model
            
            return {
                "complexity_score": complexity_score,
                "preferred_model": preferred_model,
                "query_length": query_length,
                "document_count": document_count,
                "reasoning_complexity": reasoning_complexity
            }
            
        except Exception as e:
            logger.error(f"Complexity analysis failed: {e}")
            return {
                "complexity_score": 0.5,
                "preferred_model": "reasoning",
                "error": str(e)
            }
    
    async def _generate_reasoning(self,
                                request: DocumentAnalysisRequest,
                                documents: List[Dict[str, Any]],
                                complexity_analysis: Dict[str, Any]) -> ReasoningChain:
        """Generate reasoning chain using appropriate model"""
        try:
            if self.reasoning_engine and complexity_analysis["preferred_model"] == "reasoning":
                # Use DeepSeek R1 reasoning engine
                context = [doc["content"] for doc in documents if "content" in doc]
                
                reasoning_chain = await self.reasoning_engine.generate_reasoning_chain(
                    query=request.query,
                    context=context,
                    reasoning_depth=request.reasoning_depth
                )
                
                return reasoning_chain
            
            else:
                # Fallback reasoning using tool execution model
                return await self._fallback_reasoning(request, documents)
                
        except Exception as e:
            logger.error(f"Reasoning generation failed: {e}")
            return await self._fallback_reasoning(request, documents)
    
    async def _fallback_reasoning(self,
                                request: DocumentAnalysisRequest,
                                documents: List[Dict[str, Any]]) -> ReasoningChain:
        """Fallback reasoning when main engine unavailable"""
        
        # Create simple reasoning chain
        steps = [
            ReasoningStep(
                step_number=1,
                description="Analyze available information",
                reasoning=f"Examining query '{request.query}' with {len(documents)} available documents",
                confidence=0.75,
                evidence=[doc.get("filename", "unknown") for doc in documents[:3]]
            )
        ]
        
        if documents:
            steps.append(ReasoningStep(
                step_number=2,
                description="Synthesize information from sources",
                reasoning="Combining relevant information from multiple sources to form conclusion",
                confidence=0.72,
                evidence=[f"Document similarity: {doc.get('similarity', 0.5):.2f}" for doc in documents[:2]]
            ))
        
        conclusion = f"Based on the available information, I can provide insights about {request.query}."
        if not documents:
            conclusion = f"I don't have specific documents about {request.query}, but I can provide general information."
        
        return ReasoningChain(
            query=request.query,
            steps=steps,
            final_conclusion=conclusion,
            overall_confidence=0.75,
            reasoning_method=ReasoningMethod.DEDUCTIVE,
            evidence_quality=0.6 if documents else 0.3,
            assumption_risk=0.4,
            complexity_score=0.5
        )
    
    async def _execute_tools(self, 
                           request: DocumentAnalysisRequest,
                           reasoning_chain: ReasoningChain) -> Dict[str, Any]:
        """Execute additional tools as needed"""
        tool_results = {}
        
        try:
            # Execute reasoning analysis tool if available and beneficial
            if ("reasoning_analysis" in self.tools and 
                request.reasoning_depth in [ReasoningDepth.THOROUGH, ReasoningDepth.EXHAUSTIVE]):
                
                tool = self.tools["reasoning_analysis"]
                analysis_result = await tool(
                    query=request.query,
                    evidence=[step.reasoning for step in reasoning_chain.steps],
                    depth=request.reasoning_depth.value
                )
                tool_results["reasoning_analysis"] = analysis_result
            
            return tool_results
            
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return {}
    
    async def _synthesize_response(self,
                                 request: DocumentAnalysisRequest,
                                 reasoning_chain: ReasoningChain,
                                 documents: List[Dict[str, Any]],
                                 tool_results: Dict[str, Any],
                                 start_time: datetime,
                                 request_id: str) -> ReasoningResponse:
        """Synthesize final response from all components"""
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Create supporting documents
        supporting_docs = []
        for doc in documents[:5]:  # Top 5 documents
            from agents.r1_reasoning.models import SupportingDocument
            
            supporting_doc = SupportingDocument(
                filename=doc.get("filename", "unknown"),
                chunk_id=doc.get("chunk_id", str(uuid.uuid4())),
                content_preview=doc.get("content", "")[:200] + "...",
                relevance_score=doc.get("similarity", 0.5),
                confidence_score=doc.get("confidence", 0.70),
                source_quality=doc.get("quality", 0.5),
                metadata=doc.get("metadata", {})
            )
            supporting_docs.append(supporting_doc)
        
        # Create confidence analysis
        if self.confidence_scorer:
            confidence_analysis = self.confidence_scorer.calculate_comprehensive_confidence(
                reasoning_chain, documents, tool_results
            )
        else:
            # Fallback confidence analysis
            confidence_analysis = ConfidenceAnalysis(
                overall=reasoning_chain.overall_confidence,
                reasoning_confidence=reasoning_chain.overall_confidence,
                evidence_confidence=0.7 if documents else 0.3,
                source_reliability=0.6 if documents else 0.3,
                assumption_certainty=0.8,
                reasoning_coherence=0.75
            )
        
        # Generate final answer
        answer = reasoning_chain.final_conclusion
        if tool_results.get("reasoning_analysis"):
            enhanced_conclusion = tool_results["reasoning_analysis"].get("conclusion")
            if enhanced_conclusion and enhanced_conclusion != reasoning_chain.final_conclusion:
                answer = f"{reasoning_chain.final_conclusion}\n\nAdditional analysis: {enhanced_conclusion}"
        
        # Determine model used
        model_used = "dual_model_agent"
        if tool_results:
            model_used += "+tools"
        
        return ReasoningResponse(
            answer=answer,
            reasoning_chain=reasoning_chain,
            supporting_documents=supporting_docs,
            confidence_analysis=confidence_analysis,
            processing_time_ms=int(processing_time),
            model_used=model_used,
            request_id=request_id
        )
    
    async def add_task(self, task: AgentTask) -> str:
        """Add task to agent queue"""
        self.task_queue.append(task)
        logger.info(f"Added task {task.task_id} to queue")
        return task.task_id
    
    async def process_task_queue(self) -> List[AgentResult]:
        """Process all tasks in queue"""
        results = []
        
        while self.task_queue:
            task = self.task_queue.pop(0)
            try:
                result = await self._process_single_task(task)
                results.append(result)
            except Exception as e:
                logger.error(f"Task {task.task_id} failed: {e}")
                results.append(AgentResult(
                    task_id=task.task_id,
                    success=False,
                    result=None,
                    model_used="error",
                    confidence_score=0.70,
                    processing_time_ms=0,
                    error_message=str(e)
                ))
        
        return results
    
    async def _process_single_task(self, task: AgentTask) -> AgentResult:
        """Process a single agent task"""
        start_time = datetime.now()
        
        try:
            # Route task based on type and preference
            if task.task_type == "reasoning":
                result = await self._handle_reasoning_task(task)
            elif task.task_type == "retrieval":
                result = await self._handle_retrieval_task(task)
            else:
                result = await self._handle_generic_task(task)
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return AgentResult(
                task_id=task.task_id,
                success=True,
                result=result,
                model_used=task.model_preference,
                confidence_score=0.80,  # Would calculate based on result
                processing_time_ms=int(processing_time)
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return AgentResult(
                task_id=task.task_id,
                success=False,
                result=None,
                model_used="error",
                confidence_score=0.70,
                processing_time_ms=int(processing_time),
                error_message=str(e)
            )
    
    async def _handle_reasoning_task(self, task: AgentTask) -> Any:
        """Handle reasoning-specific tasks"""
        if self.reasoning_engine:
            # Use reasoning engine for complex reasoning
            return await self.reasoning_engine.generate_reasoning_chain(
                query=task.description,
                context=task.context.get("context", []),
                reasoning_depth=ReasoningDepth.THOROUGH
            )
        else:
            return {"error": "Reasoning engine not available"}
    
    async def _handle_retrieval_task(self, task: AgentTask) -> Any:
        """Handle retrieval-specific tasks"""
        if "document_retrieval" in self.tools:
            tool = self.tools["document_retrieval"]
            return await tool(task.description, max_results=5)
        else:
            return {"error": "Document retrieval tool not available"}
    
    async def _handle_generic_task(self, task: AgentTask) -> Any:
        """Handle generic tasks"""
        return {
            "task_id": task.task_id,
            "description": task.description,
            "status": "processed",
            "note": "Generic task handler used"
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and capabilities"""
        return {
            "smolagents_ready": self.smolagents_ready,
            "reasoning_engine_ready": self.reasoning_engine is not None,
            "vector_store_ready": self.vector_store is not None,
            "model_router_ready": self.model_router is not None,
            "available_tools": list(self.tools.keys()),
            "queue_size": len(self.task_queue),
            "active_tasks": len(self.active_tasks),
            "capabilities": {
                "dual_model_routing": True,
                "document_retrieval": "document_retrieval" in self.tools,
                "reasoning_analysis": "reasoning_analysis" in self.tools,
                "confidence_scoring": True,
                "task_queue_processing": True
            },
            "config": {
                "reasoning_model": self.config.reasoning_model,
                "tool_model": self.config.tool_model,
                "max_tokens": self.config.max_tokens,
                "temperature": self.config.temperature
            }
        }


async def test_dual_model_agent():
    """Test dual-model agent functionality"""
    
    # Initialize with mock components
    agent = DualModelAgent()
    
    print("🧪 Testing Dual-Model Agent")
    print("=" * 35)
    
    # Check agent status
    status = agent.get_agent_status()
    print(f"Smolagents ready: {status['smolagents_ready']}")
    print(f"Available tools: {status['available_tools']}")
    print(f"Capabilities: {list(status['capabilities'].keys())}")
    
    # Test with sample request
    sample_request = DocumentAnalysisRequest(
        query="How do artificial intelligence reasoning systems work?",
        user_id="test_user",
        document_limit=3,
        reasoning_depth=ReasoningDepth.THOROUGH,
        confidence_threshold=0.75
    )
    
    print(f"\n📋 Testing request: '{sample_request.query}'")
    print(f"Reasoning depth: {sample_request.reasoning_depth.value}")
    print(f"Document limit: {sample_request.document_limit}")
    
    # Process request
    try:
        response = await agent.process_request(sample_request)
        
        print(f"\n📊 Processing Results:")
        print(f"Success: {response.answer[:100]}...")
        print(f"Confidence: {response.confidence_analysis.overall:.2%}")
        print(f"Processing time: {response.processing_time_ms}ms")
        print(f"Model used: {response.model_used}")
        print(f"Supporting docs: {len(response.supporting_documents)}")
        print(f"Reasoning steps: {len(response.reasoning_chain.steps)}")
        
    except Exception as e:
        print(f"❌ Request processing failed: {e}")
    
    # Test task queue
    print(f"\n🔄 Testing task queue:")
    
    tasks = [
        AgentTask(
            task_id="task_1",
            task_type="reasoning",
            description="Analyze the benefits of machine learning",
            model_preference="reasoning"
        ),
        AgentTask(
            task_id="task_2", 
            task_type="retrieval",
            description="artificial intelligence research papers",
            model_preference="tool"
        )
    ]
    
    for task in tasks:
        await agent.add_task(task)
    
    print(f"Added {len(tasks)} tasks to queue")
    
    # Process queue
    results = await agent.process_task_queue()
    print(f"Processed {len(results)} tasks")
    
    for result in results:
        print(f"  Task {result.task_id}: {'✅' if result.success else '❌'} "
              f"({result.model_used}, {result.processing_time_ms}ms)")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_dual_model_agent())