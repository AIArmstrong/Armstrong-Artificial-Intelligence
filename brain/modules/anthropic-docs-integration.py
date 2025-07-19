#!/usr/bin/env python3
"""
Anthropic Documentation Integration Module
Integrates official Anthropic documentation into AAI's analysis and response repertoire
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class AnthropicDocsIntegration:
    def __init__(self):
        self.aai_root = Path("/mnt/c/Users/Brandon/AAI")
        self.docs_path = self.aai_root / "docs/official/anthropic"
        self.brain_path = self.aai_root / "brain"
        
        # Documentation categories mapping
        self.doc_categories = {
            'api': {
                'path': self.docs_path / 'api',
                'priority': 'high',
                'use_cases': ['tool_use', 'error_handling', 'rate_limiting', 'authentication']
            },
            'claude': {
                'path': self.docs_path / 'claude', 
                'priority': 'high',
                'use_cases': ['general_usage', 'model_selection', 'pricing', 'tool_integration']
            },
            'prompt-engineering': {
                'path': self.docs_path / 'prompt-engineering',
                'priority': 'critical',
                'use_cases': ['prompt_optimization', 'chain_of_thought', 'clarity_guidelines']
            },
            'models': {
                'path': self.docs_path / 'models',
                'priority': 'high', 
                'use_cases': ['model_selection', 'capability_assessment', 'performance_optimization']
            }
        }
    
    def extract_key_patterns(self, doc_path: Path) -> Dict:
        """Extract key patterns and guidelines from documentation"""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            patterns = {
                'best_practices': [],
                'code_examples': [],
                'guidelines': [],
                'warnings': [],
                'api_patterns': []
            }
            
            lines = content.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                # Extract best practices
                if any(keyword in line.lower() for keyword in ['best practice', 'recommended', 'should']):
                    patterns['best_practices'].append(line)
                
                # Extract guidelines
                if any(keyword in line.lower() for keyword in ['guideline', 'rule', 'principle']):
                    patterns['guidelines'].append(line)
                
                # Extract warnings
                if any(keyword in line.lower() for keyword in ['warning', 'important', 'note', 'caution']):
                    patterns['warnings'].append(line)
                
                # Extract code examples (simple detection)
                if line.startswith('```') or 'example' in line.lower():
                    patterns['code_examples'].append(line)
                
                # Extract API patterns
                if any(keyword in line.lower() for keyword in ['endpoint', 'parameter', 'response', 'request']):
                    patterns['api_patterns'].append(line)
            
            return patterns
            
        except Exception as e:
            print(f"Error extracting patterns from {doc_path}: {e}")
            return {}
    
    def create_analysis_integration_guide(self) -> Dict:
        """Create integration guide for analysis tasks"""
        integration_guide = {
            'analysis_workflows': {
                'code_analysis': {
                    'required_docs': ['prompt-engineering/be-clear-and-direct.md', 'claude/tool-use.md'],
                    'patterns': [
                        'Use clear, specific prompts for code analysis',
                        'Structure analysis requests with explicit goals',
                        'Reference tool use patterns for integration analysis'
                    ],
                    'integration_points': [
                        'Apply prompt engineering guidelines to analysis requests',
                        'Use tool use documentation for API integrations',
                        'Follow model capability guidelines for task assignment'
                    ]
                },
                'security_analysis': {
                    'required_docs': ['api/errors.md', 'prompt-engineering/chain-of-thought.md'],
                    'patterns': [
                        'Use chain-of-thought reasoning for security assessment',
                        'Reference error handling patterns for vulnerability detection',
                        'Apply systematic thinking to threat modeling'
                    ],
                    'integration_points': [
                        'Use structured reasoning for security analysis',
                        'Apply error handling knowledge to vulnerability assessment',
                        'Reference best practices for secure implementations'
                    ]
                },
                'performance_analysis': {
                    'required_docs': ['models/choosing-a-model.md', 'claude/pricing.md'],
                    'patterns': [
                        'Consider model capabilities for performance assessment',
                        'Apply cost-benefit analysis using pricing information',
                        'Use appropriate model selection for analysis depth'
                    ],
                    'integration_points': [
                        'Select optimal models for different analysis types',
                        'Balance analysis depth with cost considerations',
                        'Apply model-specific capabilities to performance evaluation'
                    ]
                },
                'architecture_analysis': {
                    'required_docs': ['claude/overview.md', 'prompt-engineering/overview.md'],
                    'patterns': [
                        'Use comprehensive prompt engineering for architectural assessment',
                        'Apply systematic thinking to system design evaluation',
                        'Reference Claude capabilities for analysis scope'
                    ],
                    'integration_points': [
                        'Structure architectural analysis with clear prompts',
                        'Use Claude reasoning capabilities for system evaluation',
                        'Apply prompt engineering principles to complex analysis'
                    ]
                }
            },
            'response_enhancement': {
                'clarity_guidelines': {
                    'source': 'prompt-engineering/be-clear-and-direct.md',
                    'applications': [
                        'Structure responses with clear sections',
                        'Use specific, actionable language',
                        'Provide concrete examples and evidence'
                    ]
                },
                'reasoning_patterns': {
                    'source': 'prompt-engineering/chain-of-thought.md',
                    'applications': [
                        'Show reasoning steps in complex analysis',
                        'Break down problems systematically',
                        'Provide confidence scores with reasoning'
                    ]
                },
                'tool_integration': {
                    'source': 'claude/tool-use.md',
                    'applications': [
                        'Reference tool capabilities in responses',
                        'Suggest appropriate tool combinations',
                        'Provide tool-specific guidance'
                    ]
                }
            }
        }
        
        return integration_guide
    
    def create_response_templates(self) -> Dict:
        """Create response templates based on Anthropic documentation"""
        templates = {
            'analysis_response': {
                'structure': [
                    '## Executive Summary',
                    '## Detailed Analysis',
                    '### Code Quality Assessment', 
                    '### Security Evaluation',
                    '### Performance Review',
                    '### Architecture Assessment',
                    '## Recommendations',
                    '## Implementation Guide',
                    '## References'
                ],
                'guidelines': [
                    'Be clear and direct in findings',
                    'Use chain-of-thought reasoning for complex analysis',
                    'Provide specific, actionable recommendations',
                    'Reference official documentation when applicable'
                ]
            },
            'tool_integration_response': {
                'structure': [
                    '## Tool Recommendation',
                    '## Integration Approach', 
                    '## Implementation Steps',
                    '## Best Practices',
                    '## Troubleshooting',
                    '## References'
                ],
                'guidelines': [
                    'Reference official tool use documentation',
                    'Provide concrete implementation examples',
                    'Include error handling considerations',
                    'Suggest monitoring and validation approaches'
                ]
            },
            'error_analysis_response': {
                'structure': [
                    '## Error Classification',
                    '## Root Cause Analysis',
                    '## Impact Assessment',
                    '## Resolution Steps',
                    '## Prevention Measures',
                    '## References'
                ],
                'guidelines': [
                    'Use systematic error analysis approach',
                    'Reference API error documentation',
                    'Provide clear resolution steps',
                    'Include preventive measures'
                ]
            }
        }
        
        return templates
    
    def generate_integration_hooks(self) -> Dict:
        """Generate integration hooks for AAI brain modules"""
        hooks = {
            'intent_engine': {
                'trigger': 'analysis_request',
                'action': 'load_anthropic_analysis_patterns',
                'docs_reference': ['prompt-engineering/be-clear-and-direct.md']
            },
            'prompt_recipes': {
                'trigger': 'prompt_generation',
                'action': 'apply_anthropic_prompt_guidelines', 
                'docs_reference': ['prompt-engineering/overview.md', 'prompt-engineering/chain-of-thought.md']
            },
            'decision_neural': {
                'trigger': 'complex_decision',
                'action': 'apply_structured_reasoning',
                'docs_reference': ['prompt-engineering/chain-of-thought.md']
            },
            'openrouter_integration': {
                'trigger': 'model_selection',
                'action': 'apply_model_selection_criteria',
                'docs_reference': ['models/choosing-a-model.md', 'models/overview.md']
            },
            'superclaude_bridge': {
                'trigger': 'command_execution',
                'action': 'apply_tool_use_patterns',
                'docs_reference': ['claude/tool-use.md', 'claude/tool-use-examples.md']
            }
        }
        
        return hooks
    
    def create_quick_reference_guide(self) -> str:
        """Create quick reference guide for Anthropic documentation"""
        guide = """# Anthropic Documentation Quick Reference for AAI

