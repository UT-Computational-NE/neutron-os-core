#!/usr/bin/env python3
"""
CI/CD Documentation Quality Gate
Ensures documentation meets quality standards before deployment.
"""

import sys
import subprocess
from pathlib import Path

def run_quality_check():
    """Run the documentation quality checker."""
    docs_tools_dir = Path(__file__).parent
    checker_path = docs_tools_dir / 'doc_quality_checker.py'
    
    print("=" * 60)
    print("DOCUMENTATION QUALITY GATE")
    print("=" * 60)
    print()
    
    # Run the checker
    result = subprocess.run(
        [sys.executable, str(checker_path)],
        capture_output=True,
        text=True
    )
    
    # Show output
    print(result.stdout)
    if result.stderr:
        print("ERRORS:", result.stderr, file=sys.stderr)
    
    if result.returncode != 0:
        print("\n❌ QUALITY GATE FAILED")
        print("Documentation has quality issues that must be fixed.")
        print("\nTo fix automatically, run:")
        print(f"  python3 {checker_path} --fix")
        print("\nTo fix manually, review the issues above.")
        return 1
    else:
        print("\n✅ QUALITY GATE PASSED")
        print("Documentation meets quality standards.")
        return 0

if __name__ == '__main__':
    sys.exit(run_quality_check())