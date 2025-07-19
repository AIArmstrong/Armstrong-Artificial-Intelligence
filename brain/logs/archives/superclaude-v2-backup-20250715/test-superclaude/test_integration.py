#!/usr/bin/env python3
"""
Test SuperClaude integration with AAI
"""

import os
import subprocess
from pathlib import Path

def test_claude_md_exists():
    """Verify CLAUDE.md file exists and has content"""
    claude_file = Path("CLAUDE.md")
    assert claude_file.exists(), "CLAUDE.md not found"
    content = claude_file.read_text()
    
    # Check for key sections
    assert "@include ../../brain/Claude.md" in content, "AAI brain include missing"
    assert "@include ../../brain/modules/superclaude-bridge.md" in content, "SuperClaude bridge missing"
    print("✅ CLAUDE.md structure verified")

def test_include_paths():
    """Verify all @include paths resolve correctly"""
    base_path = Path("/mnt/c/Users/Brandon/AAI")
    
    paths_to_check = [
        "brain/Claude.md",
        "brain/modules/superclaude-bridge.md",
        "superclaude-base/CLAUDE.md"
    ]
    
    for path in paths_to_check:
        full_path = base_path / path
        assert full_path.exists(), f"Path not found: {path}"
    
    print("✅ All include paths resolve correctly")

def test_superclaude_features():
    """Test that SuperClaude features are accessible"""
    # This would normally test actual Claude behavior
    # For now, we verify the configuration structure
    
    bridge_file = Path("/mnt/c/Users/Brandon/AAI/brain/modules/superclaude-bridge.md")
    content = bridge_file.read_text()
    
    features = [
        "Thinking Modes",
        "Introspection Capabilities", 
        "Advanced Token Economy",
        "Error Recovery"
    ]
    
    for feature in features:
        assert feature in content, f"Feature missing: {feature}"
    
    print("✅ SuperClaude features configured")

def main():
    print("🧪 Testing SuperClaude + AAI Integration\n")
    
    try:
        test_claude_md_exists()
        test_include_paths()
        test_superclaude_features()
        
        print("\n✅ All tests passed! SuperClaude integration is ready.")
        print("\n📝 How to use in Claude Code:")
        print("1. Navigate to this test project")
        print("2. Claude will read CLAUDE.md and inherit both AAI + SuperClaude features")
        print("3. Test commands like [INTROSPECT] or observe token optimization")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())