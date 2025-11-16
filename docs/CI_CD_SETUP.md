# CI/CD Pipeline Setup Guide

This document describes the CI/CD pipeline configuration for the LangGraph Production Demo project.

## Overview

The project uses GitHub Actions for continuous integration and deployment, with automated testing, code quality checks, and dependency management.

## Components

### 1. GitHub Actions Workflows

#### Main CI Workflow (`.github/workflows/ci.yml`)

Runs on every push and pull request to `main` and `develop` branches.

**Jobs:**
- **Code Quality Checks**: Runs Black, Ruff, and MyPy
- **Tests**: Runs pytest on Python 3.11 and 3.12
- **Benchmarks**: Runs performance benchmarks on pull requests

**Configuration:**
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
```

#### Pre-commit Workflow (`.github/workflows/pre-commit.yml`)

Runs pre-commit hooks on all files for pull requests.

#### Dependency Review (`.github/workflows/dependency-review.yml`)

Reviews dependency changes in pull requests for security vulnerabilities.

### 2. Pre-commit Hooks (`.pre-commit-config.yaml`)

Automatically runs code quality checks before each commit.

**Hooks:**
- **General**: Trailing whitespace, end-of-file fixer, YAML/JSON validation
- **Black**: Code formatting
- **Ruff**: Linting with auto-fix
- **MyPy**: Type checking
- **Bandit**: Security checks
- **Safety**: Dependency vulnerability scanning

### 3. Dependabot (`.github/dependabot.yml`)

Automatically creates pull requests for dependency updates.

**Configuration:**
- **Schedule**: Weekly on Mondays at 9:00 AM
- **Grouping**: Groups related dependencies (langgraph, langchain, dev tools)
- **Limits**: Max 5 PRs for pip, 3 for GitHub Actions
- **Ignores**: Major version updates for stable dependencies

## Setup Instructions

### Initial Setup

1. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Run the setup script:**
   ```bash
   python scripts/setup_ci_cd.py
   ```

   This script will:
   - Install pre-commit hooks
   - Validate configurations
   - Run initial code quality checks

3. **Manual pre-commit installation (alternative):**
   ```bash
   pre-commit install
   pre-commit run --all-files
   ```

### GitHub Configuration

1. **Configure Repository Secrets:**
   
   Go to Settings → Secrets and variables → Actions, and add:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `LANGSMITH_API_KEY`: Your LangSmith API key
   - `TAVILY_API_KEY`: Your Tavily API key

2. **Enable Dependabot:**
   
   Go to Settings → Security → Dependabot and enable:
   - Dependabot alerts
   - Dependabot security updates
   - Dependabot version updates

3. **Configure Branch Protection:**
   
   Go to Settings → Branches → Add rule for `main`:
   - Require pull request reviews
   - Require status checks to pass (select CI workflows)
   - Require branches to be up to date

## Usage

### Running Checks Locally

**Run all pre-commit hooks:**
```bash
pre-commit run --all-files
```

**Run specific hooks:**
```bash
pre-commit run black --all-files
pre-commit run ruff --all-files
pre-commit run mypy --all-files
```

**Run tests:**
```bash
pytest tests/ -v
```

**Run code quality checks manually:**
```bash
black --check .
ruff check .
mypy graphs/ --ignore-missing-imports
```

### Skipping Hooks

**Skip pre-commit hooks (not recommended):**
```bash
git commit --no-verify -m "commit message"
```

**Skip specific hooks:**
```bash
SKIP=mypy git commit -m "commit message"
```

### Updating Hooks

**Update pre-commit hooks to latest versions:**
```bash
pre-commit autoupdate
```

## Workflow Details

### CI Workflow Stages

1. **Code Quality** (runs first, fails fast)
   - Black formatting check
   - Ruff linting
   - MyPy type checking (non-blocking)

2. **Tests** (runs in parallel for Python 3.11 and 3.12)
   - Install dependencies
   - Create test environment
   - Run pytest with coverage

3. **Benchmarks** (only on PRs)
   - Run performance benchmarks
   - Compare with baseline
   - Alert on performance regressions (>150%)

### Pre-commit Hook Stages

Pre-commit hooks run in this order:
1. General file checks (whitespace, EOF, etc.)
2. Black (auto-formats code)
3. Ruff (lints and auto-fixes)
4. MyPy (type checks)
5. Bandit (security checks)
6. Safety (dependency vulnerabilities)

## Troubleshooting

### Pre-commit Hooks Failing

**Issue**: Hooks fail on first run
**Solution**: This is normal. Pre-commit will auto-format files. Review changes and commit again.

**Issue**: MyPy errors
**Solution**: MyPy is configured to be lenient. Fix type hints gradually or skip with `SKIP=mypy`.

**Issue**: Bandit security warnings
**Solution**: Review warnings and fix security issues or add `# nosec` comment with justification.

### CI Workflow Failures

**Issue**: Tests fail due to missing API keys
**Solution**: Configure repository secrets or use test keys for non-integration tests.

**Issue**: Dependency conflicts
**Solution**: Update `requirements.txt` with compatible versions.

**Issue**: Timeout errors
**Solution**: Increase timeout in workflow or optimize slow tests.

### Dependabot Issues

**Issue**: Too many PRs
**Solution**: Adjust `open-pull-requests-limit` in `.github/dependabot.yml`.

**Issue**: Breaking changes
**Solution**: Review PRs carefully, run tests locally before merging.

## Best Practices

1. **Always run pre-commit before pushing:**
   ```bash
   pre-commit run --all-files
   ```

2. **Keep dependencies up to date:**
   - Review Dependabot PRs weekly
   - Test updates in a separate branch

3. **Monitor CI failures:**
   - Fix failing tests immediately
   - Don't merge PRs with failing checks

4. **Use meaningful commit messages:**
   - Follow conventional commits format
   - Example: `feat: add new graph`, `fix: resolve API error`

5. **Review code quality reports:**
   - Check Ruff and MyPy outputs
   - Address warnings and errors

## Maintenance

### Regular Tasks

**Weekly:**
- Review and merge Dependabot PRs
- Check CI workflow runs for patterns
- Update pre-commit hooks: `pre-commit autoupdate`

**Monthly:**
- Review and update GitHub Actions versions
- Audit security alerts
- Review benchmark trends

**Quarterly:**
- Review and update CI/CD configuration
- Evaluate new tools and hooks
- Update documentation

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Black Documentation](https://black.readthedocs.io/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)

## Support

For issues or questions about the CI/CD pipeline:
1. Check this documentation
2. Review workflow logs in GitHub Actions
3. Check pre-commit hook output
4. Consult the team or create an issue
