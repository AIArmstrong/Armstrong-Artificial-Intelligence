"""
OpenRouter API Client with rate limiting, retry logic, and cost tracking
"""

import os
import time
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
import aiohttp
from dotenv import load_dotenv

load_dotenv()

class OpenRouterClient:
    """
    Intelligent OpenRouter API client with built-in protections
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1"
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY must be set in .env")
        
        # Rate limiting
        self.requests_per_minute = 60
        self.request_timestamps = []
        
        # Cost tracking
        self.cost_log = []
        self.daily_cost_limit = 5.00  # $5 daily limit
        
        # Retry settings
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://aai-system.local",
            "X-Title": "AAI Brain Intelligence System"
        }
    
    def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = time.time()
        # Remove timestamps older than 1 minute
        self.request_timestamps = [ts for ts in self.request_timestamps if now - ts < 60]
        
        if len(self.request_timestamps) >= self.requests_per_minute:
            return False
        
        self.request_timestamps.append(now)
        return True
    
    def _check_daily_cost(self) -> bool:
        """Check if we're within daily cost limits"""
        today = datetime.utcnow().date()
        today_costs = [cost for cost in self.cost_log if cost['date'] == today]
        total_cost = sum(cost['amount'] for cost in today_costs)
        
        return total_cost < self.daily_cost_limit
    
    def _log_cost(self, model: str, tokens: int, cost: float):
        """Log API usage cost"""
        self.cost_log.append({
            "date": datetime.utcnow().date(),
            "timestamp": datetime.utcnow().isoformat(),
            "model": model,
            "tokens": tokens,
            "cost": cost
        })
        
        # Save to file for persistence
        cost_file = "brain/logs/openrouter_costs.json"
        try:
            with open(cost_file, 'w') as f:
                json.dump(self.cost_log, f, indent=2, default=str)
        except Exception as e:
            print(f"Cost logging error: {e}")
    
    async def _make_request(self, endpoint: str, data: Dict[Any, Any]) -> Optional[Dict]:
        """Make API request with rate limiting and retry logic"""
        
        # Check rate limits
        if not self._check_rate_limit():
            await asyncio.sleep(60)  # Wait for rate limit reset
            if not self._check_rate_limit():
                raise Exception("Rate limit exceeded")
        
        # Check cost limits
        if not self._check_daily_cost():
            raise Exception("Daily cost limit reached")
        
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=self.headers, json=data) as response:
                        if response.status == 200:
                            result = await response.json()
                            
                            # Log usage and cost
                            if 'usage' in result:
                                usage = result['usage']
                                tokens = usage.get('total_tokens', 0)
                                # Rough cost estimation (update with actual pricing)
                                estimated_cost = tokens * 0.00001  # $0.00001 per token estimate
                                self._log_cost(data.get('model', 'unknown'), tokens, estimated_cost)
                            
                            return result
                        elif response.status == 429:  # Rate limited
                            wait_time = self.retry_delay * (2 ** attempt)
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            error_text = await response.text()
                            print(f"API Error {response.status}: {error_text}")
                            return None
                            
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"Final attempt failed: {e}")
                    return None
                else:
                    wait_time = self.retry_delay * (2 ** attempt)
                    await asyncio.sleep(wait_time)
        
        return None
    
    async def generate_embeddings(self, texts: List[str], model: str = "text-embedding-ada-002") -> Optional[List[List[float]]]:
        """
        Generate embeddings for text inputs
        Returns list of embedding vectors (1536 dimensions for ada-002)
        """
        data = {
            "model": model,
            "input": texts
        }
        
        result = await self._make_request("embeddings", data)
        
        if result and 'data' in result:
            return [item['embedding'] for item in result['data']]
        
        return None
    
    async def analyze_contradiction(self, current_text: str, existing_context: str, model: str = "openai/gpt-4o-mini") -> Optional[Dict]:
        """
        Use LLM to detect contradictions between current text and existing context
        """
        prompt = f"""
        Analyze the following for logical contradictions or conflicts:

        CURRENT TEXT:
        {current_text}

        EXISTING CONTEXT:
        {existing_context}

        Respond with JSON format:
        {{
            "has_contradiction": boolean,
            "confidence": float (0-1),
            "contradiction_type": "logical|temporal|architectural|process",
            "description": "brief explanation if contradiction found",
            "suggested_resolution": "how to resolve if contradiction found"
        }}
        """
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are an expert at detecting logical contradictions and conflicts in technical documentation."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 500
        }
        
        result = await self._make_request("chat/completions", data)
        
        if result and 'choices' in result:
            try:
                content = result['choices'][0]['message']['content']
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "has_contradiction": False,
                    "confidence": 0.0,
                    "error": "Failed to parse LLM response as JSON"
                }
        
        return None
    
    def get_daily_usage(self) -> Dict[str, Any]:
        """Get today's usage statistics"""
        today = datetime.utcnow().date()
        today_costs = [cost for cost in self.cost_log if cost['date'] == today]
        
        total_cost = sum(cost['amount'] for cost in today_costs)
        total_tokens = sum(cost['tokens'] for cost in today_costs)
        request_count = len(today_costs)
        
        return {
            "date": today,
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "request_count": request_count,
            "cost_limit": self.daily_cost_limit,
            "remaining_budget": self.daily_cost_limit - total_cost
        }

# Singleton instance for brain system
_client = None

def get_openrouter_client() -> OpenRouterClient:
    """Get singleton OpenRouter client instance"""
    global _client
    if _client is None:
        _client = OpenRouterClient()
    return _client

if __name__ == "__main__":
    # Test basic functionality
    async def test_client():
        client = OpenRouterClient()
        
        # Test embeddings
        embeddings = await client.generate_embeddings(["test intent pattern"])
        if embeddings:
            print(f"Embedding dimensions: {len(embeddings[0])}")
        
        # Test contradiction detection
        contradiction = await client.analyze_contradiction(
            "Use MySQL for database",
            "We decided to use Supabase for all data storage"
        )
        if contradiction:
            print(f"Contradiction detected: {contradiction}")
        
        # Show usage
        usage = client.get_daily_usage()
        print(f"Daily usage: {usage}")
    
    asyncio.run(test_client())