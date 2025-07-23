#!/usr/bin/env python3
"""
Syntax Fixes for Relative Import Corrections
Fixes syntax errors introduced by the import fixing script
"""

import os
import re
import shutil

def fix_import_syntax(file_path):
    """Fix syntax errors in import statements"""
    print(f"🔧 Fixing syntax in {os.path.basename(file_path)}")
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Pattern to find broken import statements
        broken_pattern = r'try:\s*\n\s*from\s+\.(\w+)\s+import\s+\(\s*\nexcept ImportError:\s*\n\s*from\s+([^\s]+)\s+import\s+\(\s*\n(.*?)\)'
        
        def fix_import_block(match):
            module = match.group(1)
            fallback_path = match.group(2)
            imports = match.group(3).strip()
            
            # Clean up the imports
            import_list = []
            for line in imports.split('\n'):
                line = line.strip()
                if line and not line.startswith(')'):
                    # Remove trailing commas and clean up
                    line = line.rstrip(',').strip()
                    if line:
                        import_list.append(line)
            
            # Build corrected import block
            import_items = ',\n        '.join(import_list)
            
            corrected = f'''try:
    from .{module} import (
        {import_items}
    )
except ImportError:
    from {fallback_path}.{module} import (
        {import_items}
    )'''
            
            return corrected
        
        # Apply the fix
        new_content = re.sub(broken_pattern, fix_import_block, content, flags=re.DOTALL)
        
        # Also fix any standalone broken import patterns
        standalone_pattern = r'try:\s*\n\s*from\s+\.(\w+)\s+import\s+\(\s*\nexcept ImportError:\s*\n\s*from\s+([^\s]+)\s+import\s+\(\s*\n([^)]*?)(?=\n\w|\n\n|\Z)'
        
        def fix_standalone(match):
            module = match.group(1)
            fallback_path = match.group(2)
            imports_section = match.group(3)
            
            # Extract actual imports from the messy section
            import_items = []
            lines = imports_section.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith(')') and not line.startswith('except') and not line.startswith('from'):
                    # Clean the line
                    line = line.rstrip(',').strip()
                    if line and not line.startswith('#'):
                        import_items.append(line)
            
            if import_items:
                import_list = ',\n        '.join(import_items)
                return f'''try:
    from .{module} import (
        {import_list}
    )
except ImportError:
    from {fallback_path}.{module} import (
        {import_list}
    )'''
            else:
                return match.group(0)  # Return original if can't parse
        
        new_content = re.sub(standalone_pattern, fix_standalone, new_content, flags=re.DOTALL)
        
        if new_content != content:
            # Create backup
            shutil.copy2(file_path, file_path + '.syntax_backup')
            
            # Write fixed content
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            print(f"   ✅ Fixed syntax in {os.path.basename(file_path)}")
            return True
        else:
            print(f"   ℹ️  No syntax issues found in {os.path.basename(file_path)}")
            return True
            
    except Exception as e:
        print(f"   ❌ Error fixing syntax: {e}")
        return False

def main():
    """Fix syntax errors in all agent modules"""
    print("🔧 Fixing Syntax Errors from Import Corrections")
    print("="*50)
    
    # Files that might have syntax errors
    files_to_fix = [
        "/mnt/c/Users/Brandon/AAI/agents/orchestration/primary_agent.py",
        "/mnt/c/Users/Brandon/AAI/agents/tech_expert/recommender.py",
        "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/dual_model_agent.py",
        "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/reasoning_engine.py",
        "/mnt/c/Users/Brandon/AAI/agents/r1_reasoning/confidence_scorer.py",
        "/mnt/c/Users/Brandon/AAI/agents/tool-selection/tool_selector.py",
        "/mnt/c/Users/Brandon/AAI/agents/tool-selection/learning_engine.py",
        "/mnt/c/Users/Brandon/AAI/agents/tool-selection/fabric_integrator.py",
        "/mnt/c/Users/Brandon/AAI/agents/tool-selection/prompt_analyzer.py",
        "/mnt/c/Users/Brandon/AAI/agents/tool-selection/confidence_scorer.py",
    ]
    
    fixed_count = 0
    total_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            total_count += 1
            if fix_import_syntax(file_path):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n✅ Syntax fixes completed: {fixed_count}/{total_count} successful")

if __name__ == "__main__":
    main()