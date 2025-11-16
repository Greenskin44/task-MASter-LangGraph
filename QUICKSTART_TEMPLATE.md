# Quick Start: Using This as a Template

**⚡ Get up and running with your own LangGraph project in under 5 minutes!**

## Step 1: Create Your Project (2 minutes)

### Option A: Use GitHub Template Feature (Recommended)
1. Click the green **"Use this template"** button at the top of this repository
2. Select **"Create a new repository"**
3. Name your repository
4. Click **"Create repository"**
5. Clone your new repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

### Option B: Manual Clone
```bash
git clone https://github.com/greenskin44/task-MASter-LangGraph.git my-langgraph-project
cd my-langgraph-project
rm -rf .git
git init
```

## Step 2: Quick Customization (1 minute)

Edit these 3 files with your project info:

**1. pyproject.toml:**
```toml
[project]
name = "your-project-name"  # ← Change this
description = "Your description"  # ← Change this
authors = [{name = "Your Name"}]  # ← Change this
```

**2. README.md** (top of file):
```markdown
# Your Project Name  ← Change this

Your project description here  ← Change this
```

**3. Create .env file:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## Step 3: Install Dependencies (1 minute)

```bash
# Create virtual environment
python -m venv project-env

# Activate it
source project-env/bin/activate  # Mac/Linux
.\project-env\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Test It Works (1 minute)

```bash
# Start LangGraph Studio
langgraph dev
```

Visit http://127.0.0.1:2024 - you should see all 8 example graphs! 🎉

## What's Next?

### Keep the Examples or Remove Them?

**Option A: Keep Examples (Recommended for Learning)**
- Examples serve as reference
- Learn from working implementations
- Add your graphs alongside them

**Option B: Start Fresh**
```bash
# Remove example graphs
rm -rf graphs/studio graphs/deployment graphs/email_assistant graphs/research

# Remove example tests
rm tests/test_studio_graphs.py tests/test_deployment_graphs.py
rm tests/test_email_assistant.py tests/test_research_agent.py

# Keep the utilities
# graphs/utils/ stays!
```

### Create Your First Graph

1. **Copy the template:**
   ```bash
   mkdir -p graphs/my_first_graph
   cp graphs/TEMPLATE_GRAPH.py graphs/my_first_graph/my_graph.py
   ```

2. **Edit the template** (`graphs/my_first_graph/my_graph.py`)
   - Customize the state
   - Implement your nodes
   - Define edges

3. **Register in langgraph.json:**
   ```json
   {
     "graphs": {
       "my_first_graph": "./graphs/my_first_graph/my_graph.py:graph"
     }
   }
   ```

4. **Test it:**
   ```bash
   langgraph dev
   ```

5. **Create tests:**
   ```bash
   touch tests/test_my_first_graph.py
   ```

## Common First Steps

### Add More API Keys
Edit `.env` and `.env.example`:
```bash
# .env (actual keys - never commit!)
ANTHROPIC_API_KEY=sk-xxx
CUSTOM_API_KEY=xxx

# .env.example (placeholders)
ANTHROPIC_API_KEY=sk-xxx
CUSTOM_API_KEY=xxx
```

### Add New Dependencies
```bash
echo "anthropic==0.25.0" >> requirements.txt
pip install -r requirements.txt
```

### Run Tests
```bash
pytest tests/ -v
```

### Format Code
```bash
black .
ruff check .
```

## Detailed Guides

- **Full customization guide:** See [TEMPLATE_USAGE.md](TEMPLATE_USAGE.md)
- **Step-by-step checklist:** See [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- **Graph examples:** Explore `graphs/` directories
- **Testing examples:** See `tests/` directory

## Template Features You Get

✅ **8 Working Graph Examples**
- Parallelization
- Sub-graphs  
- Map-reduce
- Multi-agent coordination
- Memory management
- Email processing
- Research workflows

✅ **Complete Testing Suite**
- Unit tests
- Integration tests
- Performance benchmarks
- 26+ test scenarios

✅ **Development Tools**
- Black (formatting)
- Ruff (linting)
- Mypy (type checking)
- Pre-commit hooks

✅ **CI/CD Pipeline**
- GitHub Actions workflows
- Automated testing
- Dependency management
- Security scanning

✅ **Documentation Templates**
- Architecture docs
- Demo guides
- Maintenance notes
- API documentation

## Troubleshooting

**Can't install dependencies?**
```bash
# Upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt
```

**LangGraph Studio won't start?**
```bash
# Check if langgraph-cli is installed
pip install langgraph-cli

# Verify .env file exists
cp .env.example .env
# Add your API keys to .env
```

**Import errors?**
```bash
# Make sure virtual environment is activated
# You should see (project-env) in your prompt
```

**Pre-commit hooks failing?**
```bash
# Skip for now with --no-verify
git commit --no-verify -m "message"

# Or fix the pre-commit config
# See .pre-commit-config.yaml
```

## Need Help?

1. 📖 Read [TEMPLATE_USAGE.md](TEMPLATE_USAGE.md) for detailed instructions
2. 💡 Check example graphs in `graphs/` for patterns
3. 📝 Review `docs/` for architecture and design decisions
4. 🔍 Search [LangGraph docs](https://langchain-ai.github.io/langgraph/)
5. 🐛 Open an issue in the template repository

## Ready to Build!

You now have a production-ready LangGraph project structure! 

**Next steps:**
1. Customize the template files
2. Build your first graph
3. Write tests
4. Deploy!

**Happy building!** 🚀
