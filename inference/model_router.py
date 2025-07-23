"""
Intelligent Model Router for R1 Reasoning Engine

Routes inference requests between HuggingFace, Ollama, and OpenRouter
based on availability, performance, and cost considerations.
"""
import asyncio
import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

from agents.r1_reasoning.config import R1ReasoningConfig
from agents.r1_reasoning.models import InferenceBackend, ModelInferenceConfig

logger = logging.getLogger(__name__)


@dataclass
class ModelAvailability:
    """Model availability status"""
    backend: InferenceBackend
    model_name: str
    available: bool
    response_time_ms: float
    error_message: Optional[str] = None
    last_checked: float = 0.0
    success_rate: float = 1.0


@dataclass
class InferenceRequest:
    """Inference request wrapper"""
    prompt: str
    model_type: str  # "reasoning" or "tool"
    max_tokens: int = 4096
    temperature: float = 0.1
    timeout_seconds: int = 60
    prefer_local: bool = False
    require_streaming: bool = False


@dataclass
class InferenceResponse:
    """Inference response wrapper"""
    text: str
    backend_used: InferenceBackend
    model_used: str
    response_time_ms: float
    token_count: int
    confidence_score: float = 0.70
    success: bool = True
    error_message: Optional[str] = None


class ModelSelectionStrategy(Enum):
    """Model selection strategies"""
    FASTEST = "fastest"
    MOST_RELIABLE = "most_reliable"
    COST_EFFECTIVE = "cost_effective"
    LOCAL_PREFERRED = "local_preferred"
    CLOUD_PREFERRED = "cloud_preferred"


