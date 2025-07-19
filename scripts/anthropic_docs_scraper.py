#!/usr/bin/env python3
"""
Anthropic Documentation Scraper using Jina
Scrapes and organizes Anthropic docs from llms.txt into structured folders
"""

import os
import time
import requests
from pathlib import Path
from urllib.parse import urlparse
import re

class AnthropicDocsScraper:
    def __init__(self, base_path="/mnt/c/Users/Brandon/AAI/docs/official/anthropic"):
        self.base_path = Path(base_path)
        self.jina_base_url = "https://r.jina.ai/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AAI-Research-Bot/1.0'
        })
        
        # Create organized folder structure
        self.folders = {
            'api': self.base_path / 'api',
            'claude': self.base_path / 'claude', 
            'prompt-engineering': self.base_path / 'prompt-engineering',
            'use-cases': self.base_path / 'use-cases',
            'models': self.base_path / 'models',
            'admin': self.base_path / 'admin',
            'general': self.base_path / 'general'
        }
        
        # Create directories
        for folder in self.folders.values():
            folder.mkdir(parents=True, exist_ok=True)
    
    def categorize_url(self, url: str) -> str:
        """Categorize URL based on path structure"""
        if '/api/' in url and '/admin-api/' in url:
            return 'admin'
        elif '/api/' in url:
            return 'api'
        elif '/prompt-engineering/' in url:
            return 'prompt-engineering'
        elif '/use-case-guides/' in url:
            return 'use-cases'
        elif '/models/' in url:
            return 'models'
        elif '/about-claude/' in url or '/docs/' in url:
            return 'claude'
        else:
            return 'general'
    
    def clean_filename(self, url: str) -> str:
        """Extract clean filename from URL"""
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        
        # Get the last meaningful part
        if path_parts[-1].endswith('.md'):
            filename = path_parts[-1].replace('.md', '')
        else:
            filename = path_parts[-1] or path_parts[-2]
        
        # Clean filename
        filename = re.sub(r'[^\w\-_]', '_', filename)
        return f"{filename}.md"
    
    def scrape_with_jina(self, url: str) -> str:
        """Scrape content using Jina API"""
        try:
            jina_url = f"{self.jina_base_url}{url}"
            print(f"Scraping: {url}")
            
            response = self.session.get(jina_url, timeout=30)
            response.raise_for_status()
            
            content = response.text
            
            # Add metadata header
            metadata = f"""---
source_url: {url}
scraped_date: {time.strftime('%Y-%m-%d %H:%M:%S')}
scraper: Jina API via AAI Research Bot
category: anthropic_documentation
---

"""
            
            return metadata + content
            
        except Exception as e:
            print(f"Failed to scrape {url}: {str(e)}")
            return f"# Failed to scrape {url}\n\nError: {str(e)}\n"
    
    def save_content(self, content: str, category: str, filename: str):
        """Save scraped content to appropriate folder"""
        file_path = self.folders[category] / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Saved: {file_path}")
    
    def scrape_url_list(self, urls: list, delay: float = 1.0):
        """Scrape a list of URLs with delay between requests"""
        results = []
        
        for i, url in enumerate(urls):
            print(f"Progress: {i+1}/{len(urls)}")
            
            category = self.categorize_url(url)
            filename = self.clean_filename(url)
            content = self.scrape_with_jina(url)
            
            self.save_content(content, category, filename)
            
            results.append({
                'url': url,
                'category': category, 
                'filename': filename,
                'success': 'Failed to scrape' not in content
            })
            
            # Rate limiting
            if i < len(urls) - 1:
                time.sleep(delay)
        
        return results
    
    def generate_index(self, results: list):
        """Generate index file with all scraped documents"""
        index_content = f"""# Anthropic Documentation Index

Scraped on: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total documents: {len(results)}
Successful scrapes: {sum(1 for r in results if r['success'])}

## Categories

"""
        
        # Group by category
        categories = {}
        for result in results:
            cat = result['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        for category, docs in categories.items():
            index_content += f"### {category.title()}\n\n"
            for doc in docs:
                status = "✅" if doc['success'] else "❌"
                index_content += f"- {status} [{doc['filename']}](./{category}/{doc['filename']}) - {doc['url']}\n"
            index_content += "\n"
        
        # Save index
        index_path = self.base_path / "INDEX.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"Index saved: {index_path}")

# Priority URLs for immediate scraping
PRIORITY_URLS = [
    # Core Claude Documentation
    "https://docs.anthropic.com/en/docs/intro",
    "https://docs.anthropic.com/en/docs/get-started", 
    "https://docs.anthropic.com/en/docs/overview",
    
    # API Essentials
    "https://docs.anthropic.com/en/api/messages",
    "https://docs.anthropic.com/en/api/getting-started",
    "https://docs.anthropic.com/en/api/errors",
    
    # Prompt Engineering
    "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview",
    "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct",
    "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought",
    
    # Models
    "https://docs.anthropic.com/en/docs/about-claude/models/overview",
    "https://docs.anthropic.com/en/docs/about-claude/models/choosing-a-model",
    "https://docs.anthropic.com/en/docs/about-claude/pricing",
    
    # Tool Use (Critical for SuperClaude)
    "https://docs.anthropic.com/en/docs/build-with-claude/tool-use",
    "https://docs.anthropic.com/en/docs/build-with-claude/tool-use/tool-use-examples",
]

if __name__ == "__main__":
    scraper = AnthropicDocsScraper()
    
    print("Starting priority Anthropic documentation scrape...")
    results = scraper.scrape_url_list(PRIORITY_URLS, delay=2.0)
    scraper.generate_index(results)
    
    print(f"\nScraping complete!")
    print(f"Successfully scraped: {sum(1 for r in results if r['success'])}/{len(results)} documents")
    print(f"Documents saved to: {scraper.base_path}")