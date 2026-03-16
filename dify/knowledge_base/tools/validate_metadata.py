#!/usr/bin/env python3
"""
Metadata Validation Script for Avni AI Assistant Knowledge Base

Validates that all markdown files have proper YAML frontmatter with required fields.
"""

import yaml
import glob
import sys
from pathlib import Path
from typing import Tuple, List

REQUIRED_FIELDS = [
    'title',
    'category',
    'audience',
    'difficulty',
    'priority',
    'keywords',
    'last_updated'
]

OPTIONAL_FIELDS = [
    'subcategory',
    'task_types',
    'features',
    'technical_level',
    'implementation_phase',
    'complexity',
    'query_patterns',
    'answer_types',
    'related_topics',
    'prerequisites',
    'estimated_reading_time',
    'version',
    'retrieval_boost',
    'synonyms'
]

VALID_PRIORITIES = ['critical', 'high', 'medium', 'low']
VALID_DIFFICULTIES = ['beginner', 'intermediate', 'advanced']
VALID_AUDIENCES = ['implementer', 'admin', 'developer', 'all']


def validate_metadata(file_path: str) -> Tuple[bool, str]:
    """Validate metadata in a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for frontmatter
        if not content.startswith('---'):
            return False, "Missing YAML frontmatter (should start with ---)"
        
        # Extract YAML
        parts = content.split('---', 2)
        if len(parts) < 3:
            return False, "Invalid frontmatter structure (needs --- at start and end)"
        
        try:
            metadata = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            return False, f"Invalid YAML syntax: {e}"
        
        if not metadata:
            return False, "Empty frontmatter"
        
        # Check required fields
        missing = [f for f in REQUIRED_FIELDS if f not in metadata]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"
        
        # Validate priority
        if metadata['priority'] not in VALID_PRIORITIES:
            return False, f"Invalid priority '{metadata['priority']}'. Must be one of: {', '.join(VALID_PRIORITIES)}"
        
        # Validate difficulty
        if metadata['difficulty'] not in VALID_DIFFICULTIES:
            return False, f"Invalid difficulty '{metadata['difficulty']}'. Must be one of: {', '.join(VALID_DIFFICULTIES)}"
        
        # Validate audience
        if metadata['audience'] not in VALID_AUDIENCES:
            return False, f"Invalid audience '{metadata['audience']}'. Must be one of: {', '.join(VALID_AUDIENCES)}"
        
        # Validate keywords is a list
        if not isinstance(metadata['keywords'], list):
            return False, "Keywords must be a list"
        
        if len(metadata['keywords']) == 0:
            return False, "Keywords list cannot be empty"
        
        return True, "Valid metadata"
    
    except Exception as e:
        return False, f"Error reading file: {e}"


def scan_directory(directory: str, exclude_dirs: List[str] = None) -> dict:
    """Scan directory for markdown files and validate metadata."""
    if exclude_dirs is None:
        exclude_dirs = ['node_modules', '.git', '_archive', 'tools']
    
    results = {
        'valid': [],
        'invalid': [],
        'no_metadata': []
    }
    
    # Find all markdown files
    md_files = []
    for pattern in ['**/*.md', '*.md']:
        md_files.extend(glob.glob(f"{directory}/{pattern}", recursive=True))
    
    # Filter out excluded directories
    md_files = [
        f for f in md_files 
        if not any(excl in f for excl in exclude_dirs)
    ]
    
    for file_path in md_files:
        valid, message = validate_metadata(file_path)
        
        rel_path = str(Path(file_path).relative_to(directory))
        
        if valid:
            results['valid'].append(rel_path)
        elif "Missing YAML frontmatter" in message:
            results['no_metadata'].append((rel_path, message))
        else:
            results['invalid'].append((rel_path, message))
    
    return results


def print_results(results: dict):
    """Print validation results."""
    total = len(results['valid']) + len(results['invalid']) + len(results['no_metadata'])
    
    print(f"\n{'='*70}")
    print(f"METADATA VALIDATION RESULTS")
    print(f"{'='*70}\n")
    
    print(f"Total files scanned: {total}")
    print(f"✅ Valid: {len(results['valid'])}")
    print(f"❌ Invalid: {len(results['invalid'])}")
    print(f"⚠️  No metadata: {len(results['no_metadata'])}")
    
    if results['invalid']:
        print(f"\n{'='*70}")
        print("INVALID METADATA:")
        print(f"{'='*70}\n")
        for file_path, message in results['invalid']:
            print(f"❌ {file_path}")
            print(f"   {message}\n")
    
    if results['no_metadata']:
        print(f"\n{'='*70}")
        print("FILES WITHOUT METADATA:")
        print(f"{'='*70}\n")
        for file_path, message in results['no_metadata']:
            print(f"⚠️  {file_path}")
            print(f"   {message}\n")
    
    if results['valid']:
        print(f"\n{'='*70}")
        print(f"VALID FILES ({len(results['valid'])}):")
        print(f"{'='*70}\n")
        for file_path in results['valid']:
            print(f"✅ {file_path}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python validate_metadata.py <directory>")
        print("Example: python validate_metadata.py ../AI_ASSISTANT_KNOWLEDGE_BASE")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not Path(directory).exists():
        print(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)
    
    print(f"Scanning directory: {directory}")
    results = scan_directory(directory)
    print_results(results)
    
    # Exit with error code if there are invalid files
    if results['invalid'] or results['no_metadata']:
        sys.exit(1)
    else:
        print(f"\n✅ All files have valid metadata!")
        sys.exit(0)


if __name__ == '__main__':
    main()
