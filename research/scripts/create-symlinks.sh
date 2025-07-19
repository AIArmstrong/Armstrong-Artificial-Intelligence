#!/bin/bash
# research/scripts/create-symlinks.sh

# Create general symlinks
create_general_symlinks() {
    local knowledge_base="$1"
    local general_dir="$2"
    
    echo "Creating general symlinks..."
    
    # Find all *-general.md files
    find "$knowledge_base" -name "*-general.md" 2>/dev/null | while read -r file; do
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
    
    echo "Creating project symlinks..."
    
    # Find all project-specific files
    find "$knowledge_base" -name "*-*.md" ! -name "*-general.md" 2>/dev/null | while read -r file; do
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
main() {
    local research_dir="${1:-/mnt/c/Users/Brandon/AAI/research}"
    
    echo "Initializing symlink system for research directory: $research_dir"
    
    # Ensure base directories exist
    mkdir -p "$research_dir/_knowledge-base"
    mkdir -p "$research_dir/general"
    mkdir -p "$research_dir/projects"
    
    # Create symlinks
    create_general_symlinks "$research_dir/_knowledge-base" "$research_dir/general"
    create_project_symlinks "$research_dir/_knowledge-base" "$research_dir/projects"
    
    echo "Symlink system initialization complete"
}

# Execute if run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi