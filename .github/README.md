# GitHub Configuration

This directory contains GitHub-specific configuration files for CI/CD, automation, and project management.

## Contents

### Workflows (`.github/workflows/`)

1. **ci.yml** - Main CI/CD pipeline
   - Runs on: Push and PR to `main` and `develop` branches
   - Jobs:
     - `test`: Runs pytest test suite with API keys
     - `code-quality`: Runs Black, Ruff, and Mypy checks
   - Python version: 3.11
   - Caches pip dependencies for faster builds

2. **pre-commit.yml** - Pre-commit hook validation
   - Runs on: Push and PR
   - Validates all pre-commit hooks in CI
   - Caches pre-commit hooks

3. **dependency-review.yml** - Dependency security review
   - Runs on: Pull requests only
   - Reviews dependency changes for security issues
   - Fails on moderate or higher severity vulnerabilities
   - Posts summary comment in PR

### Dependabot (`dependabot.yml`)

Automated dependency updates:

- **Python packages** (`pip`):
  - Weekly updates on Mondays
  - Groups: langgraph, langchain, development tools
  - Max 5 open PRs
  - Labels: `dependencies`, `python`

- **GitHub Actions**:
  - Weekly updates on Mondays
  - Max 3 open PRs
  - Labels: `dependencies`, `github-actions`

### Templates

- **PULL_REQUEST_TEMPLATE.md**: Standard PR template with checklist

## Setup Requirements

### GitHub Secrets

Configure these secrets in repository settings for CI workflows:

```
Settings → Secrets and variables → Actions → New repository secret
```

Required secrets:
- `OPENAI_API_KEY`: OpenAI API key for LLM operations
- `TAVILY_API_KEY`: Tavily API key for web search
- `LANGSMITH_API_KEY`: LangSmith API key for tracing (optional)

### Branch Protection

Recommended branch protection rules for `main`:

- Require pull request reviews before merging
- Require status checks to pass before merging:
  - `test` (CI workflow)
  - `code-quality` (CI workflow)
  - `pre-commit` (Pre-commit workflow)
- Require branches to be up to date before merging
- Require linear history

## Workflow Status Badges

Add these badges to your README.md:

```markdown
![CI](https://github.com/your-username/langgraph-project/workflows/CI/badge.svg)
![Pre-commit](https://github.com/your-username/langgraph-project/workflows/Pre-commit%20Checks/badge.svg)
```

## Customization

### Modifying Workflows

1. Edit workflow files in `.github/workflows/`
2. Test in a feature branch
3. Verify workflows run successfully
4. Merge to main after approval

### Adjusting Dependabot

Edit `.github/dependabot.yml` to:
- Change update frequency
- Modify PR limits
- Add/remove package groups
- Change reviewers or labels

### Adding New Workflows

1. Create new `.yml` file in `.github/workflows/`
2. Define triggers, jobs, and steps
3. Test thoroughly
4. Document in this README

## Troubleshooting

### Workflow Failures

**Tests fail in CI but pass locally:**
- Check API keys are configured as secrets
- Verify Python version matches (3.11)
- Check for environment-specific issues

**Code quality checks fail:**
- Run locally: `black --check .`, `ruff check .`, `mypy graphs/`
- Fix issues and push again
- Pre-commit hooks should catch these before push

**Dependabot PRs fail:**
- Review dependency changelog for breaking changes
- Test locally before merging
- Pin versions if needed for stability

### Permissions Issues

If workflows can't post comments or update PRs:
- Check workflow permissions in repository settings
- Ensure `GITHUB_TOKEN` has necessary permissions
- Review workflow `permissions:` section

## Best Practices

1. **Always use feature branches** - Never commit directly to `main`
2. **Keep PRs focused** - One feature/fix per PR
3. **Review Dependabot PRs promptly** - Don't let them pile up
4. **Monitor workflow runs** - Check Actions tab regularly
5. **Update workflows carefully** - Test changes thoroughly

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
