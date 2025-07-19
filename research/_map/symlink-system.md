# Symbolic Linking System

## Overview
This system creates a unified research architecture where `_knowledge-base/` serves as the single source of truth, while `general/` and `projects/` folders use symbolic links to provide organized access patterns.

## Architecture Design

### Single Source of Truth
```
_knowledge-base/
├── auth/
│   ├── oauth-general.md          # General OAuth research
│   ├── oauth-myapp.md            # MyApp-specific OAuth
│   └── oauth-webapp.md           # WebApp-specific OAuth
├── database/
│   ├── mongodb-general.md        # General MongoDB research
│   ├── postgresql-myapp.md       # MyApp PostgreSQL research
│   └── redis-general.md          # General Redis research
└── api/
    ├── rest-general.md           # General REST API research
    ├── graphql-general.md        # General GraphQL research
    └── rest-myapp.md             # MyApp REST customizations
```

### Symbolic Link Organization
```
general/
├── auth/
│   └── oauth.md -> ../../_knowledge-base/auth/oauth-general.md
├── database/
│   ├── mongodb.md -> ../../_knowledge-base/database/mongodb-general.md
│   └── redis.md -> ../../_knowledge-base/database/redis-general.md
└── api/
    ├── rest.md -> ../../_knowledge-base/api/rest-general.md
    └── graphql.md -> ../../_knowledge-base/api/graphql-general.md

projects/
├── myapp/
│   └── _project-research/
│       ├── auth.md -> ../../../../_knowledge-base/auth/oauth-myapp.md
│       ├── database.md -> ../../../../_knowledge-base/database/postgresql-myapp.md
│       └── api.md -> ../../../../_knowledge-base/api/rest-myapp.md
└── webapp/
    └── _project-research/
        └── auth.md -> ../../../../_knowledge-base/auth/oauth-webapp.md
```

## File Naming Convention

### Knowledge Base Files
- **General Research**: `[technology]-general.md`
- **Project Research**: `[technology]-[project-name].md`
- **Variant Research**: `[technology]-[variant].md`

### Symbolic Link Names
- **General Links**: `[technology].md`
- **Project Links**: `[feature].md` (semantic naming)

## Implementation Scripts

### Create Symlink System
```bash
#!/bin/bash
# research/scripts/create-symlinks.sh

# Create general symlinks
create_general_symlinks() {
    local knowledge_base="$1"
    local general_dir="$2"
    
    # Find all *-general.md files
    find "$knowledge_base" -name "*-general.md" | while read -r file; do
        # Extract category and technology
        category=$(dirname "$file" | sed "s|$knowledge_base/||")
        filename=$(basename "$file")
        technology=$(echo "$filename" | sed 's/-general\.md$//')
        
        # Create category directory in general
        mkdir -p "$general_dir/$category"
        
        # Create symlink
        link_target="../../_knowledge-base/$category/$filename"
        link_path="$general_dir/$category/$technology.md"
        
        ln -sf "$link_target" "$link_path"
        echo "Created: $link_path -> $link_target"
    done
}

# Create project symlinks
create_project_symlinks() {
    local knowledge_base="$1"
    local projects_dir="$2"
    
    # Find all project-specific files
    find "$knowledge_base" -name "*-*.md" ! -name "*-general.md" | while read -r file; do
        # Extract category, technology, and project
        category=$(dirname "$file" | sed "s|$knowledge_base/||")
        filename=$(basename "$file")
        
        # Parse project name from filename
        project=$(echo "$filename" | sed 's/.*-\([^-]*\)\.md$/\1/')
        technology=$(echo "$filename" | sed "s/-$project\.md$//" | sed 's/.*-//')
        
        # Create project directory structure
        project_dir="$projects_dir/$project/_project-research"
        mkdir -p "$project_dir"
        
        # Create symlink with semantic naming
        link_target="../../../../_knowledge-base/$category/$filename"
        link_path="$project_dir/$technology.md"
        
        ln -sf "$link_target" "$link_path"
        echo "Created: $link_path -> $link_target"
    done
}

# Main execution
RESEARCH_DIR="/mnt/c/Users/Brandon/AAI/research"
create_general_symlinks "$RESEARCH_DIR/_knowledge-base" "$RESEARCH_DIR/general"
create_project_symlinks "$RESEARCH_DIR/_knowledge-base" "$RESEARCH_DIR/projects"
```

### Update Symlinks
```bash
#!/bin/bash
# research/scripts/update-symlinks.sh

update_symlinks() {
    local research_dir="$1"
    
    echo "Updating symlink system..."
    
    # Remove existing symlinks
    find "$research_dir/general" -type l -delete
    find "$research_dir/projects" -type l -delete
    
    # Recreate symlinks
    source "$research_dir/scripts/create-symlinks.sh"
    
    echo "Symlink system updated"
}

# Main execution
RESEARCH_DIR="/mnt/c/Users/Brandon/AAI/research"
update_symlinks "$RESEARCH_DIR"
```

