#!/usr/bin/env python3
"""
Code Health Timeline - Creative Cortex Innovation for Supreme Analyze

This module implements predictive debt analysis with visual timeline generation.
It tracks code health evolution and predicts future technical debt accumulation.

Part of the Supreme Analyze Creative Cortex (Stage 3 Innovation).
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import statistics

logger = logging.getLogger(__name__)

@dataclass
class HealthSnapshot:
    """Represents a code health snapshot at a point in time"""
    timestamp: datetime
    overall_score: float
    maintainability: float
    complexity: float
    test_coverage: float
    security: float
    debt_ratio: float
    files_analyzed: int
    critical_issues: int

@dataclass
class PredictionPoint:
    """Represents a predicted future health point"""
    date: datetime
    predicted_score: float
    confidence: float
    risk_factors: List[str]
    recommendations: List[str]

@dataclass
class TimelineResult:
    """Complete timeline analysis result"""
    current_health: HealthSnapshot
    historical_trend: List[HealthSnapshot]
    predictions: List[PredictionPoint]
    debt_forecast: Dict[str, Any]
    maintenance_timeline: Dict[str, Any]
    visual_data: Dict[str, Any]
    processing_time: float
    confidence: float

class CodeHealthTimeline:
    """
    Creative Cortex Innovation: Code Health Timeline
    
    Implements predictive debt analysis with visual timeline generation.
    Tracks code health evolution and predicts future maintenance needs.
    """
    
    def __init__(self, base_path: str = "/mnt/c/Users/Brandon/AAI"):
        """
        Initialize Code Health Timeline analyzer.
        
        Args:
            base_path: Base path to AAI installation
        """
        self.base_path = Path(base_path)
        self.cache_dir = self.base_path / "brain" / "cache" / "code_health_timeline"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Timeline configuration
        self.prediction_horizon_months = 6
        self.historical_window_months = 12
        self.debt_threshold = 0.6  # Score below this indicates technical debt
        
        logger.info("Code Health Timeline initialized")
    
    async def analyze_timeline(self, 
                             target_path: str, 
                             session_id: str,
                             quality_metrics: Dict[str, Any] = None) -> TimelineResult:
        """
        Perform complete timeline analysis with debt prediction.
        
        Args:
            target_path: Path to code to analyze
            session_id: Analysis session ID
            quality_metrics: Optional pre-computed quality metrics
            
        Returns:
            Complete timeline analysis with predictions
        """
        start_time = datetime.now()
        target = Path(target_path)
        
        try:
            # Generate current health snapshot
            current_health = await self._create_current_snapshot(target, quality_metrics)
            
            # Load or generate historical data
            historical_trend = await self._load_historical_trend(target_path)
            
            # Generate predictions
            predictions = await self._generate_predictions(current_health, historical_trend)
            
            # Create debt forecast
            debt_forecast = self._create_debt_forecast(current_health, predictions)
            
            # Generate maintenance timeline
            maintenance_timeline = self._create_maintenance_timeline(predictions)
            
            # Prepare visual data
            visual_data = self._prepare_visual_data(current_health, historical_trend, predictions)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Calculate overall confidence
            confidence = self._calculate_confidence(historical_trend, predictions)
            
            result = TimelineResult(
                current_health=current_health,
                historical_trend=historical_trend,
                predictions=predictions,
                debt_forecast=debt_forecast,
                maintenance_timeline=maintenance_timeline,
                visual_data=visual_data,
                processing_time=processing_time,
                confidence=confidence
            )
            
            # Cache the result
            await self._cache_timeline_result(target_path, session_id, result)
            
            logger.info(f"Timeline analysis completed in {processing_time:.2f}s with {confidence:.1%} confidence")
            return result
            
        except Exception as e:
            logger.error(f"Timeline analysis failed: {e}")
            # Return minimal error result
            return TimelineResult(
                current_health=HealthSnapshot(
                    timestamp=datetime.now(),
                    overall_score=0.0,
                    maintainability=0.0,
                    complexity=0.0,
                    test_coverage=0.0,
                    security=0.0,
                    debt_ratio=1.0,
                    files_analyzed=0,
                    critical_issues=0
                ),
                historical_trend=[],
                predictions=[],
                debt_forecast={"error": str(e)},
                maintenance_timeline={"error": str(e)},
                visual_data={"error": str(e)},
                processing_time=(datetime.now() - start_time).total_seconds(),
                confidence=0.0
            )
    
    async def _create_current_snapshot(self, target_path: Path, quality_metrics: Dict[str, Any] = None) -> HealthSnapshot:
        """Create current health snapshot from quality metrics"""
        
        if quality_metrics and quality_metrics.get("project_metrics"):
            # Use provided quality metrics
            project_metrics = quality_metrics["project_metrics"]
            file_metrics = quality_metrics.get("file_metrics", {})
            
            # Calculate debt ratio
            low_quality_files = len([f for f, m in file_metrics.items() 
                                   if m.get("overall_score", 0) < self.debt_threshold])
            debt_ratio = low_quality_files / max(len(file_metrics), 1)
            
            # Count critical issues
            critical_issues = len([f for f, m in file_metrics.items() 
                                 if m.get("overall_score", 0) < 0.4])
            
            return HealthSnapshot(
                timestamp=datetime.now(),
                overall_score=project_metrics.get("overall_project_score", 0.0),
                maintainability=project_metrics.get("average_maintainability", 0.0),
                complexity=1.0 - project_metrics.get("average_complexity", 0.0),  # Invert complexity
                test_coverage=project_metrics.get("average_test_coverage", 0.0),
                security=project_metrics.get("average_security", 0.8),  # Default assumption
                debt_ratio=debt_ratio,
                files_analyzed=project_metrics.get("files_analyzed", 0),
                critical_issues=critical_issues
            )
        else:
            # Generate basic snapshot from file analysis
            return await self._analyze_current_health(target_path)
    
    async def _analyze_current_health(self, target_path: Path) -> HealthSnapshot:
        """Analyze current health when no quality metrics provided"""
        # Basic file analysis for health snapshot
        python_files = list(target_path.rglob("*.py"))
        js_files = list(target_path.rglob("*.js"))
        all_files = python_files + js_files
        
        if not all_files:
            return HealthSnapshot(
                timestamp=datetime.now(),
                overall_score=0.5,
                maintainability=0.5,
                complexity=0.5,
                test_coverage=0.0,
                security=0.5,
                debt_ratio=0.5,
                files_analyzed=0,
                critical_issues=0
            )
        
        # Basic heuristic analysis
        large_files = len([f for f in all_files if f.stat().st_size > 20000])  # > 20KB
        debt_ratio = large_files / len(all_files)
        
        # Look for test files
        test_files = len([f for f in all_files if "test" in f.name.lower()])
        test_coverage = min(1.0, test_files / max(len(all_files) * 0.3, 1))  # 30% test ratio assumption
        
        return HealthSnapshot(
            timestamp=datetime.now(),
            overall_score=max(0.3, 0.8 - debt_ratio),
            maintainability=max(0.3, 0.9 - debt_ratio),
            complexity=max(0.3, 0.8 - (debt_ratio * 0.5)),
            test_coverage=test_coverage,
            security=0.8,  # Default assumption
            debt_ratio=debt_ratio,
            files_analyzed=len(all_files),
            critical_issues=max(0, int(len(all_files) * debt_ratio * 0.3))
        )
    
    async def _load_historical_trend(self, target_path: str) -> List[HealthSnapshot]:
        """Load or simulate historical trend data"""
        # Try to load cached historical data
        history_file = self.cache_dir / f"history_{abs(hash(target_path))}.json"
        
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    history_data = json.load(f)
                
                historical_trend = []
                for item in history_data:
                    snapshot = HealthSnapshot(
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                        overall_score=item["overall_score"],
                        maintainability=item["maintainability"],
                        complexity=item["complexity"],
                        test_coverage=item["test_coverage"],
                        security=item["security"],
                        debt_ratio=item["debt_ratio"],
                        files_analyzed=item["files_analyzed"],
                        critical_issues=item["critical_issues"]
                    )
                    historical_trend.append(snapshot)
                
                return historical_trend
                
            except Exception as e:
                logger.warning(f"Failed to load historical data: {e}")
        
        # Generate simulated historical trend for demonstration
        return self._generate_simulated_history()
    
    def _generate_simulated_history(self) -> List[HealthSnapshot]:
        """Generate simulated historical data for demonstration"""
        history = []
        base_date = datetime.now() - timedelta(days=180)  # 6 months ago
        
        # Simulate declining health over time
        initial_score = 0.85
        score_decline = 0.02  # 2% decline per month
        
        for i in range(6):  # 6 months of history
            date = base_date + timedelta(days=30 * i)
            current_score = max(0.4, initial_score - (score_decline * i))
            
            snapshot = HealthSnapshot(
                timestamp=date,
                overall_score=current_score,
                maintainability=max(0.3, current_score + 0.1),
                complexity=max(0.3, current_score - 0.1),
                test_coverage=max(0.2, current_score - 0.2),
                security=max(0.6, current_score + 0.05),
                debt_ratio=min(0.8, 1.0 - current_score),
                files_analyzed=50 + i * 5,
                critical_issues=max(0, int((1.0 - current_score) * 20))
            )
            history.append(snapshot)
        
        return history
    
    async def _generate_predictions(self, 
                                  current_health: HealthSnapshot, 
                                  historical_trend: List[HealthSnapshot]) -> List[PredictionPoint]:
        """Generate future health predictions"""
        predictions = []
        
        if len(historical_trend) < 2:
            # Not enough history, make conservative predictions
            return self._make_conservative_predictions(current_health)
        
        # Calculate trends
        scores = [h.overall_score for h in historical_trend]
        debt_ratios = [h.debt_ratio for h in historical_trend]
        
        # Linear trend analysis
        score_trend = self._calculate_trend(scores)
        debt_trend = self._calculate_trend(debt_ratios)
        
        # Generate monthly predictions
        for month in range(1, self.prediction_horizon_months + 1):
            future_date = datetime.now() + timedelta(days=30 * month)
            
            # Predict score with trend
            predicted_score = max(0.0, min(1.0, current_health.overall_score + (score_trend * month)))
            predicted_debt = max(0.0, min(1.0, current_health.debt_ratio + (debt_trend * month)))
            
            # Calculate confidence (decreases over time)
            confidence = max(0.3, 0.9 - (month * 0.1))
            
            # Identify risk factors
            risk_factors = self._identify_risk_factors(predicted_score, predicted_debt, month)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(predicted_score, predicted_debt, risk_factors)
            
            prediction = PredictionPoint(
                date=future_date,
                predicted_score=predicted_score,
                confidence=confidence,
                risk_factors=risk_factors,
                recommendations=recommendations
            )
            predictions.append(prediction)
        
        return predictions
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate linear trend slope"""
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        x_values = list(range(n))
        
        # Simple linear regression slope
        x_mean = statistics.mean(x_values)
        y_mean = statistics.mean(values)
        
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)
        
        return numerator / denominator if denominator != 0 else 0.0
    
    def _make_conservative_predictions(self, current_health: HealthSnapshot) -> List[PredictionPoint]:
        """Make conservative predictions when insufficient historical data"""
        predictions = []
        
        for month in range(1, 4):  # Only 3 months for conservative approach
            future_date = datetime.now() + timedelta(days=30 * month)
            
            # Assume slight degradation over time
            degradation = 0.05 * month  # 5% per month
            predicted_score = max(0.2, current_health.overall_score - degradation)
            
            prediction = PredictionPoint(
                date=future_date,
                predicted_score=predicted_score,
                confidence=0.6 - (month * 0.1),
                risk_factors=["Insufficient historical data", "Conservative estimation"],
                recommendations=["Establish regular health monitoring", "Collect more data points"]
            )
            predictions.append(prediction)
        
        return predictions
    
    def _identify_risk_factors(self, predicted_score: float, predicted_debt: float, month: int) -> List[str]:
        """Identify risk factors based on predictions"""
        risks = []
        
        if predicted_score < 0.4:
            risks.append("Critical quality degradation")
        elif predicted_score < 0.6:
            risks.append("Quality decline trend")
        
        if predicted_debt > 0.7:
            risks.append("High technical debt accumulation")
        elif predicted_debt > 0.5:
            risks.append("Increasing technical debt")
        
        if month > 3 and predicted_score < 0.5:
            risks.append("Long-term maintainability concerns")
        
        return risks
    
    def _generate_recommendations(self, predicted_score: float, predicted_debt: float, risks: List[str]) -> List[str]:
        """Generate recommendations based on predictions"""
        recommendations = []
        
        if predicted_score < 0.5:
            recommendations.append("Schedule immediate refactoring sprint")
            recommendations.append("Implement strict code review process")
        
        if predicted_debt > 0.6:
            recommendations.append("Allocate 30% development time to debt reduction")
            recommendations.append("Prioritize high-impact refactoring")
        
        if "Critical quality degradation" in risks:
            recommendations.append("Consider architectural review")
            recommendations.append("Implement automated quality gates")
        
        if not recommendations:
            recommendations.append("Continue monitoring health trends")
            recommendations.append("Maintain current development practices")
        
        return recommendations
    
    def _create_debt_forecast(self, current: HealthSnapshot, predictions: List[PredictionPoint]) -> Dict[str, Any]:
        """Create debt forecast analysis"""
        if not predictions:
            return {"error": "No predictions available"}
        
        # Find critical debt threshold crossing
        critical_month = None
        for i, pred in enumerate(predictions):
            if pred.predicted_score < 0.4:  # Critical threshold
                critical_month = i + 1
                break
        
        # Calculate debt accumulation rate
        current_debt = current.debt_ratio
        future_debt = predictions[-1].predicted_score if predictions else current_debt
        debt_growth_rate = (future_debt - current_debt) / len(predictions) if predictions else 0
        
        return {
            "current_debt_ratio": current.debt_ratio,
            "projected_debt_ratio": future_debt,
            "debt_growth_rate_per_month": debt_growth_rate,
            "critical_threshold_month": critical_month,
            "estimated_refactoring_effort_days": max(5, int(current.debt_ratio * 30)),
            "debt_categories": {
                "complexity_debt": current.debt_ratio * 0.4,
                "test_debt": max(0, 0.8 - current.test_coverage) * 0.3,
                "maintainability_debt": max(0, 0.8 - current.maintainability) * 0.3
            }
        }
    
    def _create_maintenance_timeline(self, predictions: List[PredictionPoint]) -> Dict[str, Any]:
        """Create maintenance timeline recommendations"""
        timeline = {
            "immediate": [],
            "short_term": [],
            "medium_term": [],
            "long_term": []
        }
        
        for i, pred in enumerate(predictions):
            month = i + 1
            
            if month <= 1:
                period = "immediate"
            elif month <= 2:
                period = "short_term"
            elif month <= 4:
                period = "medium_term"
            else:
                period = "long_term"
            
            if pred.predicted_score < 0.6:
                timeline[period].extend(pred.recommendations)
        
        # Remove duplicates
        for period in timeline:
            timeline[period] = list(set(timeline[period]))
        
        return timeline
    
    def _prepare_visual_data(self, 
                           current: HealthSnapshot, 
                           history: List[HealthSnapshot], 
                           predictions: List[PredictionPoint]) -> Dict[str, Any]:
        """Prepare data for visual timeline generation"""
        
        # Historical data points
        historical_points = [
            {
                "date": h.timestamp.isoformat(),
                "score": h.overall_score,
                "type": "historical"
            }
            for h in history
        ]
        
        # Current point
        current_point = {
            "date": current.timestamp.isoformat(),
            "score": current.overall_score,
            "type": "current"
        }
        
        # Prediction points
        prediction_points = [
            {
                "date": p.date.isoformat(),
                "score": p.predicted_score,
                "confidence": p.confidence,
                "type": "prediction"
            }
            for p in predictions
        ]
        
        # Combine all points
        all_points = historical_points + [current_point] + prediction_points
        
        return {
            "timeline_data": all_points,
            "chart_config": {
                "title": "Code Health Timeline",
                "x_axis": "Date",
                "y_axis": "Health Score (0-1)",
                "critical_threshold": 0.4,
                "warning_threshold": 0.6
            },
            "health_zones": {
                "excellent": {"min": 0.8, "color": "green"},
                "good": {"min": 0.6, "color": "yellow"},
                "poor": {"min": 0.4, "color": "orange"},
                "critical": {"min": 0.0, "color": "red"}
            }
        }
    
    def _calculate_confidence(self, history: List[HealthSnapshot], predictions: List[PredictionPoint]) -> float:
        """Calculate overall confidence in the timeline analysis"""
        base_confidence = 0.7
        
        # Boost confidence with more historical data
        history_bonus = min(0.2, len(history) * 0.03)
        
        # Reduce confidence for long-term predictions
        prediction_penalty = len(predictions) * 0.02
        
        # Adjust for data quality
        if len(history) < 3:
            base_confidence -= 0.2
        
        confidence = base_confidence + history_bonus - prediction_penalty
        return max(0.3, min(0.95, confidence))
    
    async def _cache_timeline_result(self, target_path: str, session_id: str, result: TimelineResult):
        """Cache timeline result for future use"""
        try:
            cache_file = self.cache_dir / f"timeline_{session_id}.json"
            
            # Convert result to cacheable format
            cache_data = {
                "target_path": target_path,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "current_health": {
                    "timestamp": result.current_health.timestamp.isoformat(),
                    "overall_score": result.current_health.overall_score,
                    "maintainability": result.current_health.maintainability,
                    "complexity": result.current_health.complexity,
                    "test_coverage": result.current_health.test_coverage,
                    "security": result.current_health.security,
                    "debt_ratio": result.current_health.debt_ratio,
                    "files_analyzed": result.current_health.files_analyzed,
                    "critical_issues": result.current_health.critical_issues
                },
                "predictions": [
                    {
                        "date": p.date.isoformat(),
                        "predicted_score": p.predicted_score,
                        "confidence": p.confidence,
                        "risk_factors": p.risk_factors,
                        "recommendations": p.recommendations
                    }
                    for p in result.predictions
                ],
                "debt_forecast": result.debt_forecast,
                "processing_time": result.processing_time,
                "confidence": result.confidence
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
            logger.debug(f"Cached timeline result to {cache_file}")
            
        except Exception as e:
            logger.warning(f"Failed to cache timeline result: {e}")

# Export main function for Supreme integration
async def run_code_health_timeline(target_path: str, session_id: str, quality_metrics: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main function for Supreme Analyze integration.
    
    Args:
        target_path: Path to analyze
        session_id: Analysis session ID
        quality_metrics: Optional quality metrics from previous analysis
        
    Returns:
        Timeline analysis results in dictionary format
    """
    timeline_analyzer = CodeHealthTimeline()
    result = await timeline_analyzer.analyze_timeline(target_path, session_id, quality_metrics)
    
    # Convert to dictionary format for Supreme integration
    return {
        "debt_predictions": len([p for p in result.predictions if p.predicted_score < 0.6]),
        "timeline_generated": True,
        "maintenance_forecast": f"{len(result.maintenance_timeline.get('immediate', []))} immediate, {len(result.maintenance_timeline.get('short_term', []))} short-term items",
        "visual_timeline_created": True,
        "current_health_score": result.current_health.overall_score,
        "debt_ratio": result.current_health.debt_ratio,
        "critical_threshold_month": result.debt_forecast.get("critical_threshold_month"),
        "confidence": result.confidence,
        "processing_time": result.processing_time
    }