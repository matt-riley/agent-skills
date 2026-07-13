#!/usr/bin/env python3
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import Path
import yaml


class UniqueKeySafeLoader(yaml.SafeLoader):
    pass


def construct_unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                'while constructing a mapping', node.start_mark,
                f'found duplicate key {key!r}', key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)
NAME_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
# Fuller canonical set per catalog-standard.md and the taught authoring shape
# (python validator is the primary `npm run validate` gate; the mjs in skill-authoring/
# provides additional local-authoring checks such as concrete content, orphans, order).
CANONICAL_HEADINGS = (
    '## Use this skill when',
    '## Do not use this skill when',
    '## Inputs to gather',
    '## First move',
    '## Workflow',
    '## Guardrails',
    '## Validation',
    '## Examples',
    '## Reference files',
)
ALLOWED_TOP_LEVEL_KEYS = {'name', 'description', 'license', 'compatibility', 'metadata'}
def fail(errors, message):
    errors.append(message)
def load_skill(path):
    text = path.read_text()
    m = re.match(r'^---\n(.*?)\n---\n?', text, re.S)
    if not m:
        raise ValueError('missing YAML frontmatter')
    return yaml.load(m.group(1), Loader=UniqueKeySafeLoader) or {}, text[m.end():]


def validate_frontmatter_schema(skill_path, fm, errors):
    for key in fm:
        if key not in ALLOWED_TOP_LEVEL_KEYS:
            fail(errors, f'{skill_path}: unsupported top-level frontmatter key: {key}')
    if fm.get('license') != 'GNU GPL v3':
        fail(errors, f'{skill_path}: license must be GNU GPL v3 for every catalog skill')
    if 'compatibility' in fm and (not isinstance(fm['compatibility'], str) or len(fm['compatibility']) > 500):
        fail(errors, f'{skill_path}: compatibility must be a string <= 500 chars')
    if 'metadata' in fm:
        meta = fm['metadata']
        if not isinstance(meta, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in meta.items()):
            fail(errors, f'{skill_path}: metadata must be a string-to-string map')
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
    previous_index = -1
    for heading in CANONICAL_HEADINGS:
        match = re.search(r'^' + re.escape(heading) + r'\s*$', stripped, re.M)
        if not match:
            continue
        if match.start() < previous_index:
            fail(errors, f'{skill_path}: canonical heading out of order {heading!r}')
        previous_index = match.start()

def validate_inter_skill_links(skill_path, body, skill_names, errors):
    # Match either markdown links like [text](../name/SKILL.md) or inline ../name/SKILL.md refs.
    pattern = re.compile(r'\.\./([a-z0-9-]+)/SKILL\.md')
    for m in pattern.finditer(body):
        target = m.group(1)
        if target not in skill_names:
            fail(errors, f'{skill_path}: inter-skill link refers to missing skill {target!r}')
def validate_openai_metadata(skill_dir, fm, errors):
    path = skill_dir / 'agents' / 'openai.yaml'
    if not path.exists():
        return
    try:
        data = yaml.safe_load(path.read_text()) or {}
    except Exception as exc:
        fail(errors, f'{path}: invalid YAML: {exc}')
        return
    short = (data.get('interface') or {}).get('short_description')
    if short != fm.get('description'):
        fail(errors, f'{path}: interface.short_description must match SKILL.md description')
    allow = (data.get('policy') or {}).get('allow_implicit_invocation')
    if allow is not True:
        fail(errors, f'{path}: policy.allow_implicit_invocation must be true for active catalog skills')


def validate_release_metadata(skill_path, skill_name, fm, manifest, release_packages, errors):
    key = f'skills/{skill_name}'
    if key not in release_packages and key not in manifest:
        return
    if 'license' not in fm:
        fail(errors, f'{skill_path}: release-managed skills must include license')
    meta = fm.get('metadata')
    if not isinstance(meta, dict):
        fail(errors, f'{skill_path}: release-managed skills must include metadata')
        return
    version = meta.get('version')
    if not version:
        fail(errors, f'{skill_path}: release-managed skills must include metadata.version')
    if key in manifest and version != manifest[key]:
        fail(errors, f'{skill_path}: metadata.version {version!r} must match .release-please-manifest.json {manifest[key]!r}')
    if not meta.get('maturity'):
        fail(errors, f'{skill_path}: release-managed skills must include metadata.maturity')


