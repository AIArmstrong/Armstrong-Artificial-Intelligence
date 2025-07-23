# AAI Validation Gates v1.0

## Purpose  
Define systematic validation gate placement for AAI command execution. Ensures critical checkpoints prevent execution errors and maintain system reliability.

## Validation Gate Types

### BLOCKING Validations
**Definition**: Must pass before execution can continue. System blocks until resolved.

```yaml
blocking_criteria:
  system_critical: "Core system requirements (Claude.md, standards, dashboard)"
  user_safety: "Operations that could cause data loss or system damage"
  quality_gates: "Minimum quality thresholds for deliverables"
  resource_intensive: "Operations requiring significant system resources"
  external_dependencies: "Operations requiring external service availability"
```

### WARNING Validations
**Definition**: Generate warnings but don't block execution. Used for best practices and optimizations.

```yaml
warning_criteria:
  best_practices: "Recommended patterns and approaches"
  performance: "Potential performance optimizations"
  maintainability: "Code quality and maintenance concerns"
  compatibility: "Version compatibility and deprecation warnings"
```

## Command-Specific Validation Gates

### Generate-PRP Validation Gates

#### BLOCKING Gates
```yaml
system_initialization:
  name: "System Prerequisites"
  requirements:
    - claude_md_loaded: true
    - standards_loaded: true  
    - dashboard_current: "< 5 minutes"
  error_template: "BLOCKING: System must be initialized before PRP generation"
  recovery_actions:
    - "Load /mnt/c/Users/Brandon/AAI/brain/Claude.md"
    - "Load all brain/standards/ files"
    - "Update dashboards/status.md"

requirements_complete:
  name: "User Requirements Validation"
  requirements:
    - user_input_provided: true
    - requirements_detailed: true
    - scope_defined: true
  error_template: "BLOCKING: Complete requirements needed before research"
  recovery_actions:
    - "Gather detailed user requirements"
    - "Define project scope clearly"
    - "Confirm technical specifications"

research_sufficient:
  name: "Research Depth Validation"  
  requirements:
    - pages_scraped: ">= 30"
    - official_sources: ">= 80%"
    - research_quality: ">= 90%"
  error_template: "BLOCKING: Insufficient research depth for quality PRP"
  recovery_actions:
    - "Scrape additional official documentation"
    - "Validate source authority and recency"
    - "Cross-reference findings across sources"

prp_quality_verified:
  name: "PRP Quality Gate"
  requirements:
    - completeness_score: ">= 90%"
    - technical_accuracy: ">= 95%"
    - implementation_clarity: ">= 85%"
  error_template: "BLOCKING: PRP quality below acceptable standards"
  recovery_actions:
    - "Review and enhance incomplete sections"
    - "Verify technical accuracy of all recommendations"
    - "Clarify implementation steps and requirements"
```

#### WARNING Gates
```yaml
research_breadth:
  name: "Research Source Diversity"
  requirements:
    - source_variety: ">= 5 different domains"
    - perspective_diversity: "multiple viewpoints considered"
  warning_message: "Consider expanding research source diversity"

implementation_examples:
  name: "Implementation Examples"
  requirements:
    - code_examples: ">= 3 per major component"
    - test_examples: ">= 1 per feature"
  warning_message: "Additional implementation examples recommended"
```

### Implement Validation Gates

#### BLOCKING Gates
```yaml
plan_approved:
  name: "Implementation Plan Approval"
  requirements:
    - user_approval: true
    - technical_approach_confirmed: true
    - resource_requirements_accepted: true
  error_template: "BLOCKING: Implementation plan must be approved before coding"
  recovery_actions:
    - "Present implementation plan to user"
    - "Explain technical approach and rationale"
    - "Confirm resource and timeline requirements"

code_standards_met:
  name: "Code Quality Standards"
  requirements:
    - syntax_valid: true
    - style_compliant: ">= 95%"
    - security_validated: true
    - test_coverage: ">= 80%"
  error_template: "BLOCKING: Code must meet quality standards before deployment"
  recovery_actions:
    - "Fix syntax errors and style violations"
    - "Address security vulnerabilities"
    - "Implement missing tests to meet coverage"

testing_complete:
  name: "Testing Validation"
  requirements:
    - unit_tests_pass: true
    - integration_tests_pass: true
    - manual_testing_verified: true
  error_template: "BLOCKING: All tests must pass before deployment"
  recovery_actions:
    - "Fix failing unit tests"
    - "Resolve integration test failures"
    - "Complete manual testing verification"
```

#### WARNING Gates
```yaml
performance_optimization:
  name: "Performance Considerations"
  requirements:
    - performance_analyzed: true
    - bottlenecks_identified: true
  warning_message: "Consider performance optimization opportunities"

documentation_completeness:
  name: "Documentation Quality" 
  requirements:
    - api_documented: ">= 90%"
    - examples_provided: ">= 3"
  warning_message: "Consider enhancing documentation completeness"
```

### Analyze Validation Gates

