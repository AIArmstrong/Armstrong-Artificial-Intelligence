"""
Jina Research Integration for R1 Reasoning Engine

Automated research ingestion using Jina Reader API with
AAI patterns, quality assessment, and reasoning optimization.
"""
import logging
import asyncio
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from urllib.parse import urlparse, quote

# HTTP client with fallback
try:
    import aiohttp
    HTTP_AVAILABLE = True
except ImportError:
    try:
        import requests
        HTTP_AVAILABLE = True
        USE_REQUESTS = True
    except ImportError:
        HTTP_AVAILABLE = False

# URL validation and processing
try:
    import validators
    VALIDATORS_AVAILABLE = True
except ImportError:
    VALIDATORS_AVAILABLE = False

# Content processing
import re
from pathlib import Path

# Local imports
from agents.r1_reasoning.models import (
    JinaResearchRequest, JinaResearchResult, DocumentChunk
)

logger = logging.getLogger(__name__)


@dataclass
class ResearchSource:
    """Research source configuration"""
    name: str
    base_url: str
    search_pattern: str
    quality_weight: float = 1.0
    enabled: bool = True


@dataclass
class IngestionResult:
    """Result of research ingestion process"""
    success: bool
    total_sources: int
    processed_sources: int
    total_chunks: int
    average_quality: float
    processing_time_ms: int
    results: List[JinaResearchResult]
    error_message: Optional[str] = None


