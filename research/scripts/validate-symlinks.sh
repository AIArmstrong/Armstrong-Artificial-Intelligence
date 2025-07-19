#!/bin/bash
# research/scripts/validate-symlinks.sh

validate_symlinks() {
    local research_dir="$1"
    local issues=0
    
    echo "Validating symlink system..."
    
    # Check general symlinks
    echo "Checking general symlinks..."
    find "$research_dir/general" -type l 2>/dev/null | while read -r link; do
        if [ ! -e "$link" ]; then
            echo "BROKEN: $link"
            issues=$((issues + 1))
        else
            echo "VALID: $link"
        fi
    done
    
    # Check project symlinks
    echo "Checking project symlinks..."
    find "$research_dir/projects" -type l 2>/dev/null | while read -r link; do
        if [ ! -e "$link" ]; then
            echo "BROKEN: $link"
            issues=$((issues + 1))
        else
            echo "VALID: $link"
        fi
    done
    
    # Check orphaned knowledge base files
    echo "Checking for orphaned knowledge base files..."
    find "$research_dir/_knowledge-base" -name "*.md" 2>/dev/null | while read -r file; do
        # Check if file has corresponding symlink
        filename=$(basename "$file")
        category=$(dirname "$file" | sed "s|$research_dir/_knowledge-base/||")
        
        if [[ "$filename" == *"-general.md" ]]; then
            # Check general symlink
            technology=$(echo "$filename" | sed 's/-general\.md$//')
            expected_link="$research_dir/general/$category/$technology.md"
            if [ ! -L "$expected_link" ]; then
                echo "ORPHANED: $file (missing general symlink)"
                issues=$((issues + 1))
            fi
        else
            # Check project symlink
            project=$(echo "$filename" | sed 's/.*-\([^-]*\)\.md$/\1/')
            technology=$(echo "$filename" | sed "s/-$project\.md$//" | sed 's/.*-//')
            expected_link="$research_dir/projects/$project/_project-research/$technology.md"
            if [ ! -L "$expected_link" ]; then
                echo "ORPHANED: $file (missing project symlink)"
                issues=$((issues + 1))
            fi
        fi
    done
    
    if [ $issues -eq 0 ]; then
        echo "✓ All symlinks valid, no orphaned files"
        return 0
    else
        echo "✗ Found $issues issues"
        return 1
    fi
}

# Main execution
main() {
    local research_dir="${1:-/mnt/c/Users/Brandon/AAI/research}"
    
    echo "Validating symlink system for: $research_dir"
    validate_symlinks "$research_dir"
}

# Execute if run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi