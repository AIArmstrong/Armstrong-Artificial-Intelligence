#!/usr/bin/env python3
"""
Example Recommendation Engine with Gap Analysis
Semantic matching system using embeddings to recommend examples and identify gaps
"""

import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Add the openrouter module to the path
sys.path.append(str(Path(__file__).parent / "openrouter"))

try:
    from .openrouter.embeddings import EmbeddingsEngine
    from .openrouter.router_client import OpenRouterClient
except ImportError:
    print("OpenRouter modules not found. Using placeholder implementation.")
    
    class EmbeddingGenerator:
        def generate_embeddings(self, text):
            # Simple hash-based similarity for placeholder
            return [hash(text) % 100 / 100.0] * 384
    
    class OpenRouterClient:
        def __init__(self):
            pass

class ExampleRecommendationEngine:
    def __init__(self):
        self.aai_root = Path("/mnt/c/Users/Brandon/AAI")
        self.examples_dir = self.aai_root / "examples"
        self.working_dir = self.examples_dir / "working"
        self.metadata_file = self.examples_dir / "metadata.json"
        self.prp_dir = self.aai_root / "PRPs"
        self.queue_file = self.aai_root / "brain/logs/queue.json"
        
        # Initialize embedding system
        try:
            self.embedding_generator = EmbeddingGenerator()
            self.router_client = OpenRouterClient()
        except:
            print("Using placeholder embedding system")
            self.embedding_generator = EmbeddingGenerator()
            self.router_client = None
    
    def load_examples_metadata(self):
        """Load examples metadata"""
        if not self.metadata_file.exists():
            return {"examples": {}, "index": {}}
        
        with open(self.metadata_file, 'r') as f:
            return json.load(f)
    
    def save_examples_metadata(self, metadata):
        """Save examples metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def extract_example_content(self, example_path):
        """Extract content from example file"""
        try:
            with open(example_path, 'r') as f:
                content = f.read()
            
            # Extract docstring and comments
            docstring_match = re.search(r'"""([\\s\\S]*?)"""', content)
            docstring = docstring_match.group(1) if docstring_match else ""
            
            # Extract function/class definitions
            functions = re.findall(r'def\\s+(\\w+)\\s*\\(', content)
            classes = re.findall(r'class\\s+(\\w+)\\s*\\(?', content)
            
            # Extract imports
            imports = re.findall(r'(?:from\\s+\\S+\\s+)?import\\s+([\\w\\s,]+)', content)
            
            return {
                'content': content,
                'docstring': docstring.strip(),
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'size': len(content)
            }
        except Exception as e:
            print(f"Error extracting content from {example_path}: {e}")
            return None
    
    def analyze_prp_requirements(self, prp_path):
        """Analyze PRP to extract technical requirements"""
        try:
            with open(prp_path, 'r') as f:
                content = f.read()
            
            # Extract technical requirements
            requirements = {
                'technologies': [],
                'apis': [],
                'patterns': [],
                'complexity': 'intermediate'
            }
            
            # Look for technology mentions
            tech_patterns = [
                r'\\b(python|javascript|react|fastapi|django|flask)\\b',
                r'\\b(api|rest|graphql|websocket)\\b',
                r'\\b(database|sql|mongodb|redis)\\b',
                r'\\b(async|await|threading|multiprocessing)\\b'
            ]
            
            for pattern in tech_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                requirements['technologies'].extend(matches)
            
            # Extract API requirements
            api_matches = re.findall(r'\\b(\\w+)\\s+API\\b', content, re.IGNORECASE)
            requirements['apis'] = api_matches
            
            # Determine complexity based on content
            complexity_indicators = {
                'beginner': ['simple', 'basic', 'intro', 'getting started'],
                'intermediate': ['integration', 'authentication', 'async', 'complex'],
                'advanced': ['optimization', 'scalability', 'performance', 'architecture']
            }
            
            content_lower = content.lower()
            for level, indicators in complexity_indicators.items():
                if any(indicator in content_lower for indicator in indicators):
                    requirements['complexity'] = level
                    break
            
            return requirements
        except Exception as e:
            print(f"Error analyzing PRP {prp_path}: {e}")
            return None
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts using embeddings"""
        try:
            emb1 = self.embedding_generator.generate_embeddings(text1)
            emb2 = self.embedding_generator.generate_embeddings(text2)
            
            # Calculate cosine similarity
            dot_product = sum(a * b for a, b in zip(emb1, emb2))
            magnitude1 = sum(a * a for a in emb1) ** 0.5
            magnitude2 = sum(b * b for b in emb2) ** 0.5
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return dot_product / (magnitude1 * magnitude2)
        except:
            # Fallback to simple text similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            return len(intersection) / len(union) if union else 0.0
    
    def find_similar_examples(self, requirements, threshold=0.7):
        """Find examples similar to requirements"""
        metadata = self.load_examples_metadata()
        examples = metadata.get('examples', {})
        
        similar_examples = []
        
        for example_id, example_data in examples.items():
            # Create comparison text from example
            example_text = f"{example_data.get('description', '')} {' '.join(example_data.get('tags', []))}"
            
            # Create requirements text
            req_text = f"{' '.join(requirements.get('technologies', []))} {' '.join(requirements.get('apis', []))}"
            
            # Calculate similarity
            similarity = self.calculate_similarity(example_text, req_text)
            
            if similarity >= threshold:
                similar_examples.append({
                    'id': example_id,
                    'similarity': similarity,
                    'data': example_data
                })
        
        # Sort by similarity
        similar_examples.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similar_examples
    
    def identify_gaps(self, requirements, existing_examples):
        """Identify gaps in example coverage"""
        gaps = []
        
        # Required technologies not covered
        required_techs = set(requirements.get('technologies', []))
        covered_techs = set()
        
        for example in existing_examples:
            covered_techs.update(example['data'].get('technologies', []))
        
        missing_techs = required_techs - covered_techs
        
        if missing_techs:
            gaps.append({
                'type': 'technology',
                'missing': list(missing_techs),
                'priority': 'high',
                'description': f"Missing examples for technologies: {', '.join(missing_techs)}"
            })
        
        # Required APIs not covered
        required_apis = set(requirements.get('apis', []))
        covered_apis = set()
        
        for example in existing_examples:
            # Extract API info from tags and description
            tags = example['data'].get('tags', [])
            description = example['data'].get('description', '')
            api_mentions = re.findall(r'\\b(\\w+)\\s+API\\b', description, re.IGNORECASE)
            covered_apis.update(api_mentions)
        
        missing_apis = required_apis - covered_apis
        
        if missing_apis:
            gaps.append({
                'type': 'api',
                'missing': list(missing_apis),
                'priority': 'medium',
                'description': f"Missing examples for APIs: {', '.join(missing_apis)}"
            })
        
        # Complexity coverage
        required_complexity = requirements.get('complexity', 'intermediate')
        complexity_covered = any(
            example['data'].get('complexity') == required_complexity
            for example in existing_examples
        )
        
        if not complexity_covered:
            gaps.append({
                'type': 'complexity',
                'missing': [required_complexity],
                'priority': 'medium',
                'description': f"Missing {required_complexity} level examples"
            })
        
        return gaps
    
    def generate_recommendations(self, prp_path=None, context_text=None):
        """Generate example recommendations based on PRP or context"""
        if prp_path:
            requirements = self.analyze_prp_requirements(prp_path)
        elif context_text:
            # Simple requirements extraction from context
            requirements = {
                'technologies': re.findall(r'\\b(python|javascript|api|async)\\b', context_text, re.IGNORECASE),
                'apis': re.findall(r'\\b(\\w+)\\s+API\\b', context_text, re.IGNORECASE),
                'complexity': 'intermediate'
            }
        else:
            return {'error': 'No PRP or context provided'}
        
        if not requirements:
            return {'error': 'Could not extract requirements'}
        
        # Find similar examples
        similar_examples = self.find_similar_examples(requirements)
        
        # Identify gaps
        gaps = self.identify_gaps(requirements, similar_examples)
        
        # Generate recommendations
        recommendations = {
            'timestamp': datetime.now().isoformat(),
            'requirements': requirements,
            'similar_examples': similar_examples[:5],  # Top 5
            'gaps': gaps,
            'recommendations': []
        }
        
        # Add specific recommendations
        if similar_examples:
            recommendations['recommendations'].append({
                'type': 'existing_examples',
                'priority': 'high',
                'description': f"Found {len(similar_examples)} similar examples",
                'examples': similar_examples[:3]  # Top 3
            })
        
        if gaps:
            recommendations['recommendations'].append({
                'type': 'create_examples',
                'priority': 'medium',
                'description': f"Create {len(gaps)} missing examples",
                'gaps': gaps
            })
        
        return recommendations
    
    def save_recommendations(self, recommendations, output_file="recommendations.json"):
        """Save recommendations to file"""
        output_path = self.examples_dir / output_file
        
        with open(output_path, 'w') as f:
            json.dump(recommendations, f, indent=2)
        
        return output_path
    
    def create_gap_analysis_report(self, recommendations):
        """Create human-readable gap analysis report"""
        report = f"""# Example Gap Analysis Report

## Generated: {recommendations['timestamp']}

## Requirements Analysis
**Technologies**: {', '.join(recommendations['requirements'].get('technologies', []))}
**APIs**: {', '.join(recommendations['requirements'].get('apis', []))}
**Complexity**: {recommendations['requirements'].get('complexity', 'unknown')}

## Similar Examples Found
"""
        
        for example in recommendations['similar_examples']:
            report += f"- **{example['data']['title']}** (similarity: {example['similarity']:.2f})\\n"
            report += f"  Category: {example['data']['category']}\\n"
            report += f"  Tags: {', '.join(example['data'].get('tags', []))}\\n\\n"
        
        report += "## Identified Gaps\\n"
        
        for gap in recommendations['gaps']:
            report += f"### {gap['type'].title()} Gap ({gap['priority']} priority)\\n"
            report += f"{gap['description']}\\n\\n"
        
        report += "## Recommendations\\n"
        
        for rec in recommendations['recommendations']:
            report += f"### {rec['type'].replace('_', ' ').title()}\\n"
            report += f"**Priority**: {rec['priority']}\\n"
            report += f"{rec['description']}\\n\\n"
        
        report += "---\\n*Generated by Example Recommendation Engine*"
        
        return report
    
    def process_current_queue(self):
        """Process current queue to generate recommendations"""
        try:
            with open(self.queue_file, 'r') as f:
                queue_data = json.load(f)
            
            active_tasks = queue_data.get('queue', [])
            
            all_recommendations = []
            
            for task in active_tasks:
                # Generate recommendations for each task
                context = f"{task['title']} {task['description']}"
                recommendations = self.generate_recommendations(context_text=context)
                
                if 'error' not in recommendations:
                    recommendations['task_id'] = task['id']
                    recommendations['task_title'] = task['title']
                    all_recommendations.append(recommendations)
            
            return all_recommendations
        except Exception as e:
            print(f"Error processing queue: {e}")
            return []

def main():
    engine = ExampleRecommendationEngine()
    
    # Process current queue for recommendations
    recommendations = engine.process_current_queue()
    
    print(f"Generated recommendations for {len(recommendations)} tasks")
    
    # Save recommendations
    if recommendations:
        output_path = engine.save_recommendations(recommendations, "queue-recommendations.json")
        print(f"Recommendations saved to: {output_path}")
        
        # Create gap analysis report
        for i, rec in enumerate(recommendations[:3]):  # First 3 tasks
            report = engine.create_gap_analysis_report(rec)
            report_path = engine.examples_dir / f"gap-analysis-{rec['task_id']}.md"
            
            with open(report_path, 'w') as f:
                f.write(report)
            
            print(f"Gap analysis report created: {report_path}")
    
    return recommendations

if __name__ == '__main__':
    main()