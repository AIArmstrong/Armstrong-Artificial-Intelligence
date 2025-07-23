# AAI Execution Control Standards v1.0

## Purpose
Define XML-based execution control patterns and metadata standards for AAI Roman command architecture. Ensures structured, reliable command execution with proper validation and user approval gates.

## XML Metadata Standards

### Core XML Structure
```xml
<!-- Standard XML structure for AAI command instructions -->
<ai_meta>
  <parsing_rules>
    <!-- How AI should process the instruction file -->
  </parsing_rules>
  <aai_intelligence>
    <!-- Intelligence layer activation specifications -->
  </aai_intelligence>
  <standards_integration>
    <!-- References to brain/standards/ files -->
  </standards_integration>
</ai_meta>

<process_flow>
  <!-- Sequential step execution with metadata -->
  <step number="1" name="step_identifier">
    <step_metadata>
      <!-- Step requirements and outputs -->
    </step_metadata>
    <prerequisite_validation>
      <!-- Validation checks before step execution -->
    </prerequisite_validation>
    <instructions>
      <!-- Execution instructions with control directives -->
    </instructions>
  </step>
</process_flow>
```

### AI Meta Block Standards
```xml
<ai_meta>
  <parsing_rules>
    - Process XML blocks first for structured data
    - Execute instructions in sequential order  
    - Load Claude.md before ANY execution
    - Update dashboard after EVERY step
    - Use blocking validations for critical checkpoints
    - Reference brain/standards/ for protocol enforcement
  </parsing_rules>
  
  <aai_intelligence>
    <!-- Define which of the 8 intelligence layers to activate -->
    - MEMORY: {memory_focus}
    - RESEARCH: {research_requirements}
    - HYBRID_RAG: {knowledge_synthesis_needs}
    - REASONING: {reasoning_requirements}
    - TOOL_SELECTION: {tool_optimization_focus}
    - ORCHESTRATION: {coordination_needs}
    - ARCHITECTURE: {technical_guidance_needs}
    - FOUNDATION: {quality_standards}
  </aai_intelligence>
  
  <standards_integration>
    - Load brain/standards/command-protocols.md for execution rules
    - Apply brain/standards/validation-gates.md for checkpoint definitions
    - Reference brain/standards/error-templates.md for consistent messaging
    - Follow brain/standards/intelligence-defaults.md for smart module loading
  </standards_integration>
</ai_meta>
```

### Step Metadata Standards
```xml
<step_metadata>
  <prerequisites>
    <!-- What must be true before this step can execute -->
    - {prerequisite_name}: {condition}
    - {system_state}: {required_value}
  </prerequisites>
  
  <validation>{validation_type}</validation>
  <!-- blocking | verified | warning | user_approval -->
  
  <creates>{output_identifier}</creates>
  <!-- What this step produces for later steps -->
  
  <requires>{input_identifier}</requires>
  <!-- What this step needs from previous steps -->
  
  <timeout>{duration}</timeout>
  <!-- Maximum execution time -->
  
  <retry_attempts>{number}</retry_attempts>
  <!-- Number of retry attempts on failure -->
</step_metadata>
```

## Validation Control Types

### Blocking Validations
```xml
<!-- BLOCKING: Execution cannot continue until resolved -->
<validation>blocking</validation>

<!-- Used for: -->
<!-- - System prerequisites (Claude.md loaded, standards loaded) -->
<!-- - Critical quality gates (minimum quality scores) -->
<!-- - Safety requirements (backups verified, rollback ready) -->
<!-- - Resource availability (APIs accessible, services running) -->

<!-- Example Implementation: -->
<prerequisite_validation>
  <check name="claude_md_loaded">
    <condition>memory.claude_md_content != null</condition>
    <error_template>
      BLOCKING ERROR: Claude.md must be loaded before execution.
      
      Required Actions:
      1. Read /mnt/c/Users/Brandon/AAI/brain/Claude.md
      2. Load brain/standards/command-protocols.md
      3. Load brain/standards/intelligence-defaults.md
      4. Confirm system readiness before proceeding
    </error_template>
  </check>
</prerequisite_validation>
```

