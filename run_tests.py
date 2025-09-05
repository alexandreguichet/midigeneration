#!/usr/bin/env python
"""
Test runner script with coverage reporting using Poetry
"""

import subprocess
import sys
import os

def run_tests():
    """Run tests with coverage and generate reports using Poetry"""
    print("🧪 Running tests with coverage using Poetry...")
    
    # Change to project root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if Poetry is available
    try:
        result = subprocess.run(['poetry', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Poetry not found. Please install Poetry first:")
            print("   curl -sSL https://install.python-poetry.org | python3 -")
            print("   or visit: https://python-poetry.org/docs/#installation")
            return False
        print(f"📦 Using {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Poetry not found. Please install Poetry first:")
        print("   curl -sSL https://install.python-poetry.org | python3 -")
        print("   or visit: https://python-poetry.org/docs/#installation")
        return False
    
    # Install dependencies if needed
    print("📥 Installing dependencies...")
    install_result = subprocess.run(['poetry', 'install'], capture_output=True, text=True)
    if install_result.returncode != 0:
        print("❌ Failed to install dependencies:")
        print(install_result.stderr)
        return False
    
    try:
        # Run pytest with coverage using Poetry
        result = subprocess.run([
            'poetry', 'run', 'pytest', 
            'test/', 
            '--cov=src',
            '--cov-report=html',
            '--cov-report=lcov',
            '--cov-report=term-missing',
            '--cov-branch',
            '--cov-fail-under=90',  # Start with 90% then aim for 100%
            '-v'
        ], check=False)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
            print("📊 Coverage reports generated:")
            print("   - HTML: htmlcov/index.html")
            print("   - LCOV: coverage.lcov")
        else:
            print("\n❌ Some tests failed or coverage is insufficient")
            return False
            
    except FileNotFoundError:
        print("❌ pytest not found. Poetry dependencies may not be installed correctly.")
        return False
    
    return True

def run_linting():
    """Run code quality checks"""
    print("🔍 Running code quality checks...")
    
    checks = [
        (['poetry', 'run', 'black', '--check', 'src/', 'test/'], "Black formatting"),
        (['poetry', 'run', 'isort', '--check-only', 'src/', 'test/'], "Import sorting"),
        (['poetry', 'run', 'flake8', 'src/', 'test/'], "Flake8 linting"),
        (['poetry', 'run', 'mypy', 'src/'], "Type checking"),
    ]
    
    all_passed = True
    for cmd, description in checks:
        print(f"  Running {description}...")
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            print(f"  ✅ {description} passed")
        else:
            print(f"  ❌ {description} failed")
            all_passed = False
    
    return all_passed

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run tests and code quality checks')
    parser.add_argument('--lint-only', action='store_true', help='Run only linting checks')
    parser.add_argument('--test-only', action='store_true', help='Run only tests')
    
    args = parser.parse_args()
    
    success = True
    
    if args.lint_only:
        success = run_linting()
    elif args.test_only:
        success = run_tests()
    else:
        # Run both tests and linting
        test_success = run_tests()
        lint_success = run_linting()
        success = test_success and lint_success
        
        if success:
            print("\n🎉 All checks passed!")
        else:
            print("\n💥 Some checks failed!")
    
    sys.exit(0 if success else 1)
