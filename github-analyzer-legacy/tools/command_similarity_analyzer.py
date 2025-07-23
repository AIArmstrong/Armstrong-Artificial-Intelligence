#!/usr/bin/env python3
"""
Command Similarity Analyzer for ClaudePreference → AAI Integration
Analyzes command compatibility and creates integration plan
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

@dataclass
class CommandInfo:
    name: str
    description: str
    parameters: List[str]
    examples: List[str]
    category: str
    functionality: List[str]

class CommandSimilarityAnalyzer:
    def __init__(self):
        self.aai_commands = {}
        self.claude_pref_commands = {}
        self.similarity_matrix = {}
        self.integration_plan = {}

    def analyze_commands(self):
        """Main analysis function"""
        print("🔍 Starting Command Similarity Analysis...")
        
        # Load existing AAI commands
        print("📂 Loading AAI commands...")
        self._load_aai_commands()
        
        # Load ClaudePreference commands from our analysis
        print("📂 Loading ClaudePreference commands...")
        self._load_claude_preference_commands()
        
        # Perform similarity analysis
        print("⚖️ Performing similarity analysis...")
        self._calculate_similarity_matrix()
        
        # Generate integration plan
        print("🏗️ Generating integration plan...")
        self._generate_integration_plan()
        
        # Create comprehensive report
        print("📊 Creating comprehensive report...")
        return self._create_similarity_report()

    def _load_aai_commands(self):
        """Load and parse AAI commands from .claude/commands/"""
        commands_dir = Path("/mnt/c/Users/Brandon/AAI/.claude/commands")
        
        for cmd_file in commands_dir.glob("*.md"):
            try:
                with open(cmd_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                cmd_info = self._parse_aai_command(cmd_file.stem, content)
                self.aai_commands[cmd_file.stem] = cmd_info
                
            except Exception as e:
                print(f"⚠️ Error parsing {cmd_file}: {e}")

    def _parse_aai_command(self, name: str, content: str) -> CommandInfo:
        """Parse AAI command file and extract information"""
        
        # Extract description (usually first paragraph or header)
        description_match = re.search(r'#\s+(.+?)(?:\n|$)', content)
        description = description_match.group(1) if description_match else "No description"
        
        # Extract ARGUMENTS section
        parameters = []
        args_match = re.search(r'ARGUMENTS:\s*(.+?)(?:\n\n|\n#|$)', content, re.DOTALL)
        if args_match:
            parameters = [args_match.group(1).strip()]
        
        # Extract examples
        examples = re.findall(r'Example[s]?:?\s*(.+?)(?:\n\n|\n#|$)', content, re.DOTALL | re.IGNORECASE)
        
        # Categorize based on functionality
        category = self._categorize_aai_command(name, content)
        
        # Extract functionality keywords
        functionality = self._extract_functionality_keywords(content)
        
        return CommandInfo(
            name=name,
            description=description,
            parameters=parameters,
            examples=examples,
            category=category,
            functionality=functionality
        )

    def _categorize_aai_command(self, name: str, content: str) -> str:
        """Categorize AAI command by function"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['analyze', 'review', 'audit', 'check']):
            return 'analysis'
        elif any(word in content_lower for word in ['build', 'create', 'generate', 'implement']):
            return 'development'
        elif any(word in content_lower for word in ['test', 'quality', 'lint', 'format']):
            return 'quality'
        elif any(word in content_lower for word in ['deploy', 'release', 'push', 'commit']):
            return 'deployment'
        elif any(word in content_lower for word in ['doc', 'help', 'explain', 'guide']):
            return 'documentation'
        elif any(word in content_lower for word in ['workflow', 'orchestrat', 'manage']):
            return 'workflow'
        else:
            return 'utility'

    def _extract_functionality_keywords(self, content: str) -> List[str]:
        """Extract key functionality keywords from command content"""
        keywords = []
        content_lower = content.lower()
        
        # Common functionality patterns
        patterns = [
            'analy', 'review', 'audit', 'scan', 'check', 'test', 'build', 'create',
            'generate', 'implement', 'deploy', 'release', 'document', 'explain',
            'workflow', 'orchestrat', 'manage', 'cleanup', 'improve', 'enhance',
            'debug', 'troubleshoot', 'validate', 'verify', 'optimize'
        ]
        
        for pattern in patterns:
            if pattern in content_lower:
                keywords.append(pattern)
        
        return keywords

    def _load_claude_preference_commands(self):
        """Load ClaudePreference commands from analysis results"""
        
        # Load from enhanced analysis results
        analysis_file = "/mnt/c/Users/Brandon/AAI/enhanced_analysis_20250719_111511.json"
        
        try:
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)
            
            # Extract CLI commands
            cli_commands = analysis_data.get('documentation_intelligence', {}).get('integration_points', {}).get('cli_commands', [])
            
            # Filter and categorize ClaudePreference commands
            claude_commands = [cmd for cmd in cli_commands if cmd.startswith('m-')]
            
            # Load detailed command info from ClaudePreference docs (simulated)
            self._load_claude_preference_details(claude_commands)
            
        except Exception as e:
            print(f"⚠️ Error loading ClaudePreference analysis: {e}")
            # Fallback to manual command list
            self._load_claude_preference_fallback()

    def _load_claude_preference_details(self, commands: List[str]):
        """Load detailed info for ClaudePreference commands"""
        
        # Detailed command mapping based on documentation analysis
        command_details = {
            'm-orchestrated-dev': {
                'description': 'Multi-agent development workflow with research-driven approach',
                'category': 'development',
                'functionality': ['orchestrat', 'workflow', 'multi-agent', 'research', 'review'],
                'parameters': ['requirements'],
                'examples': ['Deploy three specialized agents for collaborative development']
            },
            'm-commit-push': {
                'description': 'Automated commit and push workflow with intelligent message generation',
                'category': 'deployment',
                'functionality': ['commit', 'push', 'automat', 'workflow'],
                'parameters': ['message (optional)'],
                'examples': ['m-commit-push "feat: add user authentication"', 'm-commit-push']
            },
            'm-bug-fix': {
                'description': 'Comprehensive bug analysis, reproduction, and fix workflow',
                'category': 'development',
                'functionality': ['debug', 'fix', 'analy', 'troubleshoot'],
                'parameters': ['source (optional)'],
                'examples': ['m-bug-fix #123', 'm-bug-fix "NullPointerException"', 'm-bug-fix screenshot.png']
            },
            'm-security-scan': {
                'description': 'Comprehensive security vulnerability scanning and assessment',
                'category': 'quality',
                'functionality': ['security', 'scan', 'audit', 'vulnerab'],
                'parameters': ['scope (optional)'],
                'examples': ['m-security-scan dependencies', 'm-security-scan auth', 'm-security-scan src/api']
            },
            'm-test-generation': {
                'description': 'Automated test case generation with coverage analysis',
                'category': 'quality',
                'functionality': ['test', 'generate', 'coverage', 'automat'],
                'parameters': ['type', 'target', 'coverage'],
                'examples': ['m-test-generation unit src/auth 90%', 'm-test-generation integration api']
            },
            'm-review-code': {
                'description': 'Comprehensive code review with quality assessment and reporting',
                'category': 'analysis',
                'functionality': ['review', 'analy', 'quality', 'assess'],
                'parameters': ['target', 'depth', 'focus'],
                'examples': ['m-review-code src/auth deep security', 'm-review-code PR#123 quick']
            },
            'm-task-planner': {
                'description': 'Analyze requirements and generate structured implementation plan',
                'category': 'workflow',
                'functionality': ['plan', 'analy', 'workflow', 'structure'],
                'parameters': ['requirements document'],
                'examples': ['Structured implementation plan with dependency mapping']
            },
            'm-debate-architecture': {
                'description': 'Strategic architecture review workflow',
                'category': 'analysis',
                'functionality': ['architecture', 'review', 'strategic', 'analy'],
                'parameters': ['target'],
                'examples': ['Focuses on high-level structure and strategic evolution']
            },
            'm-debate-code': {
                'description': 'Code debate analysis workflow',
                'category': 'analysis',
                'functionality': ['code', 'review', 'analy', 'debate'],
                'parameters': ['target'],
                'examples': ['Tactical code review and implementation-level analysis']
            },
            'm-document-update': {
                'description': 'Documentation update workflow',
                'category': 'documentation',
                'functionality': ['document', 'update', 'workflow'],
                'parameters': ['target'],
                'examples': ['Automated documentation maintenance']
            },
            'm-project-cleanup': {
                'description': 'Project cleanup and maintenance workflow',
                'category': 'utility',
                'functionality': ['cleanup', 'maintain', 'organize'],
                'parameters': ['scope'],
                'examples': ['Comprehensive project cleanup']
            },
            'm-merge-branch': {
                'description': 'Branch merging workflow with conflict resolution',
                'category': 'deployment',
                'functionality': ['merge', 'branch', 'workflow'],
                'parameters': ['branch'],
                'examples': ['Smart branch merge strategies']
            },
            'm-branch-prune': {
                'description': 'Branch pruning and cleanup workflow',
                'category': 'utility',
                'functionality': ['prune', 'cleanup', 'branch'],
                'parameters': ['options'],
                'examples': ['Automated branch cleanup']
            },
            'm-next-task': {
                'description': 'Next task recommendation workflow',
                'category': 'workflow',
                'functionality': ['workflow', 'recommend', 'task'],
                'parameters': ['context'],
                'examples': ['Intelligent task recommendation']
            },
            'm-next-context': {
                'description': 'Context switching workflow',
                'category': 'workflow',
                'functionality': ['context', 'switch', 'workflow'],
                'parameters': ['target'],
                'examples': ['Smart context switching']
            },
            'm-review-completion': {
                'description': 'Review completion workflow',
                'category': 'quality',
                'functionality': ['review', 'complete', 'workflow'],
                'parameters': ['target'],
                'examples': ['Completion verification workflow']
            },
            'm-tdd-planner': {
                'description': 'Test-driven development planning workflow',
                'category': 'development',
                'functionality': ['tdd', 'plan', 'test', 'develop'],
                'parameters': ['requirements'],
                'examples': ['TDD workflow planning']
            }
        }
        
        for cmd_name, details in command_details.items():
            if cmd_name in [f'm-{cmd}' for cmd in ['orchestrated-dev', 'commit-push', 'bug-fix', 'security-scan', 'test-generation', 'review-code', 'task-planner', 'debate-architecture', 'debate-code', 'document-update', 'project-cleanup', 'merge-branch', 'branch-prune', 'next-task', 'next-context', 'review-completion', 'tdd-planner']]:
                self.claude_pref_commands[cmd_name] = CommandInfo(
                    name=cmd_name,
                    description=details['description'],
                    parameters=details['parameters'],
                    examples=details['examples'],
                    category=details['category'],
                    functionality=details['functionality']
                )

    def _load_claude_preference_fallback(self):
        """Fallback method if analysis file is unavailable"""
        print("⚠️ Using fallback ClaudePreference command data")
        # Basic command structure for testing
        pass

    def _calculate_similarity_matrix(self):
        """Calculate similarity scores between AAI and ClaudePreference commands"""
        
        for aai_name, aai_cmd in self.aai_commands.items():
            self.similarity_matrix[aai_name] = {}
            
            for cp_name, cp_cmd in self.claude_pref_commands.items():
                similarity_score = self._calculate_command_similarity(aai_cmd, cp_cmd)
                self.similarity_matrix[aai_name][cp_name] = similarity_score

    def _calculate_command_similarity(self, aai_cmd: CommandInfo, cp_cmd: CommandInfo) -> Dict[str, Any]:
        """Calculate detailed similarity score between two commands"""
        
        # Category similarity
        category_match = 1.0 if aai_cmd.category == cp_cmd.category else 0.0
        
        # Functionality overlap
        aai_funcs = set(aai_cmd.functionality)
        cp_funcs = set(cp_cmd.functionality)
        if aai_funcs and cp_funcs:
            func_overlap = len(aai_funcs.intersection(cp_funcs)) / len(aai_funcs.union(cp_funcs))
        else:
            func_overlap = 0.0
        
        # Description similarity (keyword-based)
        aai_desc_words = set(aai_cmd.description.lower().split())
        cp_desc_words = set(cp_cmd.description.lower().split())
        if aai_desc_words and cp_desc_words:
            desc_similarity = len(aai_desc_words.intersection(cp_desc_words)) / len(aai_desc_words.union(cp_desc_words))
        else:
            desc_similarity = 0.0
        
        # Overall similarity score (weighted)
        overall_score = (category_match * 0.4) + (func_overlap * 0.4) + (desc_similarity * 0.2)
        
        return {
            'overall_score': overall_score,
            'category_match': category_match,
            'functionality_overlap': func_overlap,
            'description_similarity': desc_similarity,
            'shared_functionality': list(aai_funcs.intersection(cp_funcs)),
            'unique_cp_functionality': list(cp_funcs - aai_funcs)
        }

    def _generate_integration_plan(self):
        """Generate comprehensive integration plan"""
        
        self.integration_plan = {
            'highly_compatible': [],     # >0.7 similarity - merge functionality
            'moderately_compatible': [], # 0.4-0.7 similarity - extend with flags
            'unique_commands': [],       # <0.4 similarity - consider as new
            'recommendations': []
        }
        
        # Analyze each ClaudePreference command
        for cp_name, cp_cmd in self.claude_pref_commands.items():
            best_match = self._find_best_aai_match(cp_name)
            
            if best_match:
                aai_name, similarity = best_match
                similarity_data = self.similarity_matrix[aai_name][cp_name]
                
                if similarity_data['overall_score'] >= 0.7:
                    self.integration_plan['highly_compatible'].append({
                        'claude_pref_command': cp_name,
                        'aai_command': aai_name,
                        'similarity_score': similarity_data['overall_score'],
                        'integration_type': 'merge_functionality',
                        'shared_functions': similarity_data['shared_functionality'],
                        'new_functions': similarity_data['unique_cp_functionality'],
                        'recommendation': f"Merge {cp_name} functionality into existing {aai_name} command"
                    })
                    
                elif similarity_data['overall_score'] >= 0.4:
                    self.integration_plan['moderately_compatible'].append({
                        'claude_pref_command': cp_name,
                        'aai_command': aai_name,
                        'similarity_score': similarity_data['overall_score'],
                        'integration_type': 'extend_with_flags',
                        'shared_functions': similarity_data['shared_functionality'],
                        'new_functions': similarity_data['unique_cp_functionality'],
                        'recommendation': f"Extend {aai_name} with new flags to support {cp_name} functionality"
                    })
                else:
                    self.integration_plan['unique_commands'].append({
                        'claude_pref_command': cp_name,
                        'best_aai_match': aai_name,
                        'similarity_score': similarity_data['overall_score'],
                        'integration_type': 'create_new_or_advanced',
                        'functionality': cp_cmd.functionality,
                        'recommendation': f"Consider {cp_name} as unique functionality - review for advanced namespace"
                    })
            else:
                self.integration_plan['unique_commands'].append({
                    'claude_pref_command': cp_name,
                    'best_aai_match': 'none',
                    'similarity_score': 0.0,
                    'integration_type': 'create_new',
                    'functionality': cp_cmd.functionality,
                    'recommendation': f"{cp_name} is completely unique - review for potential addition"
                })

    def _find_best_aai_match(self, cp_command: str) -> Tuple[str, float]:
        """Find the best matching AAI command for a ClaudePreference command"""
        best_match = None
        best_score = 0.0
        
        for aai_name in self.aai_commands.keys():
            if aai_name in self.similarity_matrix and cp_command in self.similarity_matrix[aai_name]:
                score = self.similarity_matrix[aai_name][cp_command]['overall_score']
                if score > best_score:
                    best_score = score
                    best_match = aai_name
        
        return (best_match, best_score) if best_match else None

    def _create_similarity_report(self) -> Dict[str, Any]:
        """Create comprehensive similarity report"""
        
        report = {
            'analysis_summary': {
                'aai_commands_analyzed': len(self.aai_commands),
                'claude_pref_commands_analyzed': len(self.claude_pref_commands),
                'highly_compatible_pairs': len(self.integration_plan['highly_compatible']),
                'moderately_compatible_pairs': len(self.integration_plan['moderately_compatible']),
                'unique_commands': len(self.integration_plan['unique_commands'])
            },
            'compatibility_matrix': self._create_compatibility_matrix(),
            'integration_recommendations': self.integration_plan,
            'implementation_phases': self._create_implementation_phases(),
            'risk_assessment': self._assess_integration_risks()
        }
        
        return report

    def _create_compatibility_matrix(self) -> List[Dict[str, Any]]:
        """Create human-readable compatibility matrix"""
        matrix = []
        
        for cp_name, cp_cmd in self.claude_pref_commands.items():
            best_match = self._find_best_aai_match(cp_name)
            
            if best_match:
                aai_name, score = best_match
                similarity_data = self.similarity_matrix[aai_name][cp_name]
                
                compatibility = "✅ High" if score >= 0.7 else "⚠️ Medium" if score >= 0.4 else "❌ Low"
                
                matrix.append({
                    'claude_pref_command': cp_name,
                    'aai_equivalent': aai_name,
                    'compatibility': compatibility,
                    'similarity_score': f"{score:.2f}",
                    'shared_functionality': ', '.join(similarity_data['shared_functionality']),
                    'new_functionality': ', '.join(similarity_data['unique_cp_functionality']),
                    'integration_notes': self._generate_integration_notes(cp_name, aai_name, score)
                })
        
        return sorted(matrix, key=lambda x: float(x['similarity_score']), reverse=True)

    def _generate_integration_notes(self, cp_name: str, aai_name: str, score: float) -> str:
        """Generate specific integration notes for a command pair"""
        if score >= 0.7:
            return f"Merge {cp_name} functionality into {aai_name}"
        elif score >= 0.4:
            return f"Extend {aai_name} with flags for {cp_name} features"
        else:
            return f"Consider {cp_name} for advanced namespace or future addition"

    def _create_implementation_phases(self) -> Dict[str, List[str]]:
        """Create phased implementation plan"""
        return {
            'phase_1_immediate': [
                "Extend highly compatible commands with new functionality",
                "Add parameter flags to existing commands",
                "Update command descriptions and help text"
            ],
            'phase_2_short_term': [
                "Implement moderate compatibility extensions",
                "Add alias support for ClaudePreference naming",
                "Create backwards compatibility layer"
            ],
            'phase_3_evaluation': [
                "Review unique commands for strategic value",
                "Consider advanced namespace implementation",
                "Plan gradual rollout of selected unique features"
            ]
        }

    def _assess_integration_risks(self) -> Dict[str, str]:
        """Assess risks of integration plan"""
        return {
            'compatibility_risk': 'Low - Most changes are additive',
            'user_confusion_risk': 'Medium - New flags may require documentation',
            'system_complexity_risk': 'Low - Existing command structure preserved',
            'maintenance_overhead': 'Low - Leveraging existing infrastructure',
            'recommended_approach': 'Gradual phased rollout with extensive testing'
        }

