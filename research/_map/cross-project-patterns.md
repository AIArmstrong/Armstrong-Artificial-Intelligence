# Cross-Project Patterns

## Purpose
Detect and track patterns that appear across multiple projects for auto-promotion to general knowledge.

## Detection Rules
- **Pattern emerges**: Similar approach found in 2+ projects
- **Auto-promote**: Pattern confirmed in 3+ projects with 0.90+ confidence
- **Archive**: Pattern deprecated when better approach found

## Discovered Patterns

### Initial State
*No patterns detected yet - system will identify reusable patterns as projects complete.*

## Pattern Template

### [Pattern Name] (Found in X projects)
- **Projects**: project-1, project-2, project-3
- **Pattern**: Brief description of the common approach
- **Status**: monitoring | ready-for-promotion | promoted | deprecated
- **Confidence**: 0.XX (based on usage success and consistency)
- **Promoted to**: general/[topic]/[pattern].md (if promoted)

## Auto-Promotion Pipeline
1. **Detection**: Pattern found in 2+ projects
2. **Monitoring**: Track usage and effectiveness
3. **Validation**: Confirm pattern in 3+ projects
4. **Promotion**: Move to general knowledge
5. **Linking**: Update project inheritance to reference general pattern

## Examples of Patterns to Watch For
- Authentication flows
- Error handling strategies
- Configuration management
- Testing approaches
- Deployment patterns
- API integration methods

---
*Pattern recognition for emergent knowledge extraction*