#!/usr/bin/env python3
"""
Optimized Jina Configuration for Research Engine
Provides different configurations based on content type and research needs
"""

import os
from typing import Dict, List, Optional
from enum import Enum

class JinaMode(Enum):
    """Different Jina scraping modes for various content types"""
    STANDARD = "standard"           # General documentation
    VISUAL = "visual"              # UI/UX docs with images
    COMPREHENSIVE = "comprehensive" # Deep technical docs
    FAST = "fast"                  # Quick content scraping
    API_DOCS = "api_docs"          # API documentation
    TUTORIAL = "tutorial"          # Step-by-step guides

class JinaOptimizedScraper:
    """
    Optimized Jina scraper with different configurations for different content types
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://r.jina.ai/"
        
        # Common settings for all modes
        self.common_headers = {
            "Authorization": f"Bearer {api_key}",
            "X-Return-Format": "markdown",  # Always use markdown
            "X-No-Cache": "true",          # Always bypass cache for fresh content
            "X-Follow-Redirect": "true",   # Follow redirects
        }
        
        # Mode-specific configurations
        self.mode_configs = {
            JinaMode.STANDARD: {
                "description": "General documentation scraping",
                "headers": {
                    "X-Engine": "direct",
                    "X-Remove-Selector": "header, footer, nav, .sidebar, .advertisement, .cookie-banner",
                    "X-Retain-Images": "none",
                    "X-Gather-All-Links": "true",
                    "X-Token-Budget": "50000"
                },
                "use_case": "Most documentation, general research"
            },
            
            JinaMode.VISUAL: {
                "description": "Documentation with important visual elements",
                "headers": {
                    "X-Engine": "browser",  # Better rendering for complex pages
                    "X-Remove-Selector": "header, footer, nav, .sidebar, .advertisement",
                    "X-Retain-Images": "all",
                    "X-Image-Caption": "true",
                    "X-Gather-All-Links": "true",
                    "X-Gather-All-Images": "true",
                    "X-Token-Budget": "100000"
                },
                "use_case": "UI/UX docs, architecture diagrams, visual tutorials"
            },
            
            JinaMode.COMPREHENSIVE: {
                "description": "Deep technical documentation with high quality",
                "headers": {
                    "X-Engine": "browser",
                    "X-Use-ReaderLM-v2": "true",  # 3x tokens but better quality
                    "X-Remove-Selector": "header, footer, nav, .sidebar, .advertisement",
                    "X-Retain-Images": "all",
                    "X-Image-Caption": "true",
                    "X-Gather-All-Links": "true",
                    "X-Gather-All-Images": "true",
                    "X-Stream-Mode": "true",
                    "X-Token-Budget": "200000"
                },
                "use_case": "Complex technical docs, comprehensive research"
            },
            
            JinaMode.FAST: {
                "description": "Quick content scraping with minimal processing",
                "headers": {
                    "X-Engine": "direct",
                    "X-Remove-Selector": "header, footer, nav, .sidebar, .advertisement, .cookie-banner, .comments",
                    "X-Retain-Images": "none",
                    "X-Gather-All-Links": "false",
                    "X-Token-Budget": "25000"
                },
                "use_case": "Quick checks, content validation"
            },
            
            JinaMode.API_DOCS: {
                "description": "API documentation with code examples",
                "headers": {
                    "X-Engine": "browser",
                    "X-Remove-Selector": "header, footer, nav, .sidebar, .advertisement",
                    "X-Retain-Images": "none",
                    "X-Gather-All-Links": "true",
                    "X-CSS-Selector": "article, .content, .documentation, .api-docs, .endpoint",
                    "X-Token-Budget": "75000"
                },
                "use_case": "API documentation, code examples"
            },
            
            JinaMode.TUTORIAL: {
                "description": "Tutorial content with step-by-step instructions",
                "headers": {
                    "X-Engine": "browser",
                    "X-Remove-Selector": "header, footer, nav, .sidebar, .advertisement",
                    "X-Retain-Images": "all",
                    "X-Image-Caption": "true",
                    "X-Gather-All-Links": "true",
                    "X-CSS-Selector": "article, .content, .tutorial, .guide, .steps",
                    "X-Token-Budget": "100000"
                },
                "use_case": "Tutorials, how-to guides, step-by-step instructions"
            }
        }
    
    def get_config(self, mode: JinaMode) -> Dict[str, str]:
        """Get complete headers configuration for a specific mode"""
        config = self.mode_configs[mode]
        headers = {**self.common_headers, **config["headers"]}
        return headers
    
    def get_curl_command(self, url: str, mode: JinaMode) -> str:
        """Generate curl command for a specific mode"""
        headers = self.get_config(mode)
        
        curl_cmd = f'curl "{self.base_url}{url}" \\\n'
        
        for key, value in headers.items():
            curl_cmd += f'  -H "{key}: {value}" \\\n'
        
        # Remove trailing backslash
        curl_cmd = curl_cmd.rstrip(' \\\n')
        
        return curl_cmd
    
    def recommend_mode(self, url: str, content_type: str = None) -> JinaMode:
        """Recommend optimal scraping mode based on URL and content type"""
        
        url_lower = url.lower()
        
        # API documentation
        if any(indicator in url_lower for indicator in ['/api/', '/reference/', '/docs/api']):
            return JinaMode.API_DOCS
        
        # Visual content
        if any(indicator in url_lower for indicator in ['/ui/', '/design/', '/components/', '/examples/']):
            return JinaMode.VISUAL
        
        # Tutorials
        if any(indicator in url_lower for indicator in ['/tutorial/', '/guide/', '/getting-started/', '/quickstart/']):
            return JinaMode.TUTORIAL
        
        # Complex documentation
        if any(indicator in url_lower for indicator in ['/documentation/', '/docs/', '/manual/']):
            return JinaMode.COMPREHENSIVE
        
        # Default
        return JinaMode.STANDARD
    
    def scrape_with_mode(self, url: str, mode: JinaMode) -> Optional[Dict]:
        """Scrape URL with specific mode configuration"""
        import requests
        
        headers = self.get_config(mode)
        
        try:
            # Use direct URL format for Jina
            response = requests.get(f"{self.base_url}{url}", headers=headers, timeout=30)
            response.raise_for_status()
            
            # Jina returns the content directly as text in markdown format
            content = response.text
            
            return {
                'url': url,
                'content': content,
                'mode': mode.value,
                'content_length': len(content),
                'success': True
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'url': url,
                'error': str(e),
                'mode': mode.value,
                'success': False
            }

def print_mode_comparison():
    """Print comparison of all available modes"""
    scraper = JinaOptimizedScraper("your_api_key")
    
    print("🔧 Jina Scraping Modes Comparison")
    print("=" * 60)
    
    for mode in JinaMode:
        config = scraper.mode_configs[mode]
        print(f"\n📋 {mode.value.upper().replace('_', ' ')}")
        print(f"   Description: {config['description']}")
        print(f"   Use Case: {config['use_case']}")
        print(f"   Engine: {config['headers'].get('X-Engine', 'default')}")
        print(f"   Images: {config['headers'].get('X-Retain-Images', 'default')}")
        print(f"   Token Budget: {config['headers'].get('X-Token-Budget', 'default')}")
        
        if 'X-Use-ReaderLM-v2' in config['headers']:
            print(f"   ⚠️  Uses ReaderLM-v2 (3x token cost)")

def generate_optimized_curl_examples():
    """Generate curl examples for different use cases"""
    api_key = os.getenv('JINA_API_KEY', 'your_api_key')
    scraper = JinaOptimizedScraper(api_key)
    
    examples = [
        ("React Documentation", "https://reactjs.org/docs/getting-started.html", JinaMode.STANDARD),
        ("Figma UI Components", "https://www.figma.com/design-system/components", JinaMode.VISUAL),
        ("Stripe API Docs", "https://stripe.com/docs/api", JinaMode.API_DOCS),
        ("Next.js Tutorial", "https://nextjs.org/learn/basics/create-nextjs-app", JinaMode.TUTORIAL),
        ("Complex Architecture", "https://docs.kubernetes.io/concepts/architecture/", JinaMode.COMPREHENSIVE)
    ]
    
    print("\n🚀 Optimized Curl Examples")
    print("=" * 60)
    
    for name, url, mode in examples:
        print(f"\n📖 {name} ({mode.value})")
        print(f"Use case: {scraper.mode_configs[mode]['use_case']}")
        print("```bash")
        print(scraper.get_curl_command(url, mode))
        print("```")

if __name__ == "__main__":
    print_mode_comparison()
    generate_optimized_curl_examples()