### User Approval Gates
```xml
<!-- USER_APPROVAL: Requires explicit user confirmation -->
<validation>user_approval</validation>

<!-- Used for: -->
<!-- - Major architectural changes -->
<!-- - Resource-intensive operations -->
<!-- - Breaking changes to existing code -->
<!-- - External service integrations -->

<!-- Example Implementation: -->
<approval_gate>
  I've analyzed your requirements and prepared the following implementation plan:
  
  [IMPLEMENTATION_PLAN_SUMMARY]
  
  This approach will:
  - {benefit_1}
  - {benefit_2}
  - {potential_risk_1} (mitigation: {mitigation_strategy})
  
  Please confirm this approach is acceptable before I proceed with implementation.
  
  Type "approved" to continue or provide feedback for adjustments.
</approval_gate>
```

### Verified Validations
```xml
<!-- VERIFIED: Check completion but don't block -->
<validation>verified</validation>

<!-- Used for: -->
<!-- - Optional enhancements -->
<!-- - Performance optimizations -->
<!-- - Best practice implementations -->
<!-- - Documentation completeness -->

<!-- Example Implementation: -->
<completion_verification>
  <check name="intelligence_layers_active">
    <condition>required_layers.all_activated == true</condition>
    <success_action>LOG: All required intelligence layers activated successfully</success_action>
    <failure_action>WARN: Some intelligence layers failed to activate - continuing with available layers</failure_action>
  </check>
</completion_verification>
```

### Warning Validations
```xml
<!-- WARNING: Generate warnings but continue execution -->
<validation>warning</validation>

<!-- Used for: -->
<!-- - Best practice violations -->
<!-- - Sub-optimal approaches -->
<!-- - Missing optimizations -->
<!-- - Documentation gaps -->

<!-- Example Implementation: -->
<warning_check>
  <check name="test_coverage">
    <condition>code_coverage >= 0.80</condition>
    <warning_message>
      WARNING: Test coverage below recommended 80% (current: {coverage_percentage}%)
      Consider adding tests for: {uncovered_functions}
    </warning_message>
  </check>
</warning_check>
```

## Instruction Control Directives

### ACTION Directive
```xml
<!-- ACTION: Execute specific operation -->
<instructions>
  ACTION: {specific_action_to_take}
  CONTEXT: {why_this_action_is_needed}
  SUCCESS_CRITERIA: {how_to_know_action_succeeded}
</instructions>

<!-- Examples: -->
<!-- ACTION: Validate all system prerequisites -->
<!-- ACTION: Generate implementation code with quality validation -->
<!-- ACTION: Synthesize research findings into actionable insights -->
```

### WAIT Directive
```xml
<!-- WAIT: Pause for user input or external event -->
<instructions>
  WAIT: {what_to_wait_for}
  TIMEOUT: {maximum_wait_time}
  FALLBACK: {what_to_do_if_timeout}
</instructions>

<!-- Examples: -->
<!-- WAIT: For user confirmation before proceeding -->
<!-- WAIT: For external API response (timeout: 30 seconds) -->
<!-- WAIT: For required file to become available -->
```

### BLOCK Directive
```xml
<!-- BLOCK: Stop execution until condition met -->
<instructions>
  BLOCK: {blocking_condition}
  REASON: {why_blocking_is_necessary}
  RESOLUTION: {how_to_resolve_block}
</instructions>

<!-- Examples: -->
<!-- BLOCK: Do not proceed without all validations passing -->
<!-- BLOCK: Cannot continue until user approves implementation plan -->
<!-- BLOCK: Insufficient research quality - cannot generate reliable PRP -->
```

