#!/usr/bin/env python3
"""
Development Environment Setup Script

This script automates the setup of the development environment including:
- Virtual environment verification
- Dependency installation
- Pre-commit hooks installation
- Environment variable validation
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], check: bool = True) -> tuple[int, str, str]:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr


def check_python_version() -> bool:
    """Check if Python version is 3.11 or higher."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"✗ Python 3.11+ required, found {version.major}.{version.minor}.{version.micro}")
        return False


def check_virtual_env() -> bool:
    """Check if running in a virtual environment."""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print("✓ Virtual environment detected")
        return True
    else:
        print("✗ Not running in a virtual environment")
        print("  Please activate your virtual environment first:")
        print("    source project-env/bin/activate  # Mac/Linux")
        print("    .\\project-env\\Scripts\\Activate.ps1  # Windows PowerShell")
        return False


def install_dependencies() -> bool:
    """Install project dependencies."""
    print("\nInstalling dependencies...")
    
    # Install main dependencies
    print("  Installing main dependencies from requirements.txt...")
    code, stdout, stderr = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    if code != 0:
        print(f"✗ Failed to install main dependencies: {stderr}")
        return False
    print("  ✓ Main dependencies installed")
    
    # Install development dependencies
    print("  Installing development dependencies from requirements-dev.txt...")
    code, stdout, stderr = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])
    if code != 0:
        print(f"✗ Failed to install development dependencies: {stderr}")
        return False
    print("  ✓ Development dependencies installed")
    
    return True


def setup_pre_commit() -> bool:
    """Install and configure pre-commit hooks."""
    print("\nSetting up pre-commit hooks...")
    
    # Check if pre-commit is installed
    code, stdout, stderr = run_command(["pre-commit", "--version"], check=False)
    if code != 0:
        print("✗ pre-commit not found, installing...")
        code, stdout, stderr = run_command([sys.executable, "-m", "pip", "install", "pre-commit"])
        if code != 0:
            print(f"✗ Failed to install pre-commit: {stderr}")
            return False
    
    # Install pre-commit hooks
    print("  Installing git hooks...")
    code, stdout, stderr = run_command(["pre-commit", "install"])
    if code != 0:
        print(f"✗ Failed to install pre-commit hooks: {stderr}")
        return False
    print("  ✓ Pre-commit hooks installed")
    
    # Run pre-commit on all files to verify setup
    print("  Running pre-commit on all files (this may take a moment)...")
    code, stdout, stderr = run_command(["pre-commit", "run", "--all-files"], check=False)
    if code != 0:
        print("  ⚠ Some pre-commit checks failed (this is normal for first run)")
        print("  Run 'pre-commit run --all-files' to see details")
    else:
        print("  ✓ All pre-commit checks passed")
    
    return True


def check_env_file() -> bool:
    """Check if .env file exists and has required variables."""
    print("\nChecking environment configuration...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        print("✗ .env file not found")
        if env_example.exists():
            print("  Creating .env from .env.example...")
            env_file.write_text(env_example.read_text())
            print("  ✓ .env file created")
            print("  ⚠ Please edit .env and add your API keys:")
            print("    - OPENAI_API_KEY")
            print("    - TAVILY_API_KEY")
            print("    - LANGSMITH_API_KEY (optional)")
        return False
    
    # Check for required API keys
    env_content = env_file.read_text()
    required_keys = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if key not in env_content or f"{key}=" in env_content and "your-" in env_content:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"⚠ Missing or placeholder API keys: {', '.join(missing_keys)}")
        print("  Please edit .env and add your actual API keys")
        return False
    
    print("✓ .env file configured")
    return True


def verify_installation() -> bool:
    """Verify that key tools are installed and working."""
    print("\nVerifying installation...")
    
    tools = {
        "black": ["black", "--version"],
        "ruff": ["ruff", "--version"],
        "mypy": ["mypy", "--version"],
        "pytest": ["pytest", "--version"],
        "pre-commit": ["pre-commit", "--version"],
    }
    
    all_ok = True
    for tool_name, command in tools.items():
        code, stdout, stderr = run_command(command, check=False)
        if code == 0:
            version = stdout.strip().split('\n')[0]
            print(f"  ✓ {tool_name}: {version}")
        else:
            print(f"  ✗ {tool_name}: not found")
            all_ok = False
    
    return all_ok


def main():
    """Main setup function."""
    print("=" * 60)
    print("LangGraph Project - Development Environment Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check virtual environment
    if not check_virtual_env():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup pre-commit hooks
    if not setup_pre_commit():
        print("\n⚠ Pre-commit setup had issues, but continuing...")
    
    # Check environment file
    env_ok = check_env_file()
    
    # Verify installation
    if not verify_installation():
        print("\n⚠ Some tools are missing, but core setup is complete")
    
    # Final summary
    print("\n" + "=" * 60)
    print("Setup Summary")
    print("=" * 60)
    print("✓ Dependencies installed")
    print("✓ Pre-commit hooks configured")
    if env_ok:
        print("✓ Environment variables configured")
    else:
        print("⚠ Environment variables need configuration")
    
    print("\nNext steps:")
    if not env_ok:
        print("  1. Edit .env and add your API keys")
        print("  2. Run: langgraph dev")
    else:
        print("  1. Run: langgraph dev")
        print("  2. Open: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024")
    
    print("\nDevelopment commands:")
    print("  pytest tests/ -v          # Run tests")
    print("  black .                   # Format code")
    print("  ruff check .              # Lint code")
    print("  pre-commit run --all-files # Run all checks")
    
    print("\n✓ Development environment setup complete!")


if __name__ == "__main__":
    main()
