#!/usr/bin/env python3
"""
Archive Project Research Command
Extracts and preserves knowledge when projects are completed
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import zipfile
import tempfile

@dataclass
class ProjectKnowledge:
    """Extracted knowledge from completed project"""
    technology: str
    project_name: str
    knowledge_type: str  # 'pattern', 'configuration', 'lesson', 'best_practice'
    content: str
    quality_score: float
    reusability_score: float
    promotion_candidate: bool
    extraction_rationale: str

@dataclass
class ProjectArchive:
    """Complete project archive"""
    project_name: str
    archive_date: str
    technologies: List[str]
    knowledge_extracted: List[ProjectKnowledge]
    files_archived: List[str]
    promotion_candidates: List[str]
    archive_path: str
    summary: str

class ProjectArchiver:
    """Archives completed projects and extracts reusable knowledge"""
    
    def __init__(self, research_dir: str):
        self.research_dir = Path(research_dir)
        self.projects_dir = self.research_dir / "projects"
        self.knowledge_base = self.research_dir / "_knowledge-base"
        self.archives_dir = self.research_dir / "archives"
        self.validation_dir = self.research_dir / "validation"
        
        # Create archives directory
        self.archives_dir.mkdir(exist_ok=True)
        
        # Knowledge extraction patterns
        self.extraction_patterns = {
            'pattern': [
                r'## (.*Pattern.*)\n(.*?)(?=\n##|\Z)',
                r'### (.*Pattern.*)\n(.*?)(?=\n###|\n##|\Z)',
                r'## Implementation\n(.*?)(?=\n##|\Z)',
                r'### Implementation\n(.*?)(?=\n###|\n##|\Z)'
            ],
            'configuration': [
                r'## Configuration\n(.*?)(?=\n##|\Z)',
                r'### Configuration\n(.*?)(?=\n###|\n##|\Z)',
                r'## Setup\n(.*?)(?=\n##|\Z)',
                r'### Setup\n(.*?)(?=\n###|\n##|\Z)'
            ],
            'lesson': [
                r'## Lessons Learned\n(.*?)(?=\n##|\Z)',
                r'### Lessons Learned\n(.*?)(?=\n###|\n##|\Z)',
                r'## Gotchas\n(.*?)(?=\n##|\Z)',
                r'### Gotchas\n(.*?)(?=\n###|\n##|\Z)',
                r'## Issues\n(.*?)(?=\n##|\Z)',
                r'### Issues\n(.*?)(?=\n###|\n##|\Z)'
            ],
            'best_practice': [
                r'## Best Practices\n(.*?)(?=\n##|\Z)',
                r'### Best Practices\n(.*?)(?=\n###|\n##|\Z)',
                r'## Recommendations\n(.*?)(?=\n##|\Z)',
                r'### Recommendations\n(.*?)(?=\n###|\n##|\Z)'
            ]
        }
        
        # Promotion thresholds
        self.promotion_thresholds = {
            'pattern': 0.85,
            'configuration': 0.80,
            'lesson': 0.75,
            'best_practice': 0.85
        }
    
    def archive_project(self, project_name: str, extract_knowledge: bool = True, 
                       cleanup: bool = False) -> ProjectArchive:
        """Archive a completed project"""
        print(f"Archiving project: {project_name}")
        
        project_path = self.projects_dir / project_name
        if not project_path.exists():
            raise ValueError(f"Project {project_name} not found")
        
        # Create archive directory
        archive_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{project_name}_{archive_date}"
        archive_path = self.archives_dir / archive_name
        archive_path.mkdir(exist_ok=True)
        
        # Extract knowledge first
        knowledge_extracted = []
        promotion_candidates = []
        
        if extract_knowledge:
            knowledge_extracted = self._extract_project_knowledge(project_name)
            promotion_candidates = [
                k.technology for k in knowledge_extracted 
                if k.promotion_candidate
            ]
        
        # Archive files
        archived_files = self._archive_project_files(project_path, archive_path)
        
        # Get project technologies
        technologies = self._get_project_technologies(project_name)
        
        # Create archive metadata
        archive = ProjectArchive(
            project_name=project_name,
            archive_date=archive_date,
            technologies=technologies,
            knowledge_extracted=knowledge_extracted,
            files_archived=archived_files,
            promotion_candidates=promotion_candidates,
            archive_path=str(archive_path),
            summary=self._generate_archive_summary(project_name, knowledge_extracted)
        )
        
        # Save archive metadata
        self._save_archive_metadata(archive)
        
        # Process promotions
        if promotion_candidates:
            self._process_promotion_candidates(knowledge_extracted)
        
        # Create compressed archive
        self._create_compressed_archive(archive_path, project_name, archive_date)
        
        # Cleanup original if requested
        if cleanup:
            self._cleanup_original_project(project_name)
        
        # Update project registry
        self._update_project_registry(archive)
        
        print(f"Project {project_name} archived successfully")
        print(f"Archive location: {archive_path}")
        print(f"Knowledge extracted: {len(knowledge_extracted)} items")
        print(f"Promotion candidates: {len(promotion_candidates)}")
        
        return archive
    
    def _extract_project_knowledge(self, project_name: str) -> List[ProjectKnowledge]:
        """Extract reusable knowledge from project research"""
        knowledge_extracted = []
        
        project_research_dir = self.projects_dir / project_name / "_project-research"
        if not project_research_dir.exists():
            return knowledge_extracted
        
        # Process each research file
        for research_file in project_research_dir.glob("*.md"):
            technology = research_file.stem
            
            try:
                content = research_file.read_text(encoding='utf-8')
                
                # Extract different types of knowledge
                for knowledge_type, patterns in self.extraction_patterns.items():
                    extracted_items = self._extract_knowledge_by_type(
                        content, technology, project_name, knowledge_type, patterns
                    )
                    knowledge_extracted.extend(extracted_items)
                    
            except Exception as e:
                print(f"Error extracting knowledge from {research_file}: {e}")
        
        return knowledge_extracted
    
    def _extract_knowledge_by_type(self, content: str, technology: str, 
                                  project_name: str, knowledge_type: str, 
                                  patterns: List[str]) -> List[ProjectKnowledge]:
        """Extract specific type of knowledge using patterns"""
        import re
        
        extracted = []
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            
            for match in matches:
                if isinstance(match, tuple):
                    title, knowledge_content = match
                    full_content = f"## {title}\n{knowledge_content}"
                else:
                    full_content = match
                
                if full_content.strip():
                    # Calculate quality and reusability scores
                    quality_score = self._calculate_knowledge_quality(full_content, knowledge_type)
                    reusability_score = self._calculate_reusability_score(full_content)
                    
                    # Check promotion candidacy
                    promotion_candidate = (
                        quality_score >= self.promotion_thresholds.get(knowledge_type, 0.8) and
                        reusability_score >= 0.75
                    )
                    
                    knowledge = ProjectKnowledge(
                        technology=technology,
                        project_name=project_name,
                        knowledge_type=knowledge_type,
                        content=full_content.strip(),
                        quality_score=quality_score,
                        reusability_score=reusability_score,
                        promotion_candidate=promotion_candidate,
                        extraction_rationale=f"Extracted {knowledge_type} from {project_name}/{technology}"
                    )
                    
                    extracted.append(knowledge)
        
        return extracted
    
    def _calculate_knowledge_quality(self, content: str, knowledge_type: str) -> float:
        """Calculate quality score for extracted knowledge"""
        score = 0.0
        
        # Base score by type
        type_scores = {
            'pattern': 0.6,
            'configuration': 0.7,
            'lesson': 0.5,
            'best_practice': 0.8
        }
        score += type_scores.get(knowledge_type, 0.6)
        
        # Content quality indicators
        if len(content) > 100:
            score += 0.1
        if '```' in content:  # Has code examples
            score += 0.15
        if any(word in content.lower() for word in ['example', 'implementation', 'usage']):
            score += 0.1
        if any(word in content.lower() for word in ['best', 'recommended', 'should', 'must']):
            score += 0.05
        
        return min(score, 1.0)
    
    def _calculate_reusability_score(self, content: str) -> float:
        """Calculate reusability score for knowledge"""
        score = 0.5  # Base score
        
        # Reusability indicators
        if any(word in content.lower() for word in ['general', 'common', 'universal', 'standard']):
            score += 0.2
        if any(word in content.lower() for word in ['specific', 'custom', 'project', 'unique']):
            score -= 0.1
        if content.count('```') >= 2:  # Multiple code examples
            score += 0.15
        if any(word in content.lower() for word in ['pattern', 'template', 'boilerplate']):
            score += 0.2
        
        return min(max(score, 0.0), 1.0)
    
    def _archive_project_files(self, project_path: Path, archive_path: Path) -> List[str]:
        """Archive project files to archive directory"""
        archived_files = []
        
        # Copy project files
        for item in project_path.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(project_path)
                dest_path = archive_path / "project_files" / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                shutil.copy2(item, dest_path)
                archived_files.append(str(relative_path))
        
        return archived_files
    
    def _get_project_technologies(self, project_name: str) -> List[str]:
        """Get list of technologies used in project"""
        technologies = []
        
        project_research_dir = self.projects_dir / project_name / "_project-research"
        if project_research_dir.exists():
            for research_file in project_research_dir.glob("*.md"):
                technologies.append(research_file.stem)
        
        return technologies
    
    def _generate_archive_summary(self, project_name: str, knowledge_extracted: List[ProjectKnowledge]) -> str:
        """Generate summary of archived project"""
        summary = f"Project {project_name} archived on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if knowledge_extracted:
            summary += f"Knowledge Extracted ({len(knowledge_extracted)} items):\n"
            
            by_type = {}
            for knowledge in knowledge_extracted:
                if knowledge.knowledge_type not in by_type:
                    by_type[knowledge.knowledge_type] = []
                by_type[knowledge.knowledge_type].append(knowledge)
            
            for knowledge_type, items in by_type.items():
                summary += f"- {knowledge_type.replace('_', ' ').title()}: {len(items)} items\n"
                
                promotable = [item for item in items if item.promotion_candidate]
                if promotable:
                    summary += f"  * {len(promotable)} promotion candidates\n"
        
        return summary
    
    def _save_archive_metadata(self, archive: ProjectArchive):
        """Save archive metadata"""
        metadata_file = Path(archive.archive_path) / "archive_metadata.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(asdict(archive), f, indent=2, default=str)
    
    def _process_promotion_candidates(self, knowledge_extracted: List[ProjectKnowledge]):
        """Process knowledge promotion candidates"""
        promotion_log = []
        
        for knowledge in knowledge_extracted:
            if knowledge.promotion_candidate:
                try:
                    # Create general research file
                    general_file = self._promote_to_general_research(knowledge)
                    
                    promotion_log.append({
                        "technology": knowledge.technology,
                        "project": knowledge.project_name,
                        "knowledge_type": knowledge.knowledge_type,
                        "general_file": str(general_file),
                        "quality_score": knowledge.quality_score,
                        "reusability_score": knowledge.reusability_score,
                        "promoted_at": datetime.now().isoformat()
                    })
                    
                    print(f"Promoted {knowledge.technology} {knowledge.knowledge_type} to general research")
                    
                except Exception as e:
                    print(f"Error promoting {knowledge.technology} {knowledge.knowledge_type}: {e}")
        
        # Save promotion log
        if promotion_log:
            log_file = self.validation_dir / "archive-promotions.log"
            
            with open(log_file, 'a') as f:
                for entry in promotion_log:
                    f.write(f"{json.dumps(entry)}\n")
    
    def _promote_to_general_research(self, knowledge: ProjectKnowledge) -> Path:
        """Promote knowledge to general research"""
        technology = knowledge.technology
        
        # Create general research file if it doesn't exist
        general_file = self.knowledge_base / technology / f"{technology}-general.md"
        general_file.parent.mkdir(parents=True, exist_ok=True)
        
        if general_file.exists():
            # Append to existing file
            existing_content = general_file.read_text()
            
            # Add promoted section
            promoted_section = f"""

