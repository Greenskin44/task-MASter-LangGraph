# New Project Setup Checklist

Use this checklist when creating a new project from this template.

## Initial Setup

- [ ] Clone or use GitHub's "Use this template" feature
- [ ] Remove git history if cloned (not needed if using template feature)
  ```bash
  rm -rf .git
  git init
  ```

## Customization

### 1. Project Metadata
- [ ] Update `pyproject.toml`:
  - [ ] Change `name` to your project name
  - [ ] Update `description`
  - [ ] Update `authors`
  - [ ] Update `Homepage` and `Repository` URLs
  - [ ] Update `keywords` if needed

- [ ] Update `README.md`:
  - [ ] Change project title and description
  - [ ] Update repository URL in clone command
  - [ ] Update LangSmith project name
  - [ ] Describe your specific graphs
  - [ ] Update or remove demo examples section

- [ ] Update `LICENSE`:
  - [ ] Change copyright holder name if needed
  - [ ] Update year if needed

- [ ] Update `CONTRIBUTING.md`:
  - [ ] Change repository URLs
  - [ ] Customize contribution guidelines for your project

### 2. Configuration Files

- [ ] Review and update `langgraph.json`:
  - [ ] Remove example graphs you don't need
  - [ ] Add your own graph paths
  - [ ] Verify Python version
  - [ ] Verify dependencies path

- [ ] Create `.env` from `.env.example`:
  ```bash
  cp .env.example .env
  ```
  - [ ] Add your API keys
  - [ ] Add any additional environment variables your graphs need

- [ ] Update `.env.example`:
  - [ ] Add placeholders for any new API keys
  - [ ] Document what each key is for
  - [ ] Remove keys you don't need

### 3. Dependencies

- [ ] Review `requirements.txt`:
  - [ ] Remove dependencies for graphs you removed
  - [ ] Add dependencies for your graphs
  - [ ] Update versions if needed

- [ ] Review `requirements-dev.txt`:
  - [ ] Customize development tools
  - [ ] Add any team-specific tools

### 4. Example Graphs (Choose One)

**Option A: Keep Examples as Reference**
- [ ] Leave example graphs in place
- [ ] Add your graphs alongside them
- [ ] Update `langgraph.json` to include both

**Option B: Remove Examples and Start Fresh**
- [ ] Delete example graph directories:
  ```bash
  rm -rf graphs/studio
  rm -rf graphs/deployment
  rm -rf graphs/email_assistant
  rm -rf graphs/research
  ```
- [ ] Delete example test files:
  ```bash
  rm tests/test_studio_graphs.py
  rm tests/test_deployment_graphs.py
  rm tests/test_email_assistant.py
  rm tests/test_research_agent.py
  ```
- [ ] Keep `graphs/utils` and `graphs/__init__.py`
- [ ] Create your first graph directory

### 5. Documentation

- [ ] Update `docs/ARCHITECTURE_DESIGN.md` with your architecture
- [ ] Update `docs/DEMO_GUIDE.md` with your demo walkthrough
- [ ] Update or remove `docs/MAINTENANCE_NOTES.md`
- [ ] Update `docs/TESTING_PLAN.md` for your tests
- [ ] Remove `docs/TESTING_RESULTS.md` (or clear for fresh results)
- [ ] Remove `docs/PERFORMANCE_BENCHMARKS.md` (or clear for fresh benchmarks)
- [ ] Keep `docs/CI_CD_SETUP.md` and `docs/ERROR_HANDLING_AND_LOGGING.md`

- [ ] Update `demo-text.txt`:
  - [ ] Remove example demos
  - [ ] Add copy-paste examples for your graphs

### 6. GitHub Configuration

- [ ] Review `.github/workflows/ci.yml`:
  - [ ] Customize test commands if needed
  - [ ] Update Python version matrix if needed

- [ ] Review `.github/workflows/pre-commit.yml`:
  - [ ] Customize as needed for your team

- [ ] Review `.github/PULL_REQUEST_TEMPLATE.md`:
  - [ ] Customize PR template for your team

- [ ] Review `.github/dependabot.yml`:
  - [ ] Adjust update frequency if needed

### 7. Testing