class ModelRouter:
    """
    Intelligent model router with AAI patterns.
    
    Routes inference requests based on:
    - Model availability and health
    - Response time requirements
    - Cost considerations
    - Local vs cloud preferences
    - AAI confidence scoring requirements
    """
    
    def __init__(self, config: R1ReasoningConfig = None):
        """Initialize model router"""
        self.config = config or R1ReasoningConfig()
        self.model_availability: Dict[str, ModelAvailability] = {}
        self.performance_history: Dict[str, List[float]] = {}
        self.selection_strategy = ModelSelectionStrategy.MOST_RELIABLE
        
        # Initialize clients (lazy loading)
        self._huggingface_client = None
        self._ollama_client = None
        self._openrouter_client = None
        
        # Health check intervals
        self.health_check_interval = 300  # 5 minutes
        self.last_health_check = 0.0
    
    async def route_inference(self, request: InferenceRequest) -> InferenceResponse:
        """
        Route inference request to best available model.
        
        Args:
            request: Inference request with model type and parameters
            
        Returns:
            InferenceResponse with result and metadata
        """
        start_time = time.time()
        
        try:
            # Check model health if needed
            await self._check_model_health_if_needed()
            
            # Select best model based on request and availability
            selected_backend, selected_model = await self._select_model(request)
            
            if not selected_backend:
                return InferenceResponse(
                    text="",
                    backend_used=InferenceBackend.HUGGINGFACE,
                    model_used="unknown",
                    response_time_ms=0,
                    token_count=0,
                    success=False,
                    error_message="No available models for inference"
                )
            
            # Execute inference with selected model
            response = await self._execute_inference(
                request=request,
                backend=selected_backend,
                model=selected_model
            )
            
            # Update performance metrics
            self._update_performance_metrics(
                backend=selected_backend,
                model=selected_model,
                success=response.success,
                response_time_ms=response.response_time_ms
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Model routing failed: {e}")
            return InferenceResponse(
                text="",
                backend_used=InferenceBackend.HUGGINGFACE,
                model_used="unknown",
                response_time_ms=int((time.time() - start_time) * 1000),
                token_count=0,
                success=False,
                error_message=str(e)
            )
    
    async def _select_model(self, request: InferenceRequest) -> Tuple[Optional[InferenceBackend], Optional[str]]:
        """Select best model based on request requirements and availability"""
        
        # Get model options based on request type
        model_options = []
        
        if request.model_type == "reasoning":
            model_options = [
                (InferenceBackend.HUGGINGFACE, self.config.REASONING_MODEL),
                (InferenceBackend.OLLAMA, "deepseek-r1:7b-8k"),
                (InferenceBackend.OPENROUTER, "deepseek/deepseek-r1-distill-llama-70b")
            ]
        elif request.model_type == "tool":
            model_options = [
                (InferenceBackend.HUGGINGFACE, self.config.TOOL_MODEL),
                (InferenceBackend.OLLAMA, "llama3.3:70b"),
                (InferenceBackend.OPENROUTER, "meta-llama/llama-3.3-70b-instruct")
            ]
        
        # Filter by availability
        available_options = []
        for backend, model in model_options:
            key = f"{backend.value}:{model}"
            if key in self.model_availability and self.model_availability[key].available:
                available_options.append((backend, model, self.model_availability[key]))
        
        if not available_options:
            logger.warning("No available models found")
            return None, None
        
        # Apply selection strategy
        if self.selection_strategy == ModelSelectionStrategy.FASTEST:
            # Select fastest responding model
            selected = min(available_options, key=lambda x: x[2].response_time_ms)
        elif self.selection_strategy == ModelSelectionStrategy.MOST_RELIABLE:
            # Select most reliable model
            selected = max(available_options, key=lambda x: x[2].success_rate)
        elif self.selection_strategy == ModelSelectionStrategy.LOCAL_PREFERRED:
            # Prefer local models (Ollama)
            local_options = [opt for opt in available_options if opt[0] == InferenceBackend.OLLAMA]
            selected = local_options[0] if local_options else available_options[0]
        elif self.selection_strategy == ModelSelectionStrategy.CLOUD_PREFERRED:
            # Prefer cloud models
            cloud_options = [opt for opt in available_options 
                           if opt[0] in [InferenceBackend.HUGGINGFACE, InferenceBackend.OPENROUTER]]
            selected = cloud_options[0] if cloud_options else available_options[0]
        else:
            # Default to first available
            selected = available_options[0]
        
        logger.info(f"Selected model: {selected[0].value}:{selected[1]} "
                   f"(response_time: {selected[2].response_time_ms}ms, "
                   f"success_rate: {selected[2].success_rate:.2%})")
        
        return selected[0], selected[1]
    
    async def _execute_inference(self,
                               request: InferenceRequest,
                               backend: InferenceBackend,
                               model: str) -> InferenceResponse:
        """Execute inference with specified backend and model"""
        start_time = time.time()
        
        try:
            if backend == InferenceBackend.HUGGINGFACE:
                client = await self._get_huggingface_client()
                result = await client.generate(
                    prompt=request.prompt,
                    model=model,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    timeout=request.timeout_seconds
                )
            elif backend == InferenceBackend.OLLAMA:
                client = await self._get_ollama_client()
                result = await client.generate(
                    prompt=request.prompt,
                    model=model,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    timeout=request.timeout_seconds
                )
            elif backend == InferenceBackend.OPENROUTER:
                client = await self._get_openrouter_client()
                result = await client.generate(
                    prompt=request.prompt,
                    model=model,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    timeout=request.timeout_seconds
                )
            else:
                raise ValueError(f"Unsupported backend: {backend}")
            
            response_time_ms = int((time.time() - start_time) * 1000)
            
            return InferenceResponse(
                text=result.get("text", ""),
                backend_used=backend,
                model_used=model,
                response_time_ms=response_time_ms,
                token_count=result.get("token_count", 0),
                confidence_score=max(0.70, min(0.95, result.get("confidence_score", 0.75))),
                success=True
            )
            
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            logger.error(f"Inference failed with {backend.value}:{model}: {e}")
            
            return InferenceResponse(
                text="",
                backend_used=backend,
                model_used=model,
                response_time_ms=response_time_ms,
                token_count=0,
                success=False,
                error_message=str(e)
            )
    
    async def _check_model_health_if_needed(self):
        """Check model health if interval has passed"""
        current_time = time.time()
        if current_time - self.last_health_check > self.health_check_interval:
            await self._check_model_health()
            self.last_health_check = current_time
    
    async def _check_model_health(self):
        """Check health of all configured models"""
        logger.info("Checking model health...")
        
        # Test models to check
        test_models = [
            (InferenceBackend.HUGGINGFACE, self.config.REASONING_MODEL),
            (InferenceBackend.HUGGINGFACE, self.config.TOOL_MODEL),
            (InferenceBackend.OLLAMA, "deepseek-r1:7b-8k"),
            (InferenceBackend.OLLAMA, "llama3.3:70b"),
            (InferenceBackend.OPENROUTER, "deepseek/deepseek-r1-distill-llama-70b")
        ]
        
        # Test each model
        for backend, model in test_models:
            await self._test_model_availability(backend, model)
    
    async def _test_model_availability(self, backend: InferenceBackend, model: str):
        """Test availability of a specific model"""
        key = f"{backend.value}:{model}"
        start_time = time.time()
        
        try:
            # Simple test prompt
            test_request = InferenceRequest(
                prompt="Test prompt for health check",
                model_type="tool",
                max_tokens=10,
                temperature=0.1,
                timeout_seconds=10
            )
            
            response = await self._execute_inference(test_request, backend, model)
            response_time_ms = int((time.time() - start_time) * 1000)
            
            self.model_availability[key] = ModelAvailability(
                backend=backend,
                model_name=model,
                available=response.success,
                response_time_ms=response_time_ms,
                error_message=response.error_message if not response.success else None,
                last_checked=time.time(),
                success_rate=self._calculate_success_rate(key)
            )
            
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            self.model_availability[key] = ModelAvailability(
                backend=backend,
                model_name=model,
                available=False,
                response_time_ms=response_time_ms,
                error_message=str(e),
                last_checked=time.time(),
                success_rate=0.0
            )
    
    def _calculate_success_rate(self, model_key: str) -> float:
        """Calculate success rate for a model"""
        if model_key not in self.performance_history:
            return 1.0
        
        history = self.performance_history[model_key]
        if not history:
            return 1.0
        
        # Consider last 10 requests
        recent_history = history[-10:]
        success_count = sum(1 for result in recent_history if result > 0)
        return success_count / len(recent_history)
    
    def _update_performance_metrics(self,
                                  backend: InferenceBackend,
                                  model: str,
                                  success: bool,
                                  response_time_ms: float):
        """Update performance metrics for a model"""
        key = f"{backend.value}:{model}"
        
        if key not in self.performance_history:
            self.performance_history[key] = []
        
        # Record success (1) or failure (0)
        self.performance_history[key].append(1 if success else 0)
        
        # Keep only last 50 results
        self.performance_history[key] = self.performance_history[key][-50:]
        
        # Update availability record
        if key in self.model_availability:
            self.model_availability[key].success_rate = self._calculate_success_rate(key)
    
    async def _get_huggingface_client(self):
        """Get HuggingFace client (lazy loading)"""
        if self._huggingface_client is None:
            from inference.huggingface_client import HuggingFaceClient
            self._huggingface_client = HuggingFaceClient()
        return self._huggingface_client
    
    async def _get_ollama_client(self):
        """Get Ollama client (lazy loading)"""
        if self._ollama_client is None:
            from inference.ollama_client import OllamaClient
            self._ollama_client = OllamaClient()
        return self._ollama_client
    
    async def _get_openrouter_client(self):
        """Get OpenRouter client (lazy loading)"""
        if self._openrouter_client is None:
            # Use existing AAI OpenRouter client
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
            from brain.modules.openrouter.router_client import OpenRouterClient
            self._openrouter_client = OpenRouterClient()
        return self._openrouter_client
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get current model availability status"""
        return {
            "total_models": len(self.model_availability),
            "available_models": sum(1 for m in self.model_availability.values() if m.available),
            "average_response_time": sum(m.response_time_ms for m in self.model_availability.values()) / len(self.model_availability) if self.model_availability else 0,
            "selection_strategy": self.selection_strategy.value,
            "last_health_check": self.last_health_check,
            "models": {
                key: {
                    "available": model.available,
                    "response_time_ms": model.response_time_ms,
                    "success_rate": model.success_rate,
                    "last_checked": model.last_checked,
                    "error_message": model.error_message
                }
                for key, model in self.model_availability.items()
            }
        }
    
    def set_selection_strategy(self, strategy: ModelSelectionStrategy):
        """Set model selection strategy"""
        self.selection_strategy = strategy
        logger.info(f"Model selection strategy changed to: {strategy.value}")


async def test_model_router():
    """Test model router functionality"""
    router = ModelRouter()
    
    # Test reasoning request
    reasoning_request = InferenceRequest(
        prompt="Analyze the pros and cons of using FastAPI for web development",
        model_type="reasoning",
        max_tokens=1024,
        temperature=0.3
    )
    
    print("Testing reasoning model routing...")
    response = await router.route_inference(reasoning_request)
    print(f"Success: {response.success}")
    print(f"Backend: {response.backend_used}")
    print(f"Model: {response.model_used}")
    print(f"Response time: {response.response_time_ms}ms")
    print(f"Confidence: {response.confidence_score}")
    
    if response.success:
        print(f"Response: {response.text[:200]}...")
    else:
        print(f"Error: {response.error_message}")
    
    # Get status
    status = router.get_model_status()
    print(f"\nModel Status: {status}")


if __name__ == "__main__":
    asyncio.run(test_model_router())