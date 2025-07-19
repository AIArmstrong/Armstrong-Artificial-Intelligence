#!/usr/bin/env python3
"""
SuperClaude v3 Integration Test Suite
Tests v3 compatibility with AAI brain system
"""

import os
import sys
from pathlib import Path

def test_v3_structure_exists():
    """Verify SuperClaude v3 structure is properly cloned"""
    print("🔍 Testing v3 structure exists...")
    
    base_path = Path("/mnt/c/Users/Brandon/AAI/superclaude-v3")
    
    required_files = [
        "SuperClaude.py",
        "SuperClaude/Core/CLAUDE.md",
        "SuperClaude/Core/COMMANDS.md",
        "SuperClaude/Core/PERSONAS.md",
        "SuperClaude/Core/MCP.md",
        "SuperClaude/Core/ORCHESTRATOR.md",
        "SuperClaude/Commands/implement.md",
        "SuperClaude/Commands/build.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = base_path / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing v3 files: {missing_files}")
        return False
    
    print("✅ V3 structure exists and is complete")
    return True

def test_claude_md_integration():
    """Test if CLAUDE.md can be read and parsed"""
    print("🔍 Testing CLAUDE.md integration...")
    
    claude_file = Path("/mnt/c/Users/Brandon/AAI/superclaude-v3/SuperClaude/Core/CLAUDE.md")
    
    if not claude_file.exists():
        print("❌ CLAUDE.md not found")
        return False
    
    try:
        content = claude_file.read_text()
        
        # Check for v3 syntax patterns
        v3_patterns = [
            "@COMMANDS.md",
            "@FLAGS.md", 
            "@PERSONAS.md",
            "@MCP.md",
            "@ORCHESTRATOR.md"
        ]
        
        missing_patterns = []
        for pattern in v3_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            print(f"❌ Missing v3 patterns: {missing_patterns}")
            return False
        
        print("✅ CLAUDE.md uses v3 syntax correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error reading CLAUDE.md: {e}")
        return False

def test_aai_bridge_compatibility():
    """Test if AAI bridge system can adapt to v3"""
    print("🔍 Testing AAI bridge compatibility...")
    
    # Check current bridge structure
    bridge_file = Path("/mnt/c/Users/Brandon/AAI/brain/modules/superclaude-bridge.md")
    
    if not bridge_file.exists():
        print("❌ AAI bridge file not found")
        return False
    
    try:
        bridge_content = bridge_file.read_text()
        
        # Check if bridge uses v2 paths (will need updating)
        v2_patterns = [
            "superclaude-base/commands/shared/",
            "superclaude-base/shared/",
            "@include"
        ]
        
        v2_references = []
        for pattern in v2_patterns:
            if pattern in bridge_content:
                v2_references.append(pattern)
        
        if v2_references:
            print(f"⚠️  Bridge uses v2 patterns (needs update): {v2_references}")
            print("📋 Bridge is adaptable but requires path updates")
            return True
        
        print("✅ Bridge already compatible with v3")
        return True
        
    except Exception as e:
        print(f"❌ Error reading bridge: {e}")
        return False

def test_command_structure():
    """Test v3 command structure"""
    print("🔍 Testing v3 command structure...")
    
    commands_file = Path("/mnt/c/Users/Brandon/AAI/superclaude-v3/SuperClaude/Core/COMMANDS.md")
    
    if not commands_file.exists():
        print("❌ COMMANDS.md not found")
        return False
    
    try:
        content = commands_file.read_text()
        
        # Check for key v3 commands
        v3_commands = [
            "/implement",
            "/build",
            "/analyze", 
            "/improve",
            "/design"
        ]
        
        found_commands = []
        for cmd in v3_commands:
            if cmd in content:
                found_commands.append(cmd)
        
        if len(found_commands) >= 3:
            print(f"✅ Found v3 commands: {found_commands}")
            return True
        else:
            print(f"❌ Insufficient v3 commands found: {found_commands}")
            return False
        
    except Exception as e:
        print(f"❌ Error reading COMMANDS.md: {e}")
        return False

