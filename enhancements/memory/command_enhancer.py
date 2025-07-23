#!/usr/bin/env python3
"""
AAI Command Enhancement Layer - Memory Integration

Enhances ALL existing AAI commands with persistent memory capabilities.
Preserves existing command functionality while adding memory intelligence.
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

# Memory and data models
from .memory_layer import MemoryLayer, MemoryContext
from .workflow_memory import WorkflowMemoryManager
from .config import MemoryConfig

@dataclass
class CommandEnhancement:
    """Represents memory enhancement for an AAI command"""
    command_type: str
    original_args: Dict[str, Any]
    memory_context: Optional[MemoryContext]
    enhanced_args: Dict[str, Any]
    confidence_score: float
    enhancement_timestamp: datetime

class AAICommandEnhancer:
    """
    Enhances existing AAI commands with memory capabilities.
    
    This class intercepts AAI command execution and adds memory context
    without modifying the original command functionality.
    """
    
    def __init__(self, config: MemoryConfig = None):
        self.config = config or MemoryConfig()
        self.memory_layer = MemoryLayer(self.config)
        self.workflow_memory = WorkflowMemoryManager(self.memory_layer)
        self.enhancement_history = []
        
        # Command enhancement strategies
        self.command_enhancers = {
            'generate-prp': self._enhance_generate_prp,
            'implement': self._enhance_implement,
            'analyze': self._enhance_analyze,
            'research': self._enhance_research,
            'build': self._enhance_build,
            'test': self._enhance_test,
            'document': self._enhance_document,
            'design': self._enhance_design
        }
        
    async def enhance_command(self, command_type: str, args: Dict[str, Any]) -> CommandEnhancement:
        """
        Enhance an AAI command with memory context.
        
        Args:
            command_type: Type of AAI command (e.g., 'generate-prp', 'implement')
            args: Original command arguments
        
        Returns:
            CommandEnhancement with memory-enhanced arguments
        """
        try:
            # Get user context for personalized memory
            user_id = self._get_user_id(args)
            
            # Retrieve relevant memory context
            memory_context = await self._get_memory_context(command_type, args, user_id)
            
            # Apply command-specific enhancement
            enhancer = self.command_enhancers.get(command_type, self._enhance_generic)
            enhanced_args = await enhancer(args, memory_context)
            
            # Calculate enhancement confidence
            confidence = self._calculate_enhancement_confidence(memory_context, enhanced_args)
            
            # Create enhancement record
            enhancement = CommandEnhancement(
                command_type=command_type,
                original_args=args,
                memory_context=memory_context,
                enhanced_args=enhanced_args,
                confidence_score=confidence,
                enhancement_timestamp=datetime.now()
            )
            
            # Store enhancement for learning
            self.enhancement_history.append(enhancement)
            
            # Log enhancement for AAI brain learning
            await self._log_enhancement(enhancement)
            
            return enhancement
            
        except Exception as e:
            # Fallback: return original args if enhancement fails
            print(f"Memory enhancement failed for {command_type}: {e}")
            return CommandEnhancement(
                command_type=command_type,
                original_args=args,
                memory_context=None,
                enhanced_args=args,  # Fallback to original
                confidence_score=0.0,
                enhancement_timestamp=datetime.now()
            )
    
    async def _enhance_generate_prp(self, args: Dict[str, Any], memory_context: MemoryContext) -> Dict[str, Any]:
        """Enhance /generate-prp command with memory intelligence"""
        enhanced_args = args.copy()
        
        if memory_context:
            # Add PRP patterns and successful implementations
            enhanced_args['memory_context'] = {
                'similar_prps': memory_context.similar_prps,
                'implementation_patterns': memory_context.implementation_patterns,
                'user_preferences': memory_context.user_preferences,
                'architectural_decisions': memory_context.architectural_decisions
            }
            
            # Add research context from previous PRPs
            if memory_context.research_findings:
                enhanced_args['research_context'] = memory_context.research_findings
            
            # Add learned technology preferences
            if memory_context.technology_preferences:
                enhanced_args['tech_preferences'] = memory_context.technology_preferences
            
            # Add confidence scoring for PRP recommendations
            enhanced_args['memory_confidence'] = memory_context.confidence_score
            
            # Add WHY rationale from memory
            enhanced_args['memory_rationale'] = (
                f"Memory enhancement provides {len(memory_context.similar_prps)} similar PRPs, "
                f"{len(memory_context.implementation_patterns)} implementation patterns, "
                f"and user preferences with {memory_context.confidence_score:.1%} confidence."
            )
        
        return enhanced_args
    
    async def _enhance_implement(self, args: Dict[str, Any], memory_context: MemoryContext) -> Dict[str, Any]:
        """Enhance /implement command with memory intelligence"""
        enhanced_args = args.copy()
        
        if memory_context:
            # Add implementation patterns and coding preferences
            enhanced_args['memory_context'] = {
                'implementation_patterns': memory_context.implementation_patterns,
                'coding_preferences': memory_context.user_preferences.get('coding', {}),
                'library_preferences': memory_context.user_preferences.get('libraries', {}),
                'successful_solutions': memory_context.successful_solutions,
                'testing_patterns': memory_context.testing_patterns
            }
            
            # Add architectural context
            if memory_context.architectural_decisions:
                enhanced_args['architectural_context'] = memory_context.architectural_decisions
            
            # Add error patterns to avoid
            if memory_context.error_patterns:
                enhanced_args['avoid_patterns'] = memory_context.error_patterns
            
            # Add code quality preferences
            enhanced_args['quality_preferences'] = memory_context.user_preferences.get('quality', {})
            
            enhanced_args['memory_confidence'] = memory_context.confidence_score
        
        return enhanced_args
    
    async def _enhance_analyze(self, args: Dict[str, Any], memory_context: MemoryContext) -> Dict[str, Any]:
        """Enhance /analyze command with memory intelligence"""
        enhanced_args = args.copy()
        
        if memory_context:
            # Add analysis patterns and methodologies
            enhanced_args['memory_context'] = {
                'analysis_patterns': memory_context.analysis_patterns,
                'methodology_preferences': memory_context.user_preferences.get('analysis', {}),
                'previous_insights': memory_context.previous_insights,
                'successful_approaches': memory_context.successful_approaches
            }
            
            # Add domain-specific knowledge
            if memory_context.domain_knowledge:
                enhanced_args['domain_context'] = memory_context.domain_knowledge
            
            # Add quality metrics preferences
            enhanced_args['quality_metrics'] = memory_context.user_preferences.get('metrics', {})
            
            enhanced_args['memory_confidence'] = memory_context.confidence_score
        
        return enhanced_args
    
    async def _enhance_research(self, args: Dict[str, Any], memory_context: MemoryContext) -> Dict[str, Any]:
        """Enhance research commands with memory intelligence"""
        enhanced_args = args.copy()
        
        if memory_context:
            # Add research patterns and source preferences
            enhanced_args['memory_context'] = {
                'research_patterns': memory_context.research_patterns,
                'source_preferences': memory_context.user_preferences.get('sources', {}),
                'previous_research': memory_context.research_findings,
                'quality_sources': memory_context.quality_sources
            }
            
            # Add Jina scraping patterns
            if memory_context.scraping_patterns:
                enhanced_args['scraping_context'] = memory_context.scraping_patterns
            
            enhanced_args['memory_confidence'] = memory_context.confidence_score
        
        return enhanced_args
    
    async def _enhance_build(self, args: Dict[str, Any], memory_context: MemoryContext) -> Dict[str, Any]:
        """Enhance /build command with memory intelligence"""
        enhanced_args = args.copy()
        
        if memory_context:
            enhanced_args['memory_context'] = {
                'build_patterns': memory_context.build_patterns,
                'optimization_preferences': memory_context.user_preferences.get('build', {}),
                'successful_configurations': memory_context.successful_configurations
            }
            
            enhanced_args['memory_confidence'] = memory_context.confidence_score
        
        return enhanced_args
    
    async def _enhance_test(self, args: Dict[str, Any], memory_context: MemoryContext) -> Dict[str, Any]:
        """Enhance /test command with memory intelligence"""
        enhanced_args = args.copy()
        
        if memory_context:
            enhanced_args['memory_context'] = {
                'testing_patterns': memory_context.testing_patterns,
                'test_preferences': memory_context.user_preferences.get('testing', {}),
                'coverage_preferences': memory_context.user_preferences.get('coverage', {}),
                'successful_test_suites': memory_context.successful_test_suites
            }
            
            enhanced_args['memory_confidence'] = memory_context.confidence_score
        
        return enhanced_args
    
    async def _enhance_document(self, args: Dict[str, Any], memory_context: MemoryContext) -> Dict[str, Any]:
        """Enhance /document command with memory intelligence"""
        enhanced_args = args.copy()
        
        if memory_context:
            enhanced_args['memory_context'] = {
                'documentation_patterns': memory_context.documentation_patterns,
                'style_preferences': memory_context.user_preferences.get('documentation', {}),
                'successful_docs': memory_context.successful_documentation
            }
            
            enhanced_args['memory_confidence'] = memory_context.confidence_score
        
        return enhanced_args
    
    async def _enhance_design(self, args: Dict[str, Any], memory_context: MemoryContext) -> Dict[str, Any]:
        """Enhance /design command with memory intelligence"""
        enhanced_args = args.copy()
        
        if memory_context:
            enhanced_args['memory_context'] = {
                'design_patterns': memory_context.design_patterns,
                'architectural_preferences': memory_context.user_preferences.get('architecture', {}),
                'successful_designs': memory_context.successful_designs
            }
            
            enhanced_args['memory_confidence'] = memory_context.confidence_score
        
        return enhanced_args
    
    async def _enhance_generic(self, args: Dict[str, Any], memory_context: MemoryContext) -> Dict[str, Any]:
        """Generic enhancement for unknown command types"""
        enhanced_args = args.copy()
        
        if memory_context:
            enhanced_args['memory_context'] = {
                'general_patterns': memory_context.general_patterns,
                'user_preferences': memory_context.user_preferences
            }
            
            enhanced_args['memory_confidence'] = memory_context.confidence_score
        
        return enhanced_args
    
    async def _get_memory_context(self, command_type: str, args: Dict[str, Any], user_id: str) -> Optional[MemoryContext]:
        """Retrieve relevant memory context for command enhancement"""
        try:
            # Extract query context from command arguments
            query_context = self._extract_query_context(command_type, args)
            
            # Get memory context from memory layer
            memory_context = await self.memory_layer.get_command_context(
                command_type=command_type,
                query_context=query_context,
                user_id=user_id
            )
            
            return memory_context
            
        except Exception as e:
            print(f"Failed to get memory context: {e}")
            return None
    
    def _extract_query_context(self, command_type: str, args: Dict[str, Any]) -> str:
        """Extract meaningful query context from command arguments"""
        if command_type == 'generate-prp':
            # For PRP generation, use the feature/project description
            return args.get('feature_description', args.get('project_name', ''))
        
        elif command_type == 'implement':
            # For implementation, use the feature or file context
            return args.get('feature', args.get('files', ''))
        
        elif command_type == 'analyze':
            # For analysis, use the target or scope
            return args.get('target', args.get('scope', ''))
        
        elif command_type == 'research':
            # For research, use the topic or query
            return args.get('topic', args.get('query', ''))
        
        # Generic extraction for other commands
        return str(args.get('description', args.get('query', args.get('topic', ''))))
    
    def _get_user_id(self, args: Dict[str, Any]) -> str:
        """Get user ID for personalized memory (consistent across sessions)"""
        # Try to get user ID from args, environment, or generate stable ID
        user_id = args.get('user_id') or os.getenv('AAI_USER_ID')
        
        if not user_id:
            # Generate stable user ID based on system info
            import hashlib
            system_info = f"{os.getenv('USER', 'default')}_{os.getcwd()}"
            user_id = hashlib.md5(system_info.encode()).hexdigest()[:12]
        
        return user_id
    
    def _calculate_enhancement_confidence(self, memory_context: Optional[MemoryContext], enhanced_args: Dict[str, Any]) -> float:
        """Calculate confidence score for command enhancement (70-95% per AAI standards)"""
        if not memory_context:
            return 0.70  # Minimum AAI confidence
        
        confidence = 0.70  # Base confidence
        
        # Add confidence based on memory quality
        if memory_context.confidence_score:
            confidence += (memory_context.confidence_score - 0.70) * 0.5
        
        # Add confidence based on memory richness
        if memory_context.similar_items:
            confidence += min(len(memory_context.similar_items) * 0.02, 0.10)
        
        # Add confidence based on user preference availability
        if memory_context.user_preferences:
            confidence += 0.05
        
        # Add confidence based on pattern availability
        if hasattr(memory_context, 'implementation_patterns') and memory_context.implementation_patterns:
            confidence += 0.05
        
        # Ensure within AAI confidence range (70-95%)
        return max(0.70, min(confidence, 0.95))
    
    async def _log_enhancement(self, enhancement: CommandEnhancement):
        """Log enhancement for AAI brain learning and analytics"""
        try:
            # Store enhancement in memory for learning
            await self.memory_layer.store_enhancement_event(enhancement)
            
            # Log to AAI brain analytics if available
            await self._log_to_aai_brain(enhancement)
            
        except Exception as e:
            print(f"Failed to log enhancement: {e}")
    
    async def _log_to_aai_brain(self, enhancement: CommandEnhancement):
        """Log to AAI brain modules for intelligence tracking"""
        try:
            # Prepare log entry for AAI brain
            log_entry = {
                'event_type': 'memory_enhancement',
                'command_type': enhancement.command_type,
                'confidence_score': enhancement.confidence_score,
                'memory_context_available': enhancement.memory_context is not None,
                'enhancement_timestamp': enhancement.enhancement_timestamp.isoformat(),
                'session_id': os.getenv('AAI_SESSION_ID', 'unknown')
            }
            
            # Write to AAI brain logs
            brain_log_path = Path('/mnt/c/Users/Brandon/AAI/brain/logs/memory-enhancements.log')
            brain_log_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(brain_log_path, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Failed to log to AAI brain: {e}")
    
    async def capture_command_success(self, enhancement: CommandEnhancement, success_outcome: Dict[str, Any]):
        """Capture successful command execution for pattern learning"""
        try:
            # Store success pattern for learning
            await self.workflow_memory.capture_successful_pattern(
                command_type=enhancement.command_type,
                original_args=enhancement.original_args,
                enhanced_args=enhancement.enhanced_args,
                outcome=success_outcome,
                memory_context=enhancement.memory_context
            )
            
            # Update user preferences based on successful outcome
            await self._update_user_preferences(enhancement, success_outcome)
            
        except Exception as e:
            print(f"Failed to capture success pattern: {e}")
    
    async def _update_user_preferences(self, enhancement: CommandEnhancement, success_outcome: Dict[str, Any]):
        """Update user preferences based on successful command outcomes"""
        try:
            user_id = self._get_user_id(enhancement.original_args)
            
            # Extract preference updates from successful outcome
            preference_updates = self._extract_preference_updates(enhancement, success_outcome)
            
            if preference_updates:
                await self.memory_layer.update_user_preferences(user_id, preference_updates)
                
        except Exception as e:
            print(f"Failed to update user preferences: {e}")
    
    def _extract_preference_updates(self, enhancement: CommandEnhancement, success_outcome: Dict[str, Any]) -> Dict[str, Any]:
        """Extract user preference updates from successful command outcomes"""
        updates = {}
        
        # Extract technology preferences
        if enhancement.command_type == 'generate-prp':
            if 'technology_choices' in success_outcome:
                updates['preferred_technologies'] = success_outcome['technology_choices']
        
        # Extract coding style preferences
        elif enhancement.command_type == 'implement':
            if 'coding_style' in success_outcome:
                updates['coding_preferences'] = success_outcome['coding_style']
        
        # Extract analysis methodology preferences
        elif enhancement.command_type == 'analyze':
            if 'analysis_methods' in success_outcome:
                updates['analysis_preferences'] = success_outcome['analysis_methods']
        
        return updates
    
    def get_enhancement_stats(self) -> Dict[str, Any]:
        """Get statistics about command enhancements"""
        if not self.enhancement_history:
            return {'total_enhancements': 0}
        
        total = len(self.enhancement_history)
        with_memory = sum(1 for e in self.enhancement_history if e.memory_context)
        avg_confidence = sum(e.confidence_score for e in self.enhancement_history) / total
        
        command_types = {}
        for enhancement in self.enhancement_history:
            cmd = enhancement.command_type
            command_types[cmd] = command_types.get(cmd, 0) + 1
        
        return {
            'total_enhancements': total,
            'enhancements_with_memory': with_memory,
            'memory_utilization_rate': with_memory / total if total > 0 else 0,
            'average_confidence': avg_confidence,
            'command_type_distribution': command_types,
            'enhancement_success_rate': with_memory / total if total > 0 else 0
        }


# Convenience functions for easy integration
async def enhance_aai_command(command_type: str, args: Dict[str, Any]) -> CommandEnhancement:
    """
    Convenience function to enhance any AAI command with memory.
    
    Usage:
        enhancement = await enhance_aai_command('generate-prp', {'feature': 'auth system'})
        enhanced_args = enhancement.enhanced_args
    """
    enhancer = AAICommandEnhancer()
    return await enhancer.enhance_command(command_type, args)


async def get_memory_enhanced_args(command_type: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to get memory-enhanced arguments for an AAI command.
    
    Usage:
        enhanced_args = await get_memory_enhanced_args('implement', {'feature': 'user auth'})
    """
    enhancement = await enhance_aai_command(command_type, args)
    return enhancement.enhanced_args


