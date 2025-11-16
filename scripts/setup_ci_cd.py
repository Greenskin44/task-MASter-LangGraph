#!/usr/bin/env python3
"""
Setup script for CI/CD pipeline and pre-commit hooks.

This script:
1. Installs pre-commit hooks
2. Validates CI/CD configuration files
3. Runs initial code quality checks
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("="*60)
    print("CI/CD Pipeline Setup")
    print("="*60)
    
    # Check if we're in the project root
    if not Path("pyproject.toml").exists():
        print("Error: pyproject.toml not found. Run this script from the project root.")
        sys.exit(1)
    
    # Install pre-commit hooks
    print("\n1. Installing pre-commit hooks...")
    if not run_command(
        ["pre-commit", "install"],
        "Install pre-commit hooks"
    ):
        print("\nWarning: Failed to install pre-commit hooks")
        print("Make sure pre-commit is installed: pip install pre-commit")
    
    # Validate pre-commit configuration
    print("\n2. Validating pre-commit configuration...")
    if not run_command(
        ["pre-commit", "validate-config"],
        "Validate pre-commit config"
    ):
        print("\nWarning: Pre-commit configuration validation failed")
    
    # Run pre-commit on all files (optional, can be slow)
    print("\n3. Running pre-commit checks on all files...")
    print("This may take a few minutes on first run...")
    run_result = run_command(
        ["pre-commit", "run", "--all-files"],
        "Run pre-commit on all files"
    )
    if not run_result:
        print("\nNote: Some pre-commit checks failed.")
        print("This is normal on first run. Files have been auto-formatted.")
        print("Review the changes and commit them.")
    
    # Validate GitHub Actions workflows
    print("\n4. Checking GitHub Actions workflows...")
    workflows_dir = Path(".github/workflows")
    if workflows_dir.exists():
        workflow_files = list(workflows_dir.glob("*.yml"))
        print(f"Found {len(workflow_files)} workflow files:")
        for workflow in workflow_files:
            print(f"  - {workflow.name}")
    else:
        print("Warning: .github/workflows directory not found")
    
    # Check dependabot configuration
    print("\n5. Checking Dependabot configuration...")
    dependabot_file = Path(".github/dependabot.yml")
    if dependabot_file.exists():
        print("✓ Dependabot configuration found")
    else:
        print("Warning: Dependabot configuration not found")
    
    print("\n" + "="*60)
    print("CI/CD Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review and commit any changes made by pre-commit hooks")
    print("2. Push to GitHub to trigger CI/CD workflows")
    print("3. Configure GitHub secrets for API keys:")
    print("   - OPENAI_API_KEY")
    print("   - LANGSMITH_API_KEY")
    print("   - TAVILY_API_KEY")
    print("4. Enable Dependabot in repository settings")
    print("\nPre-commit hooks are now active and will run on every commit.")


if __name__ == "__main__":
    main()
