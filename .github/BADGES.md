# README Badges

Add these badges to your README.md to showcase your project status and features.

## How to Use

1. Replace `YOUR_USERNAME` with your GitHub username
2. Replace `YOUR_REPO` with your repository name
3. Copy the badges you want to your README.md

## Available Badges

### Project Status

```markdown
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0.2-purple)
```

### CI/CD Status

```markdown
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/badge.svg)
![Pre-commit](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Pre-commit%20Checks/badge.svg)
```

### Code Quality

```markdown
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Ruff](https://img.shields.io/badge/linting-ruff-red)
![Type checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue)
```

### Testing

```markdown
![Tests](https://img.shields.io/badge/tests-26%2B%20scenarios-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-85%25-yellowgreen)
```

### Additional

```markdown
![Maintained](https://img.shields.io/badge/maintained-yes-brightgreen)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
```

## Example README Header

Here's how it looks all together:

```markdown
# Your Project Name

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![LangGraph](https://img.shields.io/badge/LangGraph-1.0.2-purple)
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/badge.svg)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)

Your project description here.

## Features

- Feature 1
- Feature 2
- Feature 3
```

## Customizing Badges

You can create custom badges at [shields.io](https://shields.io/):

1. Visit https://shields.io/
2. Choose "Static Badge"
3. Enter your label, message, and color
4. Copy the markdown

Example custom badge:
```markdown
![Custom](https://img.shields.io/badge/custom-badge-blue)
```

## Dynamic Badges

For dynamic badges (like test coverage), you'll need to:

1. Set up a coverage service (Codecov, Coveralls)
2. Use their badge URLs
3. Update during CI/CD runs

## Tips

- Place badges at the top of your README
- Don't overdo it - 4-8 badges is plenty
- Keep badges relevant to your project
- Update badge values when you upgrade dependencies
