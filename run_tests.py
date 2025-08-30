#!/usr/bin/env python3
"""Test runner script for the multimodal agent builder."""

import sys
import subprocess
from pathlib import Path
import argparse


def run_tests(test_type="all", verbose=False, coverage=True, markers=None, failfast=False):
    """Run tests with specified options.

    Args:
        test_type: Type of tests to run (all, unit, integration, etc.)
        verbose: Enable verbose output
        coverage: Generate coverage report
        markers: Additional pytest markers to filter tests
        failfast: Stop on first failure
    """
    # Base pytest command
    cmd = ["pytest"]

    # Add test path based on type
    if test_type == "unit":
        cmd.append("tests/unit")
    elif test_type == "integration":
        cmd.append("tests/integration")
    elif test_type == "api":
        cmd.extend(["-m", "api"])
    elif test_type == "llm":
        cmd.extend(["-m", "llm"])
    elif test_type == "agent":
        cmd.extend(["-m", "agent"])
    elif test_type == "training":
        cmd.extend(["-m", "training"])
    elif test_type != "all":
        print(f"Unknown test type: {test_type}")
        return 1

    # Add verbosity
    if verbose:
        cmd.append("-vv")
    else:
        cmd.append("-v")

    # Add coverage if requested
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term-missing"])

    # Add custom markers
    if markers:
        cmd.extend(["-m", markers])

    # Add failfast
    if failfast:
        cmd.append("-x")

    # Add color output
    cmd.append("--color=yes")

    # Print command
    print(f"Running: {' '.join(cmd)}")
    print("=" * 60)

    # Run tests
    result = subprocess.run(cmd)

    # Print coverage report location if generated
    if coverage and result.returncode == 0:
        print("\n" + "=" * 60)
        print("Coverage report generated:")
        print("  - Terminal output above")
        print("  - HTML report: htmlcov/index.html")
        print("  - Open with: open htmlcov/index.html")

    return result.returncode


def install_dependencies():
    """Install test dependencies."""
    print("Installing test dependencies...")

    deps = [
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "pytest-cov>=4.0.0",
        "pytest-mock>=3.10.0",
        "httpx>=0.24.0",
        "faker>=18.0.0",
    ]

    cmd = ["pip", "install"] + deps
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("✅ Test dependencies installed successfully")
    else:
        print("❌ Failed to install test dependencies")

    return result.returncode


def lint_code():
    """Run code linting."""
    print("Running code linting...")

    # Try to run ruff for linting
    try:
        subprocess.run(["ruff", "check", "src", "tests"], check=True)
        print("✅ Code linting passed")
        return 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to pylint if available
        try:
            subprocess.run(["pylint", "src"], check=False)
            return 0
        except FileNotFoundError:
            print("⚠️  No linter found (install ruff or pylint)")
            return 0


def format_code():
    """Format code with black."""
    print("Checking code formatting...")

    try:
        subprocess.run(["black", "--check", "src", "tests"], check=True)
        print("✅ Code formatting is correct")
        return 0
    except subprocess.CalledProcessError:
        print("⚠️  Code needs formatting (run: black src tests)")
        return 1
    except FileNotFoundError:
        print("⚠️  Black not found (install with: pip install black)")
        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run tests for the multimodal agent builder")

    parser.add_argument(
        "type",
        nargs="?",
        default="all",
        choices=["all", "unit", "integration", "api", "llm", "agent", "training"],
        help="Type of tests to run",
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    parser.add_argument("--no-cov", action="store_true", help="Disable coverage reporting")

    parser.add_argument("-m", "--markers", help="Additional pytest markers to filter tests")

    parser.add_argument("-x", "--failfast", action="store_true", help="Stop on first failure")

    parser.add_argument("--install", action="store_true", help="Install test dependencies")

    parser.add_argument("--lint", action="store_true", help="Run code linting")

    parser.add_argument("--format", action="store_true", help="Check code formatting")

    args = parser.parse_args()

    # Install dependencies if requested
    if args.install:
        return install_dependencies()

    # Run linting if requested
    if args.lint:
        return lint_code()

    # Check formatting if requested
    if args.format:
        return format_code()

    # Run tests
    return run_tests(
        test_type=args.type,
        verbose=args.verbose,
        coverage=not args.no_cov,
        markers=args.markers,
        failfast=args.failfast,
    )


if __name__ == "__main__":
    sys.exit(main())