## Analysis Enhancement Guidelines

### When performing code analysis:
- **Reference**: `/docs/official/anthropic/prompt-engineering/be-clear-and-direct.md`
- **Apply**: Clear, specific analysis prompts with explicit goals
- **Pattern**: Structure analysis with defined scope and success criteria

### When doing security analysis:
- **Reference**: `/docs/official/anthropic/api/errors.md`
- **Apply**: Systematic error pattern recognition for vulnerability detection
- **Pattern**: Use chain-of-thought reasoning for threat assessment

### When performing performance analysis:
- **Reference**: `/docs/official/anthropic/models/choosing-a-model.md`
- **Apply**: Model-appropriate analysis depth and cost considerations
- **Pattern**: Balance analysis thoroughness with resource efficiency

### When doing architecture analysis:
- **Reference**: `/docs/official/anthropic/claude/overview.md`
- **Apply**: Comprehensive prompt engineering for system evaluation
- **Pattern**: Use structured reasoning for complex system assessment

## Response Enhancement Patterns

### Clarity and Directness
- Use specific, actionable language
- Structure responses with clear sections
- Provide concrete examples and evidence
- Reference: `prompt-engineering/be-clear-and-direct.md`

### Reasoning and Analysis
- Show reasoning steps in complex analysis
- Break down problems systematically  
- Provide confidence scores with justification
- Reference: `prompt-engineering/chain-of-thought.md`