### Validate Symlinks
```bash
#!/bin/bash
# research/scripts/validate-symlinks.sh

validate_symlinks() {
    local research_dir="$1"
    local issues=0
    
    echo "Validating symlink system..."
    
    # Check general symlinks
    find "$research_dir/general" -type l | while read -r link; do
        if [ ! -e "$link" ]; then
            echo "BROKEN: $link"
            issues=$((issues + 1))
        fi
    done
    
    # Check project symlinks
    find "$research_dir/projects" -type l | while read -r link; do
        if [ ! -e "$link" ]; then
            echo "BROKEN: $link"
            issues=$((issues + 1))
        fi
    done
    
    if [ $issues -eq 0 ]; then
        echo "All symlinks valid"
    else
        echo "Found $issues broken symlinks"
    fi
}

# Main execution
RESEARCH_DIR="/mnt/c/Users/Brandon/AAI/research"
validate_symlinks "$RESEARCH_DIR"
```

## Management Commands

### Research File Creation
```bash
# Create new general research
/research create general [technology] --category [category]
# Creates: _knowledge-base/[category]/[technology]-general.md
# Creates: general/[category]/[technology].md -> symlink

# Create new project research
/research create project [project-name] [technology] --category [category]
# Creates: _knowledge-base/[category]/[technology]-[project].md
# Creates: projects/[project]/[technology].md -> symlink

# Create project override
/research override [project-name] [technology] --reason "Custom implementation"
# Creates: _knowledge-base/[category]/[technology]-[project].md
# Updates: projects/[project]/[technology].md -> new symlink
```

### Symlink Management
```bash
# Rebuild all symlinks
/research rebuild-symlinks

# Validate symlink integrity
/research validate-symlinks

# Fix broken symlinks
/research fix-symlinks

# List symlink mappings
/research list-symlinks [general|project]
```

## Access Patterns

### General Research Access
```markdown
# Direct access to general research
research/general/auth/oauth.md          # -> _knowledge-base/auth/oauth-general.md
research/general/database/mongodb.md    # -> _knowledge-base/database/mongodb-general.md
research/general/api/rest.md           # -> _knowledge-base/api/rest-general.md
```

### Project Research Access
```markdown
# Access project-specific research
research/projects/myapp/_project-research/auth.md      # -> _knowledge-base/auth/oauth-myapp.md
research/projects/myapp/_project-research/database.md  # -> _knowledge-base/database/postgresql-myapp.md
research/projects/webapp/_project-research/auth.md     # -> _knowledge-base/auth/oauth-webapp.md
```

### Knowledge Base Direct Access
```markdown
# Direct access to source files
research/_knowledge-base/auth/oauth-general.md
research/_knowledge-base/auth/oauth-myapp.md
research/_knowledge-base/database/mongodb-general.md
research/_knowledge-base/database/postgresql-myapp.md
```

## Inheritance Integration

### Inheritance Mapping
```json
{
  "symlink_inheritance": {
    "projects/myapp/_project-research/auth.md": {
      "target": "_knowledge-base/auth/oauth-myapp.md",
      "inherits_from": "_knowledge-base/auth/oauth-general.md",
      "inheritance_type": "override",
      "general_symlink": "general/auth/oauth.md"
    },
    "projects/myapp/_project-research/database.md": {
      "target": "_knowledge-base/database/postgresql-myapp.md",
      "inherits_from": "_knowledge-base/database/mongodb-general.md",
      "inheritance_type": "technology_swap",
      "general_symlink": "general/database/mongodb.md"
    }
  }
}
```

### Automatic Inheritance Tracking
- **Creation**: When project research is created, inheritance is automatically tracked
- **Updates**: When general research changes, affected project research is flagged
- **Validation**: System validates inheritance consistency during symlink updates

## Benefits

### Organization
- **Intuitive Structure**: Natural folder organization for different research types
- **Single Source**: All actual files in one location for easy backup/versioning
- **Flexible Access**: Multiple access patterns for different use cases

### Maintenance
- **Centralized Storage**: All research files in one location
- **Easy Backup**: Single directory to backup all research
- **Version Control**: Simplified git tracking with single source directory

### Performance
- **Fast Access**: Direct file system links for rapid access
- **Reduced Duplication**: No file copies, only references
- **Efficient Updates**: Changes propagate immediately through symlinks

## Error Handling

### Broken Symlinks
- **Detection**: Regular validation checks for broken links
- **Automatic Repair**: Scripts to recreate broken symlinks
- **Notification**: Alert when symlinks become invalid

### Missing Targets
- **Validation**: Check that all symlink targets exist
- **Creation**: Automatically create missing knowledge base files
- **Cleanup**: Remove orphaned symlinks

### Inconsistent Structure
- **Detection**: Validate directory structure consistency
- **Repair**: Recreate proper directory hierarchy
- **Prevention**: Automated structure maintenance

## Integration Points

### With Research Agents
- **GeneralResearcher**: Creates files in `_knowledge-base/[category]/[tech]-general.md`
- **ProjectResearcher**: Creates files in `_knowledge-base/[category]/[tech]-[project].md`
- **Auto-Symlink**: Agents automatically trigger symlink creation

### With Inheritance System
- **Mapping**: Symlinks provide inheritance relationship visualization
- **Validation**: Inheritance system validates through symlink structure
- **Updates**: Inheritance changes trigger symlink updates

### With Quality System
- **Scoring**: Quality system operates on knowledge base files
- **Validation**: Symlink integrity checked during quality validation
- **Reporting**: Quality reports reference symlink structure

---

**System Status**: Ready for implementation
**Integration**: Fully integrated with research engine architecture
**Automation**: Automated symlink creation and maintenance