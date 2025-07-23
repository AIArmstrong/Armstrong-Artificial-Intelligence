#!/usr/bin/env python3
"""
Quick Import Test to verify critical fixes
Tests only the import functionality of fixed modules
"""

import sys
import os
import importlib.util
import time

# Add project root to path
sys.path.insert(0, '/mnt/c/Users/Brandon/AAI')

def test_module_import(module_path, module_name):
    """Test if module can be imported"""
    try:
        start_time = time.time()
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            import_time = time.time() - start_time
            return True, import_time, None
        else:
            return False, 0, "Failed to create module spec"
    except Exception as e:
        import_time = time.time() - start_time
        return False, import_time, str(e)

def main():
    """Test critical modules that had import failures"""
    print("🧪 Quick Import Test - Verifying Critical Fixes")
    print("="*50)
    
    # Modules that had critical import failures
    critical_modules = [
        ("unified_intelligence_coordinator", "/mnt/c/Users/Brandon/AAI/brain/modules/unified_intelligence_coordinator.py"),
        ("analyze_command_handler", "/mnt/c/Users/Brandon/AAI/brain/modules/analyze_command_handler.py"),
        ("server_manager", "/mnt/c/Users/Brandon/AAI/mcp/server_manager.py"),
        ("delegation_engine", "/mnt/c/Users/Brandon/AAI/agents/orchestration/delegation_engine.py"),
        ("conversation_engine", "/mnt/c/Users/Brandon/AAI/agents/tech_expert/conversation_engine.py"),
        ("cache_manager", "/mnt/c/Users/Brandon/AAI/core/cache_manager.py"),
    ]
    
    results = []
    
    for module_name, module_path in critical_modules:
        if not os.path.exists(module_path):
            print(f"❌ {module_name}: Module file not found")
            results.append((module_name, False, "File not found"))
            continue
            
        success, import_time, error = test_module_import(module_path, module_name)
        
        if success:
            print(f"✅ {module_name}: Import successful ({import_time:.3f}s)")
            results.append((module_name, True, None))
        else:
            print(f"❌ {module_name}: Import failed - {error}")
            results.append((module_name, False, error))
    
    print("\n" + "="*50)
    
    # Summary
    successful = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"📊 RESULTS: {successful}/{total} modules importing successfully")
    
    if successful == total:
        print("🎉 All critical import fixes working!")
        print("✅ Ready to proceed with dependency installation and full testing")
    else:
        print("⚠️  Some modules still have import issues:")
        for module_name, success, error in results:
            if not success:
                print(f"   - {module_name}: {error}")
    
    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)