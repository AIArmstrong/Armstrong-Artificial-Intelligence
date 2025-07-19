#!/usr/bin/env python3
"""
Seamless Orchestrator - Idea to Implementation Pipeline
The ultimate goal: idea -> evaluate -> actionize (PRP) -> implement (MCP tools, new projects, etc.)
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict

# Import our custom modules
from brain.modules.unified_analytics import UnifiedAnalytics
from brain.modules.research_prp_integration import ResearchPRPIntegration
from brain.modules.integration_aware_prp_enhancer import IntegrationAwarePRPEnhancer

@dataclass
class IdeaEvaluation:
    """Evaluation results for an idea"""
    idea_id: str
    feasibility_score: float
    complexity_assessment: str
    estimated_effort: str
    success_probability: float
    recommended_approach: str
    blockers: List[str]
    prerequisites: List[str]

@dataclass
class PRPGenerationResult:
    """Results of PRP generation from idea"""
    prp_file: str
    integration_recommendations: List[str]
    research_integration: Dict
    template_suggestions: List[str]
    success_prediction: float

@dataclass
class ImplementationResult:
    """Results of implementation process"""
    project_id: str
    project_path: str
    scaffolding_success: bool
    integration_setup: Dict
    monitoring_enabled: bool
    next_steps: List[str]

class SeamlessOrchestrator:
    """Orchestrates the complete idea-to-implementation pipeline"""
    
    def __init__(self, base_path: str = "/mnt/c/Users/Brandon/AAI"):
        self.base_path = Path(base_path)
        self.ideas_path = self.base_path / "ideas"
        self.prps_path = self.base_path / "PRPs"
        self.projects_path = self.base_path / "projects"
        self.brain_path = self.base_path / "brain"
        
        # Initialize subsystems
        self.analytics = UnifiedAnalytics(str(self.base_path))
        self.research_integration = ResearchPRPIntegration(str(self.base_path))
        self.prp_enhancer = IntegrationAwarePRPEnhancer(str(self.base_path))
        
        # Ensure ideas directory exists
        self.ideas_path.mkdir(exist_ok=True)
        
        # Pipeline state tracking
        self.pipeline_state = self._load_pipeline_state()
    
    def _load_pipeline_state(self) -> Dict:
        """Load pipeline state from file"""
        state_file = self.brain_path / "pipeline_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {"active_pipelines": [], "completed_pipelines": []}
    
    def _save_pipeline_state(self):
        """Save pipeline state to file"""
        state_file = self.brain_path / "pipeline_state.json"
        with open(state_file, 'w') as f:
            json.dump(self.pipeline_state, f, indent=2)
    
    def process_idea(self, idea_text: str, context: Optional[Dict] = None) -> Dict:
        """
        Complete idea-to-implementation pipeline
        
        Flow:
        1. Capture and structure idea
        2. Evaluate feasibility and complexity
        3. Generate enhanced PRP with integrations
        4. Scaffold project with research integration
        5. Set up monitoring and contradiction checks
        6. Return actionable next steps
        """
        pipeline_id = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # 1. Capture and structure idea
            idea_capture = self._capture_idea(idea_text, context or {})
            
            # 2. Evaluate feasibility
            evaluation = self._evaluate_idea(idea_capture)
            
            # 3. Generate PRP if feasible
            if evaluation.feasibility_score >= 0.6:
                prp_result = self._generate_prp_from_idea(idea_capture, evaluation)
                
                # 4. Scaffold project
                implementation_result = self._scaffold_project_from_prp(
                    prp_result.prp_file, prp_result
                )
                
                # 5. Set up monitoring
                self._setup_pipeline_monitoring(pipeline_id, implementation_result)
                
                # 6. Track success
                self._track_pipeline_success(pipeline_id, {
                    "idea_capture": idea_capture,
                    "evaluation": evaluation,
                    "prp_result": prp_result,
                    "implementation": implementation_result
                })
                
                return {
                    "success": True,
                    "pipeline_id": pipeline_id,
                    "idea_capture": idea_capture,
                    "evaluation": asdict(evaluation),
                    "prp_result": asdict(prp_result),
                    "implementation": asdict(implementation_result),
                    "next_steps": self._generate_next_steps(implementation_result)
                }
            else:
                return {
                    "success": False,
                    "pipeline_id": pipeline_id,
                    "idea_capture": idea_capture,
                    "evaluation": asdict(evaluation),
                    "reason": "Idea feasibility too low for implementation",
                    "suggestions": self._generate_improvement_suggestions(evaluation)
                }
                
        except Exception as e:
            return {
                "success": False,
                "pipeline_id": pipeline_id,
                "error": str(e),
                "stage": "pipeline_execution"
            }
    
    def _capture_idea(self, idea_text: str, context: Dict) -> Dict:
        """Capture and structure idea with metadata"""
        idea_id = f"idea_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Extract key components from idea text
        extracted_components = self._extract_idea_components(idea_text)
        
        idea_capture = {
            "id": idea_id,
            "timestamp": datetime.now().isoformat(),
            "original_text": idea_text,
            "context": context,
            "components": extracted_components,
            "classification": self._classify_idea(idea_text),
            "keywords": self._extract_idea_keywords(idea_text)
        }
        
        # Save idea to ideas registry
        self._save_idea_to_registry(idea_capture)
        
        return idea_capture
    
    def _extract_idea_components(self, idea_text: str) -> Dict:
        """Extract key components from idea text"""
        # Simple extraction - in real implementation, use more sophisticated NLP
        components = {
            "problem_statement": "",
            "proposed_solution": "",
            "target_users": [],
            "key_features": [],
            "technical_requirements": [],
            "constraints": []
        }
        
        # Look for problem indicators
        problem_indicators = ["problem", "issue", "challenge", "need", "pain"]
        if any(indicator in idea_text.lower() for indicator in problem_indicators):
            components["problem_statement"] = idea_text[:200] + "..."
        
        # Look for solution indicators
        solution_indicators = ["solution", "approach", "method", "implement", "build"]
        if any(indicator in idea_text.lower() for indicator in solution_indicators):
            components["proposed_solution"] = idea_text[:200] + "..."
        
        # Extract technical terms
        tech_terms = ["API", "database", "frontend", "backend", "microservice", "AI", "ML"]
        components["technical_requirements"] = [
            term for term in tech_terms if term.lower() in idea_text.lower()
        ]
        
        return components
    
    def _classify_idea(self, idea_text: str) -> str:
        """Classify idea type"""
        text_lower = idea_text.lower()
        
        # Classification patterns
        if any(word in text_lower for word in ["feature", "enhance", "improve", "add"]):
            return "feature_enhancement"
        elif any(word in text_lower for word in ["fix", "bug", "error", "issue"]):
            return "bug_fix"
        elif any(word in text_lower for word in ["new", "create", "build", "develop"]):
            return "new_project"
        elif any(word in text_lower for word in ["optimize", "performance", "speed"]):
            return "optimization"
        elif any(word in text_lower for word in ["integrate", "connect", "sync"]):
            return "integration"
        else:
            return "general"
    
    def _extract_idea_keywords(self, idea_text: str) -> List[str]:
        """Extract keywords from idea text"""
        # Simple keyword extraction
        import re
        words = re.findall(r'\\b[a-zA-Z]{3,}\\b', idea_text.lower())
        
        # Filter out common words
        common_words = {"the", "and", "for", "are", "but", "not", "you", "all", "can", "had", "her", "was", "one", "our", "out", "day", "get", "has", "him", "his", "how", "man", "new", "now", "old", "see", "two", "way", "who", "boy", "did", "its", "let", "put", "say", "she", "too", "use"}
        
        keywords = [word for word in set(words) if word not in common_words and len(word) > 3]
        return keywords[:10]  # Top 10 keywords
    
    def _save_idea_to_registry(self, idea_capture: Dict):
        """Save idea to ideas registry"""
        registry_file = self.ideas_path / "idea_registry.json"
        
        # Load existing registry
        registry = {"ideas": []}
        if registry_file.exists():
            try:
                with open(registry_file, 'r') as f:
                    registry = json.load(f)
            except:
                pass
        
        # Add new idea
        registry["ideas"].append(idea_capture)
        
        # Save updated registry
        with open(registry_file, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def _evaluate_idea(self, idea_capture: Dict) -> IdeaEvaluation:
        """Evaluate idea feasibility and complexity"""
        idea_text = idea_capture["original_text"]
        components = idea_capture["components"]
        
        # Feasibility assessment
        feasibility_score = self._calculate_feasibility_score(idea_text, components)
        
        # Complexity assessment
        complexity = self._assess_complexity(idea_text, components)
        
        # Effort estimation
        effort = self._estimate_effort(complexity, components)
        
        # Success probability
        success_probability = self._calculate_success_probability(
            feasibility_score, complexity, components
        )
        
        # Recommended approach
        recommended_approach = self._recommend_approach(
            feasibility_score, complexity, components
        )
        
        # Identify blockers
        blockers = self._identify_blockers(components)
        
        # Prerequisites
        prerequisites = self._identify_prerequisites(components)
        
        return IdeaEvaluation(
            idea_id=idea_capture["id"],
            feasibility_score=feasibility_score,
            complexity_assessment=complexity,
            estimated_effort=effort,
            success_probability=success_probability,
            recommended_approach=recommended_approach,
            blockers=blockers,
            prerequisites=prerequisites
        )
    
    def _calculate_feasibility_score(self, idea_text: str, components: Dict) -> float:
        """Calculate feasibility score (0.0 to 1.0)"""
        score = 0.5  # Base score
        
        # Boost for clear problem statement
        if components.get("problem_statement"):
            score += 0.2
        
        # Boost for proposed solution
        if components.get("proposed_solution"):
            score += 0.2
        
        # Boost for technical requirements
        if components.get("technical_requirements"):
            score += 0.1
        
        # Penalty for vague language
        vague_indicators = ["maybe", "might", "could", "possibly", "perhaps"]
        if any(indicator in idea_text.lower() for indicator in vague_indicators):
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _assess_complexity(self, idea_text: str, components: Dict) -> str:
        """Assess project complexity"""
        complexity_score = 0
        
        # Technical complexity
        tech_count = len(components.get("technical_requirements", []))
        if tech_count > 5:
            complexity_score += 3
        elif tech_count > 2:
            complexity_score += 2
        elif tech_count > 0:
            complexity_score += 1
        
        # Text-based complexity indicators
        complex_indicators = ["microservice", "distributed", "scalable", "enterprise", "integration"]
        complexity_score += sum(1 for indicator in complex_indicators if indicator in idea_text.lower())
        
        # Length-based complexity
        if len(idea_text) > 1000:
            complexity_score += 2
        elif len(idea_text) > 500:
            complexity_score += 1
        
        # Map score to complexity level
        if complexity_score >= 6:
            return "enterprise"
        elif complexity_score >= 4:
            return "complex"
        elif complexity_score >= 2:
            return "moderate"
        else:
            return "simple"
    
    def _estimate_effort(self, complexity: str, components: Dict) -> str:
        """Estimate effort required"""
        effort_mapping = {
            "simple": "1-2 days",
            "moderate": "1-2 weeks",
            "complex": "1-2 months",
            "enterprise": "3-6 months"
        }
        
        return effort_mapping.get(complexity, "unknown")
    
    def _calculate_success_probability(self, feasibility: float, complexity: str, components: Dict) -> float:
        """Calculate success probability"""
        base_probability = feasibility
        
        # Adjust based on complexity
        complexity_penalty = {
            "simple": 0.0,
            "moderate": 0.1,
            "complex": 0.2,
            "enterprise": 0.3
        }
        
        adjusted_probability = base_probability - complexity_penalty.get(complexity, 0.2)
        
        # Boost for well-defined requirements
        if len(components.get("technical_requirements", [])) > 2:
            adjusted_probability += 0.1
        
        return max(0.0, min(1.0, adjusted_probability))
    
    def _recommend_approach(self, feasibility: float, complexity: str, components: Dict) -> str:
        """Recommend implementation approach"""
        if feasibility < 0.4:
            return "Research and refine idea before implementation"
        elif complexity == "simple":
            return "Direct implementation with basic scaffolding"
        elif complexity == "moderate":
            return "PRP-driven implementation with template composition"
        elif complexity == "complex":
            return "Phased implementation with MVP approach"
        else:
            return "Comprehensive planning with risk assessment"
    
    def _identify_blockers(self, components: Dict) -> List[str]:
        """Identify potential blockers"""
        blockers = []
        
        # Technical blockers
        if not components.get("technical_requirements"):
            blockers.append("Unclear technical requirements")
        
        if not components.get("problem_statement"):
            blockers.append("Unclear problem definition")
        
        # Complexity blockers
        if len(components.get("technical_requirements", [])) > 5:
            blockers.append("High technical complexity")
        
        return blockers
    
    def _identify_prerequisites(self, components: Dict) -> List[str]:
        """Identify prerequisites"""
        prerequisites = []
        
        # Based on technical requirements
        tech_reqs = components.get("technical_requirements", [])
        if "API" in tech_reqs:
            prerequisites.append("API design and documentation")
        if "database" in tech_reqs:
            prerequisites.append("Database schema design")
        if "frontend" in tech_reqs:
            prerequisites.append("UI/UX design")
        
        return prerequisites
    
    def _generate_prp_from_idea(self, idea_capture: Dict, evaluation: IdeaEvaluation) -> PRPGenerationResult:
        """Generate enhanced PRP from idea"""
        # Create PRP content
        prp_content = self._create_prp_content(idea_capture, evaluation)
        
        # Save PRP file
        prp_filename = f"{idea_capture['id']}_generated_prp.md"
        prp_path = self.prps_path / prp_filename
        
        with open(prp_path, 'w') as f:
            f.write(prp_content)
        
        # Enhance PRP with integrations
        enhancement_result = self.prp_enhancer.enhance_prp(prp_filename)
        
        # Integrate research
        research_matches = self.research_integration.find_relevant_research(
            prp_content, idea_capture.get("keywords", []), {}
        )
        
        research_integration_result = self.research_integration.integrate_research_into_prp(
            prp_filename, research_matches
        )
        
        # Get template suggestions
        template_suggestions = self.analytics.get_template_recommendations(
            prp_content, idea_capture.get("keywords", [])
        )
        
        return PRPGenerationResult(
            prp_file=prp_filename,
            integration_recommendations=enhancement_result.get("recommendations", {}).get("integrations", []),
            research_integration=research_integration_result,
            template_suggestions=template_suggestions,
            success_prediction=evaluation.success_probability
        )
    
    def _create_prp_content(self, idea_capture: Dict, evaluation: IdeaEvaluation) -> str:
        """Create PRP content from idea and evaluation"""
        content = f"""# PRP: {idea_capture['id']}

