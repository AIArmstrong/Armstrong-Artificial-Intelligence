#!/usr/bin/env python3
"""
OpenRouter LLM Integration for Research Engine
Advanced research analysis and contradiction detection using OpenRouter's LLM gateway
"""

import json
import os
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import time
from datetime import datetime

@dataclass
class ResearchAnalysis:
    """Results from OpenRouter LLM analysis"""
    technology: str
    analysis_type: str
    confidence: float
    summary: str
    key_findings: List[str]
    contradictions: List[str]
    recommendations: List[str]
    quality_score: float
    timestamp: str

@dataclass
class ContradictionDetection:
    """Contradiction detection results"""
    source1: str
    source2: str
    contradiction_type: str
    severity: str  # 'high', 'medium', 'low'
    description: str
    resolution_suggestion: str
    confidence: float

class OpenRouterResearchAgent:
    """OpenRouter-powered research agent for advanced analysis"""
    
    def __init__(self, api_key: str, research_dir: str):
        self.api_key = api_key
        self.research_dir = Path(research_dir)
        self.base_url = "https://openrouter.ai/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://aai-research-engine.local",
            "X-Title": "AAI Research Engine"
        })
        
        # Model configuration
        self.models = {
            "analysis": "anthropic/claude-3.5-sonnet",
            "contradiction": "openai/gpt-4o",
            "validation": "google/gemini-pro-1.5",
            "synthesis": "anthropic/claude-3.5-sonnet"
        }
        
        # Rate limiting
        self.rate_limit = {
            "requests_per_minute": 20,
            "last_request_time": 0,
            "request_count": 0,
            "window_start": time.time()
        }
    
    def _rate_limit_check(self):
        """Check and enforce rate limiting"""
        current_time = time.time()
        
        # Reset window if needed
        if current_time - self.rate_limit["window_start"] >= 60:
            self.rate_limit["request_count"] = 0
            self.rate_limit["window_start"] = current_time
        
        # Check if we're at limit
        if self.rate_limit["request_count"] >= self.rate_limit["requests_per_minute"]:
            sleep_time = 60 - (current_time - self.rate_limit["window_start"])
            if sleep_time > 0:
                print(f"Rate limit reached, sleeping for {sleep_time:.1f}s")
                time.sleep(sleep_time)
                self.rate_limit["request_count"] = 0
                self.rate_limit["window_start"] = time.time()
        
        # Minimum delay between requests
        if current_time - self.rate_limit["last_request_time"] < 1:
            time.sleep(1 - (current_time - self.rate_limit["last_request_time"]))
        
        self.rate_limit["request_count"] += 1
        self.rate_limit["last_request_time"] = time.time()
    
    def _make_request(self, model: str, messages: List[Dict[str, str]], max_tokens: int = 4000) -> Optional[str]:
        """Make request to OpenRouter API"""
        self._rate_limit_check()
        
        try:
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.3,
                "top_p": 0.9
            }
            
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"OpenRouter API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error making OpenRouter request: {e}")
            return None
    
    def analyze_research_content(self, content: str, technology: str, analysis_type: str = "comprehensive") -> Optional[ResearchAnalysis]:
        """Analyze research content using OpenRouter LLM"""
        
        system_prompt = f"""You are an expert research analyst specializing in {technology}. 
        Analyze the provided research content and provide a comprehensive analysis.
        
        Focus on:
        1. Technical accuracy and completeness
        2. Implementation quality and best practices
        3. Potential issues or gaps
        4. Quality scoring (0.0-1.0)
        5. Specific recommendations for improvement
        
        Provide structured analysis with clear ratings and actionable insights."""
        
        user_prompt = f"""Analyze this {technology} research content:

{content}

Please provide:
1. Overall quality score (0.0-1.0)
2. Key findings (3-5 bullet points)
3. Any contradictions or inconsistencies
4. Specific recommendations
5. Confidence level in your analysis

Format your response as JSON with the following structure:
{{
    "quality_score": 0.0,
    "confidence": 0.0,
    "summary": "Brief summary",
    "key_findings": ["finding1", "finding2"],
    "contradictions": ["contradiction1"],
    "recommendations": ["rec1", "rec2"]
}}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._make_request(self.models["analysis"], messages)
        
        if response:
            try:
                # Extract JSON from response
                json_match = self._extract_json_from_response(response)
                if json_match:
                    result = json.loads(json_match)
                    
                    return ResearchAnalysis(
                        technology=technology,
                        analysis_type=analysis_type,
                        confidence=result.get("confidence", 0.0),
                        summary=result.get("summary", ""),
                        key_findings=result.get("key_findings", []),
                        contradictions=result.get("contradictions", []),
                        recommendations=result.get("recommendations", []),
                        quality_score=result.get("quality_score", 0.0),
                        timestamp=datetime.now().isoformat()
                    )
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing analysis response: {e}")
                print(f"Response: {response}")
        
        return None
    
    def detect_contradictions(self, content1: str, content2: str, source1: str, source2: str) -> List[ContradictionDetection]:
        """Detect contradictions between two research sources"""
        
        system_prompt = """You are an expert at detecting contradictions and inconsistencies between technical documentation.
        
        Analyze two research sources and identify any contradictions, conflicts, or inconsistencies.
        
        Focus on:
        1. Technical contradictions (different approaches, conflicting information)
        2. Implementation conflicts (incompatible patterns)
        3. Version differences (outdated vs current information)
        4. Best practice conflicts (conflicting recommendations)
        
        Rate severity: high (critical conflicts), medium (significant differences), low (minor inconsistencies)."""
        
        user_prompt = f"""Compare these two research sources and identify contradictions:

