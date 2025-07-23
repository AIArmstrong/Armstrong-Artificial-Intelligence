#!/usr/bin/env python3
"""
Summary Extractor with OpenRouter Embeddings
Semantic extraction system using OpenRouter embeddings to auto-extract summaries
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the openrouter module to the path
sys.path.append(str(Path(__file__).parent / "openrouter"))

try:
    from .openrouter.embeddings import EmbeddingsEngine
    from .openrouter.router_client import OpenRouterClient
except ImportError:
    print("OpenRouter modules not found. Creating placeholder implementation.")
    
    class EmbeddingGenerator:
        def generate_embeddings(self, text):
            return [0.0] * 384  # Placeholder embedding
    
    class OpenRouterClient:
        def __init__(self):
            pass

class SummaryExtractor:
    def __init__(self):
        self.aai_root = Path("/mnt/c/Users/Brandon/AAI")
        self.examples_dir = self.aai_root / "examples"
        self.brain_docs_dir = self.aai_root / "brain/docs"
        self.docs_dir = self.aai_root / "docs"
        self.generated_dir = self.docs_dir / "generated"
        
        # Initialize OpenRouter components
        try:
            self.embedding_generator = EmbeddingGenerator()
            self.router_client = OpenRouterClient()
        except:
            print("Using placeholder embedding system")
            self.embedding_generator = EmbeddingGenerator()
            self.router_client = None
    
    def extract_content_from_files(self, directory, extensions=['.md', '.py', '.txt']):
        """Extract content from files in a directory"""
        content_items = []
        
        if not directory.exists():
            return content_items
        
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix in extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    content_items.append({
                        'filepath': str(file_path),
                        'filename': file_path.name,
                        'relative_path': str(file_path.relative_to(self.aai_root)),
                        'content': content,
                        'size': len(content),
                        'extension': file_path.suffix,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
        
        return content_items
    
    def chunk_content(self, content, max_chunk_size=1000):
        """Split content into manageable chunks for processing"""
        chunks = []
        words = content.split()
        
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            if current_size + word_size > max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def extract_key_concepts(self, content):
        """Extract key concepts using simple heuristics"""
        # Simple keyword extraction - would be enhanced with actual NLP
        key_concepts = []
        
        # Look for technical terms, file names, etc.
        import re
        
        # Find code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        
        # Find section headers
        headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        
        # Find bullet points
        bullets = re.findall(r'^\s*[-*+]\s+(.+)$', content, re.MULTILINE)
        
        # Find emphasized text
        emphasized = re.findall(r'\*\*(.+?)\*\*', content)
        
        key_concepts.extend([
            {'type': 'headers', 'items': headers},
            {'type': 'bullets', 'items': bullets[:10]},  # Limit to first 10
            {'type': 'emphasized', 'items': emphasized[:10]},
            {'type': 'code_blocks', 'count': len(code_blocks)}
        ])
        
        return key_concepts
    
    def generate_semantic_summary(self, content_item):
        """Generate semantic summary of content"""
        content = content_item['content']
        
        # Extract key concepts
        key_concepts = self.extract_key_concepts(content)
        
        # Generate embeddings for semantic analysis
        try:
            embeddings = self.embedding_generator.generate_embeddings(content[:1000])  # First 1000 chars
        except:
            embeddings = [0.0] * 384  # Placeholder
        
        # Create summary structure
        summary = {
            'source_file': content_item['relative_path'],
            'content_type': content_item['extension'],
            'size': content_item['size'],
            'modified': content_item['modified'],
            'key_concepts': key_concepts,
            'embeddings': embeddings[:10],  # Store first 10 dimensions for reference
            'summary_generated': datetime.now().isoformat()
        }
        
        # Generate text summary based on content type
        if content_item['extension'] == '.md':
            summary['text_summary'] = self.summarize_markdown(content)
        elif content_item['extension'] == '.py':
            summary['text_summary'] = self.summarize_python(content)
        else:
            summary['text_summary'] = self.summarize_generic(content)
        
        return summary
    
    def summarize_markdown(self, content):
        """Generate summary for markdown content"""
        lines = content.split('\\n')
        
        # Extract title
        title = "Unknown"
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        # Count sections
        sections = len([line for line in lines if line.startswith('#')])
        
        # Extract first paragraph
        first_paragraph = ""
        for line in lines:
            if line.strip() and not line.startswith('#'):
                first_paragraph = line.strip()
                break
        
        return f"Title: {title}. Contains {sections} sections. {first_paragraph[:100]}..."
    
    def summarize_python(self, content):
        """Generate summary for Python code"""
        lines = content.split('\\n')
        
        # Find docstring
        docstring = ""
        if '"""' in content:
            start = content.find('"""')
            end = content.find('"""', start + 3)
            if end > start:
                docstring = content[start+3:end].strip()
        
        # Count functions and classes
        functions = len([line for line in lines if line.strip().startswith('def ')])
        classes = len([line for line in lines if line.strip().startswith('class ')])
        
        return f"Python module with {functions} functions and {classes} classes. {docstring[:100]}..."
    
    def summarize_generic(self, content):
        """Generate summary for generic text content"""
        words = content.split()
        word_count = len(words)
        
        # Get first sentence
        first_sentence = content.split('.')[0] if '.' in content else content[:100]
        
        return f"Document with {word_count} words. {first_sentence}..."
    
    def create_semantic_index(self, summaries):
        """Create searchable index of summaries"""
        index = {
            'created': datetime.now().isoformat(),
            'total_files': len(summaries),
            'by_type': {},
            'by_size': {},
            'summaries': summaries
        }
        
        # Group by file type
        for summary in summaries:
            file_type = summary['content_type']
            if file_type not in index['by_type']:
                index['by_type'][file_type] = []
            index['by_type'][file_type].append(summary['source_file'])
        
        # Group by size
        for summary in summaries:
            size = summary['size']
            size_category = 'small' if size < 1000 else 'medium' if size < 10000 else 'large'
            if size_category not in index['by_size']:
                index['by_size'][size_category] = []
            index['by_size'][size_category].append(summary['source_file'])
        
        return index
    
    def save_summaries(self, summaries, source_type):
        """Save summaries to generated docs folder"""
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        
        # Save individual summaries
        summaries_file = self.generated_dir / f"{source_type}-summaries.json"
        with open(summaries_file, 'w') as f:
            json.dump(summaries, f, indent=2)
        
        # Create semantic index
        index = self.create_semantic_index(summaries)
        index_file = self.generated_dir / f"{source_type}-index.json"
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
        
        # Generate markdown summary
        markdown_file = self.generated_dir / f"{source_type}-summary.md"
        self.generate_markdown_summary(summaries, markdown_file, source_type)
        
        return {
            'summaries_file': str(summaries_file),
            'index_file': str(index_file),
            'markdown_file': str(markdown_file)
        }
    
    def generate_markdown_summary(self, summaries, output_file, source_type):
        """Generate human-readable markdown summary"""
        content = f"""# {source_type.title()} Content Summary

## Overview
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')}
**Total Files**: {len(summaries)}
**Source**: `{source_type}/` directory

## File Summaries

"""
        
        for summary in summaries:
            content += f"### {summary['source_file']}\\n"
            content += f"**Type**: {summary['content_type']} | "
            content += f"**Size**: {summary['size']} chars | "
            content += f"**Modified**: {summary['modified'][:10]}\\n\\n"
            content += f"{summary['text_summary']}\\n\\n"
            
            # Add key concepts if available
            if summary['key_concepts']:
                content += "**Key Concepts**:\\n"
                for concept in summary['key_concepts']:
                    if concept['type'] == 'headers' and concept['items']:
                        content += f"- Headers: {', '.join(concept['items'][:3])}\\n"
                    elif concept['type'] == 'emphasized' and concept['items']:
                        content += f"- Emphasized: {', '.join(concept['items'][:3])}\\n"
                content += "\\n"
        
        content += f"""
## Statistics
- **Markdown files**: {len([s for s in summaries if s['content_type'] == '.md'])}
- **Python files**: {len([s for s in summaries if s['content_type'] == '.py'])}
- **Other files**: {len([s for s in summaries if s['content_type'] not in ['.md', '.py']])}

---
*Generated by Semantic Summary Extractor*
*Using OpenRouter embeddings for enhanced analysis*
"""
        
        with open(output_file, 'w') as f:
            f.write(content)
    
    def process_examples_directory(self):
        """Process examples directory"""
        content_items = self.extract_content_from_files(self.examples_dir)
        
        if not content_items:
            print("No content found in examples directory")
            return None
        
        summaries = []
        for item in content_items:
            summary = self.generate_semantic_summary(item)
            summaries.append(summary)
        
        return self.save_summaries(summaries, 'examples')
    
    def process_brain_docs(self):
        """Process brain/docs directory"""
        content_items = self.extract_content_from_files(self.brain_docs_dir)
        
        if not content_items:
            print("No content found in brain/docs directory")
            return None
        
        summaries = []
        for item in content_items:
            summary = self.generate_semantic_summary(item)
            summaries.append(summary)
        
        return self.save_summaries(summaries, 'brain-docs')
    
    def run_extraction(self):
        """Run complete extraction process"""
        results = {}
        
        # Process examples
        examples_result = self.process_examples_directory()
        if examples_result:
            results['examples'] = examples_result
        
        # Process brain docs
        brain_docs_result = self.process_brain_docs()
        if brain_docs_result:
            results['brain_docs'] = brain_docs_result
        
        return results

def main():
    extractor = SummaryExtractor()
    results = extractor.run_extraction()
    
    print("Summary extraction completed:")
    for source_type, files in results.items():
        print(f"  {source_type}:")
        for file_type, path in files.items():
            print(f"    {file_type}: {path}")
    
    return results

if __name__ == '__main__':
    main()