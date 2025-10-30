# Scripts

This directory contains utility scripts for the LangGraph productionalization project.

## validate_demo_examples.py

Validates all JSON examples in `demo-text.txt` to ensure they are properly formatted and parseable.

### Usage

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
