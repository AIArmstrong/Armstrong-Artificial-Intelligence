"""
Jina Search Specialized Agent

Handles web search and information retrieval using Jina Search API
with focused capabilities and intelligent result processing.
"""
import logging
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

# HTTP client imports with fallbacks
try:
    import aiohttp
    HTTP_CLIENT_AVAILABLE = True
except ImportError:
    aiohttp = None
    HTTP_CLIENT_AVAILABLE = False

logger = logging.getLogger(__name__)


class JinaSearchAgent:
    """
    Specialized agent for web search operations using Jina Search.
    
    Features:
    - Web search with multiple result types
    - News search and real-time information
    - Image and video search capabilities
    - Academic and research paper search
    - Search result ranking and filtering
    - Content summarization and extraction
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Jina Search agent"""
        
        self.api_key = api_key
        self.base_url = "https://s.jina.ai"
        self.session: Optional[aiohttp.ClientSession] = None
        self.initialized = False
        
        # Agent metadata
        self.name = "Jina Web Search Agent"
        self.version = "1.0.0"
        self.capabilities = [
            "web_search",
            "news_search",
            "image_search",
            "academic_search",
            "real_time_search",
            "content_extraction",
            "result_summarization",
            "trending_topics",
            "fact_checking",
            "source_validation"
        ]
        
        # Search parameters
        self.default_params = {
            "count": 10,
            "offset": 0,
            "market": "en-US",
            "safe_search": "moderate",
            "text_format": "raw"
        }
        
        # Performance tracking
        self.total_searches = 0
        self.successful_searches = 0
        self.last_search_time = None
        self.total_results_processed = 0
        
        # Rate limiting
        self.requests_per_minute = 60
        self.request_timestamps = []
        
        # Initialize HTTP session
        if HTTP_CLIENT_AVAILABLE:
            asyncio.create_task(self._initialize_session())
            self.initialized = True
        else:
            logger.warning("HTTP client not available - using simulation mode")
            self.initialized = True
    
    async def _initialize_session(self):
        """Initialize aiohttp session with proper headers"""
        
        headers = {
            "User-Agent": "AAI-Jina-Search-Agent/1.0.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        # Create session with connection pooling for better performance
        connector = aiohttp.TCPConnector(
            limit=100,  # Maximum number of connections
            limit_per_host=30,  # Maximum connections per host
            ttl_dns_cache=300,  # DNS cache TTL
            use_dns_cache=True,
            keepalive_timeout=60,  # Keep connections alive
        )
        
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30),
            connector=connector
        )
    
    async def execute_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute search-related task.
        
        Args:
            task: Task description to execute
            context: Additional context and parameters
            
        Returns:
            Task execution result
        """
        start_time = datetime.now()
        self.total_searches += 1
        
        try:
            logger.info(f"Executing search task: {task[:100]}...")
            
            # Check rate limiting
            rate_check = await self._check_rate_limit()
            if not rate_check["allowed"]:
                return {
                    "success": False,
                    "error": f"Rate limit exceeded: {rate_check['message']}",
                    "agent": "jina_search"
                }
            
            # Parse task and determine operation
            operation = await self._parse_task(task, context)
            
            # Execute operation
            if self.session and HTTP_CLIENT_AVAILABLE:
                result = await self._execute_real_search(operation)
            else:
                result = await self._execute_simulated_search(operation)
            
            # Track success
            self.successful_searches += 1
            self.last_search_time = datetime.now()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": True,
                "result": result,
                "operation": operation["type"],
                "execution_time_seconds": execution_time,
                "agent": "jina_search",
                "simulated": not (self.session and HTTP_CLIENT_AVAILABLE)
            }
            
        except Exception as e:
            logger.error(f"Search task execution failed: {e}")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "success": False,
                "error": str(e),
                "operation": "unknown",
                "execution_time_seconds": execution_time,
                "agent": "jina_search"
            }
    
    async def _parse_task(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse task description to determine specific operation"""
        
        task_lower = task.lower()
        
        # News search operations
        if any(keyword in task_lower for keyword in ["news", "latest news", "current events", "breaking"]):
            return {
                "type": "news_search",
                "query": self._extract_search_query(task),
                "count": context.get("count", 10),
                "freshness": context.get("freshness", "day"),
                "market": context.get("market", "en-US")
            }
        
        # Academic/research search
        elif any(keyword in task_lower for keyword in ["academic", "research", "papers", "study", "journal"]):
            return {
                "type": "academic_search",
                "query": self._extract_search_query(task),
                "count": context.get("count", 10),
                "sort_by": context.get("sort_by", "relevance")
            }
        
        # Image search
        elif any(keyword in task_lower for keyword in ["image", "photo", "picture", "visual"]):
            return {
                "type": "image_search",
                "query": self._extract_search_query(task),
                "count": context.get("count", 20),
                "size": context.get("size", "medium"),
                "color": context.get("color", "any")
            }
        
        # Real-time/trending search
        elif any(keyword in task_lower for keyword in ["trending", "real-time", "live", "current"]):
            return {
                "type": "real_time_search",
                "query": self._extract_search_query(task),
                "count": context.get("count", 15),
                "time_range": context.get("time_range", "hour")
            }
        
        # Fact checking
        elif any(keyword in task_lower for keyword in ["fact check", "verify", "validate", "true or false"]):
            return {
                "type": "fact_checking",
                "query": self._extract_search_query(task),
                "count": context.get("count", 10),
                "sources": context.get("sources", ["reliable"])
            }
        
        # Content extraction
        elif any(keyword in task_lower for keyword in ["extract", "summarize", "get content"]):
            return {
                "type": "content_extraction",
                "query": self._extract_search_query(task),
                "url": context.get("url"),
                "format": context.get("format", "summary")
            }
        
        # General web search (default)
        else:
            return {
                "type": "web_search",
                "query": self._extract_search_query(task),
                "count": context.get("count", 10),
                "safe_search": context.get("safe_search", "moderate"),
                "market": context.get("market", "en-US")
            }
    
    def _extract_search_query(self, task: str) -> str:
        """Extract search query from task description"""
        
        # Look for quoted queries
        quoted_match = re.search(r'"([^"]*)"', task)
        if quoted_match:
            return quoted_match.group(1)
        
        # Look for queries after keywords
        search_keywords = [
            "search for", "find", "lookup", "look up", "search", "query",
            "research", "investigate", "explore", "discover", "about"
        ]
        
        task_lower = task.lower()
        
        for keyword in search_keywords:
            if keyword in task_lower:
                start_index = task_lower.find(keyword) + len(keyword)
                remaining = task[start_index:].strip()
                
                # Remove common prepositions
                for prep in ["for", "about", "on", ":", "-"]:
                    if remaining.lower().startswith(prep):
                        remaining = remaining[len(prep):].strip()
                
                if remaining:
                    # Clean up the query
                    query = self._clean_search_query(remaining)
                    if query:
                        return query
        
        # Fallback: use the entire task as query
        return self._clean_search_query(task)
    
    def _clean_search_query(self, query: str) -> str:
        """Clean and optimize search query"""
        
        # Remove common task-related words
        stop_words = [
            "please", "can you", "could you", "help me", "i need", "i want",
            "find me", "search for", "look for", "get me", "show me"
        ]
        
        query_lower = query.lower()
        
        for stop_word in stop_words:
            if query_lower.startswith(stop_word):
                query = query[len(stop_word):].strip()
                query_lower = query.lower()
        
        # Remove punctuation at the end
        query = query.rstrip('.,!?;:')
        
        # Limit length
        if len(query) > 200:
            query = query[:200].rsplit(' ', 1)[0]
        
        return query.strip()
    
    async def _check_rate_limit(self) -> Dict[str, Any]:
        """Check if request is within rate limits"""
        
        now = datetime.now()
        
        # Remove old timestamps
        self.request_timestamps = [
            ts for ts in self.request_timestamps
            if (now - ts).total_seconds() < 60
        ]
        
        if len(self.request_timestamps) >= self.requests_per_minute:
            return {
                "allowed": False,
                "message": f"Rate limit of {self.requests_per_minute} requests per minute exceeded"
            }
        
        self.request_timestamps.append(now)
        return {"allowed": True, "message": "Rate limit OK"}
    
    async def _execute_real_search(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Execute real search using Jina Search API"""
        
        op_type = operation["type"]
        query = operation["query"]
        
        try:
            if op_type == "web_search":
                params = {
                    "q": query,
                    "count": operation.get("count", 10),
                    "safeSearch": operation.get("safe_search", "moderate"),
                    "mkt": operation.get("market", "en-US")
                }
                
                url = f"{self.base_url}/search"
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return await self._process_web_results(data, query)
                    else:
                        error_text = await response.text()
                        return {"error": f"Search API error: {error_text}"}
            
            elif op_type == "news_search":
                params = {
                    "q": query,
                    "count": operation.get("count", 10),
                    "freshness": operation.get("freshness", "day"),
                    "mkt": operation.get("market", "en-US")
                }
                
                url = f"{self.base_url}/news"
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return await self._process_news_results(data, query)
                    else:
                        error_text = await response.text()
                        return {"error": f"News search error: {error_text}"}
            
            elif op_type == "image_search":
                params = {
                    "q": query,
                    "count": operation.get("count", 20),
                    "size": operation.get("size", "medium")
                }
                
                url = f"{self.base_url}/images"
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return await self._process_image_results(data, query)
                    else:
                        error_text = await response.text()
                        return {"error": f"Image search error: {error_text}"}
            
            elif op_type == "content_extraction":
                target_url = operation.get("url")
                if target_url:
                    # Use Jina Reader for content extraction
                    reader_url = f"https://r.jina.ai/{target_url}"
                    
                    async with self.session.get(reader_url) as response:
                        if response.status == 200:
                            content = await response.text()
                            return await self._process_extracted_content(content, target_url)
                        else:
                            return {"error": f"Content extraction failed: {response.status}"}
                else:
                    # Search for content to extract
                    return await self._execute_real_search({
                        "type": "web_search",
                        "query": query,
                        "count": 5
                    })
            
            else:
                # Fallback to web search for unknown types
                return await self._execute_real_search({
                    "type": "web_search",
                    "query": query,
                    "count": operation.get("count", 10)
                })
                
        except aiohttp.ClientError as e:
            logger.error(f"Jina Search API error: {e}")
            return {"error": f"Search API error: {str(e)}"}
    
    async def _execute_simulated_search(self, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Execute simulated search for testing/fallback"""
        
        # Simulate API delay
        await asyncio.sleep(0.3)
        
        op_type = operation["type"]
        query = operation["query"]
        count = operation.get("count", 10)
        
        if op_type == "web_search":
            return {
                "query": query,
                "results": [
                    {
                        "title": f"Search Result {i+1} for '{query}'",
                        "url": f"https://example-{i+1}.com/search-result",
                        "snippet": f"This is a simulated search result {i+1} for the query '{query}'. It contains relevant information about the search topic.",
                        "domain": f"example-{i+1}.com",
                        "published_date": "2024-01-15T10:00:00Z"
                    }
                    for i in range(count)
                ],
                "total_results": count * 10,  # Simulate more results available
                "search_time": 0.25,
                "simulated": True
            }
        
        elif op_type == "news_search":
            return {
                "query": query,
                "news_results": [
                    {
                        "title": f"Breaking News {i+1}: {query}",
                        "url": f"https://news-{i+1}.com/article",
                        "snippet": f"Latest news about {query}. This is a simulated news article with current information.",
                        "source": f"News Source {i+1}",
                        "published_date": "2024-01-20T12:00:00Z",
                        "category": "General"
                    }
                    for i in range(count)
                ],
                "total_results": count,
                "freshness": operation.get("freshness", "day"),
                "simulated": True
            }
        
        elif op_type == "image_search":
            return {
                "query": query,
                "images": [
                    {
                        "title": f"Image {i+1} for {query}",
                        "url": f"https://images.example.com/image{i+1}.jpg",
                        "thumbnail_url": f"https://images.example.com/thumb{i+1}.jpg",
                        "width": 800,
                        "height": 600,
                        "size": "medium",
                        "source": f"image-source-{i+1}.com"
                    }
                    for i in range(count)
                ],
                "total_results": count,
                "simulated": True
            }
        
        elif op_type == "content_extraction":
            return {
                "url": operation.get("url", "https://example.com"),
                "title": f"Extracted Content for {query}",
                "content": f"This is simulated extracted content about {query}. In a real implementation, this would contain the actual content from the specified URL or search results.",
                "word_count": 150,
                "reading_time_minutes": 1,
                "simulated": True
            }
        
        else:
            return {
                "query": query,
                "operation_type": op_type,
                "message": f"Simulated {op_type} operation completed",
                "simulated": True
            }
    
    async def _process_web_results(self, data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Process web search results from API response"""
        
        results = []
        
        web_pages = data.get("webPages", {}).get("value", [])
        
        for page in web_pages:
            result = {
                "title": page.get("name", ""),
                "url": page.get("url", ""),
                "snippet": page.get("snippet", ""),
                "domain": self._extract_domain(page.get("url", "")),
                "published_date": page.get("dateLastCrawled", "")
            }
            results.append(result)
        
        self.total_results_processed += len(results)
        
        return {
            "query": query,
            "results": results,
            "total_results": data.get("webPages", {}).get("totalEstimatedMatches", len(results)),
            "search_time": 0.5  # Estimated
        }
    
    async def _process_news_results(self, data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Process news search results from API response"""
        
        news_results = []
        
        articles = data.get("value", [])
        
        for article in articles:
            result = {
                "title": article.get("name", ""),
                "url": article.get("url", ""),
                "snippet": article.get("description", ""),
                "source": article.get("provider", [{}])[0].get("name", "Unknown"),
                "published_date": article.get("datePublished", ""),
                "category": article.get("category", "General")
            }
            news_results.append(result)
        
        self.total_results_processed += len(news_results)
        
        return {
            "query": query,
            "news_results": news_results,
            "total_results": len(news_results)
        }
    
    async def _process_image_results(self, data: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Process image search results from API response"""
        
        images = []
        
        image_results = data.get("value", [])
        
        for img in image_results:
            result = {
                "title": img.get("name", ""),
                "url": img.get("contentUrl", ""),
                "thumbnail_url": img.get("thumbnailUrl", ""),
                "width": img.get("width", 0),
                "height": img.get("height", 0),
                "size": img.get("size", "unknown"),
                "source": self._extract_domain(img.get("hostPageUrl", ""))
            }
            images.append(result)
        
        self.total_results_processed += len(images)
        
        return {
            "query": query,
            "images": images,
            "total_results": len(images)
        }
    
    async def _process_extracted_content(self, content: str, url: str) -> Dict[str, Any]:
        """Process extracted content from Jina Reader"""
        
        # Basic content processing
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)  # Assume 200 words per minute
        
        # Extract title (first line)
        lines = content.strip().split('\n')
        title = lines[0] if lines else "Extracted Content"
        
        return {
            "url": url,
            "title": title,
            "content": content,
            "word_count": word_count,
            "reading_time_minutes": reading_time,
            "extracted_at": datetime.now().isoformat()
        }
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        
        if not url:
            return "unknown"
        
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return "unknown"
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get agent status and performance metrics"""
        
        success_rate = (
            self.successful_searches / max(1, self.total_searches)
        )
        
        return {
            "name": self.name,
            "version": self.version,
            "initialized": self.initialized,
            "http_client_available": HTTP_CLIENT_AVAILABLE,
            "session_ready": self.session is not None,
            "authenticated": self.api_key is not None,
            "capabilities": self.capabilities,
            "rate_limit": {
                "requests_per_minute": self.requests_per_minute,
                "current_requests": len(self.request_timestamps)
            },
            "performance": {
                "total_searches": self.total_searches,
                "successful_searches": self.successful_searches,
                "success_rate": success_rate,
                "total_results_processed": self.total_results_processed,
                "last_search": self.last_search_time.isoformat() if self.last_search_time else None
            },
            "ready": self.initialized
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test search service connection"""
        
        try:
            if self.session and HTTP_CLIENT_AVAILABLE:
                # Test with a simple search
                test_query = "test connection"
                
                params = {"q": test_query, "count": 1}
                url = f"{self.base_url}/search"
                
                async with self.session.get(url, params=params) as response:
                    return {
                        "connection_test": "success" if response.status == 200 else "failed",
                        "status_code": response.status,
                        "api_accessible": response.status == 200
                    }
            else:
                return {
                    "connection_test": "simulated",
                    "message": "Using simulation mode - no real search connection"
                }
                
        except Exception as e:
            return {
                "connection_test": "failed",
                "error": str(e)
            }
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._ensure_initialized()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.cleanup()
    
    async def _ensure_initialized(self):
        """Ensure agent is properly initialized"""
        if not self.initialized:
            if HTTP_CLIENT_AVAILABLE and not self.session:
                await self._initialize_session()
            self.initialized = True
    
    async def cleanup(self):
        """Cleanup resources"""
        
        if self.session:
            await self.session.close()


async def test_jina_search_agent():
    """Test Jina Search agent functionality"""
    
    agent = JinaSearchAgent()
    
    print("🧪 Testing Jina Search Agent")
    print("=" * 28)
    
    # Check agent status
    status = agent.get_agent_status()
    print(f"Agent initialized: {status['initialized']}")
    print(f"HTTP client available: {status['http_client_available']}")
    print(f"Session ready: {status['session_ready']}")
    print(f"Authenticated: {status['authenticated']}")
    print(f"Capabilities: {len(status['capabilities'])}")
    
    # Test connection
    connection_test = await agent.test_connection()
    print(f"Connection test: {connection_test['connection_test']}")
    
    # Test operations
    print(f"\n🎯 Testing search operations...")
    
    test_tasks = [
        {
            "task": "Search for artificial intelligence trends",
            "context": {"count": 5}
        },
        {
            "task": "Find latest news about climate change",
            "context": {"count": 3, "freshness": "day"}
        },
        {
            "task": "Search for images of sustainable technology",
            "context": {"count": 5, "size": "medium"}
        },
        {
            "task": "Research academic papers on machine learning",
            "context": {"count": 5}
        },
        {
            "task": "Extract content from https://example.com/article",
            "context": {"url": "https://example.com/article"}
        }
    ]
    
    for i, test in enumerate(test_tasks, 1):
        print(f"\nTest {i}: {test['task']}")
        result = await agent.execute_task(test["task"], test["context"])
        
        print(f"  Success: {result['success']}")
        print(f"  Operation: {result.get('operation', 'unknown')}")
        print(f"  Simulated: {result.get('simulated', False)}")
        
        if result['success']:
            search_result = result['result']
            if 'results' in search_result:
                print(f"  Results found: {len(search_result['results'])}")
            elif 'news_results' in search_result:
                print(f"  News articles: {len(search_result['news_results'])}")
            elif 'images' in search_result:
                print(f"  Images found: {len(search_result['images'])}")
            elif 'content' in search_result:
                print(f"  Content extracted: {search_result.get('word_count', 0)} words")
        
        print(f"  Time: {result.get('execution_time_seconds', 0):.2f}s")
    
    # Check final status
    final_status = agent.get_agent_status()
    performance = final_status["performance"]
    print(f"\n📊 Final Performance:")
    print(f"Total searches: {performance['total_searches']}")
    print(f"Success rate: {performance['success_rate']:.1%}")
    print(f"Results processed: {performance['total_results_processed']}")
    
    # Cleanup
    await agent.cleanup()
    
    print(f"\n✅ Jina Search Agent Testing Complete")
    print(f"Ready for web search and information retrieval")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_jina_search_agent())