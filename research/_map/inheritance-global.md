# Global Inheritance Rules

## Purpose
Master registry of all inheritance relationships between general research and project-specific overrides.

## Inheritance Model
Like CSS cascading: General research = base layer, Project research = override layer

## Global Rules

### Resolution Order
1. **Check general/** first for base knowledge
2. **Apply project overrides** in order specified
3. **Log conflicts** in validation/contradictions.md
4. **Update inheritance maps** when conflicts resolved

### Override Types
- **EXTENDS**: Project research adds to general knowledge
- **OVERRIDES**: Project research replaces section of general knowledge  
- **SPECIALIZES**: Project research provides domain-specific implementation
- **CONFLICTS**: Project research contradicts general knowledge (needs resolution)

## Active Inheritance Maps

### Initial State
*No inheritance relationships established yet - maps will be created as projects develop.*

## Project Inheritance Registry

### Template
```
Project: [project-name]
Inheritance File: research/projects/[project-name]/inheritance.md
Base Dependencies: 
  - general/[topic1]/[file1].md
  - general/[topic2]/[file2].md
Override Types:
  - [file].md EXTENDS general/[topic]/[base].md
  - [file].md OVERRIDES section X.X of general/[topic]/[base].md
Last Updated: [timestamp]
```

## Conflict Resolution
When project research conflicts with general knowledge:
1. **Investigate** - Determine which is more accurate/current
2. **Update** - Correct the outdated information
3. **Propagate** - Update all affected projects
4. **Document** - Log resolution in contradictions.md

---
*Master inheritance coordination for consistent knowledge management*