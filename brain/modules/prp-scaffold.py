#!/usr/bin/env python3
"""
PRP Scaffolding System - Seamless PRP to Project Automation
Transforms approved PRPs into structured projects with metadata, templates, and readiness checks.
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re
import yaml

class PRPScaffolder:
    """Automated PRP to Project scaffolding with readiness checks and integration awareness"""
    
    def __init__(self, base_path: str = "/mnt/c/Users/Brandon/AAI"):
        self.base_path = Path(base_path)
        self.prps_path = self.base_path / "PRPs"
        self.projects_path = self.base_path / "projects"
        self.templates_path = self.base_path / "templates"
        self.integrations_path = self.base_path / "integrations"
        self.research_path = self.base_path / "research"
        self.brain_path = self.base_path / "brain"
        
    def scaffold_from_prp(self, prp_file: str, force_override: bool = False) -> Dict:
        """
        Main scaffolding function: PRP → Project with full automation
        
        Flow:
        1. Parse PRP and extract metadata
        2. Run readiness checks (blockers, dependencies)
        3. Analyze integration requirements
        4. Compose modular templates
        5. Create project structure
        6. Generate project.json metadata
        7. Set up monitoring and contradiction checks
        """
        print(f"🚀 Starting PRP scaffolding for: {prp_file}")
        
        # 1. Parse PRP
        prp_data = self._parse_prp(prp_file)
        if not prp_data:
            return {"error": "Failed to parse PRP file"}
            
        project_name = prp_data["project_name"]
        project_path = self.projects_path / project_name
        
        # Check if project already exists
        if project_path.exists() and not force_override:
            return {"error": f"Project {project_name} already exists. Use force_override=True to recreate."}
            
        # 2. Readiness checks
        readiness_result = self._check_readiness(prp_data)
        if not readiness_result["ready"]:
            return {
                "error": "Project not ready for scaffolding",
                "blockers": readiness_result["blockers"],
                "suggestions": readiness_result["suggestions"]
            }
            
        # 3. Integration analysis
        integration_requirements = self._analyze_integration_requirements(prp_data)
        
        # 4. Template composition
        template_components = self._compose_templates(prp_data, integration_requirements)
        
        # 5. Create project structure
        self._create_project_structure(project_path, template_components)
        
        # 6. Generate project.json
        project_metadata = self._generate_project_metadata(
            prp_data, prp_file, integration_requirements, template_components
        )
        
        # 7. Set up monitoring
        self._setup_monitoring(project_path, project_metadata)
        
        # 8. Pull relevant research
        self._integrate_research(project_path, prp_data)
        
        # 9. Log scaffolding event
        self._log_scaffolding_event(project_name, prp_file, project_metadata)
        
        return {
            "success": True,
            "project_name": project_name,
            "project_path": str(project_path),
            "metadata": project_metadata,
            "integration_requirements": integration_requirements,
            "template_components": template_components
        }
    
    def _parse_prp(self, prp_file: str) -> Optional[Dict]:
        """Parse PRP file and extract key metadata including v3 YAML frontmatter"""
        prp_path = self.prps_path / prp_file
        if not prp_path.exists():
            print(f"❌ PRP file not found: {prp_path}")
            return None
            
        try:
            with open(prp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter (v3 format)
            metadata = self._parse_yaml_frontmatter(content)
            
            # Extract project name (prioritize metadata, fallback to filename)
            project_name = metadata.get('project_name', prp_file.replace('.md', '').replace('_', '-'))
            
            # Parse key sections
            sections = self._extract_prp_sections(content)
            
            # Build comprehensive data structure
            prp_data = {
                "project_name": project_name,
                "prp_file": prp_file,
                "content": content,
                "sections": sections,
                "tech_stack": self._extract_tech_stack(content),
                "integrations": self._extract_integration_mentions(content),
                "complexity": self._assess_complexity(content),
                "testing_requirements": self._extract_testing_requirements(content)
            }
            
            # Merge v3 metadata if available
            if metadata:
                prp_data.update({
                    "metadata": metadata,
                    "id": metadata.get('id', f"prp-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
                    "priority": metadata.get('priority', 'medium'),
                    "auto_scaffold": metadata.get('auto_scaffold', False),
                    "estimated_effort": metadata.get('estimated_effort', 'unknown'),
                    "complexity_override": metadata.get('complexity', None),
                    "tags": metadata.get('tags', []),
                    "research_topics": self._extract_research_topics(content),
                    "example_references": self._extract_example_references(content),
                    "dependencies": self._extract_dependencies(content)
                })
                # Override complexity if specified in metadata
                if metadata.get('complexity'):
                    prp_data["complexity"] = metadata.get('complexity')
                    
            return prp_data
            
        except Exception as e:
            print(f"❌ Error parsing PRP: {e}")
            return None
    
    def _extract_prp_sections(self, content: str) -> Dict:
        """Extract key sections from PRP content"""
        sections = {}
        
        # Common PRP sections
        section_patterns = {
            "overview": r"## Overview\n(.*?)(?=\n##|\Z)",
            "requirements": r"## Requirements\n(.*?)(?=\n##|\Z)",
            "implementation": r"## Implementation\n(.*?)(?=\n##|\Z)",
            "testing": r"## Testing\n(.*?)(?=\n##|\Z)",
            "architecture": r"## Architecture\n(.*?)(?=\n##|\Z)"
        }
        
        for section, pattern in section_patterns.items():
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                sections[section] = match.group(1).strip()
                
        return sections
    
    def _parse_yaml_frontmatter(self, content: str) -> Dict:
        """Parse YAML frontmatter from PRP v3 format"""
        try:
            # Check if content starts with YAML frontmatter
            if not content.startswith('---\n'):
                return {}
            
            # Find the end of frontmatter
            end_marker = content.find('\n---\n', 4)
            if end_marker == -1:
                return {}
            
            # Extract YAML content
            yaml_content = content[4:end_marker]
            
            # Parse YAML
            return yaml.safe_load(yaml_content) or {}
            
        except Exception as e:
            print(f"⚠️ Warning: Could not parse YAML frontmatter: {e}")
            return {}
    
    def _extract_research_topics(self, content: str) -> List[Dict]:
        """Extract research topics from v3 format"""
        try:
            # Look for research_topics section in YAML blocks
            research_pattern = r'research_topics:\n(.*?)```'
            match = re.search(research_pattern, content, re.DOTALL)
            if match:
                yaml_content = "research_topics:\n" + match.group(1).strip()
                data = yaml.safe_load(yaml_content)
                return data.get('research_topics', []) if data else []
        except Exception as e:
            print(f"⚠️ Warning: Could not parse research topics: {e}")
        return []
    
    def _extract_example_references(self, content: str) -> List[str]:
        """Extract example pattern references from v3 format"""
        try:
            # Look for example_references section
            example_pattern = r'example_references:(.*?)pattern_similarity_threshold'
            match = re.search(example_pattern, content, re.DOTALL)
            if match:
                yaml_content = match.group(1).strip()
                return yaml.safe_load(yaml_content) or []
        except Exception:
            pass
        return []
    
    def _extract_dependencies(self, content: str) -> Dict:
        """Extract dependency graph from v3 format"""
        try:
            # Look for dependencies section
            deps_pattern = r'dependencies:(.*?)```'
            match = re.search(deps_pattern, content, re.DOTALL)
            if match:
                yaml_content = match.group(1).strip()
                return yaml.safe_load(yaml_content) or {}
        except Exception:
            pass
        return {}
    
    def _extract_tech_stack(self, content: str) -> List[str]:
        """Extract technology stack from PRP content"""
        tech_patterns = [
            r"Python", r"JavaScript", r"TypeScript", r"React", r"Node\.js",
            r"FastAPI", r"Django", r"Flask", r"PostgreSQL", r"MongoDB",
            r"Redis", r"Docker", r"Kubernetes", r"AWS", r"Azure", r"GCP"
        ]
        
        tech_stack = []
        for pattern in tech_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                tech_stack.append(pattern)
                
        return tech_stack
    
    def _extract_integration_mentions(self, content: str) -> List[str]:
        """Extract integration requirements from PRP content"""
        integration_patterns = [
            r"SuperClaude", r"OpenRouter", r"Jina", r"Supabase",
            r"OpenAI", r"Anthropic", r"MCP", r"API", r"webhook"
        ]
        
        integrations = []
        for pattern in integration_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                integrations.append(pattern)
                
        return integrations
    
    def _assess_complexity(self, content: str) -> str:
        """Assess project complexity based on PRP content"""
        complexity_indicators = {
            "simple": ["basic", "simple", "minimal", "quick"],
            "medium": ["moderate", "standard", "typical", "reasonable"],
            "complex": ["complex", "advanced", "sophisticated", "comprehensive"],
            "enterprise": ["enterprise", "large-scale", "production", "scalable"]
        }
        
        content_lower = content.lower()
        scores = {}
        
        for level, indicators in complexity_indicators.items():
            scores[level] = sum(1 for indicator in indicators if indicator in content_lower)
            
        # Additional complexity factors
        if len(content) > 5000:
            scores["complex"] += 2
        if "microservice" in content_lower or "distributed" in content_lower:
            scores["enterprise"] += 3
            
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _extract_testing_requirements(self, content: str) -> Dict:
        """Extract testing requirements from PRP"""
        testing_types = {
            "unit": r"unit test|unit testing",
            "integration": r"integration test|integration testing",
            "e2e": r"e2e|end-to-end|end to end",
            "api": r"api test|api testing",
            "performance": r"performance test|load test|stress test"
        }
        
        requirements = {}
        for test_type, pattern in testing_types.items():
            if re.search(pattern, content, re.IGNORECASE):
                requirements[test_type] = True
                
        return requirements
    
    def _check_readiness(self, prp_data: Dict) -> Dict:
        """
        Comprehensive readiness checks before project creation
        
        Checks:
        - Required templates exist
        - Integration dependencies available
        - Research data sufficient
        - No conflicting projects
        """
        blockers = []
        suggestions = []
        
        # Check template availability
        required_templates = self._determine_required_templates(prp_data)
        for template in required_templates:
            template_path = self.templates_path / template
            if not template_path.exists():
                blockers.append(f"Required template missing: {template}")
                suggestions.append(f"Create template at: {template_path}")
        
        # Check integration availability
        for integration in prp_data["integrations"]:
            integration_path = self.integrations_path / integration.lower()
            if not integration_path.exists():
                blockers.append(f"Integration not available: {integration}")
                suggestions.append(f"Set up integration: {integration}")
        
        # Check research data
        research_keywords = self._extract_research_keywords(prp_data)
        if research_keywords and not self._has_sufficient_research(research_keywords):
            blockers.append("Insufficient research data for project requirements")
            suggestions.append("Run research on: " + ", ".join(research_keywords))
        
        # Check for conflicting projects
        if self._has_conflicting_projects(prp_data["project_name"]):
            blockers.append("Conflicting project exists")
            suggestions.append("Review existing project or choose different name")
        
        return {
            "ready": len(blockers) == 0,
            "blockers": blockers,
            "suggestions": suggestions
        }
    
    def _determine_required_templates(self, prp_data: Dict) -> List[str]:
        """Determine which templates are required based on PRP analysis"""
        templates = ["base-project"]  # Always need base template
        
        # Add templates based on tech stack
        tech_stack = prp_data["tech_stack"]
        if any(tech in tech_stack for tech in ["Python", "FastAPI", "Django"]):
            templates.append("python-project")
        if any(tech in tech_stack for tech in ["JavaScript", "React", "Node.js"]):
            templates.append("javascript-project")
        if "Docker" in tech_stack:
            templates.append("docker-setup")
        if "API" in prp_data["integrations"]:
            templates.append("api-integration")
            
        # Add templates based on testing requirements
        if prp_data["testing_requirements"]:
            templates.append("testing-framework")
            
        return templates
    
    def _analyze_integration_requirements(self, prp_data: Dict) -> Dict:
        """Analyze and suggest integrations based on PRP content"""
        requirements = {
            "required": [],
            "suggested": [],
            "personas": [],
            "configs": {}
        }
        
        # Direct mentions
        for integration in prp_data["integrations"]:
            if integration.lower() in ["superclaude", "openrouter", "jina"]:
                requirements["required"].append(integration)
                
        # Smart suggestions based on content
        content_lower = prp_data["content"].lower()
        
        if "ai" in content_lower or "llm" in content_lower:
            requirements["suggested"].append("OpenRouter")
            
        if "scraping" in content_lower or "web data" in content_lower:
            requirements["suggested"].append("Jina")
            
        if "database" in content_lower or "storage" in content_lower:
            requirements["suggested"].append("Supabase")
            
        # SuperClaude persona suggestions
        if "architecture" in content_lower:
            requirements["personas"].append("--persona-architect")
        if "security" in content_lower:
            requirements["personas"].append("--persona-security")
        if "testing" in content_lower:
            requirements["personas"].append("--persona-tester")
            
        return requirements
    
    def _compose_templates(self, prp_data: Dict, integration_requirements: Dict) -> Dict:
        """Compose modular templates based on project requirements"""
        components = {
            "base": [],
            "integrations": [],
            "testing": [],
            "ci_cd": [],
            "custom": []
        }
        
        # Base components
        components["base"].append("init.md")
        components["base"].append("README.md")
        components["base"].append("project-structure.md")
        
        # Integration components
        for integration in integration_requirements["required"]:
            components["integrations"].append(f"{integration.lower()}-setup.md")
            
        # Testing components
        if prp_data["testing_requirements"]:
            components["testing"].append("test-framework.md")
            if "unit" in prp_data["testing_requirements"]:
                components["testing"].append("unit-tests.md")
            if "integration" in prp_data["testing_requirements"]:
                components["testing"].append("integration-tests.md")
        
        # CI/CD components
        if prp_data["complexity"] in ["complex", "enterprise"]:
            components["ci_cd"].append("github-actions.md")
            components["ci_cd"].append("deployment.md")
            
        return components
    
    def _create_project_structure(self, project_path: Path, template_components: Dict):
        """Create project directory structure with template components"""
        # Create base directories
        directories = [
            "src", "tests", "docs", "config", "scripts", "research", "templates-used"
        ]
        
        for directory in directories:
            (project_path / directory).mkdir(parents=True, exist_ok=True)
            
        # Copy and compose template components
        for category, components in template_components.items():
            for component in components:
                self._copy_template_component(project_path, category, component)
    
    def _copy_template_component(self, project_path: Path, category: str, component: str):
        """Copy individual template component to project"""
        # For now, create placeholder files - in real implementation, these would be actual templates
        component_path = project_path / "templates-used" / f"{category}-{component}"
        component_path.write_text(f"# {category.title()} Component: {component}\n\nTemplate component for {component}")
    
    def _generate_project_metadata(self, prp_data: Dict, prp_file: str, 
                                 integration_requirements: Dict, template_components: Dict) -> Dict:
        """Generate comprehensive project.json metadata"""
        return {
            "project_name": prp_data["project_name"],
            "created_date": datetime.now().isoformat(),
            "prp_link": f"PRPs/{prp_file}",
            "current_phase": "scaffolded",
            "phases": {
                "scaffolded": {"completed": True, "date": datetime.now().isoformat()},
                "in_progress": {"completed": False, "date": None},
                "testing": {"completed": False, "date": None},
                "completed": {"completed": False, "date": None},
                "archived": {"completed": False, "date": None}
            },
            "blockers": [],
            "next_steps": [
                "Review generated project structure",
                "Set up development environment",
                "Begin implementation following PRP"
            ],
            "tech_stack": prp_data["tech_stack"],
            "complexity": prp_data["complexity"],
            "integration_requirements": integration_requirements,
            "template_components": template_components,
            "testing_requirements": prp_data["testing_requirements"],
            "research_keywords": self._extract_research_keywords(prp_data),
            "dashboard_tracking": {
                "progress_percentage": 10,  # Scaffolded = 10%
                "last_updated": datetime.now().isoformat(),
                "sync_status": "in_sync"
            }
        }
    
    def _setup_monitoring(self, project_path: Path, project_metadata: Dict):
        """Set up monitoring and contradiction checking"""
        # Create monitoring config
        monitoring_config = {
            "enabled": True,
            "check_interval": "1h",
            "dashboard_sync": True,
            "contradiction_check": True,
            "log_status_triggers": ["phase_change", "blocker_added", "completion"]
        }
        
        (project_path / "config" / "monitoring.json").write_text(
            json.dumps(monitoring_config, indent=2)
        )
        
        # Create project.json
        (project_path / "project.json").write_text(
            json.dumps(project_metadata, indent=2)
        )
    
    def _integrate_research(self, project_path: Path, prp_data: Dict):
        """Pull relevant research into project research folder"""
        research_keywords = self._extract_research_keywords(prp_data)
        
        # Create research integration
        research_integration = {
            "keywords": research_keywords,
            "auto_pulled": True,
            "last_updated": datetime.now().isoformat(),
            "relevant_files": []
        }
        
        # In real implementation, this would pull from research/ folder
        (project_path / "research" / "research-integration.json").write_text(
            json.dumps(research_integration, indent=2)
        )
    
    def _extract_research_keywords(self, prp_data: Dict) -> List[str]:
        """Extract research keywords from PRP for research integration"""
        keywords = []
        
        # Add tech stack as keywords
        keywords.extend(prp_data["tech_stack"])
        
        # Add integration keywords
        keywords.extend(prp_data["integrations"])
        
        # Extract from content
        content_lower = prp_data["content"].lower()
        research_patterns = [
            r"research\s+(\w+)", r"documentation\s+for\s+(\w+)", 
            r"learn\s+about\s+(\w+)", r"study\s+(\w+)"
        ]
        
        for pattern in research_patterns:
            matches = re.findall(pattern, content_lower)
            keywords.extend(matches)
            
        return list(set(keywords))  # Remove duplicates
    
    def _has_sufficient_research(self, keywords: List[str]) -> bool:
        """Check if sufficient research exists for keywords"""
        # In real implementation, this would check research/ folder
        return True  # Placeholder
    
    def _has_conflicting_projects(self, project_name: str) -> bool:
        """Check for conflicting projects"""
        project_path = self.projects_path / project_name
        return project_path.exists()
    
    def _log_scaffolding_event(self, project_name: str, prp_file: str, metadata: Dict):
        """Log scaffolding event to brain logs"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "project_scaffolded",
            "project_name": project_name,
            "prp_file": prp_file,
            "complexity": metadata["complexity"],
            "tech_stack": metadata["tech_stack"],
            "integration_requirements": metadata["integration_requirements"],
            "success": True
        }
        
        # In real implementation, this would append to brain/logs/interactions.log
        print(f"✅ Project scaffolded: {project_name}")
        print(f"📋 Metadata: {json.dumps(log_entry, indent=2)}")

def main():
    """Main function for CLI usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python prp-scaffold.py <prp-file> [--force]")
        sys.exit(1)
        
    prp_file = sys.argv[1]
    force_override = "--force" in sys.argv
    
    scaffolder = PRPScaffolder()
    result = scaffolder.scaffold_from_prp(prp_file, force_override)
    
    if result.get("success"):
        print(f"✅ Successfully scaffolded project: {result['project_name']}")
        print(f"📂 Project location: {result['project_path']}")
    else:
        print(f"❌ Scaffolding failed: {result.get('error', 'Unknown error')}")
        if "blockers" in result:
            print("🚧 Blockers:")
            for blocker in result["blockers"]:
                print(f"   - {blocker}")
        if "suggestions" in result:
            print("💡 Suggestions:")
            for suggestion in result["suggestions"]:
                print(f"   - {suggestion}")

if __name__ == "__main__":
    main()