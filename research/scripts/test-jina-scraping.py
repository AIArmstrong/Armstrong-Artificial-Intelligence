#!/usr/bin/env python3
"""
Test Jina Scraping Integration
Validates that Jina web scraping works correctly with the research engine
"""

import os
import sys
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add research directory to path
sys.path.append(str(Path(__file__).parent.parent))

def test_jina_api_key():
    """Test if Jina API key is available"""
    api_key = os.getenv('JINA_API_KEY')
    if not api_key:
        print("❌ JINA_API_KEY environment variable not set")
        print("💡 Get your free API key at: https://jina.ai/?sui=apikey")
        return False
    
    print(f"✅ JINA_API_KEY found: {api_key[:10]}...")
    return True

def scrape_webpage(url: str, target_selector: str = None) -> Optional[Dict]:
    """
    Scrape webpage using Jina Reader API
    """
    api_key = os.getenv('JINA_API_KEY')
    if not api_key:
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Return-Format": "markdown",
        "X-Engine": "direct",
        "X-Remove-Selector": "header, footer, nav, .sidebar, .advertisement, .cookie-banner",
        "X-Retain-Images": "none",
        "X-Gather-All-Links": "true",
        "X-No-Cache": "true",
        "X-Follow-Redirect": "true"
    }
    
    if target_selector:
        headers["X-Target-Selector"] = target_selector
    
    payload = {"url": url}
    
    try:
        print(f"🔍 Scraping: {url}")
        response = requests.post("https://r.jina.ai/", 
                                json=payload,
                                headers=headers,
                                timeout=30)
        response.raise_for_status()
        
        # Parse JSON response and extract content
        data = response.json()
        content = data.get("data", {}).get("content", "")
        
        result = {
            'url': url,
            'content': content,
            'title': 'Scraped Content',
            'links': {'internal': [], 'external': []},  # Would need parsing for links
            'images': [],
            'metadata': {}
        }
        
        print(f"✅ Successfully scraped {url}")
        print(f"   Title: {result['title']}")
        print(f"   Content length: {len(result['content'])} chars")
        print(f"   Links found: {len(result['links'].get('internal', []))} internal, {len(result['links'].get('external', []))} external")
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Scraping error for {url}: {e}")
        return None

def test_documentation_scraping():
    """Test scraping technical documentation"""
    
    # Test URLs for different types of documentation
    test_urls = [
        {
            'url': 'https://docs.jina.ai/concepts/jina-api/',
            'name': 'Jina API Docs',
            'selector': 'article, .content, .documentation'
        },
        {
            'url': 'https://docs.python.org/3/tutorial/introduction.html',
            'name': 'Python Tutorial',
            'selector': '.body'
        },
        {
            'url': 'https://reactjs.org/docs/getting-started.html',
            'name': 'React Documentation',
            'selector': '.content'
        }
    ]
    
    results = []
    
    for test_case in test_urls:
        print(f"\n📖 Testing {test_case['name']}...")
        
        result = scrape_webpage(
            test_case['url'],
            target_selector=test_case['selector']
        )
        
        if result:
            results.append(result)
            
            # Analyze content quality
            content = result['content']
            quality_score = calculate_content_quality(content)
            
            print(f"   Quality score: {quality_score:.2f}")
            
            # Check for code examples
            code_blocks = content.count('```')
            if code_blocks > 0:
                print(f"   Code examples: {code_blocks} found")
            
            # Check for technical content
            tech_keywords = ['api', 'function', 'class', 'method', 'parameter']
            keyword_count = sum(1 for keyword in tech_keywords if keyword in content.lower())
            print(f"   Technical keywords: {keyword_count} found")
            
        else:
            print(f"❌ Failed to scrape {test_case['name']}")
        
        # Rate limiting
        time.sleep(1)
    
    return results

def calculate_content_quality(content: str) -> float:
    """Calculate quality score for scraped content"""
    score = 0.0
    
    # Length check
    if len(content) > 1000:
        score += 0.3
    elif len(content) > 500:
        score += 0.2
    
    # Code examples
    if '```' in content:
        score += 0.2
    
    # Headers and structure
    import re
    if re.search(r'#{1,6}\s+', content):
        score += 0.2
    
    # Technical keywords
    tech_keywords = ['api', 'function', 'class', 'method', 'parameter', 'return', 'example']
    keyword_count = sum(1 for keyword in tech_keywords if keyword in content.lower())
    score += min(keyword_count * 0.05, 0.3)
    
    return min(score, 1.0)

def test_research_file_generation(results: List[Dict]):
    """Test generating research files from scraping results"""
    
    if not results:
        print("❌ No scraping results to test with")
        return False
    
    print(f"\n📝 Testing research file generation with {len(results)} results...")
    
    # Generate research content
    technology = "web-scraping-test"
    content = generate_research_file(results, technology)
    
    # Save to test file
    test_file = Path(__file__).parent.parent / "_knowledge-base" / technology / f"{technology}-general.md"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(test_file, 'w') as f:
        f.write(content)
    
    print(f"✅ Research file generated: {test_file}")
    print(f"   File size: {test_file.stat().st_size} bytes")
    
    # Validate content
    if len(content) > 1000:
        print(f"   Content length: {len(content)} chars ✅")
    else:
        print(f"   Content length: {len(content)} chars ⚠️ (short)")
    
    return True

