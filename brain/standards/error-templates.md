# AAI Error Templates and Recovery Actions v1.0

## Purpose
Standardize error messages and recovery actions across all AAI commands for consistent user experience and effective error resolution.

## Error Template Structure

### Standard Error Format
```yaml
error_template_structure:
  header: "BLOCKING ERROR: [Clear description of what went wrong]"
  context: "[Why this error occurred and why it's blocking]"
  required_actions: "[Numbered list of specific actions to resolve]"
  prevention: "[How to prevent this error in the future]"
  escalation: "[When to seek additional help]"
```

## System-Level Error Templates

### Claude.md Loading Failures
```yaml
claude_md_not_found:
  header: "BLOCKING ERROR: Claude.md file not found or inaccessible"
  context: "The system brain file at /mnt/c/Users/Brandon/AAI/brain/Claude.md is required before any command execution. This file contains critical system intelligence and execution protocols."
  required_actions:
    1: "Verify the file exists at /mnt/c/Users/Brandon/AAI/brain/Claude.md"
    2: "Check file permissions and ensure read access"
    3: "If file is missing, restore from brain/logs/archives/"
    4: "Verify file content is not corrupted"
  prevention: "Regular automated backups are maintained in brain/logs/archives/"
  escalation: "If file cannot be restored, contact system administrator"

claude_md_corrupted:
  header: "BLOCKING ERROR: Claude.md content is corrupted or invalid"
  context: "The Claude.md file exists but contains invalid content that cannot be parsed. This prevents system intelligence from loading properly."
  required_actions:
    1: "Check file encoding (should be UTF-8)"
    2: "Validate markdown syntax and YAML frontmatter"
    3: "Compare with recent backup in brain/logs/archives/"
    4: "Restore from most recent valid backup if needed"
  prevention: "Validate Claude.md syntax before any modifications"
  escalation: "If all backups are corrupted, system rebuild may be required"
```

### Standards Loading Failures
```yaml
standards_folder_missing:
  header: "BLOCKING ERROR: brain/standards/ folder not found"
  context: "The standards folder contains critical command execution protocols. Without these files, commands cannot execute reliably."
  required_actions:
    1: "Create brain/standards/ directory"
    2: "Populate with required files: command-protocols.md, validation-gates.md, intelligence-defaults.md, error-templates.md"
    3: "Verify all standards files have proper content"
    4: "Test standards loading functionality"
  prevention: "Ensure standards folder is included in system backups"
  escalation: "Use PRP aai-roman-command-upgrade to recreate standards architecture"

standards_file_missing:
  header: "BLOCKING ERROR: Required standards file missing: {filename}"
  context: "One or more critical standards files are missing. Each file defines essential execution protocols for reliable command operation."
  required_actions:
    1: "Identify missing file: {filename}"
    2: "Create missing file with proper structure"
    3: "Populate with required protocol definitions"
    4: "Validate file loading and parsing"
  prevention: "Maintain complete standards file set and regular backups"
  escalation: "Reference AAI documentation for proper standards file structure"
```

### Dashboard Update Failures
```yaml
dashboard_outdated:
  header: "BLOCKING ERROR: Dashboard must be current before new task execution"
  context: "The system dashboard at dashboards/status.md is more than 5 minutes old. Current dashboard state is required to prevent execution conflicts and ensure proper task tracking."
  required_actions:
    1: "Open /mnt/c/Users/Brandon/AAI/dashboards/status.md"
    2: "Update with current system state and timestamp"
    3: "Log the new task initiation"
    4: "Verify dashboard reflects accurate system status"
  prevention: "Dashboard auto-update can be enabled in system settings"
  escalation: "If dashboard cannot be updated, check file permissions"

dashboard_write_failed:
  header: "BLOCKING ERROR: Cannot write to dashboard file"
  context: "The dashboard file exists but cannot be updated. This prevents proper task tracking and system state management."
  required_actions:
    1: "Check file permissions for dashboards/status.md"
    2: "Verify disk space availability"
    3: "Test file write access"
    4: "Clear any file locks if present"
  prevention: "Ensure dashboard directory has proper write permissions"
  escalation: "Check system disk space and file system integrity"
```

## Command-Specific Error Templates