def validate_support_links(skill_dir, skill_path, body, errors):
    linked = set(re.findall(r'`((?:references|scripts|assets)/[^`]+)`', body))
    linked.update(re.findall(r'\]\(((?:references|scripts|assets)/[^)]+)\)', body))
    linked_text = '\n'.join(linked) + '\n' + body
    for support_file in sorted(skill_dir.rglob('*')):
        if not support_file.is_file():
            continue
        rel = support_file.relative_to(skill_dir).as_posix()
        if rel in ('SKILL.md', 'README.md') or rel.startswith(('agents/', 'evals/')):
            continue
        if rel.startswith('scripts/tests/'):
            continue
        parent_links = []
        for parent in support_file.relative_to(skill_dir).parents:
            parent_rel = parent.as_posix()
            if parent_rel in ('.', 'references', 'assets', 'scripts'):
                continue
            parent_links.append(parent_rel + '/')
        if rel not in linked_text and not any(parent in linked_text for parent in parent_links):
            fail(errors, f'{skill_path}: support file is not linked from SKILL.md: {rel}')

    targets = set(re.findall(r'`((?:references|scripts|assets)/[^`]+)`', body))
    targets.update(re.findall(r'\]\(((?:references|scripts|assets)/[^)#?]+)', body))
    for rel in sorted(targets):
        if '*' not in rel and not (skill_dir / rel).exists():
            fail(errors, f'{skill_path}: referenced support file missing: {rel}')


def validate_stable_trigger_evals(skill_path, skill_dir, fm, errors):
    maturity = (fm.get('metadata') or {}).get('maturity')
    if maturity == 'stable' and not (skill_dir / 'evals' / 'trigger-queries.json').exists():
        fail(errors, f'{skill_path}: stable skills must include trigger evals')


def validate_scripts(skill_dir, errors):
    for script in sorted((skill_dir / 'scripts').glob('*.sh')) if (skill_dir / 'scripts').exists() else []:
        proc = subprocess.run(['bash', '-n', str(script)], text=True, capture_output=True)
        if proc.returncode != 0:
            detail = proc.stderr.strip() or f'exit {proc.returncode}'
            fail(errors, f'{script}: bash syntax check failed: {detail}')


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


def validate_catalog_invariants(catalog_root, skills_root, skill_names, errors):
    chooser_path = skills_root / 'README.md'
    chooser_text = chooser_path.read_text() if chooser_path.exists() else ''
    for skill_name in sorted(skill_names):
        skill_dir = skills_root / skill_name
        if not (skill_dir / 'agents' / 'openai.yaml').is_file():
            fail(errors, f'{skill_dir}: missing agents/openai.yaml for active skill')
        if not re.search(r'`' + re.escape(skill_name) + r'`', chooser_text):
            fail(errors, f'{chooser_path}: chooser is missing active skill {skill_name!r}')

    config_path = catalog_root / 'release-please-config.json'
    manifest_path = catalog_root / '.release-please-manifest.json'
    if not config_path.exists() or not manifest_path.exists():
        return
    config = json.loads(config_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    config_keys = set((config.get('packages') or {}).keys())
    manifest_keys = set(manifest.keys())
    if '.' not in config_keys or '.' not in manifest_keys:
        fail(errors, f"{catalog_root}: root release package '.' is required in both release files")
    if config_keys != manifest_keys:
        config_only = sorted(config_keys - manifest_keys)
        manifest_only = sorted(manifest_keys - config_keys)
        fail(
            errors,
            f'{catalog_root}: release package keysets differ '
            f'(config only: {config_only}; manifest only: {manifest_only})',
        )
    for package_path in sorted(config_keys | manifest_keys):
        if package_path == '.':
            continue
        if not (catalog_root / package_path).is_dir():
            fail(errors, f'{catalog_root}: release package path does not exist: {package_path!r}')


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = []
    skill_dirs = [p for p in sorted(root.iterdir()) if p.is_dir() and (p / 'SKILL.md').exists()]
    if not skill_dirs:
        fail(errors, f'No skill directories found under {root}')
    skill_names = {d.name for d in skill_dirs}
    catalog_root = root.parent if root.name == 'skills' else root
    manifest_path = catalog_root / '.release-please-manifest.json'
    config_path = catalog_root / 'release-please-config.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    release_packages = set()
    if config_path.exists():
        release_packages = set((json.loads(config_path.read_text()).get('packages') or {}).keys())
    validate_catalog_invariants(catalog_root, root, skill_names, errors)
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
        validate_frontmatter_schema(skill_path, fm, errors)
        validate_canonical_headings(skill_path, body, errors)
        validate_inter_skill_links(skill_path, body, skill_names, errors)
        validate_openai_metadata(skill_dir, fm, errors)
        validate_release_metadata(skill_path, skill_name, fm, manifest, release_packages, errors)
        validate_support_links(skill_dir, skill_path, body, errors)
        validate_stable_trigger_evals(skill_path, skill_dir, fm, errors)
        validate_scripts(skill_dir, errors)
        # Also validate inter-skill links inside authored support markdown under the skill.
        for support_md in sorted(skill_dir.rglob('*.md')):
            if support_md == skill_path:
                continue
            if support_md.relative_to(skill_dir).as_posix().startswith('scripts/tests/'):
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
        if trigger_file.exists() != evals_file.exists():
            fail(errors, f'{skill_dir}: trigger and functional eval files should be added together')
    validate_readme(root, skill_names, errors)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(json.dumps({'status': 'ok', 'skills_checked': len(skill_dirs)}))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