SOURCE 1 ({source1}):
{content1}

SOURCE 2 ({source2}):
{content2}

Please identify any contradictions and format as JSON array:
[
    {{
        "contradiction_type": "technical|implementation|version|best_practice",
        "severity": "high|medium|low",
        "description": "Clear description of the contradiction",
        "resolution_suggestion": "How to resolve this contradiction",
        "confidence": 0.0
    }}
]

If no contradictions found, return empty array []."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._make_request(self.models["contradiction"], messages)
        
        contradictions = []
        if response:
            try:
                json_match = self._extract_json_from_response(response)
                if json_match:
                    results = json.loads(json_match)
                    
                    for result in results:
                        contradiction = ContradictionDetection(
                            source1=source1,
                            source2=source2,
                            contradiction_type=result.get("contradiction_type", "unknown"),
                            severity=result.get("severity", "medium"),
                            description=result.get("description", ""),
                            resolution_suggestion=result.get("resolution_suggestion", ""),
                            confidence=result.get("confidence", 0.0)
                        )
                        contradictions.append(contradiction)
                        
            except json.JSONDecodeError as e:
                print(f"Error parsing contradiction response: {e}")
        
        return contradictions
    
    def validate_research_quality(self, content: str, technology: str, target_score: float = 0.90) -> Dict[str, Any]:
        """Validate research quality against target score"""
        
        system_prompt = f"""You are a quality validation expert for {technology} research.
        
        Evaluate research content against these criteria:
        1. Technical accuracy (30%)
        2. Completeness (25%)
        3. Clarity and organization (20%)
        4. Practical examples (15%)
        5. Best practices adherence (10%)
        
        Target quality score: {target_score}
        
        Provide detailed validation with specific areas for improvement."""
        
        user_prompt = f"""Validate this {technology} research content:

{content}

Please evaluate against the criteria and provide:
1. Overall quality score (0.0-1.0)
2. Detailed breakdown by criteria
3. Specific issues found
4. Actionable improvement suggestions
5. Whether it meets target score of {target_score}

Format as JSON:
{{
    "overall_score": 0.0,
    "meets_target": false,
    "criteria_scores": {{
        "technical_accuracy": 0.0,
        "completeness": 0.0,
        "clarity": 0.0,
        "examples": 0.0,
        "best_practices": 0.0
    }},
    "issues": ["issue1", "issue2"],
    "improvements": ["improvement1", "improvement2"],
    "validation_notes": "Additional notes"
}}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self._make_request(self.models["validation"], messages)
        
        if response:
            try:
                json_match = self._extract_json_from_response(response)
                if json_match:
                    return json.loads(json_match)
            except json.JSONDecodeError as e:
                print(f"Error parsing validation response: {e}")
        
        return {
            "overall_score": 0.0,
            "meets_target": False,
            "criteria_scores": {},
            "issues": [],
            "improvements": [],
            "validation_notes": "Validation failed"
        }
    
    def synthesize_research(self, contents: List[str], sources: List[str], technology: str) -> Optional[str]:
        """Synthesize multiple research sources into comprehensive content"""
        
        system_prompt = f"""You are an expert research synthesizer for {technology}.
        
        Combine multiple research sources into a comprehensive, coherent research document.
        
        Focus on:
        1. Eliminating redundancy while preserving all important information
        2. Resolving contradictions with clear explanations
        3. Organizing content logically
        4. Maintaining technical accuracy
        5. Creating cohesive narrative flow
        
        Output should be production-ready research documentation."""
        
        sources_text = ""
        for i, (content, source) in enumerate(zip(contents, sources), 1):
            sources_text += f"\nSOURCE {i} ({source}):\n{content}\n"
        
        user_prompt = f"""Synthesize these {technology} research sources into comprehensive documentation:

