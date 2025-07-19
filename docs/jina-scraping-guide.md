# Jina Web Scraping Implementation Guide

**Source**: https://docs.jina.ai/  
**Stored**: 2025-07-15 for AAI Research Engine integration

## Overview

Jina provides powerful web scraping capabilities through multiple APIs optimized for AI and research applications. This guide covers implementation for the AAI Research Engine.

## Key APIs

### 1. Reader API (r.jina.ai)
- **Purpose**: Extract structured content from web pages
- **Optimization**: Designed for downstream LLM processing
- **Best for**: Research documentation, technical content

### 2. Search API (s.jina.ai)
- **Purpose**: Web search with AI-powered results
- **Integration**: Combines search with content extraction
- **Best for**: Finding and scraping relevant research sources

### 3. DeepSearch API
- **Purpose**: Advanced semantic search capabilities
- **Integration**: Works with Reader API for comprehensive scraping
- **Best for**: Technical documentation discovery

## Authentication

```bash
# Set environment variable
export JINA_API_KEY=your_api_key_here

# Get free API key at: https://jina.ai/?sui=apikey
```

## Reader API Implementation

### Core Features
- **Structured extraction** - Clean content optimized for AI processing
- **Custom parsing** - Control extraction with headers
- **Link extraction** - Gather related URLs for comprehensive scraping
- **Image handling** - Extract and process embedded images
- **Selector targeting** - Focus on specific page elements

### Key Headers

```python
headers = {
    "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}",
    "Accept": "application/json",
    
    # Content retrieval method
    "X-Engine": "browser",  # Options: browser (best quality), direct (fastest)
    
    # Element targeting
    "X-Target-Selector": "article, .content, .documentation",  # Focus on specific elements
    "X-Remove-Selector": "nav, footer, .sidebar",  # Exclude unwanted sections
    
    # Additional data
    "X-With-Links-Summary": "true",  # Extract page links
    "X-With-Images-Summary": "true",  # Extract page images
    
    # Caching
    "X-No-Cache": "true",  # Force fresh content
    "X-Cache-Tolerance": "3600"  # Cache tolerance in seconds
}
```

## Python Implementation

### Basic Scraping Function

```python
import os
import requests
from typing import Dict, List, Optional

def scrape_webpage(url: str, target_selector: str = None) -> Optional[Dict]:
    """
    Scrape webpage using Jina Reader API
    
    Args:
        url: Target URL to scrape
        target_selector: CSS selector for specific content
    
    Returns:
        Dictionary with content, links, and metadata
    """
    headers = {
        "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}",
        "Accept": "application/json",
        "X-Engine": "browser",
        "X-With-Links-Summary": "true",
        "X-No-Cache": "true"
    }
    
    if target_selector:
        headers["X-Target-Selector"] = target_selector
    
    payload = {"url": url}
    
    try:
        response = requests.post("https://r.jina.ai/", 
                                 json=payload, 
                                 headers=headers,
                                 timeout=30)
        response.raise_for_status()
        
        data = response.json()['data']
        
        return {
            'url': url,
            'content': data.get('content', ''),
            'title': data.get('title', ''),
            'links': data.get('links', {}),
            'images': data.get('images', []),
            'metadata': data.get('metadata', {})
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Scraping error for {url}: {e}")
        return None
```

### Batch Scraping Function

```python
def scrape_multiple_urls(urls: List[str], max_pages: int = 100) -> List[Dict]:
    """
    Scrape multiple URLs with rate limiting
    
    Args:
        urls: List of URLs to scrape
        max_pages: Maximum number of pages to scrape
    
    Returns:
        List of scraping results
    """
    import time
    
    results = []
    scraped_count = 0
    
    for url in urls:
        if scraped_count >= max_pages:
            break
            
        print(f"Scraping: {url}")
        result = scrape_webpage(url)
        
        if result:
            results.append(result)
            scraped_count += 1
            
            # Extract additional links for comprehensive scraping
            if 'links' in result:
                for link_url in result['links'].get('internal', []):
                    if scraped_count < max_pages:
                        time.sleep(1)  # Rate limiting
                        link_result = scrape_webpage(link_url)
                        if link_result:
                            results.append(link_result)
                            scraped_count += 1
        
        # Rate limiting - respect API limits
        time.sleep(0.5)
    
    return results
```

