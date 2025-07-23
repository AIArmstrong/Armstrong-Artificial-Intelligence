#!/usr/bin/env python3
"""
AAI Workflow Memory Manager

Manages memory context for specific AAI workflows including /generate-prp, 
/implement, /analyze, and others. Captures successful patterns and provides
workflow-specific memory enhancement.
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path

from .memory_layer import MemoryLayer, MemoryItem, MemoryContext
from .config import MemoryConfig


@dataclass
class WorkflowPattern:
    """Represents a successful workflow pattern"""
    pattern_id: str
    user_id: str
    workflow_type: str  # 'prp_generation', 'implementation', 'analysis', etc.
    input_context: Dict[str, Any]
    actions_taken: List[Dict[str, Any]]
    successful_outcome: Dict[str, Any]
    confidence_score: float
    success_metrics: Dict[str, Any]
    created_at: datetime
    usage_count: int = 0
    success_rate: float = 1.0


@dataclass
class WorkflowContext:
    """Enhanced context for specific workflows"""
    workflow_type: str
    user_id: str
    input_context: Dict[str, Any]
    relevant_patterns: List[WorkflowPattern]
    memory_context: MemoryContext
    recommendations: List[str]
    confidence_score: float
    reasoning: str


class WorkflowMemoryManager:
    """
    Manages workflow-specific memory and pattern learning for AAI commands.
    
    Provides enhanced memory context for different types of AAI workflows,
    captures successful patterns, and learns from workflow outcomes.
    """
    
    def __init__(self, memory_layer: MemoryLayer):
        self.memory_layer = memory_layer
        self.config = memory_layer.config
        self.workflow_patterns = {}  # In-memory cache of patterns
        
        # Workflow-specific analyzers
        self.workflow_analyzers = {
            'generate-prp': self._analyze_prp_workflow,
            'implement': self._analyze_implementation_workflow,
            'analyze': self._analyze_analysis_workflow,
            'research': self._analyze_research_workflow,
            'build': self._analyze_build_workflow,
            'test': self._analyze_test_workflow,
            'document': self._analyze_documentation_workflow,
            'design': self._analyze_design_workflow
        }
    
    async def get_workflow_context(self, workflow_type: str, user_id: str, 
                                 input_context: Dict[str, Any]) -> Optional[WorkflowContext]:
        """
        Get enhanced workflow context with patterns and recommendations.
        
        Args:
            workflow_type: Type of workflow (e.g., 'generate-prp', 'implement')
            user_id: User identifier
            input_context: Context from the workflow input
        
        Returns:
            WorkflowContext with relevant patterns and recommendations
        """
        try:
            # Get base memory context
            query_context = self._extract_workflow_query(workflow_type, input_context)
            memory_context = await self.memory_layer.get_command_context(
                workflow_type, query_context, user_id
            )
            
            # Get relevant workflow patterns
            relevant_patterns = await self._get_relevant_patterns(
                workflow_type, user_id, input_context
            )
            
            # Generate workflow-specific recommendations
            recommendations = await self._generate_workflow_recommendations(
                workflow_type, input_context, relevant_patterns, memory_context
            )
            
            # Calculate workflow confidence
            confidence = self._calculate_workflow_confidence(
                memory_context, relevant_patterns, input_context
            )
            
            # Generate workflow reasoning
            reasoning = self._generate_workflow_reasoning(
                workflow_type, relevant_patterns, memory_context
            )
            
            return WorkflowContext(
                workflow_type=workflow_type,
                user_id=user_id,
                input_context=input_context,
                relevant_patterns=relevant_patterns,
                memory_context=memory_context,
                recommendations=recommendations,
                confidence_score=confidence,
                reasoning=reasoning
            )
            
        except Exception as e:
            print(f"Failed to get workflow context: {e}")
            return None
    
    async def capture_successful_pattern(self, command_type: str, original_args: Dict[str, Any],
                                       enhanced_args: Dict[str, Any], outcome: Dict[str, Any],
                                       memory_context: Optional[MemoryContext] = None):
        """
        Capture a successful workflow pattern for future learning.
        
        Args:
            command_type: Type of command that succeeded
            original_args: Original command arguments
            enhanced_args: Memory-enhanced arguments
            outcome: Successful outcome data
            memory_context: Memory context that was used
        """
        try:
            user_id = original_args.get('user_id', 'unknown')
            
            # Analyze the successful workflow
            analyzer = self.workflow_analyzers.get(command_type, self._analyze_generic_workflow)
            workflow_analysis = await analyzer(original_args, enhanced_args, outcome)
            
            # Create workflow pattern
            pattern = WorkflowPattern(
                pattern_id=self._generate_pattern_id(command_type, user_id),
                user_id=user_id,
                workflow_type=command_type,
                input_context=original_args,
                actions_taken=workflow_analysis.get('actions', []),
                successful_outcome=outcome,
                confidence_score=outcome.get('confidence_score', self.config.target_confidence),
                success_metrics=workflow_analysis.get('metrics', {}),
                created_at=datetime.now()
            )
            
            # Store pattern in memory layer
            await self._store_workflow_pattern(pattern)
            
            # Cache pattern for immediate use
            self.workflow_patterns[pattern.pattern_id] = pattern
            
            # Extract and store specific insights
            await self._extract_and_store_insights(pattern, memory_context)
            
        except Exception as e:
            print(f"Failed to capture successful pattern: {e}")
    
    async def _analyze_prp_workflow(self, original_args: Dict[str, Any], 
                                  enhanced_args: Dict[str, Any], 
                                  outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze successful PRP generation workflow"""
        actions = []
        metrics = {}
        
        # Extract successful actions
        if 'research_conducted' in outcome:
            actions.append({
                'action': 'research',
                'scope': outcome.get('research_scope', 'unknown'),
                'sources_count': outcome.get('sources_count', 0),
                'quality_score': outcome.get('research_quality', 0.0)
            })
        
        if 'technology_chosen' in outcome:
            actions.append({
                'action': 'technology_selection',
                'technology': outcome['technology_chosen'],
                'rationale': outcome.get('technology_rationale', '')
            })
        
        if 'architecture_decided' in outcome:
            actions.append({
                'action': 'architecture_design',
                'pattern': outcome['architecture_decided'],
                'complexity': outcome.get('architecture_complexity', 'medium')
            })
        
        # Extract success metrics
        metrics = {
            'prp_completeness': outcome.get('completeness_score', 0.0),
            'implementation_readiness': outcome.get('readiness_score', 0.0),
            'user_satisfaction': outcome.get('user_rating', 0.0),
            'time_to_complete': outcome.get('generation_time_minutes', 0)
        }
        
        return {
            'actions': actions,
            'metrics': metrics,
            'pattern_type': 'prp_generation',
            'complexity': self._assess_prp_complexity(original_args, outcome)
        }
    
    async def _analyze_implementation_workflow(self, original_args: Dict[str, Any], 
                                            enhanced_args: Dict[str, Any], 
                                            outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze successful implementation workflow"""
        actions = []
        metrics = {}
        
        # Extract implementation actions
        if 'code_generated' in outcome:
            actions.append({
                'action': 'code_generation',
                'language': outcome.get('programming_language', 'unknown'),
                'lines_of_code': outcome.get('lines_generated', 0),
                'files_created': outcome.get('files_count', 0)
            })
        
        if 'tests_written' in outcome:
            actions.append({
                'action': 'test_creation',
                'test_framework': outcome.get('test_framework', 'unknown'),
                'test_coverage': outcome.get('test_coverage', 0.0),
                'tests_count': outcome.get('tests_count', 0)
            })
        
        if 'dependencies_managed' in outcome:
            actions.append({
                'action': 'dependency_management',
                'dependencies_added': outcome.get('dependencies', []),
                'package_manager': outcome.get('package_manager', 'unknown')
            })
        
        # Extract implementation metrics
        metrics = {
            'code_quality': outcome.get('code_quality_score', 0.0),
            'test_pass_rate': outcome.get('test_pass_rate', 0.0),
            'build_success': outcome.get('build_successful', False),
            'implementation_time': outcome.get('implementation_time_minutes', 0)
        }
        
        return {
            'actions': actions,
            'metrics': metrics,
            'pattern_type': 'implementation',
            'complexity': self._assess_implementation_complexity(original_args, outcome)
        }
    
    async def _analyze_analysis_workflow(self, original_args: Dict[str, Any], 
                                       enhanced_args: Dict[str, Any], 
                                       outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze successful analysis workflow"""
        actions = []
        metrics = {}
        
        # Extract analysis actions
        if 'code_analyzed' in outcome:
            actions.append({
                'action': 'code_analysis',
                'analysis_type': outcome.get('analysis_type', 'general'),
                'files_analyzed': outcome.get('files_analyzed', 0),
                'issues_found': outcome.get('issues_count', 0)
            })
        
        if 'security_checked' in outcome:
            actions.append({
                'action': 'security_analysis',
                'vulnerabilities_found': outcome.get('vulnerabilities', 0),
                'security_score': outcome.get('security_score', 0.0)
            })
        
        if 'performance_analyzed' in outcome:
            actions.append({
                'action': 'performance_analysis',
                'bottlenecks_found': outcome.get('bottlenecks', 0),
                'performance_score': outcome.get('performance_score', 0.0)
            })
        
        # Extract analysis metrics
        metrics = {
            'analysis_depth': outcome.get('analysis_depth_score', 0.0),
            'insights_quality': outcome.get('insights_quality_score', 0.0),
            'actionable_items': outcome.get('actionable_items_count', 0),
            'analysis_time': outcome.get('analysis_time_minutes', 0)
        }
        
        return {
            'actions': actions,
            'metrics': metrics,
            'pattern_type': 'analysis',
            'complexity': self._assess_analysis_complexity(original_args, outcome)
        }
    
    async def _analyze_research_workflow(self, original_args: Dict[str, Any], 
                                       enhanced_args: Dict[str, Any], 
                                       outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze successful research workflow"""
        actions = []
        metrics = {}
        
        # Extract research actions
        if 'sources_scraped' in outcome:
            actions.append({
                'action': 'web_scraping',
                'sources_count': outcome.get('sources_scraped', 0),
                'pages_processed': outcome.get('pages_processed', 0),
                'scraping_tool': outcome.get('scraping_tool', 'jina')
            })
        
        if 'content_analyzed' in outcome:
            actions.append({
                'action': 'content_analysis',
                'content_quality': outcome.get('content_quality_avg', 0.0),
                'insights_extracted': outcome.get('insights_count', 0)
            })
        
        if 'research_synthesized' in outcome:
            actions.append({
                'action': 'synthesis',
                'synthesis_method': outcome.get('synthesis_method', 'ai'),
                'final_report_length': outcome.get('report_length', 0)
            })
        
        # Extract research metrics
        metrics = {
            'research_completeness': outcome.get('completeness_score', 0.0),
            'source_reliability': outcome.get('source_reliability_avg', 0.0),
            'information_accuracy': outcome.get('accuracy_score', 0.0),
            'research_time': outcome.get('research_time_minutes', 0)
        }
        
        return {
            'actions': actions,
            'metrics': metrics,
            'pattern_type': 'research',
            'complexity': self._assess_research_complexity(original_args, outcome)
        }
    
    async def _analyze_build_workflow(self, original_args: Dict[str, Any], 
                                    enhanced_args: Dict[str, Any], 
                                    outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze successful build workflow"""
        actions = []
        metrics = {}
        
        # Extract build actions
        if 'compilation_successful' in outcome:
            actions.append({
                'action': 'compilation',
                'build_tool': outcome.get('build_tool', 'unknown'),
                'compilation_time': outcome.get('compilation_time_seconds', 0),
                'warnings_count': outcome.get('warnings_count', 0)
            })
        
        if 'tests_executed' in outcome:
            actions.append({
                'action': 'testing',
                'test_runner': outcome.get('test_runner', 'unknown'),
                'tests_passed': outcome.get('tests_passed', 0),
                'tests_failed': outcome.get('tests_failed', 0),
                'coverage_percentage': outcome.get('test_coverage', 0.0)
            })
        
        # Extract build metrics
        metrics = {
            'build_success_rate': outcome.get('build_success_rate', 1.0),
            'build_time': outcome.get('total_build_time_minutes', 0),
            'artifact_size': outcome.get('artifact_size_mb', 0),
            'dependency_count': len(outcome.get('dependencies', []))
        }
        
        return {
            'actions': actions,
            'metrics': metrics,
            'pattern_type': 'build',
            'complexity': self._assess_build_complexity(original_args, outcome)
        }
    
    async def _analyze_test_workflow(self, original_args: Dict[str, Any], 
                                   enhanced_args: Dict[str, Any], 
                                   outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze successful test workflow"""
        actions = []
        metrics = {}
        
        # Extract test actions
        if 'unit_tests_run' in outcome:
            actions.append({
                'action': 'unit_testing',
                'test_count': outcome.get('unit_tests_run', 0),
                'test_framework': outcome.get('test_framework', 'unknown'),
                'mocking_used': outcome.get('mocking_used', False)
            })
        
        if 'integration_tests_run' in outcome:
            actions.append({
                'action': 'integration_testing',
                'test_count': outcome.get('integration_tests_run', 0),
                'external_dependencies': outcome.get('external_deps_tested', 0)
            })
        
        # Extract test metrics
        metrics = {
            'test_coverage': outcome.get('test_coverage_percentage', 0.0),
            'test_pass_rate': outcome.get('test_pass_rate', 0.0),
            'test_execution_time': outcome.get('test_execution_time_seconds', 0),
            'bugs_found': outcome.get('bugs_found_count', 0)
        }
        
        return {
            'actions': actions,
            'metrics': metrics,
            'pattern_type': 'test',
            'complexity': self._assess_test_complexity(original_args, outcome)
        }
    
    async def _analyze_documentation_workflow(self, original_args: Dict[str, Any], 
                                            enhanced_args: Dict[str, Any], 
                                            outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze successful documentation workflow"""
        actions = []
        metrics = {}
        
        # Extract documentation actions
        if 'api_docs_generated' in outcome:
            actions.append({
                'action': 'api_documentation',
                'documentation_tool': outcome.get('docs_tool', 'unknown'),
                'endpoints_documented': outcome.get('endpoints_documented', 0),
                'examples_included': outcome.get('examples_count', 0)
            })
        
        if 'user_guide_created' in outcome:
            actions.append({
                'action': 'user_guide',
                'guide_sections': outcome.get('guide_sections_count', 0),
                'screenshots_included': outcome.get('screenshots_count', 0)
            })
        
        # Extract documentation metrics
        metrics = {
            'documentation_completeness': outcome.get('docs_completeness_score', 0.0),
            'readability_score': outcome.get('readability_score', 0.0),
            'documentation_time': outcome.get('documentation_time_hours', 0),
            'pages_created': outcome.get('pages_created', 0)
        }
        
        return {
            'actions': actions,
            'metrics': metrics,
            'pattern_type': 'documentation',
            'complexity': self._assess_documentation_complexity(original_args, outcome)
        }
    
    async def _analyze_design_workflow(self, original_args: Dict[str, Any], 
                                     enhanced_args: Dict[str, Any], 
                                     outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze successful design workflow"""
        actions = []
        metrics = {}
        
        # Extract design actions
        if 'ui_mockups_created' in outcome:
            actions.append({
                'action': 'ui_design',
                'design_tool': outcome.get('design_tool', 'unknown'),
                'mockups_count': outcome.get('mockups_count', 0),
                'design_system_used': outcome.get('design_system_used', False)
            })
        
        if 'architecture_designed' in outcome:
            actions.append({
                'action': 'architecture_design',
                'diagram_type': outcome.get('diagram_type', 'unknown'),
                'components_designed': outcome.get('components_count', 0),
                'patterns_applied': len(outcome.get('design_patterns', []))
            })
        
        # Extract design metrics
        metrics = {
            'design_consistency_score': outcome.get('design_consistency', 0.0),
            'usability_score': outcome.get('usability_score', 0.0),
            'design_time': outcome.get('design_time_hours', 0),
            'revisions_count': outcome.get('design_revisions', 0)
        }
        
        return {
            'actions': actions,
            'metrics': metrics,
            'pattern_type': 'design',
            'complexity': self._assess_design_complexity(original_args, outcome)
        }
    
    async def _analyze_generic_workflow(self, original_args: Dict[str, Any], 
                                      enhanced_args: Dict[str, Any], 
                                      outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Generic workflow analysis for unknown command types"""
        actions = [{
            'action': 'generic_execution',
            'command_type': original_args.get('command_type', 'unknown'),
            'success': outcome.get('success', True)
        }]
        
        metrics = {
            'execution_time': outcome.get('execution_time_minutes', 0),
            'success_score': outcome.get('success_score', 0.8),
            'user_satisfaction': outcome.get('user_satisfaction', 0.8)
        }
        
        return {
            'actions': actions,
            'metrics': metrics,
            'pattern_type': 'generic',
            'complexity': 'medium'
        }
    
    async def _get_relevant_patterns(self, workflow_type: str, user_id: str, 
                                   input_context: Dict[str, Any]) -> List[WorkflowPattern]:
        """Get workflow patterns relevant to current context"""
        try:
            # Search for stored patterns in memory
            query = f"{workflow_type} pattern {input_context.get('topic', '')}"
            pattern_memories = await self.memory_layer.search_memories(
                user_id=user_id,
                query=query,
                content_type='workflow_pattern',
                limit=5,
                min_confidence=0.75
            )
            
            # Convert memories to workflow patterns
            patterns = []
            for memory in pattern_memories:
                try:
                    pattern_data = json.loads(memory.content)
                    pattern = WorkflowPattern(**pattern_data)
                    patterns.append(pattern)
                except Exception as e:
                    print(f"Failed to parse pattern from memory: {e}")
            
            # Add cached patterns
            for pattern in self.workflow_patterns.values():
                if (pattern.workflow_type == workflow_type and 
                    pattern.user_id == user_id and 
                    self._is_pattern_relevant(pattern, input_context)):
                    patterns.append(pattern)
            
            # Sort by relevance and success rate
            patterns.sort(key=lambda p: (p.success_rate, p.confidence_score), reverse=True)
            
            return patterns[:3]  # Return top 3 most relevant patterns
            
        except Exception as e:
            print(f"Failed to get relevant patterns: {e}")
            return []
    
    def _is_pattern_relevant(self, pattern: WorkflowPattern, input_context: Dict[str, Any]) -> bool:
        """Check if a pattern is relevant to the current input context"""
        # Simple relevance check - can be enhanced with more sophisticated matching
        pattern_context = pattern.input_context
        
        # Check for technology/domain overlap
        if 'technology' in input_context and 'technology' in pattern_context:
            if input_context['technology'].lower() in pattern_context['technology'].lower():
                return True
        
        # Check for feature/functionality overlap
        if 'feature' in input_context and 'feature' in pattern_context:
            feature_words = set(input_context['feature'].lower().split())
            pattern_words = set(pattern_context['feature'].lower().split())
            if len(feature_words.intersection(pattern_words)) > 0:
                return True
        
        # Check for domain/category overlap
        if 'domain' in input_context and 'domain' in pattern_context:
            if input_context['domain'] == pattern_context['domain']:
                return True
        
        return False
    
    async def _generate_workflow_recommendations(self, workflow_type: str, 
                                               input_context: Dict[str, Any],
                                               patterns: List[WorkflowPattern],
                                               memory_context: Optional[MemoryContext]) -> List[str]:
        """Generate workflow-specific recommendations"""
        recommendations = []
        
        if workflow_type == 'generate-prp':
            recommendations.extend(self._generate_prp_recommendations(input_context, patterns, memory_context))
        elif workflow_type == 'implement':
            recommendations.extend(self._generate_implementation_recommendations(input_context, patterns, memory_context))
        elif workflow_type == 'analyze':
            recommendations.extend(self._generate_analysis_recommendations(input_context, patterns, memory_context))
        elif workflow_type == 'research':
            recommendations.extend(self._generate_research_recommendations(input_context, patterns, memory_context))
        
        # Generic recommendations from patterns
        for pattern in patterns:
            if pattern.success_rate > 0.8:
                recommendations.append(f"Consider approach from previous successful {pattern.workflow_type}")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _generate_prp_recommendations(self, input_context: Dict[str, Any], 
                                    patterns: List[WorkflowPattern],
                                    memory_context: Optional[MemoryContext]) -> List[str]:
        """Generate PRP-specific recommendations"""
        recommendations = []
        
        # Technology recommendations from patterns
        successful_techs = []
        for pattern in patterns:
            if pattern.success_metrics.get('prp_completeness', 0) > 0.8:
                tech = pattern.input_context.get('technology')
                if tech:
                    successful_techs.append(tech)
        
        if successful_techs:
            most_common_tech = max(set(successful_techs), key=successful_techs.count)
            recommendations.append(f"Consider using {most_common_tech} based on previous successful PRPs")
        
        # Architecture recommendations
        if memory_context and memory_context.architectural_decisions:
            recommendations.append("Review previous architectural decisions for consistency")
        
        # Research depth recommendations
        avg_research_quality = 0
        research_count = 0
        for pattern in patterns:
            quality = pattern.success_metrics.get('research_quality', 0)
            if quality > 0:
                avg_research_quality += quality
                research_count += 1
        
        if research_count > 0:
            avg_quality = avg_research_quality / research_count
            if avg_quality > 0.8:
                recommendations.append("Maintain high research standards based on previous success")
        
        return recommendations
    
    def _generate_implementation_recommendations(self, input_context: Dict[str, Any], 
                                               patterns: List[WorkflowPattern],
                                               memory_context: Optional[MemoryContext]) -> List[str]:
        """Generate implementation-specific recommendations"""
        recommendations = []
        
        # Testing recommendations from patterns
        test_coverage_scores = []
        for pattern in patterns:
            coverage = pattern.success_metrics.get('test_coverage', 0)
            if coverage > 0:
                test_coverage_scores.append(coverage)
        
        if test_coverage_scores:
            avg_coverage = sum(test_coverage_scores) / len(test_coverage_scores)
            if avg_coverage > 0.8:
                recommendations.append(f"Aim for {avg_coverage:.0%} test coverage based on successful patterns")
        
        # Code quality recommendations
        quality_scores = []
        for pattern in patterns:
            quality = pattern.success_metrics.get('code_quality', 0)
            if quality > 0:
                quality_scores.append(quality)
        
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            if avg_quality > 0.8:
                recommendations.append("Maintain high code quality standards")
        
        return recommendations
    
    def _generate_analysis_recommendations(self, input_context: Dict[str, Any], 
                                         patterns: List[WorkflowPattern],
                                         memory_context: Optional[MemoryContext]) -> List[str]:
        """Generate analysis-specific recommendations"""
        recommendations = []
        
        # Analysis depth recommendations
        depth_scores = []
        for pattern in patterns:
            depth = pattern.success_metrics.get('analysis_depth', 0)
            if depth > 0:
                depth_scores.append(depth)
        
        if depth_scores:
            avg_depth = sum(depth_scores) / len(depth_scores)
            if avg_depth > 0.8:
                recommendations.append("Conduct deep analysis based on successful previous patterns")
        
        return recommendations
    
    def _generate_research_recommendations(self, input_context: Dict[str, Any], 
                                         patterns: List[WorkflowPattern],
                                         memory_context: Optional[MemoryContext]) -> List[str]:
        """Generate research-specific recommendations"""
        recommendations = []
        
        # Source count recommendations
        source_counts = []
        for pattern in patterns:
            for action in pattern.actions_taken:
                if action.get('action') == 'web_scraping':
                    source_counts.append(action.get('sources_count', 0))
        
        if source_counts:
            avg_sources = sum(source_counts) / len(source_counts)
            recommendations.append(f"Target {avg_sources:.0f} sources based on successful research patterns")
        
        return recommendations
    
    def _calculate_workflow_confidence(self, memory_context: Optional[MemoryContext], 
                                     patterns: List[WorkflowPattern],
                                     input_context: Dict[str, Any]) -> float:
        """Calculate confidence for workflow context"""
        confidence = self.config.min_confidence
        
        # Add confidence from memory context
        if memory_context:
            confidence += (memory_context.confidence_score - self.config.min_confidence) * 0.4
        
        # Add confidence from relevant patterns
        if patterns:
            pattern_confidence = sum(p.confidence_score for p in patterns) / len(patterns)
            confidence += (pattern_confidence - self.config.min_confidence) * 0.3
        
        # Add confidence from pattern success rates
        if patterns:
            avg_success_rate = sum(p.success_rate for p in patterns) / len(patterns)
            confidence += avg_success_rate * 0.1
        
        # Add confidence based on input context richness
        context_richness = len([v for v in input_context.values() if v])
        confidence += min(context_richness * 0.02, 0.15)
        
        return max(self.config.min_confidence, min(confidence, self.config.max_confidence))
    
    def _generate_workflow_reasoning(self, workflow_type: str, 
                                   patterns: List[WorkflowPattern],
                                   memory_context: Optional[MemoryContext]) -> str:
        """Generate reasoning for workflow recommendations"""
        reasoning_parts = []
        
        if patterns:
            successful_patterns = [p for p in patterns if p.success_rate > 0.8]
            reasoning_parts.append(f"Found {len(successful_patterns)} highly successful {workflow_type} patterns")
        
        if memory_context and memory_context.similar_items:
            reasoning_parts.append(f"Memory context includes {len(memory_context.similar_items)} relevant items")
        
        # Workflow-specific reasoning
        if workflow_type == 'generate-prp':
            reasoning_parts.append("for enhanced PRP generation with learned patterns")
        elif workflow_type == 'implement':
            reasoning_parts.append("for implementation with proven approaches")
        elif workflow_type == 'analyze':
            reasoning_parts.append("for analysis with effective methodologies")
        
        if reasoning_parts:
            return "Workflow context includes: " + ", ".join(reasoning_parts) + "."
        else:
            return f"Limited workflow context available for {workflow_type}."
    
    def _extract_workflow_query(self, workflow_type: str, input_context: Dict[str, Any]) -> str:
        """Extract query context for memory search"""
        if workflow_type == 'generate-prp':
            return f"{input_context.get('feature', '')} {input_context.get('technology', '')}"
        elif workflow_type == 'implement':
            return f"{input_context.get('feature', '')} implementation"
        elif workflow_type == 'analyze':
            return f"{input_context.get('target', '')} analysis"
        elif workflow_type == 'research':
            return input_context.get('topic', input_context.get('query', ''))
        
        return str(input_context)
    
    async def _store_workflow_pattern(self, pattern: WorkflowPattern):
        """Store workflow pattern in memory layer"""
        try:
            pattern_content = json.dumps(asdict(pattern), default=str)
            
            await self.memory_layer.store_memory(
                user_id=pattern.user_id,
                content=pattern_content,
                content_type='workflow_pattern',
                metadata={
                    'workflow_type': pattern.workflow_type,
                    'success_rate': pattern.success_rate,
                    'confidence_score': pattern.confidence_score,
                    'pattern_id': pattern.pattern_id
                },
                tags=['pattern', 'workflow', pattern.workflow_type]
            )
            
        except Exception as e:
            print(f"Failed to store workflow pattern: {e}")
    
    async def _extract_and_store_insights(self, pattern: WorkflowPattern, 
                                        memory_context: Optional[MemoryContext]):
        """Extract and store specific insights from successful patterns"""
        try:
            # Extract technology preferences
            if 'technology' in pattern.input_context:
                tech_insight = f"User successfully used {pattern.input_context['technology']} for {pattern.workflow_type}"
                await self.memory_layer.store_memory(
                    user_id=pattern.user_id,
                    content=tech_insight,
                    content_type='technology_preference',
                    metadata={
                        'technology': pattern.input_context['technology'],
                        'workflow_type': pattern.workflow_type,
                        'success_rate': pattern.success_rate
                    },
                    tags=['preference', 'technology']
                )
            
            # Extract approach preferences
            if pattern.actions_taken:
                for action in pattern.actions_taken:
                    action_insight = f"Successful {action.get('action', 'action')} in {pattern.workflow_type}"
                    await self.memory_layer.store_memory(
                        user_id=pattern.user_id,
                        content=action_insight,
                        content_type='approach_preference',
                        metadata={
                            'action_type': action.get('action'),
                            'workflow_type': pattern.workflow_type,
                            'success_metrics': action
                        },
                        tags=['preference', 'approach']
                    )
            
        except Exception as e:
            print(f"Failed to extract insights: {e}")
    
    def _generate_pattern_id(self, command_type: str, user_id: str) -> str:
        """Generate unique pattern ID"""
        import hashlib
        timestamp = datetime.now().isoformat()
        base_string = f"{command_type}_{user_id}_{timestamp}"
        return f"pattern_{hashlib.md5(base_string.encode()).hexdigest()[:12]}"
    
    def _assess_prp_complexity(self, original_args: Dict[str, Any], outcome: Dict[str, Any]) -> str:
        """Assess PRP complexity for pattern categorization"""
        complexity_score = 0
        
        # Add complexity based on research scope
        if outcome.get('sources_count', 0) > 20:
            complexity_score += 2
        elif outcome.get('sources_count', 0) > 10:
            complexity_score += 1
        
        # Add complexity based on technology stack
        if 'technology' in original_args:
            tech_count = len(original_args['technology'].split())
            complexity_score += min(tech_count, 2)
        
        # Add complexity based on integration requirements
        if outcome.get('integrations_count', 0) > 3:
            complexity_score += 2
        elif outcome.get('integrations_count', 0) > 1:
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _assess_implementation_complexity(self, original_args: Dict[str, Any], outcome: Dict[str, Any]) -> str:
        """Assess implementation complexity"""
        complexity_score = 0
        
        # Lines of code
        loc = outcome.get('lines_generated', 0)
        if loc > 1000:
            complexity_score += 2
        elif loc > 500:
            complexity_score += 1
        
        # Files created
        files = outcome.get('files_count', 0)
        if files > 10:
            complexity_score += 2
        elif files > 5:
            complexity_score += 1
        
        # Dependencies
        deps = len(outcome.get('dependencies', []))
        if deps > 10:
            complexity_score += 2
        elif deps > 5:
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _assess_analysis_complexity(self, original_args: Dict[str, Any], outcome: Dict[str, Any]) -> str:
        """Assess analysis complexity"""
        complexity_score = 0
        
        # Files analyzed
        files = outcome.get('files_analyzed', 0)
        if files > 50:
            complexity_score += 2
        elif files > 20:
            complexity_score += 1
        
        # Analysis types
        if outcome.get('security_analysis', False):
            complexity_score += 1
        if outcome.get('performance_analysis', False):
            complexity_score += 1
        if outcome.get('code_quality_analysis', False):
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _assess_research_complexity(self, original_args: Dict[str, Any], outcome: Dict[str, Any]) -> str:
        """Assess research complexity"""
        complexity_score = 0
        
        # Sources scraped
        sources = outcome.get('sources_scraped', 0)
        if sources > 50:
            complexity_score += 2
        elif sources > 20:
            complexity_score += 1
        
        # Pages processed
        pages = outcome.get('pages_processed', 0)
        if pages > 100:
            complexity_score += 2
        elif pages > 50:
            complexity_score += 1
        
        # Research depth
        if outcome.get('deep_analysis', False):
            complexity_score += 1
        if outcome.get('cross_references', 0) > 10:
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _assess_build_complexity(self, original_args: Dict[str, Any], outcome: Dict[str, Any]) -> str:
        """Assess build complexity"""
        complexity_score = 0
        
        # Build time
        build_time = outcome.get('total_build_time_minutes', 0)
        if build_time > 30:
            complexity_score += 2
        elif build_time > 10:
            complexity_score += 1
        
        # Dependencies
        deps = len(outcome.get('dependencies', []))
        if deps > 20:
            complexity_score += 2
        elif deps > 10:
            complexity_score += 1
        
        # Build steps
        if outcome.get('compilation_successful', False):
            complexity_score += 1
        if outcome.get('tests_executed', False):
            complexity_score += 1
        if outcome.get('artifact_size_mb', 0) > 100:
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _assess_test_complexity(self, original_args: Dict[str, Any], outcome: Dict[str, Any]) -> str:
        """Assess test complexity"""
        complexity_score = 0
        
        # Test count
        unit_tests = outcome.get('unit_tests_run', 0)
        integration_tests = outcome.get('integration_tests_run', 0)
        total_tests = unit_tests + integration_tests
        
        if total_tests > 1000:
            complexity_score += 2
        elif total_tests > 500:
            complexity_score += 1
        
        # Test coverage
        coverage = outcome.get('test_coverage_percentage', 0)
        if coverage > 90:
            complexity_score += 1
        
        # External dependencies tested
        if outcome.get('external_deps_tested', 0) > 5:
            complexity_score += 1
        
        # Mocking complexity
        if outcome.get('mocking_used', False):
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _assess_documentation_complexity(self, original_args: Dict[str, Any], outcome: Dict[str, Any]) -> str:
        """Assess documentation complexity"""
        complexity_score = 0
        
        # Pages created
        pages = outcome.get('pages_created', 0)
        if pages > 50:
            complexity_score += 2
        elif pages > 20:
            complexity_score += 1
        
        # Documentation types
        if outcome.get('api_docs_generated', False):
            complexity_score += 1
        if outcome.get('user_guide_created', False):
            complexity_score += 1
        if outcome.get('screenshots_count', 0) > 10:
            complexity_score += 1
        
        # Documentation time
        if outcome.get('documentation_time_hours', 0) > 40:
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def _assess_design_complexity(self, original_args: Dict[str, Any], outcome: Dict[str, Any]) -> str:
        """Assess design complexity"""
        complexity_score = 0
        
        # Mockups created
        mockups = outcome.get('mockups_count', 0)
        if mockups > 20:
            complexity_score += 2
        elif mockups > 10:
            complexity_score += 1
        
        # Design types
        if outcome.get('ui_mockups_created', False):
            complexity_score += 1
        if outcome.get('architecture_designed', False):
            complexity_score += 1
        
        # Design patterns
        patterns = len(outcome.get('design_patterns', []))
        if patterns > 5:
            complexity_score += 1
        
        # Revisions
        if outcome.get('design_revisions', 0) > 5:
            complexity_score += 1
        
        if complexity_score >= 4:
            return 'high'
        elif complexity_score >= 2:
            return 'medium'
        else:
            return 'low'


def test_workflow_memory():
    """Test workflow memory functionality"""
    import asyncio
    from .memory_layer import MemoryLayer
    from .config import MemoryConfig
    
    async def test_operations():
        config = MemoryConfig.for_testing()
        memory_layer = MemoryLayer(config)
        workflow_manager = WorkflowMemoryManager(memory_layer)
        
        print("Testing Workflow Memory Manager")
        print("=" * 40)
        
        # Test workflow context
        context = await workflow_manager.get_workflow_context(
            workflow_type='generate-prp',
            user_id='test_user',
            input_context={
                'feature': 'user authentication system',
                'technology': 'FastAPI',
                'domain': 'web_application'
            }
        )
        
        if context:
            print("✅ Workflow context generated:")
            print(f"   Workflow type: {context.workflow_type}")
            print(f"   Confidence: {context.confidence_score:.2f}")
            print(f"   Patterns found: {len(context.relevant_patterns)}")
            print(f"   Recommendations: {len(context.recommendations)}")
            print(f"   Reasoning: {context.reasoning}")
        else:
            print("⚠️ No workflow context generated")
        
        # Test successful pattern capture
        await workflow_manager.capture_successful_pattern(
            command_type='generate-prp',
            original_args={
                'feature': 'user authentication',
                'technology': 'FastAPI',
                'user_id': 'test_user'
            },
            enhanced_args={
                'feature': 'user authentication',
                'technology': 'FastAPI',
                'memory_context': {'similar_prps': [], 'user_preferences': {}}
            },
            outcome={
                'success': True,
                'confidence_score': 0.9,
                'research_conducted': True,
                'research_scope': 'comprehensive',
                'sources_count': 25,
                'research_quality': 0.85,
                'technology_chosen': 'FastAPI',
                'completeness_score': 0.9,
                'readiness_score': 0.85,
                'user_rating': 4.5,
                'generation_time_minutes': 15
            }
        )
        
        print("\n✅ Successful pattern captured")
        
        # Test pattern retrieval
        patterns = await workflow_manager._get_relevant_patterns(
            workflow_type='generate-prp',
            user_id='test_user',
            input_context={
                'feature': 'authentication system',
                'technology': 'FastAPI'
            }
        )
        
        print(f"\n🔍 Retrieved patterns: {len(patterns)}")
        for pattern in patterns:
            print(f"   - {pattern.workflow_type}: {pattern.confidence_score:.2f} confidence")
    
    asyncio.run(test_operations())


if __name__ == "__main__":
    test_workflow_memory()