def main():
    analyzer = CommandSimilarityAnalyzer()
    report = analyzer.analyze_commands()
    
    # Save detailed report
    output_file = f"command_similarity_report_{report['analysis_summary']['aai_commands_analyzed']}aai_{report['analysis_summary']['claude_pref_commands_analyzed']}cp.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n🎉 === COMMAND SIMILARITY ANALYSIS COMPLETE ===")
    print(f"📊 AAI Commands Analyzed: {report['analysis_summary']['aai_commands_analyzed']}")
    print(f"📊 ClaudePreference Commands Analyzed: {report['analysis_summary']['claude_pref_commands_analyzed']}")
    print(f"✅ Highly Compatible: {report['analysis_summary']['highly_compatible_pairs']}")
    print(f"⚠️ Moderately Compatible: {report['analysis_summary']['moderately_compatible_pairs']}")
    print(f"🆕 Unique Commands: {report['analysis_summary']['unique_commands']}")
    print(f"💾 Detailed report saved to: {output_file}")
    
    # Print top compatibility matches
    print(f"\n🏆 === TOP COMPATIBILITY MATCHES ===")
    for item in report['compatibility_matrix'][:5]:
        print(f"{item['compatibility']} {item['claude_pref_command']} → {item['aai_equivalent']} (Score: {item['similarity_score']})")
    
    return report

if __name__ == "__main__":
    main()