class JinaResearchIngester:
    """
    Automated research ingestion using Jina Reader API.
    
    Features:
    - Multi-source research aggregation
    - Content quality assessment with AAI patterns
    - Semantic chunking for reasoning optimization
    - Rate limiting and error handling
    - Configurable source priorities
    """
    
    def __init__(self,
                 jina_api_key: Optional[str] = None,
                 base_url: str = "https://r.jina.ai/",
                 rate_limit_delay: float = 1.0,
                 max_retries: int = 3,
                 timeout_seconds: int = 30):
        """Initialize Jina research ingester"""
        self.jina_api_key = jina_api_key
        self.base_url = base_url.rstrip('/')
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        
        # Initialize HTTP session
        self.session = None
        self.http_available = HTTP_AVAILABLE
        
        # Research sources configuration
        self.research_sources = self._initialize_research_sources()
        
        # Quality assessment patterns
        self.quality_patterns = self._initialize_quality_patterns()
        
        # Content filters
        self.content_filters = self._initialize_content_filters()
        
        # Rate limiting
        self.last_request_time = 0
        
        if not self.http_available:
            logger.warning("HTTP client not available - install aiohttp or requests")
    
    def _initialize_research_sources(self) -> Dict[str, ResearchSource]:
        """Initialize default research sources"""
        return {
            "arxiv": ResearchSource(
                name="arXiv",
                base_url="https://arxiv.org/search/",
                search_pattern="?query={query}&searchtype=all&abstracts=show&order=-announced_date_first&size=10",
                quality_weight=0.9,
                enabled=True
            ),
            "scholar": ResearchSource(
                name="Google Scholar",
                base_url="https://scholar.google.com/scholar",
                search_pattern="?q={query}&hl=en&as_sdt=0%2C5&as_rr=1",
                quality_weight=0.85,
                enabled=True
            ),
            "github": ResearchSource(
                name="GitHub",
                base_url="https://github.com/search",
                search_pattern="?q={query}&type=repositories&s=stars&o=desc",
                quality_weight=0.7,
                enabled=True
            ),
            "documentation": ResearchSource(
                name="Documentation Sites",
                base_url="https://www.google.com/search",
                search_pattern="?q={query}+site%3Adocs.*+OR+site%3Adocumentation.*",
                quality_weight=0.8,
                enabled=True
            )
        }
    
    def _initialize_quality_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for content quality assessment"""
        return {
            "high_quality_indicators": [
                "peer-reviewed", "published", "journal", "conference",
                "research", "study", "analysis", "methodology",
                "empirical", "systematic", "experimental", "theoretical"
            ],
            "academic_indicators": [
                "abstract", "introduction", "literature review", "methodology",
                "results", "discussion", "conclusion", "references",
                "doi:", "arxiv:", "citation", "bibliography"
            ],
            "technical_indicators": [
                "algorithm", "implementation", "framework", "architecture",
                "api", "documentation", "specification", "protocol",
                "standard", "best practices", "tutorial", "guide"
            ],
            "authority_indicators": [
                "professor", "dr.", "phd", "researcher", "scientist",
                "expert", "specialist", "university", "institution",
                "laboratory", "institute", "department"
            ],
            "low_quality_indicators": [
                "opinion", "blog post", "personal view", "unverified",
                "speculation", "rumor", "gossip", "advertisement",
                "promotional", "spam", "clickbait"
            ]
        }
    
    def _initialize_content_filters(self) -> Dict[str, Any]:
        """Initialize content filtering rules"""
        return {
            "min_content_length": 100,
            "max_content_length": 50000,
            "exclude_extensions": [".pdf", ".doc", ".docx", ".ppt", ".pptx"],
            "exclude_domains": ["example.com", "localhost", "127.0.0.1"],
            "required_languages": ["en"],
            "spam_patterns": [
                r"click here", r"buy now", r"limited time",
                r"free download", r"subscribe now"
            ]
        }
    
    async def research_topic(self, request: JinaResearchRequest) -> IngestionResult:
        """
        Research a topic using multiple sources and Jina Reader.
        
        Args:
            request: Research request parameters
            
        Returns:
            IngestionResult with processed research data
        """
        start_time = datetime.now()
        
        try:
            logger.info(f"Starting research for topic: {request.topic}")
            
            # Initialize HTTP session
            await self._ensure_session()
            
            # Generate search URLs for enabled sources
            search_urls = self._generate_search_urls(request)
            
            # Process each source
            all_results = []
            processed_count = 0
            
            for source_name, urls in search_urls.items():
                try:
                    source_results = await self._process_source(
                        source_name, urls, request
                    )
                    all_results.extend(source_results)
                    processed_count += 1
                    
                    # Rate limiting
                    await self._rate_limit()
                    
                except Exception as e:
                    logger.warning(f"Source {source_name} failed: {e}")
                    continue
            
            # Filter and rank results
            filtered_results = self._filter_and_rank_results(all_results, request)
            
            # Calculate metrics
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            average_quality = (
                sum(result.quality_score for result in filtered_results) / len(filtered_results)
                if filtered_results else 0.0
            )
            
            return IngestionResult(
                success=True,
                total_sources=len(search_urls),
                processed_sources=processed_count,
                total_chunks=len(filtered_results),
                average_quality=average_quality,
                processing_time_ms=int(processing_time),
                results=filtered_results[:request.max_pages]
            )
            
        except Exception as e:
            logger.error(f"Research ingestion failed: {e}")
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return IngestionResult(
                success=False,
                total_sources=0,
                processed_sources=0,
                total_chunks=0,
                average_quality=0.0,
                processing_time_ms=int(processing_time),
                results=[],
                error_message=str(e)
            )
        
        finally:
            await self._cleanup_session()
    
    def _generate_search_urls(self, request: JinaResearchRequest) -> Dict[str, List[str]]:
        """Generate search URLs for each enabled source"""
        search_urls = {}
        encoded_topic = quote(request.topic)
        
        for source_name, source in self.research_sources.items():
            if not source.enabled:
                continue
            
            # Filter by request preferences
            if not self._should_include_source(source_name, request):
                continue
            
            try:
                # Generate search URL
                search_url = source.base_url + source.search_pattern.format(
                    query=encoded_topic
                )
                search_urls[source_name] = [search_url]
                
            except Exception as e:
                logger.warning(f"URL generation failed for {source_name}: {e}")
                continue
        
        return search_urls
    
    def _should_include_source(self, source_name: str, request: JinaResearchRequest) -> bool:
        """Determine if source should be included based on request"""
        
        # Academic filter
        if (not request.include_academic and 
            source_name in ["arxiv", "scholar"]):
            return False
        
        # News filter
        if (not request.include_news and 
            source_name in ["news", "reuters", "techcrunch"]):
            return False
        
        # Documentation filter
        if (not request.include_documentation and 
            source_name in ["documentation", "github"]):
            return False
        
        return True
    
    async def _process_source(self, 
                            source_name: str, 
                            urls: List[str], 
                            request: JinaResearchRequest) -> List[JinaResearchResult]:
        """Process a single research source"""
        results = []
        
        for url in urls:
            try:
                # Use Jina Reader to extract content
                content_data = await self._extract_with_jina(url)
                
                if not content_data:
                    continue
                
                # Process and filter content
                processed_results = await self._process_content(
                    content_data, source_name, url, request
                )
                
                results.extend(processed_results)
                
            except Exception as e:
                logger.warning(f"URL processing failed {url}: {e}")
                continue
        
        return results
    
    async def _extract_with_jina(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract content using Jina Reader API"""
        try:
            # Construct Jina Reader URL
            jina_url = f"{self.base_url}/{url}"
            
            # Prepare headers
            headers = {
                "User-Agent": "AAI-R1-Research-Bot/1.0",
                "Accept": "application/json, text/plain, */*"
            }
            
            if self.jina_api_key:
                headers["Authorization"] = f"Bearer {self.jina_api_key}"
            
            # Make request
            if hasattr(self, 'session') and self.session:
                # Use aiohttp
                async with self.session.get(
                    jina_url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout_seconds)
                ) as response:
                    if response.status == 200:
                        content = await response.text()
                        return {
                            "url": url,
                            "content": content,
                            "status_code": response.status,
                            "headers": dict(response.headers)
                        }
                    else:
                        logger.warning(f"Jina Reader returned {response.status} for {url}")
                        return None
            
            else:
                # Fallback to requests (use asyncio.to_thread for non-blocking)
                import requests
                import asyncio
                
                def _sync_request():
                    response = requests.get(
                        jina_url,
                        headers=headers,
                        timeout=self.timeout_seconds
                    )
                    return response
                
                try:
                    response = await asyncio.to_thread(_sync_request)
                    
                    if response.status_code == 200:
                        return {
                            "url": url,
                            "content": response.text,
                            "status_code": response.status_code,
                            "headers": dict(response.headers)
                        }
                    else:
                        logger.warning(f"Jina Reader returned {response.status_code} for {url}")
                        return None
                except Exception as e:
                    logger.error(f"Async request failed for {url}: {e}")
                    return None
                    
        except Exception as e:
            logger.error(f"Jina extraction failed for {url}: {e}")
            return None
    
    async def _process_content(self,
                             content_data: Dict[str, Any],
                             source_name: str,
                             url: str,
                             request: JinaResearchRequest) -> List[JinaResearchResult]:
        """Process extracted content into research results"""
        try:
            content = content_data["content"]
            
            # Content validation
            if not self._validate_content(content):
                return []
            
            # Extract metadata
            metadata = self._extract_metadata(content, content_data)
            
            # Quality assessment
            quality_score = self._assess_content_quality(content, source_name, metadata)
            
            # Relevance scoring
            relevance_score = self._calculate_relevance(content, request.topic)
            
            # Apply quality threshold
            if quality_score < request.quality_threshold:
                return []
            
            # Determine source type
            source_type = self._determine_source_type(source_name, url, content)
            
            # Create research result
            result = JinaResearchResult(
                url=url,
                title=metadata.get("title", "Untitled"),
                content=content,
                quality_score=quality_score,
                relevance_score=relevance_score,
                source_type=source_type,
                publication_date=metadata.get("publication_date"),
                metadata={
                    "source_name": source_name,
                    "content_length": len(content),
                    "extraction_method": "jina_reader",
                    **metadata
                }
            )
            
            return [result]
            
        except Exception as e:
            logger.error(f"Content processing failed: {e}")
            return []
    
    def _validate_content(self, content: str) -> bool:
        """Validate content meets basic requirements"""
        
        # Length check
        if (len(content) < self.content_filters["min_content_length"] or
            len(content) > self.content_filters["max_content_length"]):
            return False
        
        # Spam check
        content_lower = content.lower()
        for pattern in self.content_filters["spam_patterns"]:
            if re.search(pattern, content_lower):
                return False
        
        # Language check (basic)
        if not self._is_english_content(content):
            return False
        
        return True
    
    def _is_english_content(self, content: str) -> bool:
        """Basic English language detection"""
        # Simple heuristic: check for common English words
        english_indicators = [
            "the", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "about", "into", "through"
        ]
        
        content_lower = content.lower()
        indicator_count = sum(
            1 for indicator in english_indicators 
            if f" {indicator} " in content_lower
        )
        
        # Require at least 3 common English words
        return indicator_count >= 3
    
    def _extract_metadata(self, content: str, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from content"""
        metadata = {}
        
        # Extract title (first line or heading)
        lines = content.split('\n')
        if lines:
            # Look for title patterns
            for line in lines[:10]:  # Check first 10 lines
                line = line.strip()
                if line and len(line) < 200:
                    # Heuristics for title detection
                    if (line.isupper() or 
                        line.startswith('#') or
                        not line.endswith('.') or
                        re.match(r'^[A-Z][^.]*[A-Z]', line)):
                        metadata["title"] = line.lstrip('#').strip()
                        break
        
        # Extract publication date patterns
        date_patterns = [
            r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b',  # YYYY-MM-DD
            r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',  # MM/DD/YYYY
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),?\s+(\d{4})\b'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, content)
            if match:
                try:
                    # Basic date parsing (would need more robust implementation)
                    metadata["publication_date"] = match.group(0)
                    break
                except:
                    continue
        
        # Extract author patterns
        author_patterns = [
            r'by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'author[s]?:\s*([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+et\s+al'
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                metadata["author"] = match.group(1)
                break
        
        return metadata
    
    def _assess_content_quality(self, 
                              content: str, 
                              source_name: str, 
                              metadata: Dict[str, Any]) -> float:
        """Assess content quality with AAI scoring"""
        
        content_lower = content.lower()
        quality_score = 0.5  # Base quality
        
        # Source quality weight
        source = self.research_sources.get(source_name)
        if source:
            quality_score = 0.3 + (source.quality_weight * 0.4)
        
        # High quality indicators
        high_quality_count = sum(
            1 for indicator in self.quality_patterns["high_quality_indicators"]
            if indicator in content_lower
        )
        quality_score += min(0.2, high_quality_count * 0.02)
        
        # Academic indicators
        academic_count = sum(
            1 for indicator in self.quality_patterns["academic_indicators"]
            if indicator in content_lower
        )
        quality_score += min(0.15, academic_count * 0.015)
        
        # Technical indicators
        technical_count = sum(
            1 for indicator in self.quality_patterns["technical_indicators"]
            if indicator in content_lower
        )
        quality_score += min(0.1, technical_count * 0.01)
        
        # Authority indicators
        authority_count = sum(
            1 for indicator in self.quality_patterns["authority_indicators"]
            if indicator in content_lower
        )
        quality_score += min(0.1, authority_count * 0.02)
        
        # Penalize low quality indicators
        low_quality_count = sum(
            1 for indicator in self.quality_patterns["low_quality_indicators"]
            if indicator in content_lower
        )
        quality_score -= min(0.3, low_quality_count * 0.05)
        
        # Metadata bonus
        if metadata.get("title"):
            quality_score += 0.05
        if metadata.get("author"):
            quality_score += 0.05
        if metadata.get("publication_date"):
            quality_score += 0.03
        
        # Content structure bonus
        if len(content) > 1000:
            quality_score += 0.05
        
        # Ensure valid range
        return max(0.0, min(1.0, quality_score))
    
    def _calculate_relevance(self, content: str, topic: str) -> float:
        """Calculate relevance score for topic"""
        
        content_lower = content.lower()
        topic_lower = topic.lower()
        topic_words = set(topic_lower.split())
        
        # Exact topic match
        if topic_lower in content_lower:
            relevance_score = 0.8
        else:
            relevance_score = 0.3
        
        # Word overlap scoring
        content_words = set(re.findall(r'\b\w+\b', content_lower))
        overlap = len(topic_words.intersection(content_words))
        
        if topic_words:
            word_overlap_score = overlap / len(topic_words)
            relevance_score += word_overlap_score * 0.3
        
        # Semantic proximity (simplified)
        related_terms_found = 0
        for topic_word in topic_words:
            if len(topic_word) > 3:  # Skip short words
                # Look for variations and related terms
                word_pattern = rf'\b{re.escape(topic_word)}[a-z]*\b'
                if re.search(word_pattern, content_lower):
                    related_terms_found += 1
        
        if topic_words:
            semantic_score = related_terms_found / len(topic_words)
            relevance_score += semantic_score * 0.2
        
        return max(0.0, min(1.0, relevance_score))
    
    def _determine_source_type(self, source_name: str, url: str, content: str) -> str:
        """Determine the type of source"""
        
        content_lower = content.lower()
        
        # Academic sources
        if (source_name in ["arxiv", "scholar"] or
            "arxiv.org" in url or
            any(indicator in content_lower for indicator in ["abstract", "methodology", "references"])):
            return "academic"
        
        # Documentation
        if (source_name == "documentation" or
            "docs." in url or
            "documentation" in url or
            any(indicator in content_lower for indicator in ["api", "tutorial", "guide"])):
            return "documentation"
        
        # News
        if (source_name == "news" or
            any(domain in url for domain in ["news", "reuters", "techcrunch", "wired"]) or
            any(indicator in content_lower for indicator in ["breaking", "reported", "according to"])):
            return "news"
        
        # Blog
        if (any(indicator in content_lower for indicator in ["posted by", "blog", "opinion"]) or
            "blog" in url):
            return "blog"
        
        # Default
        return "web"
    
    def _filter_and_rank_results(self, 
                                results: List[JinaResearchResult],
                                request: JinaResearchRequest) -> List[JinaResearchResult]:
        """Filter and rank research results"""
        
        # Apply date filter if specified
        if request.date_filter:
            results = self._apply_date_filter(results, request.date_filter)
        
        # Sort by combined quality and relevance score
        def combined_score(result):
            return (result.quality_score * 0.6 + result.relevance_score * 0.4)
        
        results.sort(key=combined_score, reverse=True)
        
        # Remove duplicates (by URL)
        seen_urls = set()
        unique_results = []
        
        for result in results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        return unique_results
    
    def _apply_date_filter(self, 
                          results: List[JinaResearchResult],
                          date_filter: str) -> List[JinaResearchResult]:
        """Apply date filtering to results"""
        
        if not date_filter:
            return results
        
        # Parse date filter
        cutoff_date = None
        now = datetime.now()
        
        if date_filter == "1d":
            cutoff_date = now - timedelta(days=1)
        elif date_filter == "1w":
            cutoff_date = now - timedelta(weeks=1)
        elif date_filter == "1m":
            cutoff_date = now - timedelta(days=30)
        elif date_filter == "1y":
            cutoff_date = now - timedelta(days=365)
        
        if not cutoff_date:
            return results
        
        # Filter results (keep results without dates)
        filtered_results = []
        for result in results:
            if result.publication_date:
                try:
                    # Basic date parsing (would need improvement)
                    pub_date = datetime.fromisoformat(result.publication_date)
                    if pub_date >= cutoff_date:
                        filtered_results.append(result)
                except:
                    # Include if date parsing fails
                    filtered_results.append(result)
            else:
                # Include if no date available
                filtered_results.append(result)
        
        return filtered_results
    
    async def _ensure_session(self):
        """Ensure HTTP session is available"""
        if not self.http_available:
            return
        
        try:
            import aiohttp
            if not self.session:
                timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
                self.session = aiohttp.ClientSession(timeout=timeout)
        except ImportError:
            # Will use requests fallback
            pass
    
    async def _cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _rate_limit(self):
        """Apply rate limiting between requests"""
        if self.rate_limit_delay > 0:
            current_time = datetime.now().timestamp()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.rate_limit_delay:
                sleep_time = self.rate_limit_delay - time_since_last
                await asyncio.sleep(sleep_time)
            
            self.last_request_time = datetime.now().timestamp()
    
    def get_ingester_status(self) -> Dict[str, Any]:
        """Get ingester status and configuration"""
        return {
            "http_available": self.http_available,
            "jina_api_configured": bool(self.jina_api_key),
            "base_url": self.base_url,
            "rate_limit_delay": self.rate_limit_delay,
            "timeout_seconds": self.timeout_seconds,
            "enabled_sources": [
                name for name, source in self.research_sources.items() 
                if source.enabled
            ],
            "total_sources": len(self.research_sources),
            "quality_patterns_count": sum(
                len(patterns) for patterns in self.quality_patterns.values()
            ),
            "content_filters": self.content_filters,
            "ready": self.http_available
        }


async def test_jina_research_ingester():
    """Test Jina research ingester functionality"""
    
    ingester = JinaResearchIngester()
    
    print("🧪 Testing Jina Research Ingester")
    print("=" * 40)
    
    # Check ingester status
    status = ingester.get_ingester_status()
    print(f"HTTP available: {status['http_available']}")
    print(f"Jina API configured: {status['jina_api_configured']}")
    print(f"Base URL: {status['base_url']}")
    print(f"Enabled sources: {status['enabled_sources']}")
    print(f"Ready: {status['ready']}")
    
    if not status['ready']:
        print("❌ Ingester not ready - missing HTTP client")
        return
    
    # Test with sample research request
    sample_request = JinaResearchRequest(
        topic="artificial intelligence reasoning systems",
        max_pages=3,
        quality_threshold=0.5,
        include_academic=True,
        include_news=False,
        include_documentation=True,
        date_filter="1m"
    )
    
    print(f"\\n📋 Testing research request: '{sample_request.topic}'")
    print(f"Max pages: {sample_request.max_pages}")
    print(f"Quality threshold: {sample_request.quality_threshold}")
    print(f"Date filter: {sample_request.date_filter}")
    
    # Note: Actual research would require network access
    print("\\n⚠️  Note: Full testing requires network access and Jina API")
    print("For complete testing:")
    print("  1. Set JINA_API_KEY environment variable (optional)")
    print("  2. Run: await ingester.research_topic(sample_request)")
    print("  3. Check results for quality scores and content")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_jina_research_ingester())