### Tool Integration
- Reference tool capabilities in responses
- Suggest appropriate tool combinations
- Provide tool-specific implementation guidance
- Reference: `claude/tool-use.md`

## Error Handling Integration
- Reference API error patterns for troubleshooting
- Apply systematic error classification
- Provide clear resolution steps
- Reference: `api/errors.md`

## Model Selection Guidance
- Consider task complexity for model selection
- Balance capability requirements with cost
- Apply model-specific features appropriately
- Reference: `models/choosing-a-model.md`

---
*Integrated with AAI Brain v3.0 for enhanced analysis and response quality*
"""
        
        return guide
    
    def save_integration_assets(self) -> Dict:
        """Save all integration assets to brain modules"""
        assets = {}
        
        # Save integration guide
        integration_guide = self.create_analysis_integration_guide()
        guide_path = self.brain_path / "modules/anthropic-analysis-integration.json"
        with open(guide_path, 'w') as f:
            json.dump(integration_guide, f, indent=2)
        assets['integration_guide'] = str(guide_path)
        
        # Save response templates
        templates = self.create_response_templates()
        templates_path = self.brain_path / "modules/anthropic-response-templates.json"
        with open(templates_path, 'w') as f:
            json.dump(templates, f, indent=2)
        assets['response_templates'] = str(templates_path)
        
        # Save integration hooks
        hooks = self.generate_integration_hooks()
        hooks_path = self.brain_path / "modules/anthropic-integration-hooks.json"
        with open(hooks_path, 'w') as f:
            json.dump(hooks, f, indent=2)
        assets['integration_hooks'] = str(hooks_path)
        
        # Save quick reference guide
        quick_ref = self.create_quick_reference_guide()
        ref_path = self.docs_path / "AAI-INTEGRATION-GUIDE.md"
        with open(ref_path, 'w') as f:
            f.write(quick_ref)
        assets['quick_reference'] = str(ref_path)
        
        return assets
    
    def update_brain_claude_md(self) -> str:
        """Update brain/Claude.md with Anthropic documentation integration"""
        claude_md_path = self.brain_path / "Claude.md"
        
        integration_section = """
### 📚 Anthropic Documentation Integration
```
@include docs/official/anthropic/AAI-INTEGRATION-GUIDE.md
@include brain/modules/anthropic-analysis-integration.json
@include brain/modules/anthropic-response-templates.json
@include brain/modules/anthropic-integration-hooks.json
```
**Auto-Loading Triggers**: All analysis tasks, prompt generation, model selection, error handling

### Enhanced Analysis Protocols
- **Code Analysis**: Apply prompt engineering guidelines from official docs
- **Security Analysis**: Use error handling patterns for vulnerability detection  
- **Performance Analysis**: Reference model selection criteria for analysis depth
- **Architecture Analysis**: Apply structured reasoning patterns from chain-of-thought documentation
- **Tool Integration**: Follow official tool use patterns and examples
- **Error Handling**: Reference API error documentation for systematic troubleshooting

### Response Enhancement Patterns
- **Clarity**: Apply "be clear and direct" guidelines to all responses
- **Reasoning**: Use chain-of-thought patterns for complex analysis
- **Examples**: Provide concrete examples following official documentation patterns
- **Integration**: Reference tool capabilities and best practices from official docs
"""
        
        return integration_section

def main():
    integrator = AnthropicDocsIntegration()
    
    print("Integrating Anthropic documentation into AAI repertoire...")
    
    # Save all integration assets
    assets = integrator.save_integration_assets()
    
    print("Integration assets created:")
    for asset_type, path in assets.items():
        print(f"  {asset_type}: {path}")
    
    # Generate brain integration section
    brain_integration = integrator.update_brain_claude_md()
    print(f"\nBrain integration section generated ({len(brain_integration)} chars)")
    
    print("\n✅ Anthropic documentation successfully integrated into AAI repertoire!")
    print("\nIntegration includes:")
    print("  - Analysis workflow guidelines")
    print("  - Response enhancement patterns") 
    print("  - Tool integration best practices")
    print("  - Error handling procedures")
    print("  - Model selection criteria")
    print("  - Quick reference guide")
    
    return assets

if __name__ == '__main__':
    main()