### VERIFY Directive
```xml
<!-- VERIFY: Check condition and log result -->
<instructions>
  VERIFY: {condition_to_check}
  SUCCESS_ACTION: {what_to_do_if_verified}
  FAILURE_ACTION: {what_to_do_if_verification_fails}
</instructions>

<!-- Examples: -->
<!-- VERIFY: Each intelligence layer confirms readiness -->
<!-- VERIFY: All tests pass before deployment -->
<!-- VERIFY: Generated code meets quality standards -->
```

### LOG Directive
```xml
<!-- LOG: Record execution state and progress -->
<instructions>
  LOG: {what_to_log}
  DESTINATION: {where_to_log}
  LEVEL: {log_level}
</instructions>

<!-- Examples: -->
<!-- LOG: System initialization status to execution state -->
<!-- LOG: Intelligence activation status with layer details -->
<!-- LOG: Completion status and quality metrics -->
```

## Command-Specific XML Templates

### Generate-PRP XML Template
```xml
<step number="1" name="system_initialization">
  <step_metadata>
    <prerequisites>
      - claude_md_loaded: true
      - standards_loaded: true
      - dashboard_current: true
      - user_input_validated: true
    </prerequisites>
    <validation>blocking</validation>
    <creates>system_context</creates>
    <timeout>60_seconds</timeout>
    <retry_attempts>3</retry_attempts>
  </step_metadata>
  
  <prerequisite_validation>
    <check name="claude_md_loaded">
      <condition>memory.claude_md_content != null</condition>
      <error_template>@ref brain/standards/error-templates.md#claude_md_not_found</error_template>
    </check>
    <check name="standards_loaded">
      <condition>standards.all_loaded == true</condition>
      <error_template>@ref brain/standards/error-templates.md#standards_folder_missing</error_template>
    </check>
  </prerequisite_validation>
  
  <instructions>
    ACTION: Validate all system prerequisites
    BLOCK: Do not proceed without all validations passing
    LOG: Record system initialization in execution state
    VERIFY: System ready for PRP generation workflow
  </instructions>
</step>

<step number="2" name="intelligence_activation">
  <step_metadata>
    <requires>system_initialization.complete</requires>
    <activates>
      - MEMORY: PRP pattern recognition
      - RESEARCH: Documentation scraping preparation  
      - REASONING: Analysis framework setup
      - HYBRID_RAG: Knowledge synthesis preparation
      - TOOL_SELECTION: Optimal tool chain selection
    </activates>
    <validation>verified</validation>
    <creates>intelligence_context</creates>
  </step_metadata>
  
  <intelligence_activation>
    <memory_layer>
      - Load successful PRP patterns from examples/
      - Recall user preferences and team patterns
      - Identify anti-patterns to avoid
    </memory_layer>
    <research_layer>
      - Prepare Jina API for documentation scraping
      - Initialize multi-source research coordination
      - Set quality thresholds (≥30 pages, ≥95% confidence)
    </research_layer>
  </intelligence_activation>
  
  <instructions>
    ACTION: Activate all required intelligence layers
    VERIFY: Each layer confirms readiness
    LOG: Intelligence activation status to execution state
  </instructions>
</step>
```

