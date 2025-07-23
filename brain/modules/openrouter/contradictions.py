"""
Contradiction Detection and Analysis Engine
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from .router_client import get_openrouter_client
# Import with try/catch for optional dependency
try:
    from brain.modules.supabase_cache import SupabaseCache
except ImportError:
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from supabase_cache import SupabaseCache
    except ImportError:
        # Create placeholder class for when Supabase is not available
        class SupabaseCache:
            def store_contradiction_check(self, *args, **kwargs): pass
            def get_conversation_history(self, *args, **kwargs): return []

class ContradictionEngine:
    """
    Intelligent contradiction detection using LLM analysis
    Builds knowledge base of contradiction patterns for learning
    """
    
    def __init__(self):
        self.client = get_openrouter_client()
        self.cache = SupabaseCache()
        
    async def detect_contradiction(self, current_text: str, existing_context: str, context_source: str = "unknown") -> Optional[Dict]:
        """
        Detect contradictions between current text and existing context
        Returns detailed contradiction analysis
        """
        result = await self.client.analyze_contradiction(current_text, existing_context)
        
        if result:
            # Enhance result with metadata
            enhanced_result = {
                **result,
                "current_text": current_text[:200],  # First 200 chars for reference
                "context_source": context_source,
                "timestamp": datetime.utcnow().isoformat(),
                "analysis_model": "openai/gpt-4o-mini"
            }
            
            # Cache contradiction analysis for learning
            if result.get('has_contradiction', False):
                self._cache_contradiction(enhanced_result)
            
            return enhanced_result
        
        return None
    
    def _cache_contradiction(self, contradiction_data: Dict):
        """Cache detected contradiction for pattern learning"""
        cache_key = f"contradiction_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        tags = [
            "#contradiction",
            "#conflict",
            f"#{contradiction_data.get('contradiction_type', 'unknown')}"
        ]
        
        # Add confidence-based tags
        confidence = contradiction_data.get('confidence', 0.0)
        if confidence > 0.8:
            tags.append("#high-confidence")
        elif confidence > 0.5:
            tags.append("#medium-confidence")
        else:
            tags.append("#low-confidence")
        
        self.cache.add_to_batch(cache_key, contradiction_data, tags)
    
    async def analyze_conversation_contradictions(self, conversation_history: List[str], lookback_limit: int = 10) -> List[Dict]:
        """
        Analyze recent conversation for internal contradictions
        """
        if len(conversation_history) < 2:
            return []
        
        contradictions = []
        recent_messages = conversation_history[-lookback_limit:] if len(conversation_history) > lookback_limit else conversation_history
        
        # Compare each message against previous messages
        for i, current_msg in enumerate(recent_messages):
            for j, previous_msg in enumerate(recent_messages[:i]):
                if i - j > 5:  # Don't compare messages too far apart
                    continue
                
                contradiction = await self.detect_contradiction(
                    current_msg,
                    previous_msg,
                    f"conversation_msg_{j}_vs_{i}"
                )
                
                if contradiction and contradiction.get('has_contradiction', False):
                    contradiction['message_indices'] = (j, i)
                    contradictions.append(contradiction)
        
        return contradictions
    
    async def check_against_brain_state(self, current_text: str, brain_files: List[str] = None) -> List[Dict]:
        """
        Check current text against brain system state files for contradictions
        """
        default_brain_files = [
            "brain/states/conversation-state.json",
            "brain/docs/explain.md",
            "brain/logs/interactions.log"
        ]
        
        files_to_check = brain_files or default_brain_files
        contradictions = []
        
        for file_path in files_to_check:
            try:
                with open(file_path, 'r') as f:
                    file_content = f.read()
                
                # Only check last 2000 characters to avoid token limits
                if len(file_content) > 2000:
                    file_content = file_content[-2000:]
                
                contradiction = await self.detect_contradiction(
                    current_text,
                    file_content,
                    file_path
                )
                
                if contradiction and contradiction.get('has_contradiction', False):
                    contradiction['source_file'] = file_path
                    contradictions.append(contradiction)
                    
            except FileNotFoundError:
                # File doesn't exist, skip
                continue
            except Exception as e:
                print(f"Error checking {file_path}: {e}")
                continue
        
        return contradictions
    
    async def analyze_decision_consistency(self, decision_text: str) -> Dict:
        """
        Analyze decision for consistency with past decisions
        """
        # Get past decisions from cache
        past_decisions = self.cache.query_by_tags(["#decision", "#rationale"])
        
        if not past_decisions:
            return {
                "consistency_score": 1.0,
                "contradictions": [],
                "note": "No past decisions to compare against"
            }
        
        contradictions = []
        
        # Check against recent decisions (last 10)
        recent_decisions = sorted(past_decisions, key=lambda x: x.get('created_at', ''), reverse=True)[:10]
        
        for past_decision in recent_decisions:
            past_text = str(past_decision.get('value', {}))
            
            contradiction = await self.detect_contradiction(
                decision_text,
                past_text,
                f"decision_{past_decision.get('id', 'unknown')}"
            )
            
            if contradiction and contradiction.get('has_contradiction', False):
                contradictions.append(contradiction)
        
        # Calculate consistency score
        consistency_score = max(0.0, 1.0 - (len(contradictions) * 0.2))
        
        return {
            "consistency_score": consistency_score,
            "contradictions": contradictions,
            "decisions_checked": len(recent_decisions),
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
    
    def get_contradiction_patterns(self) -> Dict[str, List[Dict]]:
        """
        Analyze cached contradictions to identify patterns
        """
        cached_contradictions = self.cache.query_by_tags(["#contradiction"])
        
        if not cached_contradictions:
            return {}
        
        patterns = {
            "by_type": {},
            "by_confidence": {"high": [], "medium": [], "low": []},
            "recurring_sources": {}
        }
        
        for contradiction in cached_contradictions:
            data = contradiction.get('value', {})
            
            # Group by contradiction type
            contradiction_type = data.get('contradiction_type', 'unknown')
            if contradiction_type not in patterns["by_type"]:
                patterns["by_type"][contradiction_type] = []
            patterns["by_type"][contradiction_type].append(data)
            
            # Group by confidence
            confidence = data.get('confidence', 0.0)
            if confidence > 0.8:
                patterns["by_confidence"]["high"].append(data)
            elif confidence > 0.5:
                patterns["by_confidence"]["medium"].append(data)
            else:
                patterns["by_confidence"]["low"].append(data)
            
            # Track recurring sources
            source = data.get('context_source', 'unknown')
            if source not in patterns["recurring_sources"]:
                patterns["recurring_sources"][source] = 0
            patterns["recurring_sources"][source] += 1
        
        return patterns
    
    async def generate_contradiction_report(self) -> Dict:
        """
        Generate comprehensive contradiction analysis report
        """
        patterns = self.get_contradiction_patterns()
        
        # Calculate statistics
        total_contradictions = sum(len(contradictions) for contradictions in patterns["by_type"].values())
        most_common_type = max(patterns["by_type"].keys(), key=lambda k: len(patterns["by_type"][k])) if patterns["by_type"] else "none"
        high_confidence_count = len(patterns["by_confidence"]["high"])
        
        # Get recent contradiction trend (last 24 hours)
        recent_contradictions = self.cache.query_by_tags(["#contradiction"])
        recent_count = len([c for c in recent_contradictions 
                           if (datetime.utcnow() - datetime.fromisoformat(c.get('created_at', '2000-01-01'))).days < 1])
        
        return {
            "summary": {
                "total_contradictions": total_contradictions,
                "most_common_type": most_common_type,
                "high_confidence_contradictions": high_confidence_count,
                "recent_24h_count": recent_count
            },
            "patterns": patterns,
            "recommendations": self._generate_recommendations(patterns),
            "report_timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_recommendations(self, patterns: Dict) -> List[str]:
        """Generate recommendations based on contradiction patterns"""
        recommendations = []
        
        # Analyze patterns and suggest improvements
        if patterns["by_type"].get("logical", []):
            recommendations.append("Consider implementing logical consistency checks before making decisions")
        
        if patterns["by_type"].get("temporal", []):
            recommendations.append("Review timeline consistency in planning and implementation")
        
        if patterns["by_type"].get("architectural", []):
            recommendations.append("Establish clear architectural principles and validate changes against them")
        
        high_confidence = len(patterns["by_confidence"]["high"])
        total = sum(len(contradictions) for contradictions in patterns["by_confidence"].values())
        
        if total > 0 and high_confidence / total > 0.5:
            recommendations.append("High proportion of high-confidence contradictions detected - review decision-making process")
        
        # Check for recurring sources
        recurring = patterns["recurring_sources"]
        if recurring:
            most_problematic = max(recurring.keys(), key=lambda k: recurring[k])
            if recurring[most_problematic] > 3:
                recommendations.append(f"Source '{most_problematic}' has multiple contradictions - needs review")
        
        return recommendations

# Convenience functions for brain system integration
async def check_for_contradictions(text: str, context_files: List[str] = None) -> List[Dict]:
    """Check text for contradictions against brain state"""
    engine = ContradictionEngine()
    return await engine.check_against_brain_state(text, context_files)

async def analyze_conversation_conflicts(conversation: List[str]) -> List[Dict]:
    """Analyze conversation history for internal conflicts"""
    engine = ContradictionEngine()
    return await engine.analyze_conversation_contradictions(conversation)

async def validate_decision_consistency(decision: str) -> Dict:
    """Validate decision against past decisions for consistency"""
    engine = ContradictionEngine()
    return await engine.analyze_decision_consistency(decision)

def get_contradiction_insights() -> Dict:
    """Get insights from contradiction pattern analysis"""
    engine = ContradictionEngine()
    return engine.get_contradiction_patterns()

if __name__ == "__main__":
    # Test contradiction detection
    async def test_contradictions():
        engine = ContradictionEngine()
        
        # Test basic contradiction detection
        contradiction = await engine.detect_contradiction(
            "We should use MySQL for the database",
            "The team decided to use Supabase for all data storage needs"
        )
        
        if contradiction:
            print(f"Contradiction detected: {contradiction}")
        
        # Test decision consistency
        consistency = await engine.analyze_decision_consistency(
            "Implement local file storage for cache"
        )
        print(f"Decision consistency: {consistency}")
        
        # Test pattern analysis
        patterns = engine.get_contradiction_patterns()
        print(f"Contradiction patterns: {patterns}")
        
        # Generate report
        report = await engine.generate_contradiction_report()
        print(f"Contradiction report: {report}")
    
    asyncio.run(test_contradictions())