"""Validate demo examples JSON formatting.

This script extracts and validates all JSON examples from demo-text.txt
to ensure they are properly formatted and can be parsed.
"""

import json
import re
from pathlib import Path


def extract_json_blocks(content: str) -> list[tuple[str, str, int]]:
    """Extract JSON code blocks from markdown content.
    
    Args:
        content: Markdown content containing JSON blocks
        
    Returns:
        List of tuples (section_name, json_content, line_number)
    """
    json_blocks = []
    lines = content.split('\n')
    current_section = "Unknown"
    in_json_block = False
    json_content = []
    start_line = 0
    
    for i, line in enumerate(lines, 1):
        # Track current section
        if line.startswith('###'):
            current_section = line.strip('# ').strip()
        
        # Detect JSON block start
        if line.strip() == '```json':
            in_json_block = True
            json_content = []
            start_line = i
            continue
        
        # Detect JSON block end
        if line.strip() == '```' and in_json_block:
            in_json_block = False
            if json_content:
                json_blocks.append((
                    current_section,
                    '\n'.join(json_content),
                    start_line
                ))
            continue
        
        # Collect JSON content
        if in_json_block:
            json_content.append(line)
    
    return json_blocks


def validate_json_examples(demo_file: Path) -> dict:
    """Validate all JSON examples in the demo file.
    
    Args:
        demo_file: Path to demo-text.txt
        
    Returns:
        Dictionary with validation results
    """
    content = demo_file.read_text(encoding='utf-8')
    json_blocks = extract_json_blocks(content)
    
    results = {
        'total': len(json_blocks),
        'valid': 0,
        'invalid': 0,
        'errors': []
    }
    
    for section, json_str, line_num in json_blocks:
        try:
            # Try to parse JSON
            parsed = json.loads(json_str)
            results['valid'] += 1
            print(f"✅ {section} (line {line_num}): Valid JSON")
        except json.JSONDecodeError as e:
            results['invalid'] += 1
            results['errors'].append({
                'section': section,
                'line': line_num,
                'error': str(e),
                'content': json_str[:100] + '...' if len(json_str) > 100 else json_str
            })
            print(f"❌ {section} (line {line_num}): Invalid JSON - {e}")
    
    return results


def main():
    """Main validation function."""
    demo_file = Path('demo-text.txt')
    
    if not demo_file.exists():
        print(f"❌ Error: {demo_file} not found")
        return 1
    
    print("Validating demo examples...\n")
    results = validate_json_examples(demo_file)
    
    print(f"\n{'='*60}")
    print(f"Validation Summary:")
    print(f"{'='*60}")
    print(f"Total JSON blocks: {results['total']}")
    print(f"Valid: {results['valid']}")
    print(f"Invalid: {results['invalid']}")
    
    if results['invalid'] > 0:
        print(f"\n{'='*60}")
        print(f"Errors Found:")
        print(f"{'='*60}")
        for error in results['errors']:
            print(f"\nSection: {error['section']}")
            print(f"Line: {error['line']}")
            print(f"Error: {error['error']}")
            print(f"Content preview: {error['content']}")
    
    return 0 if results['invalid'] == 0 else 1


if __name__ == '__main__':
    exit(main())