## {knowledge.knowledge_type.replace('_', ' ').title()} (Promoted from {knowledge.project_name})

{knowledge.content}

*Quality Score: {knowledge.quality_score:.2f} | Reusability: {knowledge.reusability_score:.2f}*
*Promoted from project: {knowledge.project_name}*
*Promotion Date: {datetime.now().strftime('%Y-%m-%d')}*
"""
            
            updated_content = existing_content + promoted_section
            general_file.write_text(updated_content)
            
        else:
            # Create new general research file
            template = f"""# {technology.title()} - General Research

## Overview
General research for {technology} - Enhanced with knowledge from completed projects.

## {knowledge.knowledge_type.replace('_', ' ').title()} (Promoted from {knowledge.project_name})

{knowledge.content}

*Quality Score: {knowledge.quality_score:.2f} | Reusability: {knowledge.reusability_score:.2f}*
*Promoted from project: {knowledge.project_name}*
*Promotion Date: {datetime.now().strftime('%Y-%m-%d')}*

## Quality Score: {knowledge.quality_score:.2f}
**Inheritance**: Base knowledge enhanced from project experience
**Source Quality**: Validated through project implementation
**Reusability**: {knowledge.reusability_score:.2f}
**Completeness**: Derived from real project usage

## Tags
#general #{technology} #promoted-from-{knowledge.project_name} #{knowledge.knowledge_type}
"""
            
            general_file.write_text(template)
        
        return general_file
    
    def _create_compressed_archive(self, archive_path: Path, project_name: str, archive_date: str):
        """Create compressed archive"""
        zip_path = archive_path.parent / f"{project_name}_{archive_date}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in archive_path.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(archive_path)
                    zipf.write(file_path, arcname)
        
        print(f"Compressed archive created: {zip_path}")
    
    def _cleanup_original_project(self, project_name: str):
        """Clean up original project files"""
        project_path = self.projects_dir / project_name
        
        # Move to cleanup directory instead of deleting
        cleanup_dir = self.archives_dir / "cleanup"
        cleanup_dir.mkdir(exist_ok=True)
        
        cleanup_path = cleanup_dir / f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(str(project_path), str(cleanup_path))
        
        print(f"Original project moved to cleanup: {cleanup_path}")
    
    def _update_project_registry(self, archive: ProjectArchive):
        """Update project registry with archive information"""
        registry_file = self.research_dir / "project-registry.json"
        
        registry = {}
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                registry = json.load(f)
        
        if "archived_projects" not in registry:
            registry["archived_projects"] = []
        
        registry["archived_projects"].append({
            "project_name": archive.project_name,
            "archive_date": archive.archive_date,
            "technologies": archive.technologies,
            "knowledge_count": len(archive.knowledge_extracted),
            "promotion_count": len(archive.promotion_candidates),
            "archive_path": archive.archive_path
        })
        
        with open(registry_file, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def list_archived_projects(self) -> List[Dict[str, Any]]:
        """List all archived projects"""
        registry_file = self.research_dir / "project-registry.json"
        
        if not registry_file.exists():
            return []
        
        with open(registry_file, 'r') as f:
            registry = json.load(f)
        
        return registry.get("archived_projects", [])
    
    def restore_project(self, project_name: str, archive_date: str) -> bool:
        """Restore project from archive"""
        try:
            # Find archive
            archive_path = self.archives_dir / f"{project_name}_{archive_date}"
            if not archive_path.exists():
                # Try compressed archive
                zip_path = self.archives_dir / f"{project_name}_{archive_date}.zip"
                if zip_path.exists():
                    # Extract compressed archive
                    with zipfile.ZipFile(zip_path, 'r') as zipf:
                        zipf.extractall(archive_path)
                else:
                    print(f"Archive not found: {project_name}_{archive_date}")
                    return False
            
            # Restore project files
            project_files_dir = archive_path / "project_files"
            if project_files_dir.exists():
                restore_path = self.projects_dir / project_name
                restore_path.mkdir(parents=True, exist_ok=True)
                
                for item in project_files_dir.rglob("*"):
                    if item.is_file():
                        relative_path = item.relative_to(project_files_dir)
                        dest_path = restore_path / relative_path
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, dest_path)
                
                print(f"Project {project_name} restored from {archive_date}")
                return True
            else:
                print(f"No project files found in archive")
                return False
                
        except Exception as e:
            print(f"Error restoring project: {e}")
            return False

def main():
    """Main execution function"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python archive-project.py <research_directory> <command> [options]")
        print("Commands:")
        print("  archive <project_name> [--extract-knowledge] [--cleanup]")
        print("  list")
        print("  restore <project_name> <archive_date>")
        sys.exit(1)
    
    research_dir = sys.argv[1]
    command = sys.argv[2]
    
    archiver = ProjectArchiver(research_dir)
    
    if command == "archive":
        if len(sys.argv) < 4:
            print("Usage: archive <project_name> [--extract-knowledge] [--cleanup]")
            sys.exit(1)
        
        project_name = sys.argv[3]
        extract_knowledge = "--extract-knowledge" in sys.argv
        cleanup = "--cleanup" in sys.argv
        
        try:
            archive = archiver.archive_project(project_name, extract_knowledge, cleanup)
            print(f"\nArchive Summary:\n{archive.summary}")
        except Exception as e:
            print(f"Error archiving project: {e}")
    
    elif command == "list":
        archived_projects = archiver.list_archived_projects()
        
        if archived_projects:
            print(f"\nArchived Projects ({len(archived_projects)}):")
            for project in archived_projects:
                print(f"  {project['project_name']} ({project['archive_date']})")
                print(f"    Technologies: {', '.join(project['technologies'])}")
                print(f"    Knowledge: {project['knowledge_count']} items")
                print(f"    Promotions: {project['promotion_count']} items")
                print()
        else:
            print("No archived projects found")
    
    elif command == "restore":
        if len(sys.argv) < 5:
            print("Usage: restore <project_name> <archive_date>")
            sys.exit(1)
        
        project_name = sys.argv[3]
        archive_date = sys.argv[4]
        
        success = archiver.restore_project(project_name, archive_date)
        if success:
            print(f"Project {project_name} restored successfully")
        else:
            print(f"Failed to restore project {project_name}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()