# Research Inheritance Template System

## Overview
This system enables CSS-like inheritance where project-specific research inherits from general research, with clear override capabilities and mapping relationships.

## Inheritance Rules

### 1. Default Inheritance
- All projects inherit from `general/` by default
- Project-specific research overrides general research for the same topic
- Overrides are explicit and tracked in this file

### 2. Override Syntax
```yaml
project_name:
  inherits_from: general
  overrides:
    - topic: "authentication"
      reason: "Project uses custom OAuth implementation"
      general_file: "general/auth/oauth.md"
      project_file: "projects/myapp/_project-research/auth-custom.md"
      confidence: 0.85
    - topic: "database"
      reason: "Project uses PostgreSQL instead of MongoDB"
      general_file: "general/db/mongodb.md"
      project_file: "projects/myapp/_project-research/postgresql.md"
      confidence: 0.90
```

### 3. Cascading Priority
1. **Project-specific research** (highest priority)
2. **General research** (fallback)
3. **Base documentation** (lowest priority)

## Template Structure

### General Research Template
```markdown
# [Technology Name] - General Research

## Overview
Brief description of technology and use cases

## Key Concepts
- Core concepts that apply across projects
- Universal patterns and best practices
- Common gotchas and solutions

## Implementation Patterns
- Reusable code patterns
- Configuration templates
- Integration approaches

## Quality Score: 0.XX
**Inheritance**: Base knowledge for all projects
**Overrides**: None (this is the base)
**Projects Using**: [list of projects that inherit this]

## Research Sources
- [Official documentation links]
- [API references]
- [Key examples]

## Tags
#general #[technology] #base-knowledge
```

### Project-Specific Research Template
```markdown
# [Technology Name] - [Project Name] Research

## Project Context
Brief description of how this technology fits into the specific project

## Inheritance
**Inherits from**: `general/[technology]/[file].md`
**Override reason**: Why project-specific research is needed
**Confidence**: 0.XX (≥0.75 for project research)

## Project-Specific Adaptations
- Deviations from general patterns
- Project-specific configuration
- Custom implementations
- Integration with project architecture

## Override Details
### What's Different
- Specific differences from general research
- Rationale for each deviation
- Impact on project architecture

### What's Inherited
- General concepts still applicable
- Base patterns being extended
- Shared best practices

## Quality Score: 0.XX
**Inheritance**: Extends `general/[technology]/[file].md`
**Overrides**: [list of specific overrides]
**Project**: [project-name]

## Research Sources
- [Project-specific documentation]
- [Custom implementation examples]
- [Integration notes]

## Tags
#project-specific #[project-name] #[technology] #override
```

## Inheritance Mapping

### Active Inheritance Chains
```yaml
# Current project inheritance relationships
inheritance_map:
  
  # Example structure (populate as projects are created)
  example_project:
    inherits_from: general
    overrides:
      - topic: "authentication"
        general_source: "general/auth/oauth.md"
        project_source: "projects/example/_project-research/auth-custom.md"
        inheritance_type: "full_override"
        confidence: 0.85
      - topic: "database"
        general_source: "general/db/mongodb.md"
        project_source: "projects/example/_project-research/postgresql.md"
        inheritance_type: "technology_swap"
        confidence: 0.90
    
    # Successful inheritances (no override needed)
    inherited_unchanged:
      - "general/api/rest-patterns.md"
      - "general/testing/unit-test-patterns.md"
      - "general/deployment/docker-patterns.md"
```

### Inheritance Types
1. **full_override**: Complete replacement of general research
2. **technology_swap**: Same concept, different technology
3. **extension**: Adds to general research without replacing
4. **configuration**: Same tech, different configuration
5. **integration**: Adapts general patterns for specific project context

## Quality Control

### Inheritance Validation
- Project research must justify overrides with confidence ≥0.75
- General research must maintain quality ≥0.90
- Override rationale must be documented
- Inheritance chains must be traceable

### Promotion Rules
When project research achieves high quality (≥0.90) and applies to multiple projects:
1. **Auto-promotion candidate**: Flag for review
2. **Generalization**: Extract project-specific elements
3. **General research update**: Enhance base knowledge
4. **Project research adjustment**: Update to inherit from enhanced general

## Symlink Management

### Symlink Structure
```
general/
├── auth/
│   └── oauth.md -> ../../_knowledge-base/auth/oauth-general.md
├── db/
│   └── mongodb.md -> ../../_knowledge-base/db/mongodb-general.md

projects/
├── myapp/
│   └── _project-research/
│       ├── auth-custom.md -> ../../../_knowledge-base/auth/oauth-myapp.md
│       └── postgresql.md -> ../../../_knowledge-base/db/postgresql-myapp.md
```

### Symlink Inheritance Rules
- General symlinks point to `_knowledge-base/[topic]/[tech]-general.md`
- Project symlinks point to `_knowledge-base/[topic]/[tech]-[project].md`
- Inheritance tracking maintains relationships between files

## Usage Commands

### Research Inheritance Commands
```bash
# Create new project research with inheritance
/research new-project [project-name] [technology] --inherits-from general/[tech]

# Override general research for specific project
/research override [project-name] [technology] --reason "Custom implementation"

# Promote project research to general
/research promote [project-name]/[technology] --to general

# View inheritance chain
/research inheritance [project-name] [technology]
```

### Validation Commands
```bash
# Validate inheritance consistency
/research validate-inheritance [project-name]

# Check for promotion candidates
/research promotion-candidates

# Update inheritance mappings
/research update-inheritance-map
```

## Integration with Research Engine

### Auto-Detection
- System automatically detects when project research overrides general
- Flags potential promotions when project research reaches 0.90+
- Suggests inheritance optimizations

### Pattern Recognition
- Identifies common override patterns across projects
- Suggests general research enhancements
- Detects inheritance anti-patterns

### Quality Scoring
- Inheritance quality considers both override rationale and implementation
- Bonus points for well-documented inheritance chains
- Penalties for unnecessary overrides

## Best Practices

### When to Override
1. **Technology differences**: Using different tech stack
2. **Project constraints**: Specific requirements or limitations
3. **Custom implementations**: Unique business logic
4. **Integration needs**: Specific architectural requirements

### When to Inherit
1. **Standard patterns**: Common implementation approaches
2. **Best practices**: Proven methodologies
3. **Configuration**: Standard setup procedures
4. **Testing**: Reusable test patterns

### Maintenance
- Regular review of inheritance chains
- Cleanup of unused overrides
- Consolidation of common patterns
- Documentation of inheritance decisions

---

**System Integration**: This inheritance system integrates with the research engine's scoring, validation, and pattern detection systems to create a comprehensive knowledge management framework.

**Quality Assurance**: All inheritance relationships are tracked, validated, and optimized through the research engine's intelligence layer.