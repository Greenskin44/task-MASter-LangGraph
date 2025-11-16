# GitHub Repository Settings Guide

Recommended settings for your new repository created from this template.

## Initial Repository Setup

When you created the repository from the template, you should configure:

### General Settings

1. **Repository Name**: Choose a descriptive name
2. **Description**: Brief description of your LangGraph project
3. **Website**: Optional - link to documentation or demo
4. **Topics**: Add relevant tags
   - Suggested: `langgraph`, `langchain`, `ai`, `agents`, `llm`, `python`

### Repository Visibility

- **Public**: For open-source projects
- **Private**: For proprietary or work projects

## Recommended Settings

### 1. Code and Automation

**Branches**
- Default branch: `main` ✅
- Branch protection rules (optional but recommended):
  - Require pull request reviews before merging
  - Require status checks to pass (CI tests)
  - Require conversation resolution before merging

**Actions**
- ✅ Allow all actions and reusable workflows
- This enables the CI/CD pipelines included in the template

### 2. Security

**Code Security and Analysis**

Enable these features:

- ✅ **Dependency graph** - Track dependencies
- ✅ **Dependabot alerts** - Security vulnerability alerts
- ✅ **Dependabot security updates** - Automatic security patches
- ✅ **Dependabot version updates** - Already configured in `.github/dependabot.yml`

**Secret Scanning**
- ✅ Enable if repository is public
- Prevents accidental API key commits

### 3. Features to Enable

- ✅ Issues - For bug tracking and feature requests
- ✅ Projects - Optional, for project management
- ✅ Discussions - Optional, for community Q&A
- ❌ Wiki - Not needed (use `docs/` folder instead)
- ❌ Sponsorships - Optional

### 4. Pull Requests

Recommended settings:

- ✅ Allow squash merging
- ✅ Allow merge commits
- ❌ Allow rebase merging (optional, your preference)
- ✅ Automatically delete head branches

### 5. Pages (Optional)

If you want to host documentation:

- **Source**: Deploy from a branch (e.g., `gh-pages`)
- **Theme**: Choose a theme
- Use for API docs or user guides

## Environment Secrets

Add these secrets for CI/CD:

**Settings → Secrets and variables → Actions → New repository secret**

Required secrets:
- `OPENAI_API_KEY` - For running tests with real API
- `TAVILY_API_KEY` - For search functionality tests
- `LANGSMITH_API_KEY` - Optional, for tracing

**Note**: Tests will skip if secrets aren't set, so these are optional for public repos.

## Branch Protection Rules

Recommended for `main` branch:

**Settings → Branches → Add branch protection rule**

Branch name pattern: `main`

Enable:
- ✅ Require a pull request before merging
  - Required approvals: 1 (for teams)
- ✅ Require status checks to pass before merging
  - Required checks: `CI`, `pre-commit`
- ✅ Require conversation resolution before merging
- ✅ Do not allow bypassing the above settings

## Labels

Recommended issue labels (create in Issues → Labels):

**Type:**
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `question` - Questions about usage

**Priority:**
- `priority: high` - Urgent issues
- `priority: medium` - Standard priority
- `priority: low` - Nice to have

**Status:**
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `wontfix` - This will not be worked on

## Issue Templates

The template includes:

- `.github/PULL_REQUEST_TEMPLATE.md` - PR template

Consider adding issue templates:

**Settings → Features → Set up templates**

Suggested templates:
- Bug report
- Feature request
- Question

## Webhooks (Optional)

For advanced integrations:

**Settings → Webhooks → Add webhook**

Use for:
- Slack/Discord notifications
- Custom CI/CD triggers
- Deployment automation

## Repository Topics

Add relevant topics to help discovery:

Suggested topics:
- `langgraph`
- `langchain`
- `ai`
- `llm`
- `agents`
- `multi-agent-system`
- `python`
- `machine-learning`
- `production-ready`
- `template`

## Social Preview Image

Create a social preview image:

**Settings → General → Social preview**

Recommended size: 1280x640 pixels

Shows when sharing your repository on social media.

## Verify Setup Checklist

After configuring:

- [ ] Repository name and description set
- [ ] Topics added
- [ ] GitHub Actions enabled
- [ ] Dependabot enabled
- [ ] Branch protection configured (if using)
- [ ] Secrets added for CI/CD
- [ ] Issue labels created
- [ ] README badges updated with your username/repo
- [ ] License file verified
- [ ] Social preview image added (optional)

## Testing GitHub Actions

After setup, trigger CI/CD:

```bash
# Make a small change
echo "# Test" >> TEST.md

# Commit and push
git add TEST.md
git commit -m "Test CI/CD"
git push

# Check Actions tab on GitHub
# Should see CI and pre-commit workflows running
```

## Troubleshooting

**Actions not running?**
- Check Settings → Actions → General
- Ensure "Allow all actions and reusable workflows" is selected

**Branch protection blocking you?**
- Create a branch and PR instead of pushing to main
- Or temporarily disable protection while setting up

**Secrets not working?**
- Verify secret names match exactly
- Secrets are case-sensitive
- Check workflow files reference correct secret names

## Resources

- [GitHub Docs - Managing Repository Settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)

---

**Your repository is now fully configured!** 🎉