*Auto-generated from idea: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Overview

**Original Idea**: {idea_capture['original_text']}

**Problem Statement**: {idea_capture['components'].get('problem_statement', 'To be defined')}

**Proposed Solution**: {idea_capture['components'].get('proposed_solution', 'To be defined')}

## Project Assessment

- **Feasibility Score**: {evaluation.feasibility_score:.1%}
- **Complexity**: {evaluation.complexity_assessment}
- **Estimated Effort**: {evaluation.estimated_effort}
- **Success Probability**: {evaluation.success_probability:.1%}
- **Recommended Approach**: {evaluation.recommended_approach}

## Requirements

### Technical Requirements
{chr(10).join(f"- {req}" for req in idea_capture['components'].get('technical_requirements', ['To be defined']))}

### Key Features
{chr(10).join(f"- {feature}" for feature in idea_capture['components'].get('key_features', ['To be defined']))}

## Implementation Plan

### Phase 1: Foundation
- Set up project structure
- Implement core functionality
- Basic testing framework

### Phase 2: Enhancement
- Add advanced features
- Integration setup
- Performance optimization

### Phase 3: Deployment
- Production preparation
- Monitoring setup
- Documentation completion

## Potential Blockers

{chr(10).join(f"- {blocker}" for blocker in evaluation.blockers)}