### Generate-PRP Error Templates
```yaml
insufficient_research_depth:
  header: "BLOCKING ERROR: Research depth insufficient for quality PRP generation"
  context: "PRP generation requires comprehensive research (minimum 30 pages) to ensure accuracy and completeness. Current research depth: {current_pages} pages."
  required_actions:
    1: "Continue Jina API scraping to reach minimum 30 pages"
    2: "Focus on official documentation sources (>80% official)"
    3: "Verify research quality score meets 90% threshold"
    4: "Cross-reference findings across multiple sources"
  prevention: "Set research targets before beginning scraping process"
  escalation: "If official sources unavailable, document limitations in PRP"

user_requirements_incomplete:
  header: "BLOCKING ERROR: User requirements insufficient for PRP generation"
  context: "Complete and detailed requirements are necessary to generate accurate PRP. Missing or unclear requirements lead to inadequate project planning."
  required_actions:
    1: "Gather detailed feature specifications"
    2: "Define technical requirements and constraints"
    3: "Clarify integration points and dependencies"
    4: "Confirm success criteria and acceptance tests"
  prevention: "Use requirements gathering template for completeness"
  escalation: "Schedule requirements review session with stakeholders"

prp_quality_below_threshold:
  header: "BLOCKING ERROR: Generated PRP quality below acceptable standards"
  context: "PRP quality score: {quality_score}%. Minimum required: 90%. Quality issues identified: {issues_list}"
  required_actions:
    1: "Review and enhance incomplete sections"
    2: "Verify technical accuracy of all recommendations"
    3: "Add missing implementation details"
    4: "Improve clarity of execution steps"
  prevention: "Use PRP quality checklist during generation"
  escalation: "Consider breaking complex PRP into smaller, focused PRPs"
```

### Implementation Error Templates
```yaml
implementation_plan_not_approved:
  header: "BLOCKING ERROR: Implementation plan requires user approval before coding"
  context: "Major implementation changes require explicit user approval to ensure alignment with requirements and expectations."
  required_actions:
    1: "Present complete implementation plan to user"
    2: "Explain technical approach and rationale"
    3: "Confirm resource requirements and timeline"
    4: "Get explicit approval before proceeding"
  prevention: "Always present implementation plan before beginning code"
  escalation: "If plan is rejected, revise approach and re-present"

code_quality_standards_failed:
  header: "BLOCKING ERROR: Generated code fails quality standards"
  context: "Code quality score: {quality_score}%. Minimum required: 90%. Issues: {issues_list}"
  required_actions:
    1: "Fix syntax errors and style violations"
    2: "Address security vulnerabilities"
    3: "Improve code documentation and comments"
    4: "Increase test coverage to minimum 80%"
  prevention: "Use code quality checkers during development"
  escalation: "Consider refactoring approach if quality issues persist"

test_failures:
  header: "BLOCKING ERROR: Tests failing - deployment blocked"
  context: "Test failures prevent safe deployment. Failing tests: {failed_tests_list}"
  required_actions:
    1: "Analyze each failing test individually"
    2: "Fix code issues causing test failures"
    3: "Update tests if requirements changed"
    4: "Verify all tests pass before proceeding"
  prevention: "Run tests continuously during development"
  escalation: "If tests cannot be fixed, review implementation approach"
```

### Analysis Error Templates
```yaml
analysis_scope_undefined:
  header: "BLOCKING ERROR: Analysis scope must be clearly defined"
  context: "Effective analysis requires clear scope definition. Undefined scope leads to incomplete or irrelevant analysis results."
  required_actions:
    1: "Define specific analysis targets and boundaries"
    2: "Specify required analysis depth and focus areas"
    3: "Clarify expected deliverables and format"
    4: "Confirm analysis timeline and resource requirements"
  prevention: "Use analysis scoping template for consistency"
  escalation: "Break large analysis into smaller, focused analyses"

analysis_agents_failed:
  header: "BLOCKING ERROR: Analysis agents failed to complete successfully"
  context: "One or more analysis agents encountered errors. Failed agents: {failed_agents_list}"
  required_actions:
    1: "Review error logs for each failed agent"
    2: "Retry failed agents with adjusted parameters"
    3: "Verify analysis targets are accessible"
    4: "Ensure sufficient system resources available"
  prevention: "Monitor agent resource usage during analysis"
  escalation: "Consider reducing analysis scope if agents continue failing"

insufficient_analysis_confidence:
  header: "BLOCKING ERROR: Analysis confidence below minimum threshold"
  context: "Analysis confidence: {confidence_score}%. Minimum required: 85%. Low confidence indicates insufficient data or analysis depth."
  required_actions:
    1: "Gather additional data sources for analysis"
    2: "Increase analysis depth and coverage"
    3: "Cross-validate findings across multiple methods"
    4: "Document confidence limitations if threshold cannot be met"
  prevention: "Set confidence targets before beginning analysis"
  escalation: "Consider qualitative analysis if quantitative confidence low"
```

