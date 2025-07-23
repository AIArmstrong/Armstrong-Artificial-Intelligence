"""
Improvement Outcome Tracking and Learning System

Tracks implementation outcomes and correlates with predictions for continuous improvement.
"""

import json
import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
import logging

from .models import ImprovementOutcome, ImprovementRecommendation, QualityMetrics
from .config import LEARNING_CONFIG, get_config

logger = logging.getLogger(__name__)

class ImprovementTracker:
    """
    Tracks improvement outcomes and learns from results to improve future recommendations.
    Integrates with memory-quality-scorer.py and unified-analytics.py.
    """
    
    def __init__(self, db_path: str = "brain/logs/improvements/outcomes.db"):
        self.db_path = db_path
        self.learning_config = LEARNING_CONFIG
        self._init_database()
        self.patterns_cache = {}
    
    def _init_database(self):
        """Initialize the outcomes tracking database"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create outcomes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS improvement_outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recommendation_id TEXT NOT NULL,
                recommendation_title TEXT,
                category TEXT,
                priority TEXT,
                risk_level TEXT,
                breaking_change_probability REAL,
                implemented BOOLEAN,
                implementation_time TEXT,
                quality_before_overall REAL,
                quality_after_overall REAL,
                success_rate REAL,
                developer_feedback TEXT,
                issues_introduced TEXT,
                actual_vs_predicted_risk REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS success_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_details TEXT,
                success_rate REAL,
                sample_count INTEGER,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create learning metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT,
                metric_value REAL,
                confidence REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def track_outcome(self, 
                     recommendation: ImprovementRecommendation,
                     outcome: ImprovementOutcome,
                     quality_before: QualityMetrics) -> Dict[str, Any]:
        """
        Track the outcome of an improvement implementation.
        
        Args:
            recommendation: The original recommendation
            outcome: The implementation outcome
            quality_before: Quality metrics before improvement
            
        Returns:
            Tracking result with success metrics and pattern updates
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Calculate success rate
            success_rate = outcome.calculate_success_rate()
            
            # Insert outcome record
            cursor.execute("""
                INSERT INTO improvement_outcomes (
                    recommendation_id, recommendation_title, category, priority,
                    risk_level, breaking_change_probability, implemented,
                    implementation_time, quality_before_overall, quality_after_overall,
                    success_rate, developer_feedback, issues_introduced,
                    actual_vs_predicted_risk
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                recommendation.id,
                recommendation.title,
                recommendation.category,
                recommendation.priority,
                recommendation.risk_level,
                recommendation.breaking_change_probability,
                outcome.implemented,
                outcome.implementation_time,
                quality_before.overall_score,
                outcome.quality_after.overall_score if outcome.quality_after else None,
                success_rate,
                outcome.developer_feedback,
                json.dumps(outcome.issues_introduced),
                outcome.actual_vs_predicted_risk
            ))
            
            conn.commit()
            
            # Update patterns if successful
            if success_rate > 0.7:
                self._update_success_patterns(recommendation, outcome, cursor)
            
            # Update learning metrics
            self._update_learning_metrics(cursor)
            
            conn.commit()
            conn.close()
            
            # Clear patterns cache
            self.patterns_cache.clear()
            
            return {
                "success": True,
                "outcome_id": cursor.lastrowid,
                "success_rate": success_rate,
                "patterns_updated": success_rate > 0.7,
                "quality_improvement": (
                    outcome.quality_after.overall_score - quality_before.overall_score
                    if outcome.quality_after else 0.0
                )
            }
            
        except Exception as e:
            logger.error(f"Failed to track outcome: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_recommendation_success_rate(self, 
                                      category: Optional[str] = None,
                                      priority: Optional[str] = None) -> float:
        """
        Get average success rate for recommendations.
        
        Args:
            category: Filter by category
            priority: Filter by priority
            
        Returns:
            Average success rate (0.0 to 1.0)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT AVG(success_rate) FROM improvement_outcomes WHERE implemented = 1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        
        cursor.execute(query, params)
        result = cursor.fetchone()[0]
        conn.close()
        
        return result if result else 0.0
    
    def get_risk_prediction_accuracy(self) -> Dict[str, float]:
        """
        Calculate accuracy of risk predictions.
        
        Returns:
            Dictionary with accuracy metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT breaking_change_probability, actual_vs_predicted_risk
            FROM improvement_outcomes
            WHERE implemented = 1 AND actual_vs_predicted_risk IS NOT NULL
        """)
        
        predictions = []
        errors = []
        
        for predicted, actual_vs_predicted in cursor.fetchall():
            predictions.append(predicted)
            errors.append(abs(actual_vs_predicted))
        
        conn.close()
        
        if not predictions:
            return {"accuracy": 0.0, "sample_size": 0}
        
        return {
            "accuracy": 1.0 - statistics.mean(errors),
            "mean_absolute_error": statistics.mean(errors),
            "std_deviation": statistics.stdev(errors) if len(errors) > 1 else 0.0,
            "sample_size": len(predictions)
        }
    
    def get_quality_improvement_stats(self) -> Dict[str, float]:
        """
        Get statistics on quality improvements achieved.
        
        Returns:
            Dictionary with quality improvement statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT quality_before_overall, quality_after_overall
            FROM improvement_outcomes
            WHERE implemented = 1 
            AND quality_before_overall IS NOT NULL 
            AND quality_after_overall IS NOT NULL
        """)
        
        improvements = []
        for before, after in cursor.fetchall():
            improvements.append(after - before)
        
        conn.close()
        
        if not improvements:
            return {"mean_improvement": 0.0, "total_improvements": 0}
        
        return {
            "mean_improvement": statistics.mean(improvements),
            "median_improvement": statistics.median(improvements),
            "total_improvements": len(improvements),
            "positive_improvements": sum(1 for i in improvements if i > 0),
            "negative_impacts": sum(1 for i in improvements if i < 0)
        }
    
    def get_success_patterns(self, min_sample_size: int = 5) -> List[Dict[str, Any]]:
        """
        Get successful improvement patterns.
        
        Args:
            min_sample_size: Minimum number of samples for a pattern
            
        Returns:
            List of successful patterns
        """
        # Check cache first
        cache_key = f"patterns_{min_sample_size}"
        if cache_key in self.patterns_cache:
            return self.patterns_cache[cache_key]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT pattern_type, pattern_details, success_rate, sample_count
            FROM success_patterns
            WHERE sample_count >= ? AND success_rate > 0.7
            ORDER BY success_rate DESC
        """, (min_sample_size,))
        
        patterns = []
        for row in cursor.fetchall():
            patterns.append({
                "type": row[0],
                "details": json.loads(row[1]),
                "success_rate": row[2],
                "sample_count": row[3]
            })
        
        conn.close()
        
        # Cache results
        self.patterns_cache[cache_key] = patterns
        
        return patterns
    
    def predict_success_probability(self, recommendation: ImprovementRecommendation) -> float:
        """
        Predict success probability based on historical patterns.
        
        Args:
            recommendation: The recommendation to evaluate
            
        Returns:
            Predicted success probability (0.0 to 1.0)
        """
        # Get relevant historical data
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find similar recommendations
        cursor.execute("""
            SELECT success_rate
            FROM improvement_outcomes
            WHERE category = ? AND priority = ? AND risk_level = ?
            AND implemented = 1
            ORDER BY timestamp DESC
            LIMIT 20
        """, (recommendation.category, recommendation.priority, recommendation.risk_level))
        
        similar_outcomes = [row[0] for row in cursor.fetchall()]
        
        # Get patterns that match
        patterns = self.get_success_patterns()
        pattern_scores = []
        
        for pattern in patterns:
            if self._pattern_matches(recommendation, pattern):
                pattern_scores.append(pattern["success_rate"])
        
        conn.close()
        
        # Combine predictions
        all_scores = similar_outcomes + pattern_scores
        
        if not all_scores:
            # No historical data, use conservative estimate
            base_prob = 0.7
            
            # Adjust based on risk
            risk_adjustment = {
                "low": 0.1,
                "medium": 0.0,
                "high": -0.1,
                "critical": -0.2
            }
            
            return max(0.3, min(0.95, base_prob + risk_adjustment.get(recommendation.risk_level, 0)))
        
        # Weighted average with recent data weighted higher
        weights = [1.0 / (i + 1) for i in range(len(all_scores))]
        weighted_sum = sum(score * weight for score, weight in zip(all_scores, weights))
        total_weight = sum(weights)
        
        return round(weighted_sum / total_weight, 3)
    
    def _update_success_patterns(self, 
                               recommendation: ImprovementRecommendation,
                               outcome: ImprovementOutcome,
                               cursor: sqlite3.Cursor):
        """Update success patterns based on outcome"""
        
        # Pattern: Category + Priority + Risk Level
        pattern_key = f"{recommendation.category}_{recommendation.priority}_{recommendation.risk_level}"
        pattern_details = {
            "category": recommendation.category,
            "priority": recommendation.priority,
            "risk_level": recommendation.risk_level,
            "typical_effort": recommendation.effort_estimate
        }
        
        # Check if pattern exists
        cursor.execute("""
            SELECT id, success_rate, sample_count
            FROM success_patterns
            WHERE pattern_type = ?
        """, (pattern_key,))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing pattern
            pattern_id, current_rate, sample_count = existing
            
            # Calculate new success rate (exponential moving average)
            alpha = 0.2  # Learning rate
            new_rate = (1 - alpha) * current_rate + alpha * outcome.calculate_success_rate()
            
            cursor.execute("""
                UPDATE success_patterns
                SET success_rate = ?, sample_count = ?, last_updated = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_rate, sample_count + 1, pattern_id))
        else:
            # Create new pattern
            cursor.execute("""
                INSERT INTO success_patterns (pattern_type, pattern_details, success_rate, sample_count)
                VALUES (?, ?, ?, ?)
            """, (pattern_key, json.dumps(pattern_details), outcome.calculate_success_rate(), 1))
    
    def _update_learning_metrics(self, cursor: sqlite3.Cursor):
        """Update learning system metrics"""
        
        # Calculate overall recommendation accuracy
        cursor.execute("""
            SELECT AVG(success_rate) FROM improvement_outcomes
            WHERE implemented = 1 AND timestamp > datetime('now', '-30 days')
        """)
        recent_success_rate = cursor.fetchone()[0] or 0.0
        
        # Calculate risk prediction accuracy
        cursor.execute("""
            SELECT AVG(ABS(actual_vs_predicted_risk))
            FROM improvement_outcomes
            WHERE actual_vs_predicted_risk IS NOT NULL
            AND timestamp > datetime('now', '-30 days')
        """)
        risk_accuracy = 1.0 - (cursor.fetchone()[0] or 0.5)
        
        # Store metrics
        metrics = [
            ("overall_success_rate", recent_success_rate, 0.8),
            ("risk_prediction_accuracy", risk_accuracy, 0.7),
            ("pattern_count", len(self.get_success_patterns()), 1.0)
        ]
        
        for name, value, confidence in metrics:
            cursor.execute("""
                INSERT INTO learning_metrics (metric_name, metric_value, confidence)
                VALUES (?, ?, ?)
            """, (name, value, confidence))
    
    def _pattern_matches(self, recommendation: ImprovementRecommendation, pattern: Dict) -> bool:
        """Check if a recommendation matches a pattern"""
        details = pattern["details"]
        
        return (
            details.get("category") == recommendation.category and
            details.get("priority") == recommendation.priority and
            details.get("risk_level") == recommendation.risk_level
        )
    
    def generate_learning_report(self) -> Dict[str, Any]:
        """Generate a comprehensive learning system report"""
        return {
            "success_metrics": {
                "overall_success_rate": self.get_recommendation_success_rate(),
                "by_category": {
                    cat: self.get_recommendation_success_rate(category=cat)
                    for cat in ["quality", "performance", "security", "maintainability", "architecture"]
                },
                "by_priority": {
                    pri: self.get_recommendation_success_rate(priority=pri)
                    for pri in ["critical", "high", "medium", "low"]
                }
            },
            "risk_accuracy": self.get_risk_prediction_accuracy(),
            "quality_improvements": self.get_quality_improvement_stats(),
            "successful_patterns": self.get_success_patterns(),
            "learning_progress": self._get_learning_progress(),
            "recommendations": self._generate_system_recommendations()
        }
    
    def _get_learning_progress(self) -> Dict[str, Any]:
        """Track learning system progress over time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get metrics over time
        cursor.execute("""
            SELECT metric_name, metric_value, timestamp
            FROM learning_metrics
            WHERE metric_name = 'overall_success_rate'
            ORDER BY timestamp DESC
            LIMIT 10
        """)
        
        progress_data = cursor.fetchall()
        conn.close()
        
        if len(progress_data) < 2:
            return {"improving": False, "trend": "insufficient_data"}
        
        # Calculate trend
        recent_values = [row[1] for row in progress_data[:5]]
        older_values = [row[1] for row in progress_data[5:10]]
        
        if older_values:
            recent_avg = statistics.mean(recent_values)
            older_avg = statistics.mean(older_values)
            improvement = recent_avg - older_avg
            
            return {
                "improving": improvement > 0,
                "trend": "improving" if improvement > 0.05 else "stable" if improvement > -0.05 else "declining",
                "improvement_rate": round(improvement, 3),
                "current_performance": round(recent_avg, 3)
            }
        
        return {"improving": False, "trend": "insufficient_data"}
    
    def _generate_system_recommendations(self) -> List[str]:
        """Generate recommendations for improving the system"""
        recommendations = []
        
        # Check success rates
        overall_success = self.get_recommendation_success_rate()
        if overall_success < 0.7:
            recommendations.append("Consider adjusting risk thresholds - current success rate is below target")
        
        # Check risk accuracy
        risk_accuracy = self.get_risk_prediction_accuracy()
        if risk_accuracy["accuracy"] < 0.8 and risk_accuracy["sample_size"] > 20:
            recommendations.append("Risk prediction model needs retraining - accuracy below threshold")
        
        # Check pattern diversity
        patterns = self.get_success_patterns()
        if len(patterns) < 10:
            recommendations.append("Limited pattern data - encourage more diverse improvement implementations")
        
        # Check for category imbalances
        category_rates = {
            cat: self.get_recommendation_success_rate(category=cat)
            for cat in ["quality", "performance", "security", "maintainability", "architecture"]
        }
        
        for cat, rate in category_rates.items():
            if rate < 0.6:
                recommendations.append(f"Low success rate for {cat} improvements - review recommendation criteria")
        
        return recommendations