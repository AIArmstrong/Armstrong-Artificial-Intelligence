#!/usr/bin/env python3
"""
OpenRouter Integration - LLM-powered semantic analysis with rate limiting
Provides structured outputs and unified API access to 40+ models
"""

import asyncio
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Type, TypeVar
from dataclasses import dataclass
from openai import AsyncOpenAI
import instructor
from pydantic import BaseModel
import backoff

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

@dataclass
class RateLimitConfig:
    """Rate limiting configuration"""
    requests_per_minute: int = 60
    requests_per_hour: int = 3600
    max_concurrent: int = 5
    backoff_factor: float = 2.0
    max_retries: int = 3

@dataclass
class UsageStats:
    """Track API usage statistics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    rate_limited_requests: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    last_reset: datetime = None

class RateLimiter:
    """
    Rate limiter for API requests with sliding window.
    """
    
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.request_times: List[datetime] = []
        self.semaphore = asyncio.Semaphore(config.max_concurrent)
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> bool:
        """
        Acquire rate limit permission.
        
        Returns:
            True if request can proceed
        """
        async with self._lock:
            now = datetime.now()
            
            # Clean old timestamps
            cutoff_minute = now - timedelta(minutes=1)
            cutoff_hour = now - timedelta(hours=1)
            
            self.request_times = [
                t for t in self.request_times if t > cutoff_hour
            ]
            
            # Check limits
            recent_minute = [t for t in self.request_times if t > cutoff_minute]
            
            if len(recent_minute) >= self.config.requests_per_minute:
                logger.warning("Rate limit exceeded: requests per minute")
                return False
            
            if len(self.request_times) >= self.config.requests_per_hour:
                logger.warning("Rate limit exceeded: requests per hour")
                return False
            
            # Record this request
            self.request_times.append(now)
            return True
    
    async def wait_if_needed(self) -> None:
        """Wait if rate limit is exceeded"""
        while not await self.acquire():
            await asyncio.sleep(1)

class OpenRouterIntegration:
    """
    OpenRouter API integration with rate limiting and structured outputs.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 base_url: str = "https://openrouter.ai/api/v1",
                 rate_limit_config: Optional[RateLimitConfig] = None):
        """
        Initialize OpenRouter integration.
        
        Args:
            api_key: OpenRouter API key (or from environment)
            base_url: API base URL
            rate_limit_config: Rate limiting configuration
        """
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key required")
        
        self.base_url = base_url
        self.rate_limit_config = rate_limit_config or RateLimitConfig()
        self.rate_limiter = RateLimiter(self.rate_limit_config)
        self.usage_stats = UsageStats(last_reset=datetime.now())
        
        # Initialize OpenAI client with OpenRouter
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=base_url
        )
        
        # Initialize Instructor for structured outputs
        self.instructor_client = instructor.from_openai(self.client)
        
        # Model configurations
        self.models = {
            'fast': 'anthropic/claude-3-haiku-20240307',
            'balanced': 'anthropic/claude-3-sonnet-20240229',
            'powerful': 'anthropic/claude-3-opus-20240229',
            'code': 'meta-llama/codellama-34b-instruct',
            'reasoning': 'openai/gpt-4-turbo'
        }
        
        self.default_model = self.models['balanced']
    
    @backoff.on_exception(
        backoff.expo,
        Exception,
        max_tries=3,
        base=2
    )
    async def complete_structured(self,
                                model: str,
                                messages: List[Dict[str, str]],
                                response_model: Type[T],
                                temperature: float = 0.3,
                                max_tokens: int = 1000,
                                **kwargs) -> T:
        """
        Get structured completion from OpenRouter.
        
        Args:
            model: Model name or alias
            messages: Chat messages
            response_model: Pydantic model for response structure
            temperature: Response randomness
            max_tokens: Maximum tokens
            **kwargs: Additional parameters
            
        Returns:
            Structured response matching response_model
        """
        # Resolve model alias
        actual_model = self.models.get(model, model)
        
        # Wait for rate limit if needed
        await self.rate_limiter.wait_if_needed()
        
        async with self.rate_limiter.semaphore:
            try:
                start_time = time.time()
                
                # Make request with instructor
                response = await self.instructor_client.chat.completions.create(
                    model=actual_model,
                    messages=messages,
                    response_model=response_model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                
                # Update usage stats
                self.usage_stats.total_requests += 1
                self.usage_stats.successful_requests += 1
                
                logger.debug(f"Structured completion took {time.time() - start_time:.2f}s")
                
                return response
                
            except Exception as e:
                self.usage_stats.total_requests += 1
                self.usage_stats.failed_requests += 1
                
                if "rate limit" in str(e).lower():
                    self.usage_stats.rate_limited_requests += 1
                
                logger.error(f"OpenRouter request failed: {e}")
                raise
    
    async def complete_text(self,
                          model: str,
                          messages: List[Dict[str, str]],
                          temperature: float = 0.7,
                          max_tokens: int = 1000,
                          **kwargs) -> str:
        """
        Get text completion from OpenRouter.
        
        Args:
            model: Model name or alias
            messages: Chat messages
            temperature: Response randomness
            max_tokens: Maximum tokens
            **kwargs: Additional parameters
            
        Returns:
            Response text
        """
        # Resolve model alias
        actual_model = self.models.get(model, model)
        
        # Wait for rate limit if needed
        await self.rate_limiter.wait_if_needed()
        
        async with self.rate_limiter.semaphore:
            try:
                start_time = time.time()
                
                response = await self.client.chat.completions.create(
                    model=actual_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                
                # Update usage stats
                self.usage_stats.total_requests += 1
                self.usage_stats.successful_requests += 1
                
                if hasattr(response, 'usage') and response.usage:
                    self.usage_stats.total_tokens += response.usage.total_tokens
                
                logger.debug(f"Text completion took {time.time() - start_time:.2f}s")
                
                return response.choices[0].message.content
                
            except Exception as e:
                self.usage_stats.total_requests += 1
                self.usage_stats.failed_requests += 1
                
                if "rate limit" in str(e).lower():
                    self.usage_stats.rate_limited_requests += 1
                
                logger.error(f"OpenRouter request failed: {e}")
                raise
    
    async def analyze_code_intent(self,
                                code: str,
                                language: str,
                                analysis_type: str = "semantic") -> Dict[str, Any]:
        """
        Analyze code intent using structured output.
        
        Args:
            code: Source code to analyze
            language: Programming language
            analysis_type: Type of analysis to perform
            
        Returns:
            Structured analysis result
        """
        # Define response model
        class CodeAnalysis(BaseModel):
            primary_purpose: str
            business_logic: str
            complexity_assessment: str
            potential_issues: List[str]
            suggestions: List[str]
            confidence: float
        
        # Prepare prompt
        messages = [
            {
                "role": "system",
                "content": f"""You are an expert code analyst. Analyze the provided {language} code and provide structured insights about its purpose, logic, and quality."""
            },
            {
                "role": "user",
                "content": f"""Analyze this {language} code:

```{language}
{code}
```

Provide:
1. Primary purpose and functionality
2. Business logic explanation
3. Complexity assessment
4. Potential issues or code smells
5. Improvement suggestions
6. Confidence in your analysis (0.0-1.0)
"""
            }
        ]
        
        try:
            result = await self.complete_structured(
                model='balanced',
                messages=messages,
                response_model=CodeAnalysis,
                temperature=0.3,
                max_tokens=800
            )
            
            return {
                'primary_purpose': result.primary_purpose,
                'business_logic': result.business_logic,
                'complexity': result.complexity_assessment,
                'issues': result.potential_issues,
                'suggestions': result.suggestions,
                'confidence': result.confidence,
                'analysis_type': analysis_type
            }
            
        except Exception as e:
            logger.error(f"Code analysis failed: {e}")
            return {
                'error': str(e),
                'analysis_type': analysis_type,
                'confidence': 0.0
            }
    
    async def detect_patterns(self,
                            code: str,
                            language: str) -> Dict[str, Any]:
        """
        Detect design patterns and architectural patterns in code.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            Detected patterns and confidence scores
        """
        class PatternDetection(BaseModel):
            design_patterns: List[str]
            architectural_patterns: List[str]
            anti_patterns: List[str]
            pattern_confidence: Dict[str, float]
            explanation: str
        
        messages = [
            {
                "role": "system",
                "content": "You are an expert in software design patterns and architecture. Identify patterns in the provided code."
            },
            {
                "role": "user",
                "content": f"""Analyze this {language} code for patterns:

```{language}
{code}
```

Identify:
1. Design patterns (e.g., Singleton, Factory, Observer)
2. Architectural patterns (e.g., MVC, Repository, Strategy)
3. Anti-patterns or code smells
4. Confidence scores for each identified pattern
5. Brief explanation of findings
"""
            }
        ]
        
        try:
            result = await self.complete_structured(
                model='balanced',
                messages=messages,
                response_model=PatternDetection,
                temperature=0.2,
                max_tokens=600
            )
            
            return {
                'design_patterns': result.design_patterns,
                'architectural_patterns': result.architectural_patterns,
                'anti_patterns': result.anti_patterns,
                'confidence_scores': result.pattern_confidence,
                'explanation': result.explanation
            }
            
        except Exception as e:
            logger.error(f"Pattern detection failed: {e}")
            return {
                'error': str(e),
                'design_patterns': [],
                'architectural_patterns': [],
                'anti_patterns': []
            }
    
    async def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models from OpenRouter"""
        try:
            # Note: This would require a direct API call to OpenRouter's models endpoint
            # For now, return our configured models
            return [
                {'id': model_id, 'alias': alias}
                for alias, model_id in self.models.items()
            ]
        except Exception as e:
            logger.error(f"Failed to get available models: {e}")
            return []
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics"""
        return {
            'total_requests': self.usage_stats.total_requests,
            'successful_requests': self.usage_stats.successful_requests,
            'failed_requests': self.usage_stats.failed_requests,
            'rate_limited_requests': self.usage_stats.rate_limited_requests,
            'success_rate': (
                self.usage_stats.successful_requests / self.usage_stats.total_requests
                if self.usage_stats.total_requests > 0 else 0
            ),
            'total_tokens': self.usage_stats.total_tokens,
            'total_cost': self.usage_stats.total_cost,
            'last_reset': self.usage_stats.last_reset.isoformat(),
            'rate_limit_config': {
                'requests_per_minute': self.rate_limit_config.requests_per_minute,
                'requests_per_hour': self.rate_limit_config.requests_per_hour,
                'max_concurrent': self.rate_limit_config.max_concurrent
            }
        }
    
    def reset_usage_stats(self) -> None:
        """Reset usage statistics"""
        self.usage_stats = UsageStats(last_reset=datetime.now())