## Intelligence Layer Error Templates

### Memory Layer Errors
```yaml
memory_loading_failed:
  header: "WARNING: Memory layer failed to load previous context"
  context: "The memory enhancement system could not load previous patterns and context. This may reduce command effectiveness but won't block execution."
  required_actions:
    1: "Check memory storage connectivity"
    2: "Verify memory cache integrity"
    3: "Clear corrupted memory cache if needed"
    4: "Continue with fresh context if necessary"
  prevention: "Regular memory cache maintenance and backups"
  escalation: "Memory system may need rebuild if issues persist"

memory_storage_full:
  header: "WARNING: Memory storage approaching capacity limits"
  context: "Memory storage: {usage_percentage}% full. This may impact learning and context retention capabilities."
  required_actions:
    1: "Archive old memory contexts to long-term storage"
    2: "Clean up temporary memory files"
    3: "Optimize memory usage patterns"
    4: "Consider expanding memory storage capacity"
  prevention: "Enable automatic memory archiving and cleanup"
  escalation: "Manual memory management may be required"
```

### Research Layer Errors
```yaml
jina_api_failure:
  header: "BLOCKING ERROR: Jina API research system unavailable"
  context: "The Jina API is required for comprehensive research but is currently unavailable. This prevents meeting research quality standards."
  required_actions:
    1: "Check Jina API connectivity and credentials"
    2: "Verify API rate limits and quota availability"
    3: "Test API with simple request to diagnose issue"
    4: "Use alternative research methods if API unavailable"
  prevention: "Monitor Jina API status and implement fallback methods"
  escalation: "Contact Jina API support if service issues persist"

research_quality_insufficient:
  header: "BLOCKING ERROR: Research quality below standards for task requirements"
  context: "Research quality: {quality_score}%. Required: 90%. Quality issues: {quality_issues}"
  required_actions:
    1: "Focus on official documentation sources"
    2: "Increase source diversity and cross-referencing"
    3: "Verify information accuracy and recency"
    4: "Expand research depth to meet quality standards"
  prevention: "Set quality targets before beginning research"
  escalation: "Consider manual research supplement if automated quality insufficient"
```

## Recovery Action Templates

### Automatic Recovery Actions
```yaml
claude_md_auto_recovery:
  trigger: "claude_md_loading_failed"
  actions:
    1: "Attempt reload from current location"
    2: "Try loading from most recent backup"
    3: "Verify file integrity and permissions"
    4: "Report success/failure to user"
  
dashboard_auto_update:
  trigger: "dashboard_outdated"
  actions:
    1: "Read current dashboard state"
    2: "Update timestamp and system status"
    3: "Log current task initiation"
    4: "Verify update successful"

research_quality_auto_enhancement:
  trigger: "research_quality_insufficient"
  actions:
    1: "Identify specific quality gaps"
    2: "Target additional official sources"
    3: "Cross-reference findings for accuracy"
    4: "Re-evaluate quality score"
```

### User-Guided Recovery Actions
```yaml
requirements_gathering_guided:
  trigger: "user_requirements_incomplete"
  process:
    1: "Present requirements template to user"
    2: "Ask specific clarifying questions"
    3: "Confirm understanding of requirements"
    4: "Document complete requirements for future reference"

implementation_plan_review:
  trigger: "implementation_plan_not_approved"
  process:
    1: "Present detailed implementation plan"
    2: "Explain technical approach and alternatives"
    3: "Discuss resource and timeline implications"
    4: "Incorporate user feedback and get approval"
```

## Error Escalation Matrix

### Escalation Levels
```yaml
level_1_automatic:
  description: "System attempts automatic recovery"
  examples: ["file_reload", "cache_clear", "service_retry"]
  timeout: "30 seconds"
  
level_2_user_notification:
  description: "User notified with recovery options"
  examples: ["missing_requirements", "quality_threshold_failures"]
  user_response_timeout: "5 minutes"
  
level_3_manual_intervention:
  description: "Manual intervention required"
  examples: ["system_corruption", "service_unavailable"]
  escalation_contacts: ["system_administrator", "technical_support"]
  
level_4_system_rebuild:
  description: "System component rebuild required"
  examples: ["standards_architecture_missing", "core_system_corruption"]
  recovery_documentation: "AAI system rebuild procedures"
```

---

**Version**: 1.0  
**Last Updated**: 2025-01-23  
**Integration**: Works with validation-gates.md and command-protocols.md  
**Coverage**: System-level, command-specific, and intelligence layer errors  
**Status**: ACTIVE - Defines standardized error handling across AAI system