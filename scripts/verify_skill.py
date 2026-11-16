#!/usr/bin/env python3
"""Validate the skill directory before packaging or release.

Checks that matter for distribution and for `skills add`:
- SKILL.md has YAML frontmatter with `name` and `description` (2-1024 chars)
- `name` matches the directory name
- every relative markdown link inside the skill resolves
- code fences are balanced in every markdown file
- no `evals/` (development fixtures) inside the distributed skill directory
- repo-level `evals/evals.json` parses as JSON when present

Usage: python scripts/verify_skill.py [skill_dir]
Exit code 1 on any error, so it can gate CI.
"""
import json
import pathlib
import re
import sys

NAME_RE = re.compile(r'^[a-z0-9][a-z0-9-]*$')
LINK_RE = re.compile(r'\]\(([^)#]+)\)')


def parse_frontmatter(text):
    if not text.startswith('---'):
        return None
    end = text.find('\n---', 3)
    if end == -1:
        return None
    block = text[3:end].strip('\n')
    data = {}
    key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if line[:1] in (' ', '\t') and key:
            data[key] = (data[key] + ' ' + line.strip()).strip()
            continue
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def main(argv):
    skill = pathlib.Path(argv[1] if len(argv) > 1 else 'cocos-creator-dev')
    errors = []
    warnings = []

    skill_md = skill / 'SKILL.md'
    if not skill_md.is_file():
        print(f'ERROR: {skill_md} not found')
        return 1
    text = skill_md.read_text(encoding='utf-8')
    meta = parse_frontmatter(text)
    if meta is None:
        errors.append('SKILL.md has no YAML frontmatter')
    else:
        name = meta.get('name', '')
        desc = meta.get('description', '')
        if not name:
            errors.append('frontmatter: missing name')
        elif name != skill.name:
            errors.append(f'frontmatter name "{name}" != directory "{skill.name}"')
        elif not NAME_RE.match(name):
            errors.append(f'frontmatter name "{name}" must be lowercase kebab-case')
        if not desc:
            errors.append('frontmatter: missing description')
        elif not (2 <= len(desc) <= 1024):
            errors.append(f'description length {len(desc)} outside 2-1024')

    markdown = sorted(skill.rglob('*.md'))
    for path in markdown:
        body = path.read_text(encoding='utf-8')
        fences = sum(1 for line in body.splitlines() if line.strip().startswith('```'))
        if fences % 2:
            errors.append(f'{path}: unbalanced code fences ({fences})')
        for target in LINK_RE.findall(body):
            if target.startswith(('http://', 'https://', 'mailto:')):
                continue
            if not (path.parent / target).exists():
                errors.append(f'{path}: broken link {target}')

    if (skill / 'evals').exists():
        errors.append('skill directory contains evals/; move development fixtures to the repo root')

    root_evals = pathlib.Path('evals/evals.json')
    if root_evals.is_file():
        try:
            data = json.loads(root_evals.read_text(encoding='utf-8'))
            evals = data.get('evals', [])
            if not evals:
                warnings.append('evals/evals.json has no evals')
            for item in evals:
                if not item.get('prompt') or not item.get('assertions'):
                    warnings.append(f"eval {item.get('id')} lacks prompt or assertions")
        except json.JSONDecodeError as exc:
            errors.append(f'evals/evals.json: {exc}')

    for path in markdown:
        if path.stat().st_size > 64 * 1024:
            warnings.append(f'{path}: larger than 64 KiB, consider splitting')

    for line in warnings:
        print(f'WARN: {line}')
    if errors:
        for line in errors:
            print(f'ERROR: {line}')
        return 1
    print(f'OK: {skill} ({len(markdown)} markdown files)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