### Research-Specific Scraping

```python
def scrape_documentation(base_url: str, technology: str) -> Dict:
    """
    Scrape technical documentation for research
    
    Args:
        base_url: Base URL of documentation
        technology: Technology name for categorization
    
    Returns:
        Structured research data
    """
    
    # Documentation-specific selectors
    doc_selectors = {
        'content': 'article, .documentation, .content, .docs',
        'remove': 'nav, footer, .sidebar, .advertisement, .cookie-banner'
    }
    
    headers = {
        "Authorization": f"Bearer {os.getenv('JINA_API_KEY')}",
        "Accept": "application/json",
        "X-Engine": "browser",
        "X-Target-Selector": doc_selectors['content'],
        "X-Remove-Selector": doc_selectors['remove'],
        "X-With-Links-Summary": "true",
        "X-No-Cache": "true"
    }
    
    payload = {"url": base_url}
    
    try:
        response = requests.post("https://r.jina.ai/", 
                                 json=payload, 
                                 headers=headers,
                                 timeout=45)
        response.raise_for_status()
        
        data = response.json()['data']
        
        # Process content for research
        content = data.get('content', '')
        
        # Extract code examples
        import re
        code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', content, re.DOTALL)
        
        # Extract key sections
        sections = extract_documentation_sections(content)
        
        return {
            'technology': technology,
            'url': base_url,
            'title': data.get('title', ''),
            'content': content,
            'sections': sections,
            'code_examples': code_blocks,
            'links': data.get('links', {}),
            'scraped_at': time.time(),
            'quality_score': calculate_content_quality(content)
        }
    
    except Exception as e:
        print(f"Documentation scraping error: {e}")
        return None

def extract_documentation_sections(content: str) -> Dict[str, str]:
    """Extract key sections from documentation content"""
    sections = {}
    
    # Common documentation sections
    section_patterns = {
        'getting_started': r'(?i)getting\s+started(.*?)(?=\n#{1,3}|\Z)',
        'installation': r'(?i)installation(.*?)(?=\n#{1,3}|\Z)',
        'api_reference': r'(?i)api\s+reference(.*?)(?=\n#{1,3}|\Z)',
        'examples': r'(?i)examples?(.*?)(?=\n#{1,3}|\Z)',
        'configuration': r'(?i)configuration(.*?)(?=\n#{1,3}|\Z)'
    }
    
    for section_name, pattern in section_patterns.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            sections[section_name] = match.group(1).strip()
    
    return sections

def calculate_content_quality(content: str) -> float:
    """Calculate quality score for scraped content"""
    score = 0.0
    
    # Length check
    if len(content) > 1000:
        score += 0.3
    
    # Code examples
    if '```' in content:
        score += 0.2
    
    # Headers and structure
    if re.search(r'#{1,6}\s+', content):
        score += 0.2
    
    # Technical keywords
    tech_keywords = ['api', 'function', 'class', 'method', 'parameter', 'return']
    keyword_count = sum(1 for keyword in tech_keywords if keyword in content.lower())
    score += min(keyword_count * 0.05, 0.3)
    
    return min(score, 1.0)
```

## Rate Limits and Best Practices

### Rate Limits
- **Reader API**: 200 requests per minute
- **Search API**: 100 requests per minute
- **Recommended**: 1-2 requests per second for sustained scraping

### Best Practices

1. **Respect robots.txt** - Check site policies before scraping
2. **Use appropriate delays** - 0.5-1 second between requests
3. **Handle errors gracefully** - Retry with exponential backoff
4. **Cache results** - Store scraped content to avoid re-scraping
5. **Use specific selectors** - Target relevant content sections

### Error Handling

```python
def robust_scrape(url: str, max_retries: int = 3) -> Optional[Dict]:
    """
    Scrape with retry logic and error handling
    """
    import time
    
    for attempt in range(max_retries):
        try:
            result = scrape_webpage(url)
            if result:
                return result
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"Max retries exceeded for {url}: {e}")
                return None
            
            # Exponential backoff
            wait_time = 2 ** attempt
            print(f"Retry {attempt + 1} for {url} in {wait_time}s")
            time.sleep(wait_time)
    
    return None
