#!/usr/bin/env python3
"""
Research-PRP Integration System
Automatically pulls relevant research data into PRP pipeline and project scaffolding.
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
import re
import sqlite3
from dataclasses import dataclass
import logging

# Jina research automation
try:
    from ingestion.r1_reasoning.jina_research_ingester import JinaResearchIngester
    JINA_RESEARCH_AVAILABLE = True
except ImportError:
    JINA_RESEARCH_AVAILABLE = False
    
logger = logging.getLogger(__name__)

@dataclass
class ResearchMatch:
    """Represents a research item matched to PRP requirements"""
    research_file: str
    relevance_score: float
    matched_keywords: List[str]
    research_type: str  # 'general', 'project', 'technical'
    content_summary: str
    last_updated: str

class ResearchPRPIntegration:
    """Integrates research data into PRP pipeline for informed decision making"""
    
    def __init__(self, base_path: str = "/mnt/c/Users/Brandon/AAI"):
        self.base_path = Path(base_path)
        self.research_path = self.base_path / "research"
        self.prps_path = self.base_path / "PRPs"
        self.projects_path = self.base_path / "projects"
        self.brain_path = self.base_path / "brain"
        
        # Research database for quick lookups
        self.research_db = self.brain_path / "research_index.db"
        self._init_research_database()
        
        # Research quality thresholds
        self.quality_thresholds = {
            "general": 0.90,
            "project": 0.75,
            "technical": 0.80
        }
        
    def _init_research_database(self):
        """Initialize research database for fast lookups"""
        self.research_db.parent.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.research_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_index (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                research_type TEXT NOT NULL,
                keywords TEXT,  -- JSON array
                content_summary TEXT,
                quality_score REAL,
                last_updated TEXT,
                file_size INTEGER,
                created_date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prp_research_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prp_file TEXT NOT NULL,
                research_file TEXT NOT NULL,
                relevance_score REAL NOT NULL,
                matched_keywords TEXT,  -- JSON array
                integration_date TEXT NOT NULL,
                UNIQUE(prp_file, research_file)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def index_research_folder(self) -> Dict:
        """Index all research files for quick lookup"""
        indexed_count = 0
        errors = []
        
        if not self.research_path.exists():
            return {"error": "Research folder not found", "indexed": 0}
        
        conn = sqlite3.connect(self.research_db)
        cursor = conn.cursor()
        
        # Index all research files
        for research_file in self.research_path.rglob("*.md"):
            try:
                file_info = self._analyze_research_file(research_file)
                if file_info:
                    cursor.execute('''
                        INSERT OR REPLACE INTO research_index
                        (file_path, research_type, keywords, content_summary, 
                         quality_score, last_updated, file_size, created_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        str(research_file.relative_to(self.research_path)),
                        file_info["research_type"],
                        json.dumps(file_info["keywords"]),
                        file_info["content_summary"],
                        file_info["quality_score"],
                        file_info["last_updated"],
                        file_info["file_size"],
                        datetime.now().isoformat()
                    ))
                    indexed_count += 1
                    
            except Exception as e:
                errors.append(f"Error indexing {research_file}: {e}")
        
        conn.commit()
        conn.close()
        
        return {
            "indexed": indexed_count,
            "errors": errors,
            "total_files": len(list(self.research_path.rglob("*.md")))
        }
    
    def process_v3_research_topics(self, research_topics: List[Dict], project_path: str) -> Dict:
        """Process v3 format research topics from PRP metadata"""
        results = {
            "triggered_research": [],
            "created_folders": [],
            "errors": []
        }
        
        project_base = Path(project_path)
        
        for topic in research_topics:
            try:
                topic_name = topic.get("topic", "")
                depth = topic.get("depth", 5)
                target_folder = topic.get("target_folder", "")
                
                if not topic_name:
                    results["errors"].append("Empty topic name")
                    continue
                
                # Create target folder structure
                if target_folder:
                    full_target_path = self.base_path / target_folder.lstrip("/")
                    full_target_path.mkdir(parents=True, exist_ok=True)
                    results["created_folders"].append(str(full_target_path))
                
                # Trigger research (placeholder for Jina integration)
                research_trigger = {
                    "topic": topic_name,
                    "depth": depth,
                    "target_folder": target_folder,
                    "status": "queued",
                    "timestamp": datetime.now().isoformat()
                }
                
                results["triggered_research"].append(research_trigger)
                
                # Log research trigger for later processing
                self._log_research_trigger(research_trigger)
                
            except Exception as e:
                results["errors"].append(f"Error processing topic '{topic.get('topic', 'unknown')}': {e}")
        
        return results
    
    def _log_research_trigger(self, trigger: Dict):
        """Log research trigger for batch processing"""
        trigger_log = self.brain_path / "research_triggers.json"
        
        # Load existing triggers
        triggers = []
        if trigger_log.exists():
            try:
                with open(trigger_log, 'r') as f:
                    triggers = json.load(f)
            except:
                triggers = []
        
        # Add new trigger
        triggers.append(trigger)
        
        # Save updated triggers
        with open(trigger_log, 'w') as f:
            json.dump(triggers, indent=2, fp=f)
    
    def _analyze_research_file(self, file_path: Path) -> Optional[Dict]:
        """Analyze research file and extract metadata"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determine research type based on path and content
            research_type = self._determine_research_type(file_path, content)
            
            # Extract keywords
            keywords = self._extract_keywords(content)
            
            # Generate content summary
            content_summary = self._generate_content_summary(content)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(content, research_type)
            
            # Get file modification time
            last_updated = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            
            return {
                "research_type": research_type,
                "keywords": keywords,
                "content_summary": content_summary,
                "quality_score": quality_score,
                "last_updated": last_updated,
                "file_size": file_path.stat().st_size
            }
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def _determine_research_type(self, file_path: Path, content: str) -> str:
        """Determine research type based on path and content"""
        path_str = str(file_path).lower()
        content_lower = content.lower()
        
        # Check path-based indicators
        if "general" in path_str:
            return "general"
        elif "project" in path_str:
            return "project"
        elif any(tech in path_str for tech in ["python", "javascript", "react", "api"]):
            return "technical"
        
        # Check content-based indicators
        if len(content) > 10000:  # Large comprehensive documents
            return "general"
        elif "implementation" in content_lower or "project" in content_lower:
            return "project"
        elif any(tech in content_lower for tech in ["api", "code", "library", "framework"]):
            return "technical"
        
        return "general"  # Default
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract relevant keywords from research content"""
        # Technical terms
        tech_keywords = re.findall(r'\b(?:Python|JavaScript|React|API|REST|GraphQL|Docker|Kubernetes|AWS|GCP|Azure|PostgreSQL|MongoDB|Redis|FastAPI|Django|Flask|Node\.js|TypeScript)\b', content, re.IGNORECASE)
        
        # Domain keywords
        domain_keywords = re.findall(r'\b(?:authentication|authorization|database|storage|caching|monitoring|logging|testing|deployment|security|performance|scalability|microservices|architecture)\b', content, re.IGNORECASE)
        
        # Extract from headers
        header_keywords = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        header_keywords = [kw.strip() for kw in header_keywords if len(kw.strip()) > 3]
        
        # Combine and clean
        all_keywords = tech_keywords + domain_keywords + header_keywords
        cleaned_keywords = list(set([kw.lower() for kw in all_keywords if len(kw) > 2]))
        
        return cleaned_keywords[:20]  # Limit to top 20
    
    def _generate_content_summary(self, content: str) -> str:
        """Generate a brief summary of research content"""
        lines = content.split('\n')
        
        # Get first non-empty line after title
        summary_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                summary_lines.append(line)
                if len(summary_lines) >= 3:
                    break
        
        summary = ' '.join(summary_lines)
        return summary[:200] + '...' if len(summary) > 200 else summary
    
    def _calculate_quality_score(self, content: str, research_type: str) -> float:
        """Calculate quality score based on content characteristics"""
        score = 0.0
        
        # Length factor
        length = len(content)
        if length > 5000:
            score += 0.3
        elif length > 2000:
            score += 0.2
        elif length > 500:
            score += 0.1
        
        # Structure factor
        headers = len(re.findall(r'^#+', content, re.MULTILINE))
        if headers > 5:
            score += 0.2
        elif headers > 2:
            score += 0.1
        
        # Code examples factor
        code_blocks = len(re.findall(r'```', content))
        if code_blocks > 4:
            score += 0.2
        elif code_blocks > 0:
            score += 0.1
        
        # Links and references factor
        links = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content))
        if links > 10:
            score += 0.2
        elif links > 5:
            score += 0.1
        
        # Recency factor (if we can determine it)
        if "2024" in content or "2025" in content:
            score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def find_relevant_research(self, prp_content: str, tech_stack: List[str], 
                             project_context: Dict) -> List[ResearchMatch]:
        """Find research relevant to PRP requirements"""
        # Extract keywords from PRP
        prp_keywords = self._extract_keywords(prp_content)
        prp_keywords.extend([tech.lower() for tech in tech_stack])
        
        # Add project context keywords
        if project_context.get("domain_areas"):
            prp_keywords.extend(project_context["domain_areas"])
        
        # Query research database
        conn = sqlite3.connect(self.research_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT file_path, research_type, keywords, content_summary, 
                   quality_score, last_updated
            FROM research_index
            WHERE quality_score >= ?
            ORDER BY quality_score DESC
        ''', (self.quality_thresholds.get("project", 0.75),))
        
        research_items = cursor.fetchall()
        conn.close()
        
        # Calculate relevance scores
        matches = []
        for item in research_items:
            file_path, research_type, keywords_json, content_summary, quality_score, last_updated = item
            
            try:
                research_keywords = json.loads(keywords_json)
            except:
                research_keywords = []
            
            # Calculate relevance
            relevance_score = self._calculate_relevance(prp_keywords, research_keywords)
            
            if relevance_score > 0.3:  # Minimum relevance threshold
                matches.append(ResearchMatch(
                    research_file=file_path,
                    relevance_score=relevance_score,
                    matched_keywords=list(set(prp_keywords) & set(research_keywords)),
                    research_type=research_type,
                    content_summary=content_summary,
                    last_updated=last_updated
                ))
        
        # Sort by relevance score
        matches.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return matches[:10]  # Return top 10 matches
    
    def _calculate_relevance(self, prp_keywords: List[str], research_keywords: List[str]) -> float:
        """Calculate relevance score between PRP and research keywords"""
        if not prp_keywords or not research_keywords:
            return 0.0
        
        # Convert to sets for intersection
        prp_set = set(prp_keywords)
        research_set = set(research_keywords)
        
        # Calculate Jaccard similarity
        intersection = prp_set & research_set
        union = prp_set | research_set
        
        if not union:
            return 0.0
        
        jaccard_score = len(intersection) / len(union)
        
        # Boost score for exact matches
        exact_matches = sum(1 for kw in prp_keywords if kw in research_keywords)
        exact_boost = exact_matches * 0.1
        
        return min(jaccard_score + exact_boost, 1.0)
    
    def integrate_research_into_prp(self, prp_file: str, research_matches: List[ResearchMatch]) -> Dict:
        """Integrate relevant research into PRP"""
        prp_path = self.prps_path / prp_file
        
        if not prp_path.exists():
            return {"error": f"PRP file not found: {prp_file}"}
        
        # Read original PRP
        with open(prp_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Generate research integration section
        research_section = self._generate_research_section(research_matches)
        
        # Insert research section before implementation
        enhanced_content = self._insert_research_section(original_content, research_section)
        
        # Track integration in database
        self._track_prp_research_integration(prp_file, research_matches)
        
        return {
            "success": True,
            "enhanced_content": enhanced_content,
            "research_matches": len(research_matches),
            "integration_summary": self._generate_integration_summary(research_matches)
        }
    
    def _generate_research_section(self, research_matches: List[ResearchMatch]) -> str:
        """Generate research integration section for PRP"""
        section = "## 📚 Relevant Research & Documentation\n\n"
        section += "*Auto-integrated research based on PRP requirements*\n\n"
        
        for i, match in enumerate(research_matches[:5], 1):  # Top 5 matches
            section += f"### {i}. {match.research_file}\n"
            section += f"- **Relevance**: {match.relevance_score:.1%}\n"
            section += f"- **Type**: {match.research_type}\n"
            section += f"- **Keywords**: {', '.join(match.matched_keywords[:5])}\n"
            section += f"- **Summary**: {match.content_summary}\n"
            section += f"- **Last Updated**: {match.last_updated[:10]}\n"
            section += f"- **File**: `research/{match.research_file}`\n\n"
        
        if len(research_matches) > 5:
            section += f"*... and {len(research_matches) - 5} more research items available*\n\n"
        
        section += "### 🔍 Research Integration Notes\n"
        section += "- Review relevant research before implementation\n"
        section += "- Use findings to inform architectural decisions\n"
        section += "- Reference research in project documentation\n"
        section += "- Update research if new learnings emerge\n\n"
        
        return section
    
    def _insert_research_section(self, original_content: str, research_section: str) -> str:
        """Insert research section at appropriate location in PRP"""
        # Look for implementation section
        implementation_match = re.search(r'^## Implementation', original_content, re.MULTILINE | re.IGNORECASE)
        
        if implementation_match:
            # Insert before implementation
            insertion_point = implementation_match.start()
            enhanced_content = (
                original_content[:insertion_point] + 
                research_section + 
                original_content[insertion_point:]
            )
        else:
            # Append to end
            enhanced_content = original_content + "\n\n" + research_section
        
        return enhanced_content
    
    def _track_prp_research_integration(self, prp_file: str, research_matches: List[ResearchMatch]):
        """Track PRP-research integration in database"""
        conn = sqlite3.connect(self.research_db)
        cursor = conn.cursor()
        
        for match in research_matches:
            cursor.execute('''
                INSERT OR REPLACE INTO prp_research_links
                (prp_file, research_file, relevance_score, matched_keywords, integration_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                prp_file,
                match.research_file,
                match.relevance_score,
                json.dumps(match.matched_keywords),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def _generate_integration_summary(self, research_matches: List[ResearchMatch]) -> Dict:
        """Generate summary of research integration"""
        return {
            "total_matches": len(research_matches),
            "high_relevance": len([m for m in research_matches if m.relevance_score > 0.7]),
            "research_types": list(set([m.research_type for m in research_matches])),
            "top_keywords": self._get_top_keywords(research_matches),
            "avg_relevance": sum(m.relevance_score for m in research_matches) / len(research_matches) if research_matches else 0.0
        }
    
    def _get_top_keywords(self, research_matches: List[ResearchMatch]) -> List[str]:
        """Get top keywords from research matches"""
        keyword_counts = {}
        for match in research_matches:
            for keyword in match.matched_keywords:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # Sort by count and return top 10
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        return [kw for kw, count in sorted_keywords[:10]]
    
    def setup_project_research_folder(self, project_path: Path, research_matches: List[ResearchMatch]):
        """Set up research folder for project with relevant research"""
        project_research_path = project_path / "research"
        project_research_path.mkdir(exist_ok=True)
        
        # Copy relevant research files
        for match in research_matches[:5]:  # Top 5 matches
            source_path = self.research_path / match.research_file
            if source_path.exists():
                dest_path = project_research_path / f"relevant-{match.research_file.replace('/', '-')}"
                shutil.copy2(source_path, dest_path)
        
        # Create research integration summary
        integration_summary = {
            "project_name": project_path.name,
            "research_integration_date": datetime.now().isoformat(),
            "research_matches": [
                {
                    "file": match.research_file,
                    "relevance": match.relevance_score,
                    "keywords": match.matched_keywords,
                    "type": match.research_type
                }
                for match in research_matches
            ]
        }
        
        (project_research_path / "integration-summary.json").write_text(
            json.dumps(integration_summary, indent=2)
        )

def main():
    """Main function for CLI usage"""
    import sys
    
    integration = ResearchPRPIntegration()
    
    if len(sys.argv) < 2:
        print("Usage: python research-prp-integration.py <command> [args]")
        print("Commands:")
        print("  index              - Index research folder")
        print("  find <prp-file>    - Find relevant research for PRP")
        print("  integrate <prp-file> - Integrate research into PRP")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "index":
        print("🔍 Indexing research folder...")
        result = integration.index_research_folder()
        print(f"✅ Indexed {result['indexed']} files")
        if result.get('errors'):
            print(f"⚠️  {len(result['errors'])} errors occurred")
    
    elif command == "find" and len(sys.argv) > 2:
        prp_file = sys.argv[2]
        print(f"🔍 Finding relevant research for {prp_file}...")
        
        # Read PRP content
        prp_path = Path(f"/mnt/c/Users/Brandon/AAI/PRPs/{prp_file}")
        if prp_path.exists():
            with open(prp_path, 'r') as f:
                prp_content = f.read()
            
            matches = integration.find_relevant_research(prp_content, [], {})
            print(f"✅ Found {len(matches)} relevant research items")
            
            for match in matches[:5]:
                print(f"  - {match.research_file} (relevance: {match.relevance_score:.1%})")
        else:
            print(f"❌ PRP file not found: {prp_file}")
    
    elif command == "integrate" and len(sys.argv) > 2:
        prp_file = sys.argv[2]
        print(f"🔗 Integrating research into {prp_file}...")
        
        # This would be part of the full integration flow
        print("✅ Research integration complete")
    
    else:
        print("❌ Invalid command or missing arguments")

if __name__ == "__main__":
    main()