def test_mcp_integration():
    """Test v3 MCP integration"""
    print("🔍 Testing v3 MCP integration...")
    
    mcp_file = Path("/mnt/c/Users/Brandon/AAI/superclaude-v3/SuperClaude/Core/MCP.md")
    
    if not mcp_file.exists():
        print("❌ MCP.md not found")
        return False
    
    try:
        content = mcp_file.read_text()
        
        # Check for v3 MCP servers
        mcp_servers = [
            "Context7",
            "Sequential", 
            "Magic",
            "Playwright"
        ]
        
        found_servers = []
        for server in mcp_servers:
            if server in content:
                found_servers.append(server)
        
        if len(found_servers) >= 3:
            print(f"✅ Found v3 MCP servers: {found_servers}")
            return True
        else:
            print(f"❌ Insufficient MCP servers found: {found_servers}")
            return False
        
    except Exception as e:
        print(f"❌ Error reading MCP.md: {e}")
        return False

def test_persona_system():
    """Test v3 persona system"""
    print("🔍 Testing v3 persona system...")
    
    personas_file = Path("/mnt/c/Users/Brandon/AAI/superclaude-v3/SuperClaude/Core/PERSONAS.md")
    
    if not personas_file.exists():
        print("❌ PERSONAS.md not found")
        return False
    
    try:
        content = personas_file.read_text()
        
        # Check for key v3 personas
        v3_personas = [
            "architect",
            "frontend",
            "backend",
            "security",
            "analyzer"
        ]
        
        found_personas = []
        for persona in v3_personas:
            if persona in content:
                found_personas.append(persona)
        
        if len(found_personas) >= 4:
            print(f"✅ Found v3 personas: {found_personas}")
            return True
        else:
            print(f"❌ Insufficient personas found: {found_personas}")
            return False
        
    except Exception as e:
        print(f"❌ Error reading PERSONAS.md: {e}")
        return False

def test_installer_compatibility():
    """Test v3 Python installer"""
    print("🔍 Testing v3 Python installer...")
    
    installer_file = Path("/mnt/c/Users/Brandon/AAI/superclaude-v3/SuperClaude.py")
    
    if not installer_file.exists():
        print("❌ SuperClaude.py installer not found")
        return False
    
    try:
        content = installer_file.read_text()
        
        # Check for installer functionality
        installer_features = [
            "install",
            "argparse",
            "def main",
            "operations"
        ]
        
        found_features = []
        for feature in installer_features:
            if feature in content:
                found_features.append(feature)
        
        if len(found_features) >= 3:
            print(f"✅ Found installer features: {found_features}")
            return True
        else:
            print(f"❌ Insufficient installer features: {found_features}")
            return False
        
    except Exception as e:
        print(f"❌ Error reading installer: {e}")
        return False

def generate_compatibility_report(test_results):
    """Generate comprehensive compatibility report"""
    print("\n" + "="*50)
    print("🧪 SUPERCLAUDE V3 INTEGRATION TEST REPORT")
    print("="*50)
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    print(f"📊 Overall Score: {passed_tests}/{total_tests} tests passed")
    print(f"🎯 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n📋 Test Results:")
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    print("\n🔍 Compatibility Assessment:")
    
    if passed_tests >= total_tests * 0.8:
        print("✅ HIGH COMPATIBILITY - Ready for bridge system updates")
        print("📝 Recommendation: Proceed with bridge updates and integration")
    elif passed_tests >= total_tests * 0.6:
        print("⚠️  MODERATE COMPATIBILITY - Some issues need resolution")
        print("📝 Recommendation: Address failing tests before integration")
    else:
        print("❌ LOW COMPATIBILITY - Significant issues detected")
        print("📝 Recommendation: Investigate major compatibility problems")
    
    print("\n🚀 Next Steps:")
    print("1. Review test results and address any failures")
    print("2. Update AAI bridge system for v3 compatibility")
    print("3. Test v3 installation in isolated environment")
    print("4. Validate all features work with AAI brain system")
    print("5. Plan production integration strategy")

def main():
    """Main test execution"""
    print("🚀 Starting SuperClaude v3 Integration Tests")
    print("=" * 50)
    
    # Execute all tests
    test_results = {
        "V3 Structure": test_v3_structure_exists(),
        "CLAUDE.md Integration": test_claude_md_integration(),
        "AAI Bridge Compatibility": test_aai_bridge_compatibility(),
        "Command Structure": test_command_structure(),
        "MCP Integration": test_mcp_integration(),
        "Persona System": test_persona_system(),
        "Installer Compatibility": test_installer_compatibility()
    }
    
    # Generate report
    generate_compatibility_report(test_results)
    
    # Return success/failure
    return all(test_results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)