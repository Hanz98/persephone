#!/usr/bin/env python3
"""
Development environment verification script for Persephone
Run this script to verify your development environment is set up correctly.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return True if successful."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"  ✅ {description} - OK")
            return True
        else:
            print(f"  ❌ {description} - FAILED")
            print(f"     Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ⏰ {description} - TIMEOUT")
        return False
    except Exception as e:
        print(f"  ❌ {description} - ERROR: {e}")
        return False


def check_file_exists(filepath, description):
    """Check if a file exists."""
    print(f"🔍 {description}...")
    if Path(filepath).exists():
        print(f"  ✅ {description} - OK")
        return True
    else:
        print(f"  ❌ {description} - MISSING")
        return False


def main():
    """Main verification function."""
    print("🚀 Persephone Development Environment Verification")
    print("=" * 50)
    
    checks = []
    
    # Check Python version
    print(f"🔍 Python version...")
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"  ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} - OK")
        checks.append(True)
    else:
        print(f"  ❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} - TOO OLD (need 3.8+)")
        checks.append(False)
    
    # Check if we're in a virtual environment
    print(f"🔍 Virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"  ✅ Virtual environment active - OK")
        checks.append(True)
    else:
        print(f"  ⚠️  Virtual environment not detected - RECOMMENDED but not required")
        checks.append(True)  # Not a hard failure
    
    # Check required commands
    commands = [
        ("python --version", "Python executable"),
        ("pip --version", "pip package manager"),
        ("git --version", "Git version control"),
        ("black --version", "Black code formatter"),
        ("flake8 --version", "Flake8 linter"),
        ("mypy --version", "MyPy type checker"),
        ("pytest --version", "pytest testing framework"),
        ("pre-commit --version", "pre-commit hooks"),
    ]
    
    for cmd, desc in commands:
        checks.append(run_command(cmd, desc))
    
    # Check project files
    files = [
        ("pyproject.toml", "Project configuration"),
        ("README.md", "README documentation"),
        ("src/persephone/__init__.py", "Main application module"),
        ("tests/conftest.py", "Test configuration"),
        (".pre-commit-config.yaml", "Pre-commit configuration"),
    ]
    
    for filepath, desc in files:
        checks.append(check_file_exists(filepath, desc))
    
    # Run basic tests
    test_commands = [
        ("python -c 'import persephone; print(\"Import successful\")'", "Import persephone module"),
        ("black src/ tests/ --check", "Code formatting check"),
        ("flake8 src/ tests/ --exit-zero", "Linting check"),
        ("mypy src/ --ignore-missing-imports", "Type checking"),
        ("pytest tests/ --tb=short -q", "Run test suite"),
    ]
    
    for cmd, desc in test_commands:
        checks.append(run_command(cmd, desc))
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"🎉 All checks passed! ({passed}/{total})")
        print("Your development environment is ready for Persephone development!")
        return 0
    elif passed >= total * 0.8:  # 80% or more
        print(f"✅ Most checks passed ({passed}/{total})")
        print("Your development environment is mostly ready.")
        print("Please review the failed checks above and fix them if needed.")
        return 0
    else:
        print(f"❌ Several checks failed ({passed}/{total})")
        print("Please fix the issues above before continuing development.")
        return 1


if __name__ == "__main__":
    sys.exit(main())