#### BLOCKING Gates
```yaml
scope_confirmed:
  name: "Analysis Scope Confirmation"
  requirements:
    - analysis_targets_defined: true
    - analysis_depth_specified: true
    - user_expectations_clear: true
  error_template: "BLOCKING: Analysis scope must be confirmed before execution"
  recovery_actions:
    - "Define specific analysis targets"
    - "Specify required analysis depth"
    - "Clarify user expectations and deliverables"

analysis_complete:
  name: "Analysis Completion Verification"
  requirements:
    - all_agents_completed: true
    - findings_synthesized: true
    - confidence_threshold_met: ">= 85%"
  error_template: "BLOCKING: Analysis must be complete before reporting"
  recovery_actions:
    - "Ensure all analysis agents completed successfully"
    - "Synthesize findings from all analysis dimensions"
    - "Achieve minimum confidence threshold"

recommendations_actionable:
  name: "Actionable Recommendations"
  requirements:
    - recommendations_specific: true
    - priority_assigned: true
    - implementation_guidance: true
  error_template: "BLOCKING: Recommendations must be actionable"
  recovery_actions:
    - "Make recommendations specific and measurable"
    - "Assign clear priorities to each recommendation"
    - "Provide implementation guidance for each item"
```

## Validation Implementation Framework

### Validation Gate Class Structure
```python
class ValidationGate:
    def __init__(self, name: str, gate_type: str, requirements: dict, blocking: bool):
        self.name = name
        self.gate_type = gate_type  # "system", "quality", "user", "resource"
        self.requirements = requirements
        self.blocking = blocking
        
    def validate(self) -> ValidationResult:
        """Execute validation with detailed results"""
        pass
        
    def generate_error_message(self, failed_requirements: list) -> str:
        """Generate structured error message"""
        pass
        
    def generate_recovery_actions(self, failed_requirements: list) -> list:
        """Generate specific recovery actions"""
        pass
```

### Systematic Gate Placement Strategy

#### High-Impact Decision Points
```yaml
user_approval_gates:
  - architectural_changes: "Major system architecture modifications"
  - breaking_changes: "Changes that break existing functionality"
  - external_integrations: "New external service integrations"
  - resource_intensive_operations: "Operations requiring significant resources"
  - data_modifications: "Operations that modify persistent data"
```

#### Quality Assurance Points
```yaml
quality_gates:
  - minimum_confidence_thresholds: "85% for analysis, 90% for implementation"
  - completeness_requirements: "All required sections/components present"
  - accuracy_validation: "Technical accuracy verified"
  - test_coverage_minimums: "80% for new code, 95% for critical paths"
```

#### System Safety Points  
```yaml
safety_gates:
  - system_state_validation: "System in valid state before operations"
  - backup_verification: "Critical data backed up before modifications"
  - rollback_readiness: "Ability to rollback changes if needed"
  - dependency_availability: "Required dependencies available and accessible"
```

## Validation Testing Framework

### Gate Testing Requirements
```yaml
validation_testing:
  unit_tests:
    - test_blocking_gates_actually_block: true
    - test_warning_gates_generate_warnings: true
    - test_error_messages_are_helpful: true
    - test_recovery_actions_work: true
    
  integration_tests:
    - test_command_execution_with_gates: true
    - test_multiple_gate_failures: true
    - test_gate_bypass_impossible: true
    - test_user_approval_flow: true
    
  user_acceptance_tests:
    - test_error_messages_understandable: true
    - test_recovery_actions_actionable: true
    - test_blocking_behavior_appropriate: true
    - test_warning_behavior_helpful: true
```

### Validation Effectiveness Metrics
```yaml
success_metrics:
  gate_effectiveness:
    - prevented_errors: "Count of errors prevented by gates"
    - false_positives: "< 5% false positive rate"
    - user_satisfaction: ">= 90% user approval of gate behavior"
    - system_reliability: "99% protocol adherence rate"
    
  performance_impact:
    - validation_overhead: "< 10% execution time overhead"
    - user_interruption_frequency: "Minimize unnecessary user interruptions"
    - recovery_success_rate: ">= 95% successful error recovery"
```

## Gate Maintenance and Evolution

### Continuous Improvement Process
```yaml
improvement_cycle:
  monitoring:
    - track_gate_trigger_frequency: "Which gates trigger most often"
    - analyze_false_positives: "Gates that block unnecessarily"
    - measure_recovery_effectiveness: "How well recovery actions work"
    
  analysis:
    - identify_missing_gates: "Errors that could be prevented"
    - optimize_gate_placement: "Better placement for effectiveness"
    - refine_error_messages: "Improve clarity and helpfulness"
    
  implementation:
    - add_new_gates: "Based on identified gaps"
    - modify_existing_gates: "Based on effectiveness analysis"
    - remove_ineffective_gates: "Gates that don't add value"
```

### Version Control and Documentation
```yaml
change_management:
  version_tracking: "Track all changes to validation gates"
  impact_analysis: "Analyze impact of gate changes"
  rollback_capability: "Ability to rollback problematic changes"
  user_communication: "Communicate gate changes to users"
```

---

**Version**: 1.0  
**Last Updated**: 2025-01-23  
**Integration**: Works with command-protocols.md and intelligence-defaults.md  
**Status**: ACTIVE - Defines validation gate placement and behavior