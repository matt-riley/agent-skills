#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
import yaml
NAME_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
CANONICAL_HEADINGS = (
    '## Use this skill when',
    '## Do not use this skill when',
    '## Inputs to gather',
    '## First move',
    '## Guardrails',
)
def fail(errors, message):
    errors.append(message)
def load_skill(path):
    text = path.read_text()
    m = re.match(r'^---\n(.*?)\n---\n?', text, re.S)
    if not m:
        raise ValueError('missing YAML frontmatter')
    return yaml.safe_load(m.group(1)) or {}, text[m.end():]
def validate_trigger_queries(path, errors):
    data = json.loads(path.read_text())
    if not isinstance(data, list):
        fail(errors, f'{path}: trigger queries must be a JSON array')
        return
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            fail(errors, f'{path}: item {idx} must be an object')
            continue
        if not isinstance(item.get('query'), str) or not item['query'].strip():
            fail(errors, f'{path}: item {idx} missing non-empty query')
        if not isinstance(item.get('should_trigger'), bool):
            fail(errors, f'{path}: item {idx} missing boolean should_trigger')
def validate_evals(path, skill_name, errors):
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        fail(errors, f'{path}: evals.json must be an object')
        return
    if data.get('skill_name') != skill_name:
        fail(errors, f'{path}: skill_name must equal {skill_name!r}')
    evals = data.get('evals')
    if not isinstance(evals, list) or not evals:
        fail(errors, f'{path}: evals must be a non-empty array')
        return
    for idx, item in enumerate(evals):
        if not isinstance(item, dict):
            fail(errors, f'{path}: eval {idx} must be an object')
            continue
        for key in ('id', 'prompt', 'expected_behavior'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                fail(errors, f'{path}: eval {idx} missing non-empty {key}')
        assertions = item.get('assertions')
        if not isinstance(assertions, list) or not assertions or not all(isinstance(a, str) and a.strip() for a in assertions):
            fail(errors, f'{path}: eval {idx} assertions must be a non-empty string array')
        files = item.get('files', [])
        if not isinstance(files, list) or not all(isinstance(f, str) for f in files):
            fail(errors, f'{path}: eval {idx} files must be a string array when present')
FENCE_RE = re.compile(r'^```.*?^```', re.M | re.S)
def strip_fences(body):
    return FENCE_RE.sub('', body)
def validate_canonical_headings(skill_path, body, errors):
    stripped = strip_fences(body)
    for heading in CANONICAL_HEADINGS:
        if not re.search(r'^' + re.escape(heading) + r'\s*$', stripped, re.M):
            fail(errors, f'{skill_path}: missing canonical heading {heading!r}')
def validate_inter_skill_links(skill_path, body, skill_names, errors):
    # Match either markdown links like [text](../name/SKILL.md) or inline ../name/SKILL.md refs.
    pattern = re.compile(r'\.\./([a-z0-9-]+)/SKILL\.md')
    for m in pattern.finditer(body):
        target = m.group(1)
        if target not in skill_names:
            fail(errors, f'{skill_path}: inter-skill link refers to missing skill {target!r}')
def validate_readme(root, skill_names, errors):
    readme = root / 'README.md'
    if not readme.exists():
        return
    text = readme.read_text()
    # Collect backtick-wrapped kebab-case tokens that look like skill-name references.
    candidates = set(re.findall(r'`([a-z][a-z0-9-]+)`', text))
    # Only treat hyphenated tokens as skill names to avoid false positives on plain words/commands.
    for token in sorted(candidates):
        if '-' not in token:
            continue
        if not NAME_RE.match(token):
            continue
        # Skip tokens that are obviously not skills (e.g. file extensions, flags, env vars).
        if token.startswith('-'):
            continue
        # Only enforce tokens that appear in contexts suggesting they are skill references:
        # either alongside another known skill name, or in a table/list row that references skills.
        if token in skill_names:
            continue
        # If the token looks like a skill name (kebab-case, no file extension, not a known
        # non-skill term) AND is surrounded by skill-chooser context, flag it.
        # Heuristic: surrounding 80 chars contain the word "skill" or another known skill name.
        for m in re.finditer(r'`' + re.escape(token) + r'`', text):
            window = text[max(0, m.start() - 120): m.end() + 120].lower()
            if 'skill' in window or any(n in window for n in skill_names):
                fail(errors, f'{readme}: references unknown skill `{token}`')
                break
def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = []
    skill_dirs = [p for p in sorted(root.iterdir()) if p.is_dir() and (p / 'SKILL.md').exists()]
    if not skill_dirs:
        fail(errors, f'No skill directories found under {root}')
    skill_names = {d.name for d in skill_dirs}
    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        skill_path = skill_dir / 'SKILL.md'
        try:
            fm, body = load_skill(skill_path)
        except Exception as exc:
            fail(errors, f'{skill_path}: {exc}')
            continue
        if fm.get('name') != skill_name:
            fail(errors, f'{skill_path}: name must match directory name {skill_name!r}')
        if not isinstance(fm.get('name'), str) or not NAME_RE.match(fm['name']):
            fail(errors, f'{skill_path}: invalid kebab-case name')
        desc = fm.get('description')
        if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024:
            fail(errors, f'{skill_path}: description must be a non-empty string <= 1024 chars')
        if 'license' in fm and not isinstance(fm['license'], str):
            fail(errors, f'{skill_path}: license must be a string')
        if 'compatibility' in fm and (not isinstance(fm['compatibility'], str) or len(fm['compatibility']) > 500):
            fail(errors, f'{skill_path}: compatibility must be a string <= 500 chars')
        if 'metadata' in fm:
            meta = fm['metadata']
            if not isinstance(meta, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in meta.items()):
                fail(errors, f'{skill_path}: metadata must be a string-to-string map')
        if 'allowed-tools' in fm and not isinstance(fm['allowed-tools'], str):
            fail(errors, f'{skill_path}: allowed-tools must be a string')
        validate_canonical_headings(skill_path, body, errors)
        validate_inter_skill_links(skill_path, body, skill_names, errors)
        # Also validate inter-skill links inside authored support markdown under the skill.
        for support_md in sorted(skill_dir.rglob('*.md')):
            if support_md == skill_path:
                continue
            try:
                support_body = support_md.read_text()
            except Exception:
                continue
            validate_inter_skill_links(support_md, support_body, skill_names, errors)
        trigger_file = skill_dir / 'evals' / 'trigger-queries.json'
        evals_file = skill_dir / 'evals' / 'evals.json'
        if trigger_file.exists():
            validate_trigger_queries(trigger_file, errors)
        if evals_file.exists():
            validate_evals(evals_file, skill_name, errors)
        for rel in re.findall(r'`((?:references|scripts|assets)/[^`]+)`', body):
            rel_path = rel.split()[0]
            if '*' in rel_path:
                continue
            if not (skill_dir / rel_path).exists():
                fail(errors, f'{skill_path}: referenced support file missing: {rel_path}')
    validate_readme(root, skill_names, errors)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(json.dumps({'status': 'ok', 'skills_checked': len(skill_dirs)}))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
