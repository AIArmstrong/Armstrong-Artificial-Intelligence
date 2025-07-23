"""
Ollama Inference Client for R1 Reasoning Engine

Handles local model inference via Ollama with support for
DeepSeek R1 and other models with AAI confidence scoring.
"""
import asyncio
import time
import json
from typing import Dict, Any, Optional, AsyncGenerator
import logging

import aiohttp
from agents.r1_reasoning.config import R1ReasoningConfig

logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Ollama local inference client with AAI patterns.
    
    Features:
    - Local DeepSeek R1 inference
    - Streaming response handling
    - Model management and loading
    - AAI confidence scoring
    - Custom model configurations
    """
    
    def __init__(self, config: R1ReasoningConfig = None):
        """Initialize Ollama client"""
        self.config = config or R1ReasoningConfig()
        self.base_url = self.config.OLLAMA_BASE_URL
        self.headers = {"Content-Type": "application/json"}
        
        # Session for connection pooling
        self._session: Optional[aiohttp.ClientSession] = None
        
        # Model availability cache
        self._available_models: Optional[list] = None
        self._models_last_checked = 0.0
        self._model_check_interval = 300  # 5 minutes
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.TIMEOUT_SECONDS)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
    
    async def generate(self,
                      prompt: str,
                      model: str,
                      max_tokens: int = 4096,
                      temperature: float = 0.1,
                      timeout: int = 60,
                      stream: bool = False) -> Dict[str, Any]:
        """
        Generate text using Ollama model.
        
        Args:
            prompt: Input prompt
            model: Model name (e.g., "deepseek-r1:7b-8k")
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            timeout: Request timeout in seconds
            stream: Whether to stream response
            
        Returns:
            Dict containing generated text and metadata
        """
        start_time = time.time()
        
        # Check if model is available
        if not await self._is_model_available(model):
            return {
                "text": "",
                "token_count": 0,
                "confidence_score": 0.70,
                "response_time_ms": 100,
                "model_used": model,
                "success": False,
                "error": f"Model {model} not available in Ollama"
            }
        
        # Prepare request
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "num_ctx": 8192,  # Context window
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        try:
            session = await self._get_session()
            
            async with session.post(url, json=payload, headers=self.headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error {response.status}: {error_text}")
                
                if stream:
                    # Handle streaming response
                    generated_text = ""
                    async for chunk in self._process_streaming_response(response):
                        generated_text += chunk
                    result_text = generated_text
                else:
                    # Handle standard response
                    result = await response.json()
                    result_text = result.get("response", "")
                
                response_time_ms = int((time.time() - start_time) * 1000)
                
                # Calculate confidence score
                confidence_score = self._calculate_confidence_score(
                    prompt=prompt,
                    response=result_text,
                    model=model,
                    response_time_ms=response_time_ms
                )
                
                # Estimate token count
                token_count = self._estimate_token_count(result_text)
                
                return {
                    "text": result_text,
                    "token_count": token_count,
                    "confidence_score": confidence_score,
                    "response_time_ms": response_time_ms,
                    "model_used": model,
                    "success": True
                }
                
        except asyncio.TimeoutError:
            logger.error(f"Ollama request timeout for model {model}")
            return {
                "text": "",
                "token_count": 0,
                "confidence_score": 0.70,
                "response_time_ms": timeout * 1000,
                "model_used": model,
                "success": False,
                "error": "Request timeout"
            }
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            logger.error(f"Ollama generation failed for model {model}: {e}")
            return {
                "text": "",
                "token_count": 0,
                "confidence_score": 0.70,
                "response_time_ms": response_time_ms,
                "model_used": model,
                "success": False,
                "error": str(e)
            }
    
    async def _process_streaming_response(self, response) -> AsyncGenerator[str, None]:
        """Process streaming response from Ollama"""
        async for chunk in response.content.iter_chunked(1024):
            chunk_text = chunk.decode('utf-8', errors='ignore')
            
            # Ollama streams JSON objects separated by newlines
            for line in chunk_text.strip().split('\n'):
                if line.strip():
                    try:
                        data = json.loads(line)
                        if 'response' in data:
                            yield data['response']
                    except json.JSONDecodeError:
                        continue
    
    async def generate_reasoning(self,
                               query: str,
                               context: Optional[str] = None,
                               model: str = "deepseek-r1:7b-8k") -> Dict[str, Any]:
        """
        Generate structured reasoning using local DeepSeek R1.
        
        Args:
            query: Question or problem to reason about
            context: Optional context information
            model: Local model to use
            
        Returns:
            Dict with reasoning chain and confidence scores
        """
        # Construct reasoning prompt optimized for DeepSeek R1
        reasoning_prompt = self._build_reasoning_prompt(query, context)
        
        result = await self.generate(
            prompt=reasoning_prompt,
            model=model,
            max_tokens=self.config.MAX_TOKENS,
            temperature=self.config.REASONING_TEMPERATURE
        )
        
        if result["success"]:
            # Parse reasoning from R1 output
            reasoning_data = self._parse_reasoning_output(result["text"])
            result.update(reasoning_data)
        
        return result
    
    def _build_reasoning_prompt(self, query: str, context: Optional[str] = None) -> str:
        """Build optimized reasoning prompt for local DeepSeek R1"""
        
        prompt_parts = [
            "<|im_start|>system",
            "You are an AI assistant that provides structured reasoning and analysis.",
            "Break down your reasoning into clear steps with confidence scores (70-95%).",
            "Format your response with clear sections for reasoning steps and conclusion.",
            "<|im_end|>",
            "",
            "<|im_start|>user"
        ]
        
        if context:
            prompt_parts.extend([
                "Context:",
                context,
                ""
            ])
        
        prompt_parts.extend([
            "Query:",
            query,
            "",
            "Please provide step-by-step reasoning with:",
            "1. Clear reasoning steps with confidence scores",
            "2. Evidence and assumptions for each step",
            "3. A final conclusion with overall confidence",
            "<|im_end|>",
            "",
            "<|im_start|>assistant"
        ])
        
        return "\n".join(prompt_parts)
    
    def _parse_reasoning_output(self, output: str) -> Dict[str, Any]:
        """Parse structured reasoning from local R1 output"""
        reasoning_data = {
            "reasoning_steps": [],
            "final_conclusion": "",
            "reasoning_confidence": 0.70,
            "evidence_quality": 0.5,
            "assumption_risk": 0.5
        }
        
        try:
            # Clean up the output
            output = output.replace("<|im_end|>", "").strip()
            lines = output.split('\n')
            
            current_step = None
            step_counter = 0
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Look for step indicators
                if any(indicator in line.lower() for indicator in ['step', 'first', 'second', 'third', 'finally', 'conclusion']):
                    step_counter += 1
                    
                    # Extract confidence if present
                    confidence = 0.75  # Default
                    import re
                    conf_match = re.search(r'(\d+)%', line)
                    if conf_match:
                        confidence = min(0.95, max(0.70, int(conf_match.group(1)) / 100))
                    
                    current_step = {
                        "step_number": step_counter,
                        "description": line,
                        "reasoning": "",
                        "confidence": confidence,
                        "evidence": [],
                        "assumptions": []
                    }
                    reasoning_data["reasoning_steps"].append(current_step)
                
                # Add content to current step
                elif current_step and line:
                    if current_step["reasoning"]:
                        current_step["reasoning"] += " " + line
                    else:
                        current_step["reasoning"] = line
                
                # Look for conclusion
                if any(indicator in line.lower() for indicator in ['conclusion', 'summary', 'overall']):
                    reasoning_data["final_conclusion"] = line
                    
                    # Extract overall confidence
                    import re
                    conf_match = re.search(r'(\d+)%', line)
                    if conf_match:
                        reasoning_data["reasoning_confidence"] = min(0.95, max(0.70, int(conf_match.group(1)) / 100))
            
            # Calculate quality metrics
            if reasoning_data["reasoning_steps"]:
                avg_confidence = sum(step["confidence"] for step in reasoning_data["reasoning_steps"]) / len(reasoning_data["reasoning_steps"])
                reasoning_data["evidence_quality"] = min(1.0, avg_confidence * 1.1)
                reasoning_data["assumption_risk"] = max(0.0, 1.0 - avg_confidence * 0.9)
            
        except Exception as e:
            logger.warning(f"Failed to parse local reasoning output: {e}")
        
        return reasoning_data
    
    async def _is_model_available(self, model: str) -> bool:
        """Check if model is available in Ollama"""
        try:
            available_models = await self._get_available_models()
            return model in available_models
        except Exception:
            return False
    
    async def _get_available_models(self) -> list:
        """Get list of available models from Ollama"""
        current_time = time.time()
        
        # Use cached result if recent
        if (self._available_models is not None and 
            current_time - self._models_last_checked < self._model_check_interval):
            return self._available_models
        
        try:
            session = await self._get_session()
            url = f"{self.base_url}/api/tags"
            
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    result = await response.json()
                    models = [model["name"] for model in result.get("models", [])]
                    self._available_models = models
                    self._models_last_checked = current_time
                    return models
                else:
                    logger.warning(f"Failed to get Ollama models: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting Ollama models: {e}")
            return []
    
    async def pull_model(self, model: str) -> bool:
        """Pull/download a model to Ollama"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/api/pull"
            payload = {"name": model}
            
            async with session.post(url, json=payload, headers=self.headers) as response:
                if response.status == 200:
                    # Stream the pull progress
                    async for chunk in response.content.iter_chunked(1024):
                        chunk_text = chunk.decode('utf-8', errors='ignore')
                        for line in chunk_text.strip().split('\n'):
                            if line.strip():
                                try:
                                    data = json.loads(line)
                                    if data.get("status"):
                                        logger.info(f"Pulling {model}: {data['status']}")
                                except json.JSONDecodeError:
                                    continue
                    
                    # Refresh available models cache
                    self._available_models = None
                    return True
                else:
                    logger.error(f"Failed to pull model {model}: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error pulling model {model}: {e}")
            return False
    
    async def create_custom_model(self, 
                                model_name: str, 
                                base_model: str,
                                modelfile_content: str) -> bool:
        """Create a custom model with specific configuration"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/api/create"
            payload = {
                "name": model_name,
                "modelfile": modelfile_content
            }
            
            async with session.post(url, json=payload, headers=self.headers) as response:
                if response.status == 200:
                    logger.info(f"Successfully created custom model: {model_name}")
                    # Refresh available models cache
                    self._available_models = None
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create model {model_name}: {error_text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error creating custom model {model_name}: {e}")
            return False
    
    def _calculate_confidence_score(self,
                                  prompt: str,
                                  response: str,
                                  model: str,
                                  response_time_ms: int) -> float:
        """Calculate AAI-compliant confidence score for local inference"""
        base_confidence = 0.75  # Slightly higher for local models
        
        # Response quality factors
        if len(response) > 100:
            base_confidence += 0.05
        if len(response) > 500:
            base_confidence += 0.03
        
        # Local inference bonus (more predictable)
        base_confidence += 0.02
        
        # Model-specific adjustments
        if "deepseek-r1" in model.lower():
            base_confidence += 0.08  # R1 reasoning bonus
        if "7b" in model.lower():
            base_confidence -= 0.02  # Smaller model penalty
        if "70b" in model.lower():
            base_confidence += 0.03  # Larger model bonus
        
        # Response time factor (local should be consistent)
        if response_time_ms < 5000:
            base_confidence += 0.02
        elif response_time_ms > 30000:
            base_confidence -= 0.05
        
        # Ensure within AAI range
        return max(0.70, min(0.95, base_confidence))
    
    def _estimate_token_count(self, text: str) -> int:
        """Estimate token count from text"""
        # Rough estimation: ~4 characters per token
        return len(text) // 4
    
    async def get_model_info(self, model: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        try:
            session = await self._get_session()
            url = f"{self.base_url}/api/show"
            payload = {"name": model}
            
            async with session.post(url, json=payload, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"Model {model} not found"}
                    
        except Exception as e:
            return {"error": str(e)}
    
    async def close(self):
        """Close the client session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()