def test_command_enhancement():
    """Test command enhancement functionality"""
    import asyncio
    
    async def test_enhancement():
        enhancer = AAICommandEnhancer()
        
        # Test PRP enhancement
        prp_args = {'feature': 'user authentication system', 'technology': 'FastAPI'}
        prp_enhancement = await enhancer.enhance_command('generate-prp', prp_args)
        
        print("PRP Enhancement:")
        print(f"  Original args: {prp_enhancement.original_args}")
        print(f"  Enhanced args keys: {list(prp_enhancement.enhanced_args.keys())}")
        print(f"  Confidence: {prp_enhancement.confidence_score:.2f}")
        print()
        
        # Test implementation enhancement
        impl_args = {'feature': 'JWT token authentication', 'language': 'Python'}
        impl_enhancement = await enhancer.enhance_command('implement', impl_args)
        
        print("Implementation Enhancement:")
        print(f"  Original args: {impl_enhancement.original_args}")
        print(f"  Enhanced args keys: {list(impl_enhancement.enhanced_args.keys())}")
        print(f"  Confidence: {impl_enhancement.confidence_score:.2f}")
        print()
        
        # Get stats
        stats = enhancer.get_enhancement_stats()
        print("Enhancement Stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    asyncio.run(test_enhancement())


if __name__ == "__main__":
    test_command_enhancement()