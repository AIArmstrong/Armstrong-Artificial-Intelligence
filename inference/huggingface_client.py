"""
HuggingFace Inference Client for R1 Reasoning Engine

Handles DeepSeek R1 and other model inference via HuggingFace Hub API
with streaming, timeout handling, and AAI confidence scoring.
"""
import asyncio
import time
import json
from typing import Dict, Any, Optional, AsyncGenerator
import logging

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    
from agents.r1_reasoning.config import R1ReasoningConfig

logger = logging.getLogger(__name__)


class HuggingFaceClient:
    """
    HuggingFace inference client with AAI patterns.
    
    Features:
    - DeepSeek R1 optimized prompting
    - Streaming response handling
    - Timeout and retry logic
    - AAI confidence scoring
    - Token usage tracking
    """
    
    def __init__(self, config: R1ReasoningConfig = None):
        """Initialize HuggingFace client"""
        self.config = config or R1ReasoningConfig()
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            "Authorization": f"Bearer {self.config.HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Rate limiting
        self.last_request_time = 0.0
        self.min_request_interval = 1.0  # Minimum seconds between requests
        
        # Session for connection pooling
        self._session: Optional[aiohttp.ClientSession] = None
    
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
        Generate text using HuggingFace model.
        
        Args:
            prompt: Input prompt
            model: Model name (e.g., "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B")
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            timeout: Request timeout in seconds
            stream: Whether to stream response
            
        Returns:
            Dict containing generated text and metadata
        """
        start_time = time.time()
        
        # Rate limiting
        await self._apply_rate_limiting()
        
        # Prepare request
        url = f"{self.base_url}/{model}"
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "do_sample": temperature > 0.0,
                "return_full_text": False,
                "use_cache": False
            },
            "options": {
                "wait_for_model": True,
                "use_cache": False
            }
        }
        
        if stream:
            payload["stream"] = True
        
        try:
            session = await self._get_session()
            
            async with session.post(url, json=payload, headers=self.headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"HuggingFace API error {response.status}: {error_text}")
                
                if stream:
                    # Handle streaming response
                    generated_text = ""
                    async for chunk in self._process_streaming_response(response):
                        generated_text += chunk
                    result_text = generated_text
                else:
                    # Handle standard response
                    result = await response.json()
                    if isinstance(result, list) and len(result) > 0:
                        result_text = result[0].get("generated_text", "")
                    else:
                        result_text = result.get("generated_text", "")
                
                response_time_ms = int((time.time() - start_time) * 1000)
                
                # Calculate confidence score based on response quality
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
            logger.error(f"HuggingFace request timeout for model {model}")
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
            logger.error(f"HuggingFace generation failed for model {model}: {e}")
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
        """Process streaming response from HuggingFace"""
        buffer = ""
        
        async for chunk in response.content.iter_chunked(1024):
            buffer += chunk.decode('utf-8', errors='ignore')
            
            # Process complete lines
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                line = line.strip()
                
                if line.startswith('data: '):
                    try:
                        data = json.loads(line[6:])  # Remove 'data: ' prefix
                        if 'token' in data:
                            yield data['token']['text']
                        elif 'generated_text' in data:
                            yield data['generated_text']
                    except json.JSONDecodeError:
                        continue
    
    async def generate_reasoning(self,
                               query: str,
                               context: Optional[str] = None,
                               model: str = None) -> Dict[str, Any]:
        """
        Generate structured reasoning using DeepSeek R1.
        
        Args:
            query: Question or problem to reason about
            context: Optional context information
            model: Model to use (defaults to configured reasoning model)
            
        Returns:
            Dict with reasoning chain and confidence scores
        """
        model = model or self.config.REASONING_MODEL
        
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
        """Build optimized reasoning prompt for DeepSeek R1"""
        
        prompt_parts = [
            "You are an AI assistant that provides structured reasoning and analysis.",
            "Your task is to analyze the given query and provide step-by-step reasoning.",
            "",
            "Guidelines:",
            "- Break down your reasoning into clear, logical steps",
            "- Provide confidence scores for each step (70-95%)",
            "- Identify assumptions and evidence",
            "- Give a final conclusion with overall confidence",
            "",
            "Format your response as:",
            "## Reasoning Steps",
            "1. [Step description] (Confidence: XX%)",
            "   Reasoning: [detailed reasoning]",
            "   Evidence: [supporting evidence]",
            "   Assumptions: [key assumptions]",
            "",
            "## Final Conclusion",
            "[Your conclusion] (Overall Confidence: XX%)",
            "",
        ]
        
        if context:
            prompt_parts.extend([
                "## Context Information",
                context,
                ""
            ])
        
        prompt_parts.extend([
            "## Query",
            query,
            "",
            "## Response"
        ])
        
        return "\n".join(prompt_parts)
    
    def _parse_reasoning_output(self, output: str) -> Dict[str, Any]:
        """Parse structured reasoning from R1 output"""
        reasoning_data = {
            "reasoning_steps": [],
            "final_conclusion": "",
            "reasoning_confidence": 0.70,
            "evidence_quality": 0.5,
            "assumption_risk": 0.5
        }
        
        try:
            lines = output.split('\n')
            current_step = None
            in_conclusion = False
            
            for line in lines:
                line = line.strip()
                
                # Parse reasoning steps
                if line.startswith(('#', '##')) and 'reasoning steps' in line.lower():
                    in_conclusion = False
                    continue
                elif line.startswith(('#', '##')) and 'conclusion' in line.lower():
                    in_conclusion = True
                    continue
                
                # Parse numbered steps
                if line and line[0].isdigit() and '.' in line:
                    # Extract step and confidence
                    step_text = line
                    confidence = 0.70
                    
                    # Look for confidence score
                    if 'confidence:' in line.lower():
                        import re
                        conf_match = re.search(r'confidence:\s*(\d+)%', line.lower())
                        if conf_match:
                            confidence = min(0.95, max(0.70, int(conf_match.group(1)) / 100))
                    
                    current_step = {
                        "description": step_text,
                        "confidence": confidence,
                        "reasoning": "",
                        "evidence": [],
                        "assumptions": []
                    }
                    reasoning_data["reasoning_steps"].append(current_step)
                
                # Parse step details
                elif current_step and not in_conclusion:
                    if line.lower().startswith('reasoning:'):
                        current_step["reasoning"] = line[10:].strip()
                    elif line.lower().startswith('evidence:'):
                        current_step["evidence"] = [line[9:].strip()]
                    elif line.lower().startswith('assumptions:'):
                        current_step["assumptions"] = [line[12:].strip()]
                
                # Parse conclusion
                elif in_conclusion and line:
                    reasoning_data["final_conclusion"] = line
                    
                    # Extract overall confidence
                    if 'confidence:' in line.lower():
                        import re
                        conf_match = re.search(r'confidence:\s*(\d+)%', line.lower())
                        if conf_match:
                            reasoning_data["reasoning_confidence"] = min(0.95, max(0.70, int(conf_match.group(1)) / 100))
            
            # Calculate evidence quality and assumption risk
            if reasoning_data["reasoning_steps"]:
                avg_confidence = sum(step["confidence"] for step in reasoning_data["reasoning_steps"]) / len(reasoning_data["reasoning_steps"])
                reasoning_data["evidence_quality"] = min(1.0, avg_confidence * 1.2)
                reasoning_data["assumption_risk"] = max(0.0, 1.0 - avg_confidence)
            
        except Exception as e:
            logger.warning(f"Failed to parse reasoning output: {e}")
        
        return reasoning_data
    
    def _calculate_confidence_score(self,
                                  prompt: str,
                                  response: str,
                                  model: str,
                                  response_time_ms: int) -> float:
        """Calculate AAI-compliant confidence score"""
        base_confidence = 0.70  # AAI minimum
        
        # Response length factor
        if len(response) > 100:
            base_confidence += 0.05
        if len(response) > 500:
            base_confidence += 0.05
        
        # Response time factor (faster can indicate cached/confident responses)
        if response_time_ms < 2000:
            base_confidence += 0.03
        elif response_time_ms > 30000:
            base_confidence -= 0.05
        
        # Model-specific adjustments
        if "deepseek-r1" in model.lower():
            base_confidence += 0.10  # R1 models are reasoning-optimized
        
        # Response quality indicators
        quality_indicators = [
            "reasoning:", "evidence:", "conclusion:",
            "analysis:", "step", "because", "therefore"
        ]
        
        quality_count = sum(1 for indicator in quality_indicators 
                          if indicator in response.lower())
        
        if quality_count >= 3:
            base_confidence += 0.05
        
        # Ensure within AAI range
        return max(0.70, min(0.95, base_confidence))
    
    def _estimate_token_count(self, text: str) -> int:
        """Estimate token count from text"""
        # Rough estimation: ~4 characters per token
        return len(text) // 4
    
    async def _apply_rate_limiting(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last)
        
        self.last_request_time = time.time()
    
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


async def test_huggingface_client():
    """Test HuggingFace client functionality"""
    
    async with HuggingFaceClient() as client:
        # Test basic generation
        print("Testing basic generation...")
        result = await client.generate(
            prompt="What are the benefits of FastAPI?",
            model="microsoft/DialoGPT-medium",
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
        
        # Test reasoning generation
        print("\nTesting reasoning generation...")
        reasoning_result = await client.generate_reasoning(
            query="Should we migrate from Django to FastAPI?",
            context="Our current Django app serves 10,000 users with REST APIs"
        )
        
        print(f"Success: {reasoning_result['success']}")
        if reasoning_result['success']:
            print(f"Reasoning steps: {len(reasoning_result.get('reasoning_steps', []))}")
            print(f"Conclusion: {reasoning_result.get('final_conclusion', 'N/A')[:100]}...")
            print(f"Overall confidence: {reasoning_result.get('reasoning_confidence', 0.70)}")


if __name__ == "__main__":
    asyncio.run(test_huggingface_client())