async def test_ollama_client():
    """Test Ollama client functionality"""
    
    async with OllamaClient() as client:
        # Check available models
        print("Checking available models...")
        models = await client._get_available_models()
        print(f"Available models: {models}")
        
        if not models:
            print("No models available. Consider pulling a model:")
            print("ollama pull llama3.2:3b")
            return
        
        # Test basic generation with first available model
        test_model = models[0]
        print(f"\nTesting basic generation with {test_model}...")
        
        result = await client.generate(
            prompt="What are the benefits of using local AI models?",
            model=test_model,
            max_tokens=200,
            temperature=0.1
        )
        
        print(f"Success: {result['success']}")
        if result['success']:
            print(f"Response: {result['text'][:200]}...")
            print(f"Confidence: {result['confidence_score']}")
            print(f"Response time: {result['response_time_ms']}ms")
        else:
            print(f"Error: {result['error']}")
        
        # Test reasoning if DeepSeek R1 model available
        r1_models = [m for m in models if "deepseek" in m.lower() and "r1" in m.lower()]
        if r1_models:
            print(f"\nTesting reasoning with {r1_models[0]}...")
            reasoning_result = await client.generate_reasoning(
                query="Should we use local AI models for reasoning tasks?",
                context="We have GPU resources and want to maintain data privacy",
                model=r1_models[0]
            )
            
            print(f"Success: {reasoning_result['success']}")
            if reasoning_result['success']:
                print(f"Reasoning steps: {len(reasoning_result.get('reasoning_steps', []))}")
                print(f"Conclusion: {reasoning_result.get('final_conclusion', 'N/A')[:100]}...")


if __name__ == "__main__":
    asyncio.run(test_ollama_client())