```

## Integration with Research Engine

### Research File Generation

```python
def generate_research_file(scraping_results: List[Dict], technology: str) -> str:
    """
    Generate research markdown file from scraping results
    """
    content = f"""# {technology.title()} - General Research

## Overview
Research gathered from official documentation and sources.

## Key Concepts
"""
    
    for result in scraping_results:
        if result.get('sections', {}).get('getting_started'):
            content += f"\n### Getting Started\n{result['sections']['getting_started']}\n"
        
        if result.get('sections', {}).get('api_reference'):
            content += f"\n### API Reference\n{result['sections']['api_reference']}\n"
    
    content += "\n## Implementation Examples\n"
    
    for i, result in enumerate(scraping_results, 1):
        if result.get('code_examples'):
            content += f"\n### Example {i}\n"
            for code in result['code_examples'][:2]:  # Limit to 2 examples
                content += f"```\n{code}\n```\n"
    
    content += f"""
## Research Sources
"""
    
    for result in scraping_results:
        content += f"- [{result.get('title', 'Documentation')}]({result.get('url')})\n"
    
    # Calculate overall quality score
    avg_quality = sum(r.get('quality_score', 0) for r in scraping_results) / len(scraping_results)
    
    content += f"""
## Quality Score: {avg_quality:.2f}
**Source Quality**: Official documentation
**Completeness**: Comprehensive scraping of {len(scraping_results)} sources
**Reusability**: High - General implementation patterns

## Tags
#general #{technology} #scraped-documentation #jina-research
"""
    
    return content
```

## Usage Examples

### Basic Usage
```python
# Set API key
os.environ['JINA_API_KEY'] = 'your_api_key'

# Scrape single page
result = scrape_webpage('https://reactjs.org/docs/getting-started.html')

# Scrape documentation
docs = scrape_documentation('https://docs.python.org/3/', 'python')
```

### Research Engine Integration
```python
# Scrape for research creation
def create_research_from_scraping(technology: str, documentation_urls: List[str]):
    """Create research file from scraped documentation"""
    
    results = []
    for url in documentation_urls:
        result = scrape_documentation(url, technology)
        if result:
            results.append(result)
    
    if results:
        research_content = generate_research_file(results, technology)
        
        # Save to knowledge base
        file_path = f"research/_knowledge-base/{technology}/{technology}-general.md"
        with open(file_path, 'w') as f:
            f.write(research_content)
        
        print(f"Research file created: {file_path}")
        return file_path
    
    return None

# Example usage
create_research_from_scraping('react', [
    'https://reactjs.org/docs/getting-started.html',
    'https://reactjs.org/docs/hooks-intro.html',
    'https://reactjs.org/docs/components-and-props.html'
])
```

## Testing Jina Integration

```python
def test_jina_scraping():
    """Test Jina scraping functionality"""
    
    # Test basic scraping
    test_url = "https://docs.jina.ai/concepts/jina-api/"
    result = scrape_webpage(test_url)
    
    if result:
        print("✅ Jina scraping working!")
        print(f"Title: {result.get('title')}")
        print(f"Content length: {len(result.get('content', ''))}")
        print(f"Links found: {len(result.get('links', {}))}")
        return True
    else:
        print("❌ Jina scraping failed")
        return False

# Run test
if __name__ == "__main__":
    test_jina_scraping()
```

---

**Implementation Status**: Ready for integration into AAI Research Engine  
**Documentation Source**: https://docs.jina.ai/  
**Last Updated**: 2025-07-15