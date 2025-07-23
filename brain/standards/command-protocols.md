# AAI Command Execution Protocols v1.0

## Purpose
Define core command execution protocols for AAI system reliability and consistency. This file ensures 99% protocol adherence through structured execution patterns.

## Mandatory Pre-Execution Sequence

### Phase 1: System Initialization (BLOCKING)
```yaml
required_steps:
  1. claude_md_loading:
      file: "/mnt/c/Users/Brandon/AAI/brain/Claude.md"
      validation: "content loaded and parsed successfully"
      error_action: "BLOCK execution until resolved"
      
  2. standards_loading:
      files: 
        - "brain/standards/command-protocols.md"
        - "brain/standards/validation-gates.md" 
        - "brain/standards/intelligence-defaults.md"
      validation: "all standards files loaded"
      error_action: "BLOCK execution until resolved"
      
  3. dashboard_validation:
      file: "/mnt/c/Users/Brandon/AAI/dashboards/status.md"
      requirement: "last_update < 5 minutes"
      error_action: "UPDATE dashboard then proceed"
      
  4. execution_state_init:
      requirement: "initialize command execution tracking"
      creates: "execution_context with step tracking"
```

### Phase 2: Intelligence Layer Activation
```yaml
smart_module_loading:
  memory_layer:
    trigger: "ALWAYS"
    module: "brain/modules/mem0-memory-enhancement.md"
    function: "Load command-specific patterns and user preferences"
    
  research_layer:
    trigger: "research_needed || prp_generation || documentation_tasks"
    module: "brain/modules/research-prp-integration.py"
    function: "30-100 page documentation research with Jina API"
    
  reasoning_layer:
    trigger: "decisions_required || analysis_tasks || complex_logic"
    module: "brain/modules/enhanced-repository-analyzer.py"
    function: "O1-style reasoning with 70-95% confidence scoring"
    
  tool_selection:
    trigger: "ALWAYS"  
    module: "brain/modules/smart-tool-selector.py"
    function: "Optimal tool chain selection for task"
    
  orchestration:
    trigger: "multi_step_tasks || external_services || complex_workflows"
    module: "brain/modules/seamless-orchestrator.py"
    function: "Multi-agent coordination and task delegation"
```

## Command-Specific Execution Patterns

### Generate-PRP Protocol
```yaml
execution_sequence:
  1. system_initialization: [BLOCKING]
  2. requirements_gathering: [USER_APPROVAL_REQUIRED]
  3. research_phase: [VALIDATION: min_30_pages]
  4. analysis_synthesis: [VALIDATION: confidence_score >= 85%]
  5. prp_generation: [VALIDATION: all_sections_complete]
  6. quality_review: [VALIDATION: quality_score >= 90%] 
  7. dashboard_update: [BLOCKING]
  8. completion_logging: [REQUIRED]

critical_validations:
  - Claude.md + standards loaded before execution
  - User requirements complete and approved
  - Research depth meets 30+ page minimum
  - PRP quality gates passed (90%+ score)
  - Dashboard updated with results
```

### Implement Protocol  
```yaml
execution_sequence:
  1. system_initialization: [BLOCKING]
  2. implementation_plan_review: [USER_APPROVAL_REQUIRED]
  3. persona_activation: [AUTO: based on tech stack]
  4. code_generation: [VALIDATION: quality_standards_met]
  5. testing_integration: [VALIDATION: tests_pass]
  6. security_review: [VALIDATION: security_standards_met]
  7. documentation_update: [REQUIRED]
  8. dashboard_update: [BLOCKING]
  9. completion_logging: [REQUIRED]

critical_validations:
  - Implementation plan approved by user
  - Code meets quality standards (>90% score)
  - Security validation passed
  - Tests implemented and passing
  - Documentation updated
```

### Analyze Protocol
```yaml
execution_sequence:
  1. system_initialization: [BLOCKING]
  2. analysis_scope_confirmation: [USER_APPROVAL_REQUIRED]
  3. multi_agent_deployment: [AUTO: quality, security, performance, architecture]
  4. parallel_analysis: [VALIDATION: all_agents_complete]
  5. findings_synthesis: [VALIDATION: actionable_recommendations]
  6. quality_scoring: [VALIDATION: confidence >= 85%]
  7. dashboard_update: [BLOCKING] 
  8. completion_logging: [REQUIRED]

critical_validations:
  - Analysis scope confirmed and complete
  - All analysis agents completed successfully
  - Findings synthesized into actionable recommendations
  - Quality threshold met (85%+ confidence)
  - Dashboard updated with analysis results
```

## Blocking Validation Types

### BLOCKING Validations
- **System Prerequisites**: Claude.md loaded, standards loaded, dashboard current
- **User Approvals**: Major operations, architectural changes, resource-intensive tasks
- **Quality Gates**: Minimum confidence thresholds, completeness requirements
- **Completion Requirements**: Dashboard updates, logging, state persistence

### WARNING Validations  
- **Best Practice Violations**: Sub-optimal patterns, missing optimizations
- **Performance Concerns**: Potential scalability issues, efficiency improvements
- **Maintenance Issues**: Code complexity, documentation gaps

## Error Recovery Protocols

### Three-Attempt Rule
```yaml
error_handling:
  attempt_1: "Execute with current context"
  attempt_2: "Execute with enhanced context and error analysis"
  attempt_3: "Execute with user guidance and simplified approach"
  failure_action: "BLOCK and request user intervention"
```

### Recovery Templates
```yaml
claude_md_loading_failure:
  error_message: "BLOCKING ERROR: Claude.md must be loaded before execution."
  recovery_actions:
    - "Verify file exists at /mnt/c/Users/Brandon/AAI/brain/Claude.md"
    - "Check file permissions and accessibility"
    - "Reload file contents and retry"
    - "Contact user if file is missing or corrupted"
    
standards_loading_failure:
  error_message: "BLOCKING ERROR: Standards files must be loaded before execution."
  recovery_actions:
    - "Verify brain/standards/ folder exists"
    - "Check all required standards files present"
    - "Load each standards file individually"
    - "Report specific missing files to user"
    
dashboard_outdated:
  error_message: "BLOCKING ERROR: Dashboard must be current before new task."
  recovery_actions:
    - "Update /mnt/c/Users/Brandon/AAI/dashboards/status.md"
    - "Log current task initiation with timestamp"
    - "Verify dashboard reflects current system state"
    - "Proceed only after successful update"
```

## Success Metrics

### Protocol Adherence Target: 99%
- **Critical Steps**: Zero skipped mandatory steps
- **Validation Gates**: 100% blocking validations enforced
- **User Approvals**: All required approvals obtained
- **Dashboard Updates**: 100% completion rate
- **Quality Standards**: 95%+ average quality scores

### Monitoring and Improvement
- **Execution Tracking**: Log all command executions with step completion
- **Failure Analysis**: Analyze and document all protocol failures
- **Continuous Improvement**: Update protocols based on failure patterns
- **User Feedback Integration**: Incorporate user preferences and feedback

---

**Version**: 1.0  
**Last Updated**: 2025-01-23  
**Compatibility**: AAI v3.0 Research Engine  
**Status**: ACTIVE - This file defines mandatory execution protocols