- [ ] Update `pytest.ini`:
  - [ ] Adjust test markers if needed
  - [ ] Customize test options

- [ ] Update `tests/conftest.py`:
  - [ ] Add fixtures for your graphs
  - [ ] Remove unused fixtures

- [ ] Create test files for your graphs:
  ```bash
  touch tests/test_my_graph.py
  ```

- [ ] Update or remove `tests/test_benchmarks.py`:
  - [ ] Add benchmarks for your graphs
  - [ ] Remove example benchmarks

### 8. Code Quality

- [ ] Review `.pre-commit-config.yaml`:
  - [ ] Adjust hooks as needed
  - [ ] Update tool versions

- [ ] Review `pyproject.toml` tool configurations:
  - [ ] Black settings
  - [ ] Ruff settings
  - [ ] Mypy settings

## Development Environment Setup

- [ ] Create virtual environment:
  ```bash
  python -m venv project-env
  source project-env/bin/activate  # Mac/Linux
  .\project-env\Scripts\Activate.ps1  # Windows
  ```

- [ ] Install dependencies:
  ```bash
  pip install -r requirements.txt
  pip install -r requirements-dev.txt
  ```

- [ ] Install pre-commit hooks:
  ```bash
  pip install pre-commit
  pre-commit install
  ```

- [ ] Test the setup:
  ```bash
  langgraph dev
  ```

## First Graph Development

- [ ] Create your first graph:
  ```bash
  mkdir -p graphs/my_graph
  touch graphs/my_graph/__init__.py
  ```

- [ ] Copy template:
  ```bash
  cp graphs/TEMPLATE_GRAPH.py graphs/my_graph/my_graph.py
  ```

- [ ] Implement your graph logic

- [ ] Add to `langgraph.json`:
  ```json
  {
    "graphs": {
      "my_graph": "./graphs/my_graph/my_graph.py:graph"
    }
  }
  ```

- [ ] Create tests:
  ```bash
  touch tests/test_my_graph.py
  ```

- [ ] Write tests for your graph

- [ ] Run tests:
  ```bash
  pytest tests/test_my_graph.py -v
  ```

## Git and GitHub

- [ ] Initialize git repository (if not done):
  ```bash
  git init
  ```

- [ ] Create initial commit:
  ```bash
  git add .
  git commit -m "Initial commit from template"
  ```

- [ ] Create GitHub repository (on GitHub website)

- [ ] Add remote and push:
  ```bash
  git remote add origin https://github.com/yourusername/your-repo.git
  git branch -M main
  git push -u origin main
  ```

## Optional: Enable GitHub Features

- [ ] Enable GitHub Actions in repository settings
- [ ] Enable Dependabot alerts
- [ ] Add repository description
- [ ] Add repository topics/tags
- [ ] Add repository to GitHub organizations if applicable
- [ ] Set up branch protection rules
- [ ] Configure GitHub Pages if documenting online

## Documentation Updates

- [ ] Add repository badges to README.md:
  - [ ] CI status badge
  - [ ] License badge
  - [ ] Python version badge

- [ ] Create CHANGELOG.md for tracking changes

- [ ] Review and update all documentation links

## Final Checks

- [ ] Run all tests:
  ```bash
  pytest tests/ -v
  ```

- [ ] Run code quality checks:
  ```bash
  black .
  ruff check .
  mypy graphs/
  ```

- [ ] Run pre-commit on all files:
  ```bash
  pre-commit run --all-files
  ```

- [ ] Test LangGraph Studio:
  ```bash
  langgraph dev
  ```

- [ ] Verify all graphs load in Studio UI

- [ ] Test example inputs (from demo-text.txt)

- [ ] Review all documentation is accurate

- [ ] Commit any final changes:
  ```bash
  git add .
  git commit -m "Complete initial setup"
  git push
  ```

## You're Ready!

✅ Your project is now set up and ready for development!

---

**Next Steps:**
1. Start building your graphs
2. Write tests as you go
3. Update documentation
4. Commit regularly
5. Use the example graphs as reference

**Resources:**
- See [TEMPLATE_USAGE.md](TEMPLATE_USAGE.md) for detailed guidance
- Review example graphs for patterns
- Check [LangGraph docs](https://langchain-ai.github.io/langgraph/)
