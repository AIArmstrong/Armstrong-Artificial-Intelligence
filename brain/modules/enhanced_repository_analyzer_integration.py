"""
Integration patch for Enhanced Repository Analyzer quality scoring.

This module patches the existing analyzer to add quality scoring capabilities.
"""

import importlib.util
import sys
from pathlib import Path

def enhance_repository_analyzer():
    """
    Enhance the repository analyzer with quality scoring capabilities.
    
    This function patches the existing EnhancedRepositoryAnalyzer class
    to add multi-dimensional quality scoring methods.
    """
    try:
        # Import the existing analyzer
        from brain.modules.enhanced_repository_analyzer import EnhancedRepositoryAnalyzer
        from brain.modules.enhanced_repository_analyzer_quality import QualityAnalysisEnhancement
        
        # Check if quality scoring is available
        try:
            from brain.modules.supreme_improve import MultiDimensionalScorer
            quality_available = True
        except ImportError:
            quality_available = False
        
        if not quality_available:
            return EnhancedRepositoryAnalyzer
        
        # Create enhanced version of the class
        class EnhancedRepositoryAnalyzerWithQuality(EnhancedRepositoryAnalyzer):
            """Enhanced Repository Analyzer with integrated quality scoring"""
            
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                
                # Add quality enhancement
                if hasattr(self, 'quality_scorer') and self.quality_scorer:
                    self.quality_enhancement = QualityAnalysisEnhancement(
                        self.quality_scorer, 
                        self.db_path
                    )
                else:
                    self.quality_enhancement = None
            
            async def _perform_quality_analysis(self, repo_path, session_id):
                """Delegate to quality enhancement module"""
                if self.quality_enhancement:
                    return await self.quality_enhancement.perform_quality_analysis(repo_path, session_id)
                else:
                    return {'error': 'Quality enhancement not available', 'project_metrics': None}
            
            async def _generate_improvement_recommendations(self, repo_path, quality_results):
                """Delegate to quality enhancement module"""
                if self.quality_enhancement:
                    return await self.quality_enhancement.generate_improvement_recommendations(repo_path, quality_results)
                else:
                    return []
        
        return EnhancedRepositoryAnalyzerWithQuality
        
    except Exception as e:
        print(f"Failed to enhance repository analyzer: {e}")
        # Return original class if enhancement fails
        try:
            from brain.modules.enhanced_repository_analyzer import EnhancedRepositoryAnalyzer
            return EnhancedRepositoryAnalyzer
        except:
            return None

# Auto-enhance when module is imported
EnhancedRepositoryAnalyzer = enhance_repository_analyzer()

# Export the enhanced version
__all__ = ['EnhancedRepositoryAnalyzer']