{sources_text}

Create a well-structured research document that:
1. Combines all relevant information
2. Resolves any contradictions
3. Eliminates redundancy
4. Maintains technical accuracy
5. Follows markdown formatting
6. Includes all important code examples
7. Provides clear implementation guidance

The output should be ready for use as general research documentation."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self._make_request(self.models["synthesis"], messages, max_tokens=6000)
    
    def _extract_json_from_response(self, response: str) -> Optional[str]:
        """Extract JSON from LLM response"""
        # Try to find JSON in response
        import re
        
        # Look for JSON objects
        json_patterns = [
            r'```json\s*(\{.*?\})\s*```',
            r'```\s*(\{.*?\})\s*```',
            r'(\{.*?\})',
            r'```json\s*(\[.*?\])\s*```',
            r'```\s*(\[.*?\])\s*```',
            r'(\[.*?\])'
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                return match.group(1)
        
        return None
    
    def process_research_file(self, file_path: Path) -> Optional[ResearchAnalysis]:
        """Process a research file with OpenRouter analysis"""
        try:
            content = file_path.read_text(encoding='utf-8')
            technology = file_path.stem
            
            # Extract technology from filename if it includes project suffix
            if '-' in technology:
                technology = technology.split('-')[0]
            
            return self.analyze_research_content(content, technology)
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return None
    
    def batch_analyze_research(self, research_dir: Path) -> List[ResearchAnalysis]:
        """Batch analyze all research files in directory"""
        analyses = []
        
        # Process knowledge base files
        knowledge_base = research_dir / "_knowledge-base"
        if knowledge_base.exists():
            for category_dir in knowledge_base.iterdir():
                if category_dir.is_dir():
                    for research_file in category_dir.glob("*.md"):
                        print(f"Analyzing {research_file}")
                        analysis = self.process_research_file(research_file)
                        if analysis:
                            analyses.append(analysis)
        
        return analyses
    
    def detect_cross_file_contradictions(self, research_dir: Path) -> List[ContradictionDetection]:
        """Detect contradictions across all research files"""
        contradictions = []
        
        # Collect all research files
        research_files = []
        knowledge_base = research_dir / "_knowledge-base"
        
        if knowledge_base.exists():
            for category_dir in knowledge_base.iterdir():
                if category_dir.is_dir():
                    for research_file in category_dir.glob("*.md"):
                        research_files.append(research_file)
        
        # Compare files pairwise
        for i in range(len(research_files)):
            for j in range(i + 1, len(research_files)):
                file1 = research_files[i]
                file2 = research_files[j]
                
                # Only compare files for same technology
                tech1 = file1.stem.split('-')[0]
                tech2 = file2.stem.split('-')[0]
                
                if tech1 == tech2:
                    try:
                        content1 = file1.read_text(encoding='utf-8')
                        content2 = file2.read_text(encoding='utf-8')
                        
                        print(f"Checking contradictions: {file1.name} vs {file2.name}")
                        file_contradictions = self.detect_contradictions(
                            content1, content2, str(file1), str(file2)
                        )
                        contradictions.extend(file_contradictions)
                        
                    except Exception as e:
                        print(f"Error comparing {file1} and {file2}: {e}")
        
        return contradictions
    
    def save_analysis_results(self, analyses: List[ResearchAnalysis], output_file: Path):
        """Save analysis results to file"""
        results = {
            "analyses": [asdict(analysis) for analysis in analyses],
            "summary": {
                "total_files": len(analyses),
                "average_quality": sum(a.quality_score for a in analyses) / len(analyses) if analyses else 0.0,
                "high_quality_count": len([a for a in analyses if a.quality_score >= 0.90]),
                "medium_quality_count": len([a for a in analyses if 0.75 <= a.quality_score < 0.90]),
                "low_quality_count": len([a for a in analyses if a.quality_score < 0.75])
            },
            "timestamp": datetime.now().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Analysis results saved to {output_file}")
    
    def save_contradiction_results(self, contradictions: List[ContradictionDetection], output_file: Path):
        """Save contradiction detection results"""
        results = {
            "contradictions": [asdict(contradiction) for contradiction in contradictions],
            "summary": {
                "total_contradictions": len(contradictions),
                "high_severity": len([c for c in contradictions if c.severity == "high"]),
                "medium_severity": len([c for c in contradictions if c.severity == "medium"]),
                "low_severity": len([c for c in contradictions if c.severity == "low"])
            },
            "timestamp": datetime.now().isoformat()
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Contradiction results saved to {output_file}")

def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python openrouter-integration.py <research_directory> [command]")
        print("Commands: analyze, contradictions, validate, synthesize")
        sys.exit(1)
    
    research_dir = Path(sys.argv[1])
    command = sys.argv[2] if len(sys.argv) > 2 else "analyze"
    
    # Load API key from environment
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        sys.exit(1)
    
    agent = OpenRouterResearchAgent(api_key, research_dir)
    
    if command == "analyze":
        print("Starting batch research analysis...")
        analyses = agent.batch_analyze_research(research_dir)
        
        if analyses:
            output_file = research_dir / "_map" / "openrouter-analysis.json"
            agent.save_analysis_results(analyses, output_file)
            
            print(f"\nAnalysis complete! Processed {len(analyses)} files")
            avg_quality = sum(a.quality_score for a in analyses) / len(analyses)
            print(f"Average quality score: {avg_quality:.2f}")
        else:
            print("No research files found to analyze")
    
    elif command == "contradictions":
        print("Starting contradiction detection...")
        contradictions = agent.detect_cross_file_contradictions(research_dir)
        
        if contradictions:
            output_file = research_dir / "validation" / "openrouter-contradictions.json"
            agent.save_contradiction_results(contradictions, output_file)
            
            print(f"\nContradiction detection complete! Found {len(contradictions)} contradictions")
            high_severity = len([c for c in contradictions if c.severity == "high"])
            if high_severity > 0:
                print(f"⚠️  {high_severity} high-severity contradictions need immediate attention")
        else:
            print("No contradictions detected")
    
    elif command == "validate":
        print("Starting quality validation...")
        # Implement validation command
        pass
    
    elif command == "synthesize":
        print("Starting research synthesis...")
        # Implement synthesis command
        pass
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()