#!/usr/bin/env python3
"""
Integration-Aware PRP Enhancement System
Automatically enhances PRPs with integration recommendations, persona suggestions, and smart annotations.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
import yaml

class IntegrationAwarePRPEnhancer:
    """Enhances PRPs with intelligent integration recommendations and persona suggestions"""
    
    def __init__(self, base_path: str = "/mnt/c/Users/Brandon/AAI"):
        self.base_path = Path(base_path)
        self.prps_path = self.base_path / "PRPs"
        self.integrations_path = self.base_path / "integrations"
        self.brain_path = self.base_path / "brain"
        
        # Load integration metadata
        self.integration_metadata = self._load_integration_metadata()
        
        # Load persona mappings
        self.persona_mappings = self._load_persona_mappings()
        
        # Integration detection patterns
        self.integration_patterns = {
            "superclaude": [
                r"ai.{0,20}(assist|help|automat|generat)",
                r"claude.{0,20}(code|develop|implement)",
                r"persona.{0,20}(architect|security|tester)",
                r"multi.{0,20}agent",
                r"intelligent.{0,20}(workflow|process|system)"
            ],
            "openrouter": [
                r"llm.{0,20}(integration|api|call)",
                r"language.{0,20}model",
                r"ai.{0,20}(generation|completion|chat)",
                r"(gpt|claude|anthropic).{0,20}api",
                r"embedding.{0,20}(search|similarity|vector)"
            ],
            "jina": [
                r"web.{0,20}(scrap|crawl|extract)",
                r"content.{0,20}(extraction|parsing|analysis)",
                r"document.{0,20}(processing|analysis|search)",
                r"scraping.{0,20}(api|service|tool)",
                r"data.{0,20}(harvest|collection|mining)"
            ],
            "supabase": [
                r"database.{0,20}(integration|connection|storage)",
                r"real.{0,20}time.{0,20}(data|sync|updates)",
                r"authentication.{0,20}(system|service|api)",
                r"storage.{0,20}(solution|system|service)",
                r"backend.{0,20}(service|api|infrastructure)"
            ]
        }
    
    def _load_integration_metadata(self) -> Dict:
        """Load integration metadata from integrations folder"""
        metadata = {}
        
        for integration_dir in self.integrations_path.iterdir():
            if integration_dir.is_dir():
                metadata_file = integration_dir / "metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata[integration_dir.name] = json.load(f)
                    except Exception as e:
                        print(f"Warning: Could not load metadata for {integration_dir.name}: {e}")
                
                # Load from README if no metadata file
                elif (integration_dir / "README.md").exists():
                    metadata[integration_dir.name] = self._extract_metadata_from_readme(
                        integration_dir / "README.md"
                    )
        
        return metadata
    
    def _load_persona_mappings(self) -> Dict:
        """Load SuperClaude persona mappings"""
        return {
            "architecture": "--persona-architect",
            "security": "--persona-security", 
            "testing": "--persona-tester",
            "data": "--persona-data",
            "performance": "--persona-performance",
            "ui": "--persona-ui",
            "devops": "--persona-devops",
            "research": "--persona-research",
            "integration": "--persona-integration"
        }
    
    def _extract_metadata_from_readme(self, readme_path: Path) -> Dict:
        """Extract basic metadata from README file"""
        try:
            with open(readme_path, 'r') as f:
                content = f.read()
                
            return {
                "description": self._extract_description(content),
                "capabilities": self._extract_capabilities(content),
                "usage_patterns": self._extract_usage_patterns(content)
            }
        except Exception:
            return {}
    
    def _extract_description(self, content: str) -> str:
        """Extract description from README content"""
        # Look for first paragraph after title
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#'):
                return line.strip()
        return ""
    
    def _extract_capabilities(self, content: str) -> List[str]:
        """Extract capabilities from README content"""
        capabilities = []
        
        # Look for capability patterns
        capability_patterns = [
            r"- .{0,50}capabilit",
            r"- .{0,50}feature",
            r"- .{0,50}support",
            r"- .{0,50}enable"
        ]
        
        for pattern in capability_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            capabilities.extend(matches)
        
        return capabilities[:5]  # Limit to top 5
    
    def _extract_usage_patterns(self, content: str) -> List[str]:
        """Extract usage patterns from README content"""
        patterns = []
        
        # Look for usage examples
        usage_section = re.search(r"## Usage.*?(?=\n##|\Z)", content, re.DOTALL | re.IGNORECASE)
        if usage_section:
            # Extract code blocks
            code_blocks = re.findall(r"```[\s\S]*?```", usage_section.group(0))
            patterns.extend(code_blocks[:3])  # Limit to top 3
        
        return patterns
    
    def enhance_prp(self, prp_file: str, output_file: Optional[str] = None) -> Dict:
        """
        Main enhancement function: analyze PRP and add integration recommendations
        
        Returns:
        {
            "original_prp": str,
            "enhanced_prp": str,
            "recommendations": {
                "integrations": List[str],
                "personas": List[str],
                "enhancements": List[str]
            },
            "metadata": Dict
        }
        """
        prp_path = self.prps_path / prp_file
        if not prp_path.exists():
            return {"error": f"PRP file not found: {prp_file}"}
        
        # Read original PRP
        with open(prp_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Analyze PRP content
        analysis = self._analyze_prp_content(original_content)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analysis)
        
        # Enhance PRP content
        enhanced_content = self._enhance_prp_content(original_content, recommendations)
        
        # Save enhanced version if output file specified
        if output_file:
            output_path = self.prps_path / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_content)
        
        return {
            "original_prp": original_content,
            "enhanced_prp": enhanced_content,
            "recommendations": recommendations,
            "metadata": {
                "prp_file": prp_file,
                "analysis": analysis,
                "enhancement_date": datetime.now().isoformat()
            }
        }
    
    def _analyze_prp_content(self, content: str) -> Dict:
        """Analyze PRP content for integration opportunities"""
        analysis = {
            "tech_stack": self._extract_tech_stack(content),
            "complexity": self._assess_complexity(content),
            "domain_areas": self._identify_domain_areas(content),
            "integration_signals": self._detect_integration_signals(content),
            "workflow_patterns": self._identify_workflow_patterns(content)
        }
        
        return analysis
    
    def _extract_tech_stack(self, content: str) -> List[str]:
        """Extract mentioned technologies from PRP"""
        tech_patterns = [
            r"Python", r"JavaScript", r"TypeScript", r"React", r"Node\.js",
            r"FastAPI", r"Django", r"Flask", r"PostgreSQL", r"MongoDB",
            r"Redis", r"Docker", r"Kubernetes", r"AWS", r"Azure", r"GCP",
            r"REST", r"GraphQL", r"WebSocket", r"gRPC"
        ]
        
        tech_stack = []
        for pattern in tech_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                tech_stack.append(pattern.replace(r"\\.", "."))
        
        return tech_stack
    
    def _assess_complexity(self, content: str) -> str:
        """Assess project complexity"""
        complexity_indicators = {
            "simple": ["basic", "simple", "minimal", "quick", "prototype"],
            "moderate": ["moderate", "standard", "typical", "reasonable", "production"],
            "complex": ["complex", "advanced", "sophisticated", "comprehensive", "enterprise"],
            "enterprise": ["enterprise", "large-scale", "distributed", "microservice", "scalable"]
        }
        
        content_lower = content.lower()
        scores = {}
        
        for level, indicators in complexity_indicators.items():
            scores[level] = sum(1 for indicator in indicators if indicator in content_lower)
        
        # Additional complexity factors
        if len(content) > 5000:
            scores["complex"] += 1
        if len(content) > 10000:
            scores["enterprise"] += 1
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _identify_domain_areas(self, content: str) -> List[str]:
        """Identify project domain areas"""
        domain_patterns = {
            "architecture": r"(architect|design|structure|pattern|framework)",
            "security": r"(security|auth|encrypt|protect|vulnerability)",
            "testing": r"(test|qa|quality|validation|verification)",
            "data": r"(data|database|storage|analytics|pipeline)",
            "ui": r"(ui|user interface|frontend|react|vue|angular)",
            "api": r"(api|rest|graphql|endpoint|service)",
            "devops": r"(devops|deploy|ci/cd|docker|kubernetes|pipeline)",
            "performance": r"(performance|optimize|scale|cache|load)",
            "integration": r"(integration|connect|sync|webhook|api)"
        }
        
        identified_domains = []
        content_lower = content.lower()
        
        for domain, pattern in domain_patterns.items():
            if re.search(pattern, content_lower):
                identified_domains.append(domain)
        
        return identified_domains
    
    def _detect_integration_signals(self, content: str) -> Dict:
        """Detect signals for specific integrations"""
        detected_signals = {}
        content_lower = content.lower()
        
        for integration, patterns in self.integration_patterns.items():
            matches = []
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    matches.append(pattern)
            
            if matches:
                detected_signals[integration] = {
                    "confidence": len(matches) / len(patterns),
                    "matched_patterns": matches
                }
        
        return detected_signals
    
    def _identify_workflow_patterns(self, content: str) -> List[str]:
        """Identify workflow patterns that suggest specific integrations"""
        workflow_patterns = {
            "data_pipeline": r"(extract|transform|load|pipeline|etl)",
            "ai_workflow": r"(ai|ml|model|generate|process|analyze)",
            "automation": r"(automat|trigger|schedule|batch|process)",
            "real_time": r"(real.{0,5}time|streaming|live|instant)",
            "collaboration": r"(collaborat|team|multi.{0,5}user|shared)"
        }
        
        identified_patterns = []
        content_lower = content.lower()
        
        for pattern_name, pattern in workflow_patterns.items():
            if re.search(pattern, content_lower):
                identified_patterns.append(pattern_name)
        
        return identified_patterns
    
    def _generate_recommendations(self, analysis: Dict) -> Dict:
        """Generate integration and persona recommendations"""
        recommendations = {
            "integrations": [],
            "personas": [],
            "enhancements": []
        }
        
        # Integration recommendations based on signals
        for integration, signal_data in analysis["integration_signals"].items():
            if signal_data["confidence"] >= 0.3:  # 30% confidence threshold
                recommendations["integrations"].append({
                    "integration": integration,
                    "confidence": signal_data["confidence"],
                    "reason": f"Detected {len(signal_data['matched_patterns'])} relevant patterns",
                    "setup_priority": "high" if signal_data["confidence"] >= 0.6 else "medium"
                })
        
        # Persona recommendations based on domain areas
        for domain in analysis["domain_areas"]:
            if domain in self.persona_mappings:
                persona = self.persona_mappings[domain]
                recommendations["personas"].append({
                    "persona": persona,
                    "domain": domain,
                    "usage_suggestion": f"Use {persona} for {domain}-related tasks"
                })
        
        # Enhancement suggestions based on complexity and workflow
        complexity = analysis["complexity"]
        if complexity in ["complex", "enterprise"]:
            recommendations["enhancements"].append(
                "Consider implementing comprehensive monitoring and analytics"
            )
            recommendations["enhancements"].append(
                "Add automated testing and CI/CD pipeline"
            )
        
        if "real_time" in analysis["workflow_patterns"]:
            recommendations["enhancements"].append(
                "Implement real-time monitoring and alerting"
            )
        
        if "ai_workflow" in analysis["workflow_patterns"]:
            recommendations["enhancements"].append(
                "Add AI model versioning and experiment tracking"
            )
        
        return recommendations
    
    def _enhance_prp_content(self, original_content: str, recommendations: Dict) -> str:
        """Enhance PRP content with integration recommendations"""
        enhanced_content = original_content
        
        # Add integration recommendations section
        if recommendations["integrations"]:
            integration_section = self._generate_integration_section(recommendations["integrations"])
            enhanced_content += f"\n\n{integration_section}"
        
        # Add persona recommendations section
        if recommendations["personas"]:
            persona_section = self._generate_persona_section(recommendations["personas"])
            enhanced_content += f"\n\n{persona_section}"
        
        # Add enhancement suggestions
        if recommendations["enhancements"]:
            enhancement_section = self._generate_enhancement_section(recommendations["enhancements"])
            enhanced_content += f"\n\n{enhancement_section}"
        
        # Add metadata footer
        metadata_footer = self._generate_metadata_footer(recommendations)
        enhanced_content += f"\n\n{metadata_footer}"
        
        return enhanced_content
    
    def _generate_integration_section(self, integrations: List[Dict]) -> str:
        """Generate integration recommendations section"""
        section = "## 🔗 Recommended Integrations\n\n"
        section += "*Auto-generated based on PRP analysis*\n\n"
        
        for integration in integrations:
            section += f"### {integration['integration'].title()}\n"
            section += f"- **Confidence**: {integration['confidence']:.1%}\n"
            section += f"- **Priority**: {integration['setup_priority']}\n"
            section += f"- **Reason**: {integration['reason']}\n"
            
            # Add integration-specific setup hints
            if integration['integration'] == 'superclaude':
                section += "- **Setup**: Add SuperClaude bridge module to project\n"
                section += "- **Usage**: Use personas for specialized tasks\n"
            elif integration['integration'] == 'jina':
                section += "- **Setup**: Configure Jina Reader API for content extraction\n"
                section += "- **Usage**: Implement web scraping workflows\n"
            elif integration['integration'] == 'supabase':
                section += "- **Setup**: Set up Supabase project and authentication\n"
                section += "- **Usage**: Use for real-time data and user management\n"
            
            section += "\n"
        
        return section
    
    def _generate_persona_section(self, personas: List[Dict]) -> str:
        """Generate persona recommendations section"""
        section = "## 👥 Recommended SuperClaude Personas\n\n"
        section += "*Personas suggested based on project domain areas*\n\n"
        
        for persona in personas:
            section += f"### {persona['persona']}\n"
            section += f"- **Domain**: {persona['domain']}\n"
            section += f"- **Usage**: {persona['usage_suggestion']}\n"
            section += f"- **Command**: `claude-code --persona={persona['persona'].replace('--persona-', '')} \"[task description]\"`\n\n"
        
        return section
    
    def _generate_enhancement_section(self, enhancements: List[str]) -> str:
        """Generate enhancement suggestions section"""
        section = "## ✨ Enhancement Suggestions\n\n"
        section += "*Additional recommendations to improve project success*\n\n"
        
        for i, enhancement in enumerate(enhancements, 1):
            section += f"{i}. {enhancement}\n"
        
        return section
    
    def _generate_metadata_footer(self, recommendations: Dict) -> str:
        """Generate metadata footer"""
        footer = "---\n"
        footer += "*Enhanced with Integration-Aware PRP System*\n"
        footer += f"*Enhancement Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        footer += f"*Integrations Analyzed: {len(self.integration_patterns)} types*\n"
        footer += f"*Recommendations Generated: {len(recommendations['integrations'])} integrations, {len(recommendations['personas'])} personas*\n"
        
        return footer

def main():
    """Main function for CLI usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python integration-aware-prp-enhancer.py <prp-file> [output-file]")
        sys.exit(1)
    
    prp_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    enhancer = IntegrationAwarePRPEnhancer()
    result = enhancer.enhance_prp(prp_file, output_file)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print(f"✅ Enhanced PRP: {prp_file}")
    print(f"📊 Recommendations:")
    print(f"   - Integrations: {len(result['recommendations']['integrations'])}")
    print(f"   - Personas: {len(result['recommendations']['personas'])}")
    print(f"   - Enhancements: {len(result['recommendations']['enhancements'])}")
    
    if output_file:
        print(f"💾 Enhanced version saved to: {output_file}")

if __name__ == "__main__":
    main()