# Scripts

This directory contains utility scripts for development, testing, and project setup.

## Available Scripts

### setup_dev_environment.py

Sets up the complete development environment including virtual environment, dependencies, and pre-commit hooks.

**Usage:**
```bash
python scripts/setup_dev_environment.py
```

**What it does:**
- Creates virtual environment
- Installs requirements.txt and requirements-dev.txt
- Installs pre-commit hooks
- Validates setup

### setup_ci_cd.py

Initializes CI/CD configuration and validates GitHub Actions workflows.

**Usage:**
```bash
python scripts/setup_ci_cd.py
```

**What it does:**
- Validates GitHub Actions workflow files
- Checks pre-commit configuration
- Verifies CI/CD setup

### run_benchmarks.py

Runs performance benchmarks and generates reports.

**Usage:**
```bash
# Run all benchmarks
python scripts/run_benchmarks.py

# Save baseline
python scripts/run_benchmarks.py --save baseline

# Compare with baseline
python scripts/run_benchmarks.py --compare baseline

# Generate histogram
python scripts/run_benchmarks.py --histogram
```

**Options:**
- `--save NAME`: Save benchmark results as baseline
- `--compare NAME`: Compare current run with saved baseline
- `--histogram`: Generate performance histogram

### validate_demo_examples.py

Validates all JSON examples in `demo-text.txt` to ensure they are properly formatted and parseable.

**Usage:**

```bash
python scripts/validate_demo_examples.py
```

### Output

The script will:
- Extract all JSON code blocks from demo-text.txt
- Validate each JSON block for syntax errors
- Report validation results with line numbers
- Provide a summary of valid/invalid examples

### Example Output

```
Validating demo examples...

✅ 1. Parallelization: Web + Wikipedia Search (line 17): Valid JSON
✅ 2. Sub-Graphs: Log Analysis (line 50): Valid JSON
...

============================================================
Validation Summary:
============================================================
Total JSON blocks: 36
Valid: 36
Invalid: 0
```

### Exit Codes

- `0`: All examples are valid
- `1`: One or more examples have JSON formatting errors

### When to Use

Run this script:
- After modifying demo-text.txt
- Before committing changes to demo examples
- As part of CI/CD validation
- When troubleshooting demo example issues