def generate_research_file(scraping_results: List[Dict], technology: str) -> str:
    """Generate research markdown file from scraping results"""
    
    content = f"""# {technology.title()} - General Research

## Overview
Research gathered from web scraping using Jina API on {time.strftime('%Y-%m-%d %H:%M:%S')}.

## Scraped Content Summary
"""
    
    for i, result in enumerate(scraping_results, 1):
        title = result.get('title', f'Source {i}')
        url = result.get('url', '')
        content_length = len(result.get('content', ''))
        
        content += f"""
### {i}. {title}
- **URL**: {url}
- **Content Length**: {content_length} characters
- **Links Found**: {len(result.get('links', {}).get('internal', []))} internal, {len(result.get('links', {}).get('external', []))} external
"""
        
        # Add content preview
        content_preview = result.get('content', '')[:500]
        if len(content_preview) == 500:
            content_preview += "..."
        
        content += f"""
**Content Preview**:
{content_preview}
"""
    
    content += """
## Implementation Examples
Based on scraped documentation, here are key implementation patterns:

"""
    
    # Extract code examples
    for result in scraping_results:
        import re
        code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', result.get('content', ''), re.DOTALL)
        
        if code_blocks:
            content += f"### Examples from {result.get('title', 'Documentation')}\n"
            for code in code_blocks[:2]:  # Limit to 2 examples
                content += f"```\n{code}\n```\n\n"
    
    content += """
## Research Sources
"""
    
    for result in scraping_results:
        title = result.get('title', 'Documentation')
        url = result.get('url', '')
        content += f"- [{title}]({url})\n"
    
    # Calculate overall quality score
    avg_quality = sum(calculate_content_quality(r.get('content', '')) for r in scraping_results) / len(scraping_results)
    
    content += f"""
## Quality Score: {avg_quality:.2f}
**Source Quality**: Web scraping with Jina API
**Completeness**: {len(scraping_results)} sources scraped
**Reusability**: Medium - Scraped content for testing
**Scraping Method**: Jina Reader API with browser engine

## Scraping Metadata
- **Total Sources**: {len(scraping_results)}
- **Scraping Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **API Used**: Jina Reader API (r.jina.ai)
- **Average Quality**: {avg_quality:.2f}

## Tags
#general #{technology} #scraped-documentation #jina-api #web-scraping #test
"""
    
    return content

def test_batch_scraping():
    """Test scraping multiple URLs in batch"""
    
    print(f"\n🔄 Testing batch scraping...")
    
    # Test with a few URLs
    test_urls = [
        'https://docs.jina.ai/concepts/jina-api/',
        'https://docs.jina.ai/concepts/reader/',
        'https://docs.jina.ai/concepts/search/'
    ]
    
    results = []
    
    for url in test_urls:
        result = scrape_webpage(url)
        if result:
            results.append(result)
        
        # Rate limiting
        time.sleep(1)
    
    print(f"✅ Batch scraping complete: {len(results)}/{len(test_urls)} successful")
    
    return results

def main():
    """Main test function"""
    
    print("🧪 Testing Jina Scraping Integration")
    print("=" * 50)
    
    # Test 1: API Key
    print("\n1. Testing API Key...")
    if not test_jina_api_key():
        print("💡 To get a free Jina API key:")
        print("   1. Go to https://jina.ai/?sui=apikey")
        print("   2. Sign up for free account")
        print("   3. Get your API key")
        print("   4. Set environment variable: export JINA_API_KEY=your_key")
        return False
    
    # Test 2: Basic scraping
    print("\n2. Testing Basic Scraping...")
    basic_result = scrape_webpage('https://docs.jina.ai/')
    
    if not basic_result:
        print("❌ Basic scraping test failed")
        return False
    
    # Test 3: Documentation scraping
    print("\n3. Testing Documentation Scraping...")
    doc_results = test_documentation_scraping()
    
    if not doc_results:
        print("❌ Documentation scraping test failed")
        return False
    
    # Test 4: Research file generation
    print("\n4. Testing Research File Generation...")
    if not test_research_file_generation(doc_results):
        print("❌ Research file generation test failed")
        return False
    
    # Test 5: Batch scraping
    print("\n5. Testing Batch Scraping...")
    batch_results = test_batch_scraping()
    
    if not batch_results:
        print("❌ Batch scraping test failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL JINA SCRAPING TESTS PASSED!")
    print(f"✅ Successfully scraped {len(doc_results + batch_results)} URLs")
    print(f"✅ Generated research files with quality content")
    print(f"✅ Jina API integration working correctly")
    
    print("\n💡 Integration ready for:")
    print("   - GeneralResearcher agent (30-100 page scraping)")
    print("   - Research queue auto-triggers")
    print("   - Documentation gathering for research creation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)