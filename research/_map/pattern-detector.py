#!/usr/bin/env python3
"""
Cross-Project Pattern Detector
Analyzes project-specific research to identify patterns suitable for promotion to general knowledge
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import hashlib
import yaml

@dataclass
class PatternCandidate:
    """Represents a potential pattern for promotion to general knowledge"""
    pattern_id: str
    pattern_type: str  # 'implementation', 'configuration', 'integration', 'best_practice'
    technology: str
    description: str
    projects: List[str]
    similarity_score: float
    quality_scores: Dict[str, float]
    code_examples: List[str]
    confidence: float
    promotion_rationale: str

@dataclass
class PatternAnalysis:
    """Results of pattern analysis across projects"""
    candidates: List[PatternCandidate]
    cross_project_metrics: Dict[str, Any]
    recommendations: List[str]
    analysis_timestamp: str

class CrossProjectPatternDetector:
    """Detects patterns across project research for auto-promotion to general knowledge"""
    
    def __init__(self, research_dir: str):
        self.research_dir = Path(research_dir)
        self.knowledge_base = self.research_dir / "_knowledge-base"
        self.projects_dir = self.research_dir / "projects"
        self.validation_dir = self.research_dir / "validation"
        self.map_dir = self.research_dir / "_map"
        
        # Pattern detection thresholds
        self.similarity_threshold = 0.75
        self.min_projects = 2
        self.promotion_threshold = 0.85
        
    def analyze_patterns(self) -> PatternAnalysis:
        """Main analysis method - detects patterns across all projects"""
        print("Starting cross-project pattern analysis...")
        
        # Collect all project research
        project_research = self._collect_project_research()
        
        # Group by technology
        tech_groups = self._group_by_technology(project_research)
        
        # Detect patterns within each technology group
        candidates = []
        for tech, projects in tech_groups.items():
            if len(projects) >= self.min_projects:
                tech_candidates = self._detect_technology_patterns(tech, projects)
                candidates.extend(tech_candidates)
        
        # Calculate cross-project metrics
        metrics = self._calculate_cross_project_metrics(project_research)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(candidates, metrics)
        
        analysis = PatternAnalysis(
            candidates=candidates,
            cross_project_metrics=metrics,
            recommendations=recommendations,
            analysis_timestamp=self._get_timestamp()
        )
        
        # Save analysis results
        self._save_analysis(analysis)
        
        return analysis
    
    def _collect_project_research(self) -> Dict[str, Dict[str, Any]]:
        """Collect all project research files with metadata"""
        project_research = {}
        
        if not self.projects_dir.exists():
            return project_research
            
        for project_dir in self.projects_dir.iterdir():
            if not project_dir.is_dir():
                continue
                
            project_name = project_dir.name
            research_dir = project_dir / "_project-research"
            
            if not research_dir.exists():
                continue
                
            project_research[project_name] = {}
            
            for research_file in research_dir.glob("*.md"):
                # Read file content
                try:
                    content = research_file.read_text(encoding='utf-8')
                    
                    # Extract metadata
                    metadata = self._extract_metadata(content)
                    
                    # Extract code examples
                    code_examples = self._extract_code_examples(content)
                    
                    # Extract patterns
                    patterns = self._extract_patterns(content)
                    
                    project_research[project_name][research_file.stem] = {
                        'file_path': str(research_file),
                        'content': content,
                        'metadata': metadata,
                        'code_examples': code_examples,
                        'patterns': patterns,
                        'technology': research_file.stem
                    }
                    
                except Exception as e:
                    print(f"Error reading {research_file}: {e}")
                    continue
        
        return project_research
    
    def _group_by_technology(self, project_research: Dict[str, Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group project research by technology"""
        tech_groups = defaultdict(list)
        
        for project_name, project_files in project_research.items():
            for tech_name, file_data in project_files.items():
                tech_groups[tech_name].append({
                    'project': project_name,
                    'technology': tech_name,
                    **file_data
                })
        
        return dict(tech_groups)
    
    def _detect_technology_patterns(self, technology: str, projects: List[Dict[str, Any]]) -> List[PatternCandidate]:
        """Detect patterns within a specific technology across projects"""
        candidates = []
        
        # Implementation patterns
        impl_patterns = self._detect_implementation_patterns(technology, projects)
        candidates.extend(impl_patterns)
        
        # Configuration patterns
        config_patterns = self._detect_configuration_patterns(technology, projects)
        candidates.extend(config_patterns)
        
        # Integration patterns
        integration_patterns = self._detect_integration_patterns(technology, projects)
        candidates.extend(integration_patterns)
        
        # Best practice patterns
        best_practice_patterns = self._detect_best_practice_patterns(technology, projects)
        candidates.extend(best_practice_patterns)
        
        return candidates
    
    def _detect_implementation_patterns(self, technology: str, projects: List[Dict[str, Any]]) -> List[PatternCandidate]:
        """Detect common implementation patterns"""
        patterns = []
        
        # Group code examples by similarity
        code_groups = self._group_similar_code(projects)
        
        for group_id, code_examples in code_groups.items():
            if len(code_examples) >= self.min_projects:
                # Calculate similarity score
                similarity = self._calculate_code_similarity(code_examples)
                
                if similarity >= self.similarity_threshold:
                    # Get projects using this pattern
                    pattern_projects = [ex['project'] for ex in code_examples]
                    
                    # Get quality scores
                    quality_scores = {
                        proj: self._get_project_quality_score(proj, technology)
                        for proj in pattern_projects
                    }
                    
                    # Calculate confidence
                    confidence = self._calculate_pattern_confidence(
                        similarity, quality_scores, len(pattern_projects)
                    )
                    
                    if confidence >= self.promotion_threshold:
                        pattern = PatternCandidate(
                            pattern_id=f"impl_{technology}_{group_id}",
                            pattern_type="implementation",
                            technology=technology,
                            description=f"Common {technology} implementation pattern",
                            projects=pattern_projects,
                            similarity_score=similarity,
                            quality_scores=quality_scores,
                            code_examples=[ex['code'] for ex in code_examples],
                            confidence=confidence,
                            promotion_rationale=f"Used in {len(pattern_projects)} projects with {similarity:.2f} similarity"
                        )
                        patterns.append(pattern)
        
        return patterns
    
    def _detect_configuration_patterns(self, technology: str, projects: List[Dict[str, Any]]) -> List[PatternCandidate]:
        """Detect common configuration patterns"""
        patterns = []
        
        # Extract configuration sections
        config_sections = []
        for project in projects:
            configs = self._extract_configuration_sections(project['content'])
            for config in configs:
                config_sections.append({
                    'project': project['project'],
                    'config': config,
                    'technology': technology
                })
        
        # Group similar configurations
        config_groups = self._group_similar_configs(config_sections)
        
        for group_id, configs in config_groups.items():
            if len(configs) >= self.min_projects:
                similarity = self._calculate_config_similarity(configs)
                
                if similarity >= self.similarity_threshold:
                    pattern_projects = [cfg['project'] for cfg in configs]
                    quality_scores = {
                        proj: self._get_project_quality_score(proj, technology)
                        for proj in pattern_projects
                    }
                    
                    confidence = self._calculate_pattern_confidence(
                        similarity, quality_scores, len(pattern_projects)
                    )
                    
                    if confidence >= self.promotion_threshold:
                        pattern = PatternCandidate(
                            pattern_id=f"config_{technology}_{group_id}",
                            pattern_type="configuration",
                            technology=technology,
                            description=f"Common {technology} configuration pattern",
                            projects=pattern_projects,
                            similarity_score=similarity,
                            quality_scores=quality_scores,
                            code_examples=[cfg['config'] for cfg in configs],
                            confidence=confidence,
                            promotion_rationale=f"Configuration used in {len(pattern_projects)} projects"
                        )
                        patterns.append(pattern)
        
        return patterns
    
    def _detect_integration_patterns(self, technology: str, projects: List[Dict[str, Any]]) -> List[PatternCandidate]:
        """Detect common integration patterns"""
        patterns = []
        
        # Extract integration sections
        integration_sections = []
        for project in projects:
            integrations = self._extract_integration_sections(project['content'])
            for integration in integrations:
                integration_sections.append({
                    'project': project['project'],
                    'integration': integration,
                    'technology': technology
                })
        
        # Group similar integrations
        integration_groups = self._group_similar_integrations(integration_sections)
        
        for group_id, integrations in integration_groups.items():
            if len(integrations) >= self.min_projects:
                similarity = self._calculate_integration_similarity(integrations)
                
                if similarity >= self.similarity_threshold:
                    pattern_projects = [integ['project'] for integ in integrations]
                    quality_scores = {
                        proj: self._get_project_quality_score(proj, technology)
                        for proj in pattern_projects
                    }
                    
                    confidence = self._calculate_pattern_confidence(
                        similarity, quality_scores, len(pattern_projects)
                    )
                    
                    if confidence >= self.promotion_threshold:
                        pattern = PatternCandidate(
                            pattern_id=f"integration_{technology}_{group_id}",
                            pattern_type="integration",
                            technology=technology,
                            description=f"Common {technology} integration pattern",
                            projects=pattern_projects,
                            similarity_score=similarity,
                            quality_scores=quality_scores,
                            code_examples=[integ['integration'] for integ in integrations],
                            confidence=confidence,
                            promotion_rationale=f"Integration pattern used in {len(pattern_projects)} projects"
                        )
                        patterns.append(pattern)
        
        return patterns
    
    def _detect_best_practice_patterns(self, technology: str, projects: List[Dict[str, Any]]) -> List[PatternCandidate]:
        """Detect common best practice patterns"""
        patterns = []
        
        # Extract best practice sections
        best_practices = []
        for project in projects:
            practices = self._extract_best_practices(project['content'])
            for practice in practices:
                best_practices.append({
                    'project': project['project'],
                    'practice': practice,
                    'technology': technology
                })
        
        # Group similar best practices
        practice_groups = self._group_similar_practices(best_practices)
        
        for group_id, practices in practice_groups.items():
            if len(practices) >= self.min_projects:
                similarity = self._calculate_practice_similarity(practices)
                
                if similarity >= self.similarity_threshold:
                    pattern_projects = [prac['project'] for prac in practices]
                    quality_scores = {
                        proj: self._get_project_quality_score(proj, technology)
                        for proj in pattern_projects
                    }
                    
                    confidence = self._calculate_pattern_confidence(
                        similarity, quality_scores, len(pattern_projects)
                    )
                    
                    if confidence >= self.promotion_threshold:
                        pattern = PatternCandidate(
                            pattern_id=f"practice_{technology}_{group_id}",
                            pattern_type="best_practice",
                            technology=technology,
                            description=f"Common {technology} best practice",
                            projects=pattern_projects,
                            similarity_score=similarity,
                            quality_scores=quality_scores,
                            code_examples=[prac['practice'] for prac in practices],
                            confidence=confidence,
                            promotion_rationale=f"Best practice adopted in {len(pattern_projects)} projects"
                        )
                        patterns.append(pattern)
        
        return patterns
    
    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """Extract metadata from markdown content"""
        metadata = {}
        
        # Extract quality score
        quality_match = re.search(r'Quality Score:\s*(\d+\.\d+)', content)
        if quality_match:
            metadata['quality_score'] = float(quality_match.group(1))
        
        # Extract inheritance info
        inherits_match = re.search(r'\*\*Inherits from\*\*:\s*`([^`]+)`', content)
        if inherits_match:
            metadata['inherits_from'] = inherits_match.group(1)
        
        # Extract confidence
        confidence_match = re.search(r'\*\*Confidence\*\*:\s*(\d+\.\d+)', content)
        if confidence_match:
            metadata['confidence'] = float(confidence_match.group(1))
        
        return metadata
    
    def _extract_code_examples(self, content: str) -> List[str]:
        """Extract code examples from markdown content"""
        code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', content, re.DOTALL)
        return [block.strip() for block in code_blocks if block.strip()]
    
    def _extract_patterns(self, content: str) -> List[str]:
        """Extract pattern descriptions from content"""
        patterns = []
        
        # Look for pattern sections
        pattern_sections = re.findall(r'## (.*Pattern.*)\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        for title, content_block in pattern_sections:
            patterns.append(f"{title}: {content_block.strip()}")
        
        return patterns
    
    def _group_similar_code(self, projects: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group similar code examples"""
        code_groups = defaultdict(list)
        
        for project in projects:
            for code_example in project['code_examples']:
                # Create hash for similarity grouping
                code_hash = self._get_code_hash(code_example)
                code_groups[code_hash].append({
                    'project': project['project'],
                    'code': code_example
                })
        
        return dict(code_groups)
    
    def _get_code_hash(self, code: str) -> str:
        """Generate hash for code similarity"""
        # Normalize code (remove whitespace, comments)
        normalized = re.sub(r'\s+', ' ', code.strip())
        normalized = re.sub(r'//.*?\n', '', normalized)
        normalized = re.sub(r'/\*.*?\*/', '', normalized, flags=re.DOTALL)
        
        return hashlib.md5(normalized.encode()).hexdigest()[:8]
    
    def _calculate_code_similarity(self, code_examples: List[Dict[str, Any]]) -> float:
        """Calculate similarity score for code examples"""
        if len(code_examples) < 2:
            return 0.0
        
        # Simple similarity based on common patterns
        total_similarity = 0.0
        comparisons = 0
        
        for i in range(len(code_examples)):
            for j in range(i + 1, len(code_examples)):
                similarity = self._compare_code_strings(
                    code_examples[i]['code'], 
                    code_examples[j]['code']
                )
                total_similarity += similarity
                comparisons += 1
        
        return total_similarity / comparisons if comparisons > 0 else 0.0
    
    def _compare_code_strings(self, code1: str, code2: str) -> float:
        """Compare two code strings for similarity"""
        # Simple token-based similarity
        tokens1 = set(re.findall(r'\w+', code1.lower()))
        tokens2 = set(re.findall(r'\w+', code2.lower()))
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _get_project_quality_score(self, project: str, technology: str) -> float:
        """Get quality score for project's technology research"""
        try:
            # Look for quality score in project research
            project_file = self.projects_dir / project / "_project-research" / f"{technology}.md"
            if project_file.exists():
                content = project_file.read_text(encoding='utf-8')
                quality_match = re.search(r'Quality Score:\s*(\d+\.\d+)', content)
                if quality_match:
                    return float(quality_match.group(1))
        except:
            pass
        
        return 0.75  # Default project quality threshold
    
    def _calculate_pattern_confidence(self, similarity: float, quality_scores: Dict[str, float], project_count: int) -> float:
        """Calculate confidence score for pattern promotion"""
        avg_quality = sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0.75
        
        # Weighted confidence calculation
        confidence = (
            similarity * 0.4 +           # Pattern similarity
            avg_quality * 0.4 +          # Quality of implementations
            min(project_count / 5, 1.0) * 0.2  # Number of projects (capped at 5)
        )
        
        return confidence
    
    def _extract_configuration_sections(self, content: str) -> List[str]:
        """Extract configuration sections from content"""
        config_sections = []
        
        # Look for configuration blocks
        config_patterns = [
            r'## Configuration\n(.*?)(?=\n##|\Z)',
            r'### Configuration\n(.*?)(?=\n###|\n##|\Z)',
            r'## Setup\n(.*?)(?=\n##|\Z)',
            r'### Setup\n(.*?)(?=\n###|\n##|\Z)'
        ]
        
        for pattern in config_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            config_sections.extend([match.strip() for match in matches if match.strip()])
        
        return config_sections
    
    def _group_similar_configs(self, configs: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group similar configuration sections"""
        config_groups = defaultdict(list)
        
        for config in configs:
            config_hash = self._get_config_hash(config['config'])
            config_groups[config_hash].append(config)
        
        return dict(config_groups)
    
    def _get_config_hash(self, config: str) -> str:
        """Generate hash for configuration similarity"""
        # Normalize configuration
        normalized = re.sub(r'\s+', ' ', config.strip())
        normalized = re.sub(r'#.*?\n', '', normalized)  # Remove comments
        
        return hashlib.md5(normalized.encode()).hexdigest()[:8]
    
    def _calculate_config_similarity(self, configs: List[Dict[str, Any]]) -> float:
        """Calculate similarity for configuration sections"""
        if len(configs) < 2:
            return 0.0
        
        # Compare configurations for similarity
        total_similarity = 0.0
        comparisons = 0
        
        for i in range(len(configs)):
            for j in range(i + 1, len(configs)):
                similarity = self._compare_config_strings(
                    configs[i]['config'],
                    configs[j]['config']
                )
                total_similarity += similarity
                comparisons += 1
        
        return total_similarity / comparisons if comparisons > 0 else 0.0
    
    def _compare_config_strings(self, config1: str, config2: str) -> float:
        """Compare two configuration strings"""
        # Extract key-value pairs or settings
        settings1 = self._extract_config_settings(config1)
        settings2 = self._extract_config_settings(config2)
        
        if not settings1 or not settings2:
            return 0.0
        
        common_settings = settings1.intersection(settings2)
        all_settings = settings1.union(settings2)
        
        return len(common_settings) / len(all_settings) if all_settings else 0.0
    
    def _extract_config_settings(self, config: str) -> Set[str]:
        """Extract configuration settings from text"""
        settings = set()
        
        # Look for key-value patterns
        patterns = [
            r'(\w+)\s*[:=]\s*([^\n]+)',  # key: value or key = value
            r'(\w+)\s*=\s*([^\n]+)',     # key = value
            r'--(\w+)(?:\s+([^\s]+))?',  # --flag value
            r'-(\w+)(?:\s+([^\s]+))?'    # -flag value
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, config)
            for match in matches:
                if isinstance(match, tuple):
                    key = match[0]
                    value = match[1] if len(match) > 1 else ""
                    settings.add(f"{key}={value}")
                else:
                    settings.add(match)
        
        return settings
    
    def _extract_integration_sections(self, content: str) -> List[str]:
        """Extract integration sections from content"""
        integration_sections = []
        
        # Look for integration blocks
        integration_patterns = [
            r'## Integration.*?\n(.*?)(?=\n##|\Z)',
            r'### Integration.*?\n(.*?)(?=\n###|\n##|\Z)',
            r'## Implementation.*?\n(.*?)(?=\n##|\Z)',
            r'### Implementation.*?\n(.*?)(?=\n###|\n##|\Z)'
        ]
        
        for pattern in integration_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            integration_sections.extend([match.strip() for match in matches if match.strip()])
        
        return integration_sections
    
    def _group_similar_integrations(self, integrations: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group similar integration sections"""
        integration_groups = defaultdict(list)
        
        for integration in integrations:
            integration_hash = self._get_integration_hash(integration['integration'])
            integration_groups[integration_hash].append(integration)
        
        return dict(integration_groups)
    
    def _get_integration_hash(self, integration: str) -> str:
        """Generate hash for integration similarity"""
        # Focus on key integration patterns
        normalized = re.sub(r'\s+', ' ', integration.strip())
        
        # Extract key integration terms
        integration_terms = re.findall(r'\b(?:import|require|include|use|connect|configure|setup|install)\b', normalized.lower())
        
        key_content = ' '.join(integration_terms)
        return hashlib.md5(key_content.encode()).hexdigest()[:8]
    
    def _calculate_integration_similarity(self, integrations: List[Dict[str, Any]]) -> float:
        """Calculate similarity for integration sections"""
        if len(integrations) < 2:
            return 0.0
        
        total_similarity = 0.0
        comparisons = 0
        
        for i in range(len(integrations)):
            for j in range(i + 1, len(integrations)):
                similarity = self._compare_integration_strings(
                    integrations[i]['integration'],
                    integrations[j]['integration']
                )
                total_similarity += similarity
                comparisons += 1
        
        return total_similarity / comparisons if comparisons > 0 else 0.0
    
    def _compare_integration_strings(self, integration1: str, integration2: str) -> float:
        """Compare two integration strings"""
        # Extract integration patterns
        patterns1 = self._extract_integration_patterns(integration1)
        patterns2 = self._extract_integration_patterns(integration2)
        
        if not patterns1 or not patterns2:
            return 0.0
        
        common_patterns = patterns1.intersection(patterns2)
        all_patterns = patterns1.union(patterns2)
        
        return len(common_patterns) / len(all_patterns) if all_patterns else 0.0
    
    def _extract_integration_patterns(self, integration: str) -> Set[str]:
        """Extract integration patterns from text"""
        patterns = set()
        
        # Look for common integration patterns
        integration_patterns = [
            r'import\s+(\w+)',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]',
            r'use\s+(\w+)',
            r'connect\s*\(\s*([^)]+)\)',
            r'configure\s*\(\s*([^)]+)\)',
            r'new\s+(\w+)\s*\(',
            r'\.(\w+)\s*\(',
            r'@(\w+)'
        ]
        
        for pattern in integration_patterns:
            matches = re.findall(pattern, integration)
            patterns.update(matches)
        
        return patterns
    
    def _extract_best_practices(self, content: str) -> List[str]:
        """Extract best practice sections from content"""
        best_practices = []
        
        # Look for best practice blocks
        practice_patterns = [
            r'## Best Practices\n(.*?)(?=\n##|\Z)',
            r'### Best Practices\n(.*?)(?=\n###|\n##|\Z)',
            r'## Recommendations\n(.*?)(?=\n##|\Z)',
            r'### Recommendations\n(.*?)(?=\n###|\n##|\Z)'
        ]
        
        for pattern in practice_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            best_practices.extend([match.strip() for match in matches if match.strip()])
        
        # Also look for bullet points with best practices
        practice_bullets = re.findall(r'- (.*(?:best practice|recommendation|should|must|avoid).*)', content, re.IGNORECASE)
        best_practices.extend(practice_bullets)
        
        return best_practices
    
    def _group_similar_practices(self, practices: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group similar best practice sections"""
        practice_groups = defaultdict(list)
        
        for practice in practices:
            practice_hash = self._get_practice_hash(practice['practice'])
            practice_groups[practice_hash].append(practice)
        
        return dict(practice_groups)
    
    def _get_practice_hash(self, practice: str) -> str:
        """Generate hash for practice similarity"""
        # Focus on key practice terms
        normalized = re.sub(r'\s+', ' ', practice.strip().lower())
        
        # Extract key practice indicators
        practice_terms = re.findall(r'\b(?:should|must|avoid|never|always|recommend|best|practice|use|dont|better|prefer)\b', normalized)
        
        key_content = ' '.join(practice_terms)
        return hashlib.md5(key_content.encode()).hexdigest()[:8]
    
    def _calculate_practice_similarity(self, practices: List[Dict[str, Any]]) -> float:
        """Calculate similarity for best practice sections"""
        if len(practices) < 2:
            return 0.0
        
        total_similarity = 0.0
        comparisons = 0
        
        for i in range(len(practices)):
            for j in range(i + 1, len(practices)):
                similarity = self._compare_practice_strings(
                    practices[i]['practice'],
                    practices[j]['practice']
                )
                total_similarity += similarity
                comparisons += 1
        
        return total_similarity / comparisons if comparisons > 0 else 0.0
    
    def _compare_practice_strings(self, practice1: str, practice2: str) -> float:
        """Compare two practice strings"""
        # Extract practice concepts
        concepts1 = self._extract_practice_concepts(practice1)
        concepts2 = self._extract_practice_concepts(practice2)
        
        if not concepts1 or not concepts2:
            return 0.0
        
        common_concepts = concepts1.intersection(concepts2)
        all_concepts = concepts1.union(concepts2)
        
        return len(common_concepts) / len(all_concepts) if all_concepts else 0.0
    
    def _extract_practice_concepts(self, practice: str) -> Set[str]:
        """Extract practice concepts from text"""
        concepts = set()
        
        # Extract meaningful terms
        words = re.findall(r'\b\w+\b', practice.lower())
        
        # Filter for meaningful practice concepts
        meaningful_words = [
            word for word in words
            if len(word) > 3 and word not in {
                'should', 'must', 'avoid', 'never', 'always', 'recommend',
                'best', 'practice', 'better', 'prefer', 'this', 'that',
                'with', 'from', 'have', 'been', 'will', 'when', 'what'
            }
        ]
        
        concepts.update(meaningful_words)
        return concepts
    
    def _calculate_cross_project_metrics(self, project_research: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate metrics across all projects"""
        metrics = {
            'total_projects': len(project_research),
            'total_technologies': 0,
            'technology_distribution': {},
            'average_quality_by_tech': {},
            'pattern_coverage': {},
            'promotion_candidates': 0
        }
        
        all_technologies = set()
        tech_quality_scores = defaultdict(list)
        
        for project_name, project_files in project_research.items():
            for tech_name, file_data in project_files.items():
                all_technologies.add(tech_name)
                
                # Track technology distribution
                metrics['technology_distribution'][tech_name] = metrics['technology_distribution'].get(tech_name, 0) + 1
                
                # Track quality scores
                if 'metadata' in file_data and 'quality_score' in file_data['metadata']:
                    tech_quality_scores[tech_name].append(file_data['metadata']['quality_score'])
        
        metrics['total_technologies'] = len(all_technologies)
        
        # Calculate average quality by technology
        for tech, scores in tech_quality_scores.items():
            if scores:
                metrics['average_quality_by_tech'][tech] = sum(scores) / len(scores)
        
        return metrics
    
    def _generate_recommendations(self, candidates: List[PatternCandidate], metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # High-confidence promotion candidates
        high_confidence = [c for c in candidates if c.confidence >= 0.90]
        if high_confidence:
            recommendations.append(f"🎯 {len(high_confidence)} high-confidence patterns ready for immediate promotion")
        
        # Medium-confidence candidates needing review
        medium_confidence = [c for c in candidates if 0.80 <= c.confidence < 0.90]
        if medium_confidence:
            recommendations.append(f"📋 {len(medium_confidence)} patterns need review before promotion")
        
        # Technology-specific recommendations
        tech_usage = metrics.get('technology_distribution', {})
        popular_techs = [tech for tech, count in tech_usage.items() if count >= 3]
        if popular_techs:
            recommendations.append(f"🔥 Focus on {', '.join(popular_techs)} - used in 3+ projects")
        
        # Quality improvement recommendations
        avg_quality = metrics.get('average_quality_by_tech', {})
        low_quality_techs = [tech for tech, quality in avg_quality.items() if quality < 0.80]
        if low_quality_techs:
            recommendations.append(f"⚠️ Improve quality for {', '.join(low_quality_techs)} before promotion")
        
        return recommendations
    
    def _save_analysis(self, analysis: PatternAnalysis):
        """Save analysis results to file"""
        output_file = self.map_dir / "pattern-analysis.json"
        
        # Convert to serializable format
        analysis_dict = {
            'candidates': [asdict(candidate) for candidate in analysis.candidates],
            'cross_project_metrics': analysis.cross_project_metrics,
            'recommendations': analysis.recommendations,
            'analysis_timestamp': analysis.analysis_timestamp
        }
        
        with open(output_file, 'w') as f:
            json.dump(analysis_dict, f, indent=2)
        
        print(f"Pattern analysis saved to {output_file}")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def promote_pattern(self, pattern_id: str) -> bool:
        """Promote a pattern to general knowledge"""
        try:
            # Load analysis
            analysis_file = self.map_dir / "pattern-analysis.json"
            if not analysis_file.exists():
                print("No pattern analysis found. Run analyze_patterns() first.")
                return False
            
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)
            
            # Find pattern
            pattern_data = None
            for candidate in analysis_data['candidates']:
                if candidate['pattern_id'] == pattern_id:
                    pattern_data = candidate
                    break
            
            if not pattern_data:
                print(f"Pattern {pattern_id} not found in analysis")
                return False
            
            # Create general research file
            general_file = self._create_general_research_file(pattern_data)
            
            # Update inheritance mappings
            self._update_inheritance_mappings(pattern_data)
            
            # Log promotion
            self._log_pattern_promotion(pattern_data)
            
            print(f"Pattern {pattern_id} promoted to general knowledge: {general_file}")
            return True
            
        except Exception as e:
            print(f"Error promoting pattern {pattern_id}: {e}")
            return False
    
    def _create_general_research_file(self, pattern_data: Dict[str, Any]) -> str:
        """Create general research file from pattern"""
        technology = pattern_data['technology']
        pattern_type = pattern_data['pattern_type']
        
        # Create category directory
        category_dir = self.knowledge_base / technology
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename
        filename = f"{technology}-general.md"
        file_path = category_dir / filename
        
        # Generate content
        content = self._generate_general_research_content(pattern_data)
        
        # Write file
        with open(file_path, 'w') as f:
            f.write(content)
        
        return str(file_path)
    
    def _generate_general_research_content(self, pattern_data: Dict[str, Any]) -> str:
        """Generate general research content from pattern"""
        technology = pattern_data['technology']
        pattern_type = pattern_data['pattern_type']
        description = pattern_data['description']
        projects = pattern_data['projects']
        code_examples = pattern_data['code_examples']
        confidence = pattern_data['confidence']
        
        content = f"""# {technology.title()} - General Research

## Overview
{description} - Promoted from cross-project pattern analysis

## Key Concepts
- Common implementation patterns identified across {len(projects)} projects
- Validated {pattern_type} pattern with {confidence:.2f} confidence
- Reusable across different project contexts

## Implementation Patterns
### {pattern_type.replace('_', ' ').title()} Pattern
"""
        
        for i, example in enumerate(code_examples[:3], 1):
            content += f"""
#### Example {i}
```
{example}
```
"""
        
        content += f"""
## Best Practices
- Pattern validated across projects: {', '.join(projects)}
- Confidence score: {confidence:.2f}
- Suitable for general use across similar projects

## Quality Score: {confidence:.2f}
**Inheritance**: Base knowledge promoted from project patterns
**Source Quality**: Cross-project validation
**Reusability**: High - Used in {len(projects)} projects
**Completeness**: Derived from real implementations

## Research Sources
- Project implementations: {', '.join(projects)}
- Pattern analysis: Cross-project validation
- Confidence validation: {confidence:.2f}

## Cross-References
- Original projects: {', '.join(projects)}
- Pattern type: {pattern_type}
- Promotion date: {self._get_timestamp()}

## Tags
#general #{technology} #pattern-promoted #{pattern_type}
"""
        
        return content
    
    def _update_inheritance_mappings(self, pattern_data: Dict[str, Any]):
        """Update inheritance mappings after promotion"""
        # Update inheritance.md with new general research
        inheritance_file = self.map_dir / "inheritance.md"
        
        if inheritance_file.exists():
            content = inheritance_file.read_text()
            
            # Add promotion note
            promotion_note = f"""
### Pattern Promotion - {self._get_timestamp()}
**Pattern**: {pattern_data['pattern_id']}
**Technology**: {pattern_data['technology']}
**Type**: {pattern_data['pattern_type']}
**Projects**: {', '.join(pattern_data['projects'])}
**Confidence**: {pattern_data['confidence']:.2f}
**Status**: Promoted to general knowledge
"""
            
            # Append to file
            with open(inheritance_file, 'a') as f:
                f.write(promotion_note)
    
    def _log_pattern_promotion(self, pattern_data: Dict[str, Any]):
        """Log pattern promotion event"""
        log_file = self.validation_dir / "pattern-promotions.log"
        
        log_entry = f"{self._get_timestamp()} | PROMOTED | {pattern_data['pattern_id']} | {pattern_data['technology']} | {pattern_data['confidence']:.2f} | {', '.join(pattern_data['projects'])}\n"
        
        with open(log_file, 'a') as f:
            f.write(log_entry)

def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python pattern-detector.py <research_directory>")
        sys.exit(1)
    
    research_dir = sys.argv[1]
    detector = CrossProjectPatternDetector(research_dir)
    
    print("Starting cross-project pattern detection...")
    analysis = detector.analyze_patterns()
    
    print(f"\nPattern Analysis Complete!")
    print(f"Found {len(analysis.candidates)} pattern candidates")
    print(f"Recommendations: {len(analysis.recommendations)}")
    
    for rec in analysis.recommendations:
        print(f"  {rec}")
    
    # Show top candidates
    top_candidates = sorted(analysis.candidates, key=lambda x: x.confidence, reverse=True)[:5]
    
    if top_candidates:
        print(f"\nTop {len(top_candidates)} Pattern Candidates:")
        for i, candidate in enumerate(top_candidates, 1):
            print(f"  {i}. {candidate.pattern_id} ({candidate.technology}) - {candidate.confidence:.2f}")
            print(f"     Projects: {', '.join(candidate.projects)}")
            print(f"     Type: {candidate.pattern_type}")
    
    print(f"\nResults saved to {research_dir}/_map/pattern-analysis.json")

if __name__ == "__main__":
    main()