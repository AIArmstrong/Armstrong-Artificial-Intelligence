#!/usr/bin/env python3
"""
Unified Analytics Module - Cross-Folder Success Tracking & Intelligence
Tracks relationships between PRPs, Projects, Templates, and Integrations for seamless flow optimization.
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import re
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class PRPProjectMapping:
    """Mapping between PRP and Project with success metrics"""
    prp_id: str
    project_id: str
    template_ids: List[str]
    integration_ids: List[str]
    created_date: str
    status: str
    success_score: float
    completion_time: Optional[str] = None
    blockers: List[str] = None
    lessons_learned: List[str] = None

@dataclass
class TemplateUsageMetrics:
    """Template usage and success metrics"""
    template_id: str
    usage_count: int
    success_rate: float
    avg_completion_time: float
    common_blockers: List[str]
    improvement_suggestions: List[str]

@dataclass
class IntegrationEffectiveness:
    """Integration effectiveness across projects"""
    integration_id: str
    project_count: int
    success_rate: float
    avg_setup_time: float
    common_issues: List[str]
    recommended_personas: List[str]

class UnifiedAnalytics:
    """Central analytics system for cross-folder intelligence"""
    
    def __init__(self, base_path: str = "/mnt/c/Users/Brandon/AAI"):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / "brain" / "analytics.db"
        self.prps_path = self.base_path / "PRPs"
        self.projects_path = self.base_path / "projects"
        self.templates_path = self.base_path / "templates"
        self.integrations_path = self.base_path / "integrations"
        
        self._init_database()
    
    def _init_database(self):
        """Initialize analytics database with required tables"""
        self.db_path.parent.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # PRP-Project mappings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prp_project_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prp_id TEXT NOT NULL,
                project_id TEXT NOT NULL,
                template_ids TEXT,  -- JSON array
                integration_ids TEXT,  -- JSON array
                created_date TEXT NOT NULL,
                status TEXT NOT NULL,
                success_score REAL,
                completion_time TEXT,
                blockers TEXT,  -- JSON array
                lessons_learned TEXT,  -- JSON array
                UNIQUE(prp_id, project_id)
            )
        ''')
        
        # Template usage metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS template_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_id TEXT UNIQUE NOT NULL,
                usage_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                total_completion_time REAL DEFAULT 0,
                common_blockers TEXT,  -- JSON array
                improvement_suggestions TEXT,  -- JSON array
                last_updated TEXT NOT NULL
            )
        ''')
        
        # Integration effectiveness table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integration_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                integration_id TEXT UNIQUE NOT NULL,
                project_count INTEGER DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                total_setup_time REAL DEFAULT 0,
                common_issues TEXT,  -- JSON array
                recommended_personas TEXT,  -- JSON array
                last_updated TEXT NOT NULL
            )
        ''')
        
        # Success patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS success_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL,
                pattern_data TEXT NOT NULL,  -- JSON
                success_rate REAL NOT NULL,
                usage_count INTEGER DEFAULT 0,
                created_date TEXT NOT NULL,
                last_used TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_prp_to_project(self, prp_id: str, project_id: str, 
                           template_ids: List[str], integration_ids: List[str],
                           status: str = "scaffolded") -> bool:
        """Track new PRP to Project mapping"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO prp_project_mappings 
                (prp_id, project_id, template_ids, integration_ids, created_date, status, success_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                prp_id, project_id, json.dumps(template_ids), json.dumps(integration_ids),
                datetime.now().isoformat(), status, 0.0
            ))
            
            # Update template usage metrics
            for template_id in template_ids:
                self._update_template_usage(cursor, template_id)
            
            # Update integration metrics
            for integration_id in integration_ids:
                self._update_integration_usage(cursor, integration_id)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error tracking PRP to Project: {e}")
            return False
    
    def update_project_status(self, project_id: str, status: str, 
                            success_score: Optional[float] = None,
                            blockers: Optional[List[str]] = None) -> bool:
        """Update project status and metrics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            update_fields = ["status = ?"]
            update_values = [status]
            
            if success_score is not None:
                update_fields.append("success_score = ?")
                update_values.append(success_score)
            
            if blockers is not None:
                update_fields.append("blockers = ?")
                update_values.append(json.dumps(blockers))
            
            if status == "completed":
                update_fields.append("completion_time = ?")
                update_values.append(datetime.now().isoformat())
            
            update_values.append(project_id)
            
            cursor.execute(f'''
                UPDATE prp_project_mappings 
                SET {", ".join(update_fields)}
                WHERE project_id = ?
            ''', update_values)
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error updating project status: {e}")
            return False
    
    def _update_template_usage(self, cursor, template_id: str):
        """Update template usage statistics"""
        cursor.execute('''
            INSERT OR IGNORE INTO template_metrics (template_id, last_updated)
            VALUES (?, ?)
        ''', (template_id, datetime.now().isoformat()))
        
        cursor.execute('''
            UPDATE template_metrics 
            SET usage_count = usage_count + 1,
                last_updated = ?
            WHERE template_id = ?
        ''', (datetime.now().isoformat(), template_id))
    
    def _update_integration_usage(self, cursor, integration_id: str):
        """Update integration usage statistics"""
        cursor.execute('''
            INSERT OR IGNORE INTO integration_metrics (integration_id, last_updated)
            VALUES (?, ?)
        ''', (integration_id, datetime.now().isoformat()))
        
        cursor.execute('''
            UPDATE integration_metrics 
            SET project_count = project_count + 1,
                last_updated = ?
            WHERE integration_id = ?
        ''', (datetime.now().isoformat(), integration_id))
    
    def get_prp_success_patterns(self) -> List[Dict]:
        """Identify successful PRP patterns for recommendations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT prp_id, template_ids, integration_ids, success_score, completion_time
            FROM prp_project_mappings
            WHERE success_score >= 0.8 AND status = 'completed'
            ORDER BY success_score DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        patterns = []
        for row in results:
            prp_id, template_ids, integration_ids, success_score, completion_time = row
            patterns.append({
                "prp_id": prp_id,
                "template_ids": json.loads(template_ids) if template_ids else [],
                "integration_ids": json.loads(integration_ids) if integration_ids else [],
                "success_score": success_score,
                "completion_time": completion_time
            })
        
        return patterns
    
    def get_template_recommendations(self, prp_content: str, tech_stack: List[str]) -> List[str]:
        """Get template recommendations based on PRP content and success patterns"""
        patterns = self.get_prp_success_patterns()
        
        # Analyze PRP content for similar patterns
        content_keywords = self._extract_keywords(prp_content)
        
        # Score templates based on past success
        template_scores = defaultdict(float)
        
        for pattern in patterns:
            # Check if this pattern matches current PRP characteristics
            similarity = self._calculate_similarity(content_keywords, tech_stack, pattern)
            
            if similarity > 0.5:  # Similar enough to be relevant
                for template_id in pattern["template_ids"]:
                    template_scores[template_id] += pattern["success_score"] * similarity
        
        # Sort by score and return top recommendations
        sorted_templates = sorted(template_scores.items(), key=lambda x: x[1], reverse=True)
        return [template_id for template_id, score in sorted_templates[:5]]
    
    def get_integration_recommendations(self, prp_content: str, 
                                     project_complexity: str) -> List[str]:
        """Get integration recommendations based on content and complexity"""
        patterns = self.get_prp_success_patterns()
        
        # Analyze content for integration indicators
        content_lower = prp_content.lower()
        integration_indicators = {
            "superclaude": ["ai", "claude", "assistant", "automation"],
            "openrouter": ["llm", "language model", "ai generation"],
            "jina": ["scraping", "web data", "content extraction"],
            "supabase": ["database", "storage", "persistence"]
        }
        
        recommendations = []
        for integration, indicators in integration_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                recommendations.append(integration)
        
        # Add complexity-based recommendations
        if project_complexity in ["complex", "enterprise"]:
            recommendations.extend(["monitoring", "analytics", "ci-cd"])
        
        return list(set(recommendations))
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract relevant keywords from content"""
        # Simple keyword extraction - in real implementation, use more sophisticated NLP
        keywords = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
        return list(set(keywords))
    
    def _calculate_similarity(self, content_keywords: List[str], tech_stack: List[str], 
                            pattern: Dict) -> float:
        """Calculate similarity between current PRP and successful pattern"""
        # Simple similarity calculation - in real implementation, use embedding similarity
        
        # Get historical data for this pattern (would need to store more metadata)
        pattern_keywords = set(content_keywords)  # Simplified
        current_keywords = set(content_keywords)
        
        if not pattern_keywords and not current_keywords:
            return 0.0
        
        intersection = pattern_keywords & current_keywords
        union = pattern_keywords | current_keywords
        
        return len(intersection) / len(union) if union else 0.0
    
    def get_analytics_dashboard(self) -> Dict:
        """Generate comprehensive analytics dashboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Overall metrics
        cursor.execute('SELECT COUNT(*) FROM prp_project_mappings')
        total_projects = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM prp_project_mappings WHERE status = "completed"')
        completed_projects = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(success_score) FROM prp_project_mappings WHERE status = "completed"')
        avg_success_score = cursor.fetchone()[0] or 0.0
        
        # Template metrics
        cursor.execute('''
            SELECT template_id, usage_count, 
                   CAST(success_count AS REAL) / usage_count as success_rate
            FROM template_metrics 
            ORDER BY usage_count DESC 
            LIMIT 10
        ''')
        top_templates = cursor.fetchall()
        
        # Integration metrics
        cursor.execute('''
            SELECT integration_id, project_count,
                   CAST(success_count AS REAL) / project_count as success_rate
            FROM integration_metrics
            ORDER BY project_count DESC
            LIMIT 10
        ''')
        top_integrations = cursor.fetchall()
        
        # Recent activity
        cursor.execute('''
            SELECT prp_id, project_id, status, created_date, success_score
            FROM prp_project_mappings
            ORDER BY created_date DESC
            LIMIT 10
        ''')
        recent_activity = cursor.fetchall()
        
        conn.close()
        
        return {
            "overview": {
                "total_projects": total_projects,
                "completed_projects": completed_projects,
                "completion_rate": completed_projects / total_projects if total_projects > 0 else 0.0,
                "avg_success_score": avg_success_score
            },
            "template_performance": [
                {
                    "template_id": row[0],
                    "usage_count": row[1],
                    "success_rate": row[2] or 0.0
                }
                for row in top_templates
            ],
            "integration_performance": [
                {
                    "integration_id": row[0],
                    "project_count": row[1],
                    "success_rate": row[2] or 0.0
                }
                for row in top_integrations
            ],
            "recent_activity": [
                {
                    "prp_id": row[0],
                    "project_id": row[1],
                    "status": row[2],
                    "created_date": row[3],
                    "success_score": row[4]
                }
                for row in recent_activity
            ]
        }
    
    def identify_bottlenecks(self) -> Dict:
        """Identify bottlenecks in the PRP → Project flow"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Projects stuck in phases
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM prp_project_mappings
            WHERE status NOT IN ('completed', 'archived')
            GROUP BY status
        ''')
        stuck_projects = cursor.fetchall()
        
        # Common blockers
        cursor.execute('''
            SELECT blockers
            FROM prp_project_mappings
            WHERE blockers IS NOT NULL AND blockers != '[]'
        ''')
        blocker_data = cursor.fetchall()
        
        # Parse blockers
        all_blockers = []
        for row in blocker_data:
            blockers = json.loads(row[0])
            all_blockers.extend(blockers)
        
        # Count blocker frequency
        blocker_counts = defaultdict(int)
        for blocker in all_blockers:
            blocker_counts[blocker] += 1
        
        conn.close()
        
        return {
            "stuck_projects": [
                {"status": row[0], "count": row[1]}
                for row in stuck_projects
            ],
            "common_blockers": [
                {"blocker": blocker, "count": count}
                for blocker, count in sorted(blocker_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ]
        }
    
    def suggest_improvements(self) -> List[str]:
        """Generate improvement suggestions based on analytics"""
        dashboard = self.get_analytics_dashboard()
        bottlenecks = self.identify_bottlenecks()
        
        suggestions = []
        
        # Low completion rate
        if dashboard["overview"]["completion_rate"] < 0.6:
            suggestions.append("Consider simplifying PRP requirements or improving project scaffolding")
        
        # Low success scores
        if dashboard["overview"]["avg_success_score"] < 0.7:
            suggestions.append("Review and enhance template quality based on successful patterns")
        
        # Common blockers
        if bottlenecks["common_blockers"]:
            top_blocker = bottlenecks["common_blockers"][0]
            suggestions.append(f"Address common blocker: {top_blocker['blocker']} (affects {top_blocker['count']} projects)")
        
        # Template performance
        low_performing_templates = [
            t for t in dashboard["template_performance"] 
            if t["success_rate"] < 0.6 and t["usage_count"] > 2
        ]
        
        if low_performing_templates:
            suggestions.append("Improve or replace low-performing templates: " + 
                             ", ".join(t["template_id"] for t in low_performing_templates))
        
        return suggestions

def main():
    """Main function for CLI usage"""
    analytics = UnifiedAnalytics()
    
    # Generate analytics dashboard
    dashboard = analytics.get_analytics_dashboard()
    print("📊 Analytics Dashboard")
    print("=" * 50)
    print(json.dumps(dashboard, indent=2))
    
    # Identify bottlenecks
    bottlenecks = analytics.identify_bottlenecks()
    print("\n🚧 Bottlenecks Analysis")
    print("=" * 50)
    print(json.dumps(bottlenecks, indent=2))
    
    # Get improvement suggestions
    suggestions = analytics.suggest_improvements()
    print("\n💡 Improvement Suggestions")
    print("=" * 50)
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")

if __name__ == "__main__":
    main()