## Prerequisites

{chr(10).join(f"- {prereq}" for prereq in evaluation.prerequisites)}

## Success Criteria

- [ ] Core functionality implemented
- [ ] Integration tests passing
- [ ] Performance benchmarks met
- [ ] Documentation complete
- [ ] Production deployment successful

## Notes

- Generated from idea classification: {idea_capture['classification']}
- Keywords: {', '.join(idea_capture['keywords'])}
- Context: {idea_capture['context']}

---
*Auto-generated PRP from Seamless Orchestrator*
"""
        
        return content
    
    def _scaffold_project_from_prp(self, prp_file: str, prp_result: PRPGenerationResult) -> ImplementationResult:
        """Scaffold project from PRP using our automation"""
        # Import our scaffolding module
        from brain.modules.prp_scaffold import PRPScaffolder
        
        scaffolder = PRPScaffolder(str(self.base_path))
        scaffolding_result = scaffolder.scaffold_from_prp(prp_file)
        
        if scaffolding_result.get("success"):
            project_id = scaffolding_result["project_name"]
            project_path = scaffolding_result["project_path"]
            
            # Set up integrations
            integration_setup = self._setup_integrations(
                project_path, prp_result.integration_recommendations
            )
            
            # Enable monitoring
            monitoring_success = self._enable_project_monitoring(project_path)
            
            # Track in analytics
            self.analytics.track_prp_to_project(
                prp_file, project_id,
                prp_result.template_suggestions,
                [integ["integration"] for integ in prp_result.integration_recommendations],
                "scaffolded"
            )
            
            return ImplementationResult(
                project_id=project_id,
                project_path=project_path,
                scaffolding_success=True,
                integration_setup=integration_setup,
                monitoring_enabled=monitoring_success,
                next_steps=self._generate_implementation_next_steps(scaffolding_result)
            )
        else:
            return ImplementationResult(
                project_id="",
                project_path="",
                scaffolding_success=False,
                integration_setup={},
                monitoring_enabled=False,
                next_steps=[f"Fix scaffolding issues: {scaffolding_result.get('error', 'Unknown error')}"]
            )
    
    def _setup_integrations(self, project_path: str, integration_recommendations: List[Dict]) -> Dict:
        """Set up recommended integrations"""
        setup_results = {}
        
        for integration in integration_recommendations:
            integration_name = integration.get("integration", "")
            try:
                # Create integration setup placeholder
                setup_results[integration_name] = {
                    "status": "configured",
                    "confidence": integration.get("confidence", 0.0),
                    "setup_files": [f"config/{integration_name}-config.json"]
                }
            except Exception as e:
                setup_results[integration_name] = {
                    "status": "failed",
                    "error": str(e)
                }
        
        return setup_results
    
    def _enable_project_monitoring(self, project_path: str) -> bool:
        """Enable project monitoring"""
        try:
            # Create monitoring configuration
            monitoring_config = {
                "enabled": True,
                "check_interval": "1h",
                "dashboard_sync": True,
                "contradiction_check": True
            }
            
            monitoring_file = Path(project_path) / "config" / "monitoring.json"
            monitoring_file.parent.mkdir(exist_ok=True)
            
            with open(monitoring_file, 'w') as f:
                json.dump(monitoring_config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Warning: Could not enable monitoring: {e}")
            return False
    
    def _generate_implementation_next_steps(self, scaffolding_result: Dict) -> List[str]:
        """Generate next steps for implementation"""
        return [
            f"Review project structure at {scaffolding_result['project_path']}",
            "Set up development environment",
            "Begin implementation following PRP specification",
            "Run /log status to sync with dashboard",
            "Set up CI/CD pipeline if needed",
            "Begin testing framework setup"
        ]
    
    def _setup_pipeline_monitoring(self, pipeline_id: str, implementation_result: ImplementationResult):
        """Set up monitoring for the entire pipeline"""
        self.pipeline_state["active_pipelines"].append({
            "pipeline_id": pipeline_id,
            "project_id": implementation_result.project_id,
            "project_path": implementation_result.project_path,
            "created_date": datetime.now().isoformat(),
            "status": "active",
            "monitoring_enabled": implementation_result.monitoring_enabled
        })
        
        self._save_pipeline_state()
    
    def _track_pipeline_success(self, pipeline_id: str, pipeline_data: Dict):
        """Track pipeline success metrics"""
        success_metrics = {
            "pipeline_id": pipeline_id,
            "feasibility_score": pipeline_data["evaluation"]["feasibility_score"],
            "complexity": pipeline_data["evaluation"]["complexity_assessment"],
            "scaffolding_success": pipeline_data["implementation"]["scaffolding_success"],
            "integration_count": len(pipeline_data["prp_result"]["integration_recommendations"]),
            "template_count": len(pipeline_data["prp_result"]["template_suggestions"]),
            "timestamp": datetime.now().isoformat()
        }
        
        # Save to analytics
        success_file = self.brain_path / "pipeline_success_metrics.json"
        
        metrics_data = {"pipelines": []}
        if success_file.exists():
            try:
                with open(success_file, 'r') as f:
                    metrics_data = json.load(f)
            except:
                pass
        
        metrics_data["pipelines"].append(success_metrics)
        
        with open(success_file, 'w') as f:
            json.dump(metrics_data, f, indent=2)
    
    def _generate_next_steps(self, implementation_result: ImplementationResult) -> List[str]:
        """Generate actionable next steps"""
        if implementation_result.scaffolding_success:
            return [
                f"📁 Navigate to project: {implementation_result.project_path}",
                "🔧 Set up development environment",
                "📋 Review PRP requirements and implementation plan",
                "⚙️ Configure integrations as needed",
                "🧪 Set up testing framework",
                "📊 Run /log status to sync with dashboard",
                "🚀 Begin implementation phase"
            ]
        else:
            return [
                "🔍 Review scaffolding errors",
                "📋 Refine PRP requirements",
                "🔧 Address identified blockers",
                "🔄 Retry scaffolding process"
            ]
    
    def _generate_improvement_suggestions(self, evaluation: IdeaEvaluation) -> List[str]:
        """Generate improvement suggestions for low-feasibility ideas"""
        suggestions = []
        
        if evaluation.feasibility_score < 0.4:
            suggestions.append("Clarify problem statement and requirements")
        
        if not evaluation.prerequisites:
            suggestions.append("Define technical prerequisites and dependencies")
        
        if evaluation.complexity_assessment == "enterprise":
            suggestions.append("Consider breaking down into smaller, manageable phases")
        
        suggestions.extend([
            "Gather more specific requirements",
            "Research similar existing solutions",
            "Validate problem with potential users",
            "Create proof of concept first"
        ])
        
        return suggestions

def main():
    """Main function for CLI usage"""
    import sys
    
    orchestrator = SeamlessOrchestrator()
    
    if len(sys.argv) < 2:
        print("Usage: python seamless-orchestrator.py \"<idea-text>\" [context.json]")
        print("Example: python seamless-orchestrator.py \"Build a task management system with AI integration\"")
        sys.exit(1)
    
    idea_text = sys.argv[1]
    context = {}
    
    if len(sys.argv) > 2:
        try:
            with open(sys.argv[2], 'r') as f:
                context = json.load(f)
        except:
            print("Warning: Could not load context file")
    
    print(f"🚀 Processing idea: {idea_text}")
    print("=" * 60)
    
    result = orchestrator.process_idea(idea_text, context)
    
    if result["success"]:
        print(f"✅ Pipeline successful! ID: {result['pipeline_id']}")
        print(f"📊 Feasibility: {result['evaluation']['feasibility_score']:.1%}")
        print(f"🎯 Complexity: {result['evaluation']['complexity_assessment']}")
        print(f"📋 PRP Generated: {result['prp_result']['prp_file']}")
        print(f"📁 Project Created: {result['implementation']['project_id']}")
        print(f"🔗 Integrations: {len(result['prp_result']['integration_recommendations'])}")
        
        print("\\n📝 Next Steps:")
        for i, step in enumerate(result['next_steps'], 1):
            print(f"  {i}. {step}")
    else:
        print(f"❌ Pipeline failed: {result.get('reason', 'Unknown error')}")
        if result.get('suggestions'):
            print("\\n💡 Suggestions:")
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"  {i}. {suggestion}")

if __name__ == "__main__":
    main()