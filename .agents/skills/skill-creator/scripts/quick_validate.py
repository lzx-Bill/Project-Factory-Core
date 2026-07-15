#!/usr/bin/env python3
"""
Quick validation script for skills - minimal version
"""

import json
import re
import sys
from pathlib import Path


def parse_frontmatter(text):
    """Parse the small top-level YAML subset used by SKILL.md files."""
    result = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith('#'):
            index += 1
            continue
        if line[0].isspace():
            index += 1  # Nested metadata is allowed but not validated here.
            continue
        if ':' not in line:
            raise ValueError(f"invalid top-level frontmatter line: {line}")

        key, raw_value = line.split(':', 1)
        key, raw_value = key.strip(), raw_value.strip()
        if raw_value in {'|', '|-', '>', '>-'}:
            block = []
            index += 1
            while index < len(lines) and (not lines[index] or lines[index][0].isspace()):
                block.append(lines[index].strip())
                index += 1
            result[key] = ('\n' if raw_value.startswith('|') else ' ').join(block).strip()
            continue
        if raw_value.startswith("'") and raw_value.endswith("'"):
            value = raw_value[1:-1].replace("''", "'")
        elif raw_value.startswith('"') and raw_value.endswith('"'):
            value = json.loads(raw_value)
        elif raw_value.lower() in {'true', 'false'}:
            value = raw_value.lower() == 'true'
        elif not raw_value:
            value = {}
        else:
            value = raw_value
        result[key] = value
        index += 1
    return result

def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Read and validate frontmatter
    content = skill_md.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False, "No YAML frontmatter found"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse the top-level YAML subset used by local skills. This intentionally
    # avoids a runtime PyYAML dependency for the repository's bootstrap check.
    try:
        frontmatter = parse_frontmatter(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except (ValueError, json.JSONDecodeError) as e:
        return False, f"Invalid YAML in frontmatter: {e}"

    # Define allowed properties
    # Support both the older local skill format and the current VS Code skill frontmatter.
    ALLOWED_PROPERTIES = {
        'name',
        'description',
        'license',
        'allowed-tools',
        'metadata',
        'compatibility',
        'argument-hint',
        'user-invocable',
        'disable-model-invocation',
    }

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (kebab-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be kebab-case (lowercase letters, digits, and hyphens only)"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"Name is too long ({len(name)} characters). Maximum is 64 characters."

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description must be a string, got {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description is too long ({len(description)} characters). Maximum is 1024 characters."

    argument_hint = frontmatter.get('argument-hint', '')
    if argument_hint:
        if not isinstance(argument_hint, str):
            return False, f"argument-hint must be a string, got {type(argument_hint).__name__}"
        if len(argument_hint) > 1024:
            return False, f"argument-hint is too long ({len(argument_hint)} characters). Maximum is 1024 characters."

    for bool_key in ('user-invocable', 'disable-model-invocation'):
        if bool_key in frontmatter and not isinstance(frontmatter[bool_key], bool):
            return False, f"{bool_key} must be a boolean, got {type(frontmatter[bool_key]).__name__}"

    # Validate compatibility field if present (optional)
    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, f"Compatibility must be a string, got {type(compatibility).__name__}"
        if len(compatibility) > 500:
            return False, f"Compatibility is too long ({len(compatibility)} characters). Maximum is 500 characters."

    return True, "Skill is valid!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
