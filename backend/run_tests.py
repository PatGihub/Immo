#!/usr/bin/env python
"""Script to run tests"""
import subprocess
import sys

def run_tests():
    """Run all tests with pytest"""
    print("Running Password Tests...")
    print("=" * 60)
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd="."
    )
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
