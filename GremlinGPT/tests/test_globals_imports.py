#!/usr/bin/env python3
"""
Test to verify that the enhanced backend.globals resolves import path failures
This test simulates the import patterns used throughout the GremlinGPT system
"""

import sys
import os

# Add the GremlinGPT directory to Python path
gremlin_path = "/home/runner/work/Ascend-Institute/Ascend-Institute/GremlinGPT"
sys.path.insert(0, gremlin_path)

def test_core_imports():
    """Test core configuration and utility imports"""
    try:
        from backend.globals import CFG, logger, DATA_DIR, resolve_path, MEM
        assert CFG is not None, "CFG should be loaded"
        assert logger is not None, "Logger should be available"
        assert DATA_DIR is not None, "DATA_DIR should be resolved"
        assert callable(resolve_path), "resolve_path should be callable"
        print("✅ Core imports: PASSED")
        return True
    except Exception as e:
        print(f"❌ Core imports: FAILED - {e}")
        return False

def test_path_imports():
    """Test path configuration imports"""
    try:
        from backend.globals import (
            BASE_DIR, MODELS_DIR, CHECKPOINTS_DIR, LOG_FILE,
            VECTOR_STORE_PATH, FAISS_PATH, CHROMA_PATH, METADATA_DB_PATH
        )
        paths = [BASE_DIR, MODELS_DIR, CHECKPOINTS_DIR, LOG_FILE,
                VECTOR_STORE_PATH, FAISS_PATH, CHROMA_PATH, METADATA_DB_PATH]
        
        for path in paths:
            assert path is not None, f"Path {path} should not be None"
        
        print("✅ Path imports: PASSED")
        return True
    except Exception as e:
        print(f"❌ Path imports: FAILED - {e}")
        return False

def test_config_imports():
    """Test configuration object imports"""
    try:
        from backend.globals import HARDWARE, NLP, AGENT, SCRAPER, MEMORY, SYSTEM, LOOP, ROLES
        configs = [HARDWARE, NLP, AGENT, SCRAPER, MEMORY, SYSTEM, LOOP, ROLES]
        
        for config in configs:
            assert isinstance(config, dict), f"Config {config} should be a dict"
        
        print("✅ Config imports: PASSED")
        return True
    except Exception as e:
        print(f"❌ Config imports: FAILED - {e}")
        return False

def test_function_imports():
    """Test function imports that should be available"""
    try:
        from backend.globals import (
            save_state, load_state, set_dashboard_backend, get_dashboard_backend,
            load_config, get_default_config
        )
        
        # Test that core functions are available
        assert callable(save_state), "save_state should be callable"
        assert callable(load_state), "load_state should be callable"
        assert callable(set_dashboard_backend), "set_dashboard_backend should be callable"
        assert callable(get_dashboard_backend), "get_dashboard_backend should be callable"
        
        print("✅ Function imports: PASSED")
        return True
    except Exception as e:
        print(f"❌ Function imports: FAILED - {e}")
        return False

def test_wildcard_import():
    """Test that wildcard import works without errors"""
    try:
        # Import in a controlled namespace
        test_namespace = {}
        exec("from backend.globals import *", test_namespace)
        
        # Check that core items are imported
        required_items = ['CFG', 'logger', 'DATA_DIR', 'BASE_DIR', 'MEM']
        for item in required_items:
            assert item in test_namespace, f"{item} should be available via wildcard import"
        
        imported_count = len([k for k in test_namespace.keys() if not k.startswith('_')])
        assert imported_count >= 20, f"Should import at least 20 items, got {imported_count}"
        
        print(f"✅ Wildcard import: PASSED ({imported_count} items imported)")
        return True
    except Exception as e:
        print(f"❌ Wildcard import: FAILED - {e}")
        return False

def test_no_crashes():
    """Test that importing globals doesn't crash the system"""
    try:
        import backend.globals
        # If we get here, the import succeeded without sys.exit() or crashes
        print("✅ No crashes: PASSED")
        return True
    except SystemExit:
        print("❌ No crashes: FAILED - sys.exit() was called")
        return False
    except Exception as e:
        print(f"❌ No crashes: FAILED - {e}")
        return False

def run_import_tests():
    """Run all import tests to verify the fix"""
    print("Testing enhanced backend.globals import system...")
    print("=" * 60)
    
    tests = [
        test_no_crashes,
        test_core_imports,
        test_path_imports,
        test_config_imports,
        test_function_imports,
        test_wildcard_import,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 SUCCESS: All import tests passed!")
        print("✅ The enhanced backend.globals successfully resolves import failures")
        print("✅ System-wide imports are now working through centralized globals")
        return True
    else:
        print("❌ Some tests failed. Import system needs further fixes.")
        return False

if __name__ == "__main__":
    success = run_import_tests()
    sys.exit(0 if success else 1)