### Implementation XML Template
```xml
<step number="1" name="implementation_plan_review">
  <step_metadata>
    <requires>system_initialization.complete</requires>
    <validation>user_approval</validation>
    <creates>approved_implementation_plan</creates>
  </step_metadata>
  
  <approval_gate>
    Based on your requirements, I've prepared this implementation plan:
    
    **Technical Approach**: {approach_summary}
    **Architecture Decisions**: {key_architectural_choices}
    **Technology Stack**: {selected_technologies}
    **Implementation Phases**: {phase_breakdown}
    **Quality Standards**: {quality_requirements}
    **Testing Strategy**: {testing_approach}
    **Timeline Estimate**: {estimated_timeline}
    
    This approach balances {trade_off_explanation}.
    
    Please review and confirm this plan before I begin implementation.
    Type "approved" to proceed or provide feedback for adjustments.
  </approval_gate>
  
  <instructions>
    ACTION: Present implementation plan to user
    WAIT: For user approval before proceeding
    BLOCK: Do not begin coding without explicit approval
    LOG: Implementation plan approval status
  </instructions>
</step>

<step number="2" name="code_generation">
  <step_metadata>
    <requires>approved_implementation_plan</requires>
    <validation>blocking</validation>
    <creates>implementation_code</creates>
  </step_metadata>
  
  <quality_validation>
    <check name="code_quality">
      <condition>quality_score >= 0.90</condition>
      <error_template>@ref brain/standards/error-templates.md#code_quality_standards_failed</error_template>
    </check>
    <check name="security_standards">
      <condition>security_validation_passed == true</condition>
      <error_template>Security validation failed - address vulnerabilities before proceeding</error_template>
    </check>
  </quality_validation>
  
  <instructions>
    ACTION: Generate implementation code with quality validation
    VERIFY: Code meets all quality and security standards
    BLOCK: Do not proceed if quality gates fail
    LOG: Code generation results and quality metrics
  </instructions>
</step>
```

## Error Handling Integration

### Error Template References
```xml
<!-- Reference standardized error templates -->
<error_template>@ref brain/standards/error-templates.md#{template_id}</error_template>

<!-- Examples: -->
<error_template>@ref brain/standards/error-templates.md#claude_md_not_found</error_template>
<error_template>@ref brain/standards/error-templates.md#insufficient_research_depth</error_template>
<error_template>@ref brain/standards/error-templates.md#implementation_plan_not_approved</error_template>
```

### Custom Error Templates
```xml
<!-- Define custom error template when standard ones don't apply -->
<error_template>
  BLOCKING ERROR: {specific_error_description}
  
  Context: {why_this_error_occurred}
  
  Required Actions:
  1. {specific_action_1}
  2. {specific_action_2}
  3. {specific_action_3}
  
  Prevention: {how_to_prevent_future_occurrences}
  
  Escalation: {when_to_seek_additional_help}
</error_template>
```

## Performance and Optimization Standards

### Execution Efficiency
```xml
<!-- Optimize XML processing for performance -->
<step_metadata>
  <parallel_execution>true</parallel_execution>
  <!-- Allow this step to run in parallel with others -->
  
  <cache_results>true</cache_results>
  <!-- Cache step results for reuse -->
  
  <lazy_loading>true</lazy_loading>
  <!-- Load resources only when needed -->
</step_metadata>
```

### Resource Management
```xml
<!-- Manage system resources during execution -->
<resource_requirements>
  <memory_limit>256MB</memory_limit>
  <cpu_cores>2</cpu_cores>
  <execution_time_limit>300_seconds</execution_time_limit>
  <api_rate_limit>requests_per_minute: 60</api_rate_limit>
</resource_requirements>
```

## Integration with Brain/Standards

### Standards File Loading Order
```xml
<standards_integration>
  <!-- Load standards in dependency order -->
  1: "brain/standards/command-protocols.md"      <!-- Core execution rules -->
  2: "brain/standards/validation-gates.md"       <!-- Validation definitions -->
  3: "brain/standards/intelligence-defaults.md"  <!-- Smart module loading -->
  4: "brain/standards/error-templates.md"        <!-- Error handling -->
  5: "brain/standards/execution-control.md"      <!-- XML processing rules -->
</standards_integration>
```

### Cross-Reference Syntax
```xml
<!-- Reference other standards files -->
@ref brain/standards/{filename}.md#{section_id}

<!-- Examples: -->
@ref brain/standards/validation-gates.md#blocking_validations
@ref brain/standards/error-templates.md#claude_md_loading_failures
@ref brain/standards/intelligence-defaults.md#generate_prp_intelligence
```

---

**Version**: 1.0  
**Last Updated**: 2025-01-23  
**Integration**: Core component of AAI Roman command architecture  
**Dependencies**: All other brain/standards/ files  
**Status**: ACTIVE - Defines XML execution control patterns for reliable command execution