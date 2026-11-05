#!/usr/bin/env python3
"""Build and validate the plugin ZIP without connecting to external services."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile

from jsonschema import Draft202012Validator
from PIL import Image
import yaml

ROOT = Path(__file__).resolve().parents[1]
FILES = ('plugin.json', 'mcp.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json',
         '.cursor-plugin/plugin.json', '.mcp.json', 'LICENSE', 'README.md')
DIRECTORIES = ('skills', 'assets')
CATEGORIES = {'Business & Operations', 'Communication', 'Creativity', 'Data & Analytics',
              'Developer Tools', 'Education & Research', 'Entertainment', 'Finance',
              'Healthcare', 'Other', 'Productivity', 'Scientific Research', 'Security', 'Travel'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_file(files, name):
    require(name in files, f'Missing {name}')
    value = json.loads(files[name].decode('utf-8'))
    require(isinstance(value, dict), f'{name} must be an object')
    return value


def packaged_path(value):
    require(isinstance(value, str) and value.startswith('./'), f'Invalid package path: {value}')
    name = value[2:]
    require(name and '\\' not in name and all(p not in ('', '.', '..') for p in name.split('/')),
            f'Unsafe package path: {value}')
    return name


def https_url(value):
    require(isinstance(value, str) and len(value) <= 1024, 'Invalid URL')
    parsed = urlsplit(value)
    require(parsed.scheme == 'https' and parsed.hostname and not parsed.username
            and not parsed.password and not any(c.isspace() for c in value), f'Invalid HTTPS URL: {value}')


def validate_files(files, tag=None):
    for name in FILES:
        require(name in files, f'Missing {name}')
    manifest = json_file(files, 'plugin.json')
    mcp = json_file(files, 'mcp.json')
    for name, value in [('plugin', manifest), ('mcp', mcp)]:
        schema = json.loads((ROOT / 'scripts/schemas' / f'{name}.schema.json').read_text())
        Draft202012Validator(schema).validate(value)
    version = manifest.get('version', '')
    require(re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', version), 'Version must be release SemVer')
    require(manifest['name'] == 'bitrefill', 'Plugin identity must remain bitrefill')
    if tag:
        require(tag == f'v{version}', f'Tag {tag} does not match manifest v{version}')
    extension = manifest['extensions']['com.openai']
    interface = extension['interface']
    for field, limit in [('displayName', 30), ('shortDescription', 30), ('longDescription', 4000), ('developerName', 80)]:
        value = interface[field]
        require(isinstance(value, str) and value.strip() and len(value) <= limit, f'Invalid {field}')
        require(field == 'longDescription' or '\n' not in value, f'{field} must be single-line')
    require(interface['category'] in CATEGORIES, 'Unsupported OpenAI category')
    capabilities = interface['capabilities']
    require(isinstance(capabilities, list) and len(capabilities) <= 20
            and all(isinstance(v, str) and v.strip() and len(v) <= 120 for v in capabilities), 'Invalid capabilities')
    for field in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        https_url(interface[field])
    prompts = interface.get('defaultPrompt', [])
    prompts = [prompts] if isinstance(prompts, str) else prompts
    require(isinstance(prompts, list) and len(prompts) <= 3, 'Invalid starter prompts')
    normalized = []
    for prompt in prompts:
        require(isinstance(prompt, str) and prompt.strip() and len(prompt) <= 128
                and '\n' not in prompt and '@' not in prompt, 'Invalid starter prompt')
        normalized.append(' '.join(unicodedata.normalize('NFKC', prompt).split()).casefold())
    require(len(set(normalized)) == len(normalized), 'Duplicate starter prompts')
    for field, minimum in [('logo', 256), ('composerIcon', 48)]:
        name = packaged_path(interface[field])
        require(name in files, f'Missing asset: {name}')
        require(len(files[name]) <= 5 * 1024 * 1024, f'Asset too large: {name}')
        with Image.open(io.BytesIO(files[name])) as image:
            require(image.format == 'PNG' and image.width == image.height
                    and minimum <= image.width <= 4096, f'Invalid PNG dimensions: {name}')
            image.verify()
    for name in ('plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json', '.cursor-plugin/plugin.json'):
        value = json_file(files, name)
        overlay = value.get('extensions', {}).get('com.openai', {})
        require(value.get('apps') is None and overlay.get('apps') is None, f'App binding prohibited: {name}')
        require('hooks' not in value and 'hooks' not in overlay, f'Public upload cannot include hooks: {name}')
        require(value['name'] == manifest['name'], f'Identity mismatch: {name}')
        require(value.get('version', version) == version, f'Version mismatch: {name}')
    codex = json_file(files, '.codex-plugin/plugin.json')
    require(codex['interface'] == interface, 'Codex presentation differs from portable manifest')
    require(codex['extensions']['com.openai'] == {k: v for k, v in extension.items() if k != 'interface'},
            'Codex review/publication metadata differs')
    require(codex['skills'] == './skills/' and codex['mcpServers'] == './.mcp.json', 'Invalid Codex components')
    legacy_mcp = json_file(files, '.mcp.json')['mcpServers']
    require(set(mcp['mcpServers']) == set(legacy_mcp) == {'bitrefill'}, 'MCP server mismatch')
    for name, server in mcp['mcpServers'].items():
        require(server['type'] == 'streamable-http', 'Portable MCP requires streamable-http')
        https_url(server['url'])
        require(server['url'] == legacy_mcp[name]['url'] == 'https://api.bitrefill.com/mcp', 'MCP endpoint mismatch')
    skills = [name for name in files if re.fullmatch(r'skills/[^/.][^/]*/SKILL\.md', name)]
    require(skills, 'No usable skills')
    names = set()
    for name in skills:
        require(len(files[name]) <= 1024 * 1024, f'Skill too large: {name}')
        text = files[name].decode('utf-8')
        require(text.startswith('---\n'), f'Missing frontmatter: {name}')
        frontmatter = yaml.safe_load(text.split('---', 2)[1])
        require(isinstance(frontmatter, dict), f'Invalid frontmatter: {name}')
        skill_name = frontmatter.get('name')
        require(skill_name == PurePosixPath(name).parent.name and skill_name not in names, f'Invalid skill name: {name}')
        names.add(skill_name)
        description = frontmatter.get('description')
        require(isinstance(description, str) and 0 < len(description.strip()) <= 1024, f'Invalid skill description: {name}')
        require(frontmatter['metadata']['version'] == version, f'Skill version mismatch: {name}')
    for name, data in files.items():
        if name.endswith('agents/openai.yaml'):
            agent = yaml.safe_load(data.decode('utf-8'))
            require(isinstance(agent, dict), f'Invalid agent metadata: {name}')
            require(set(agent.get('policy', {})) <= {'products', 'allow_implicit_invocation'}, 'Unsupported agent policy')
            require(type(agent.get('policy', {}).get('allow_implicit_invocation', True)) is bool, 'Invalid invocation policy')
            for field in ('display_name', 'short_description'):
                require(isinstance(agent['interface'][field], str) and agent['interface'][field].strip(), f'Invalid agent {field}')
        if name.startswith('skills/') and name.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', data.decode('utf-8')):
                if urlsplit(target).scheme or target.startswith('#'):
                    continue
                target_path = PurePosixPath(name).parent / unquote(target.split('#', 1)[0])
                parts = []
                for part in target_path.parts:
                    if part == '..':
                        require(parts, f'Reference escapes archive: {name}')
                        parts.pop()
                    elif part != '.':
                        parts.append(part)
                resolved = '/'.join(parts)
                require(resolved in files or any(f.startswith(resolved + '/') for f in files),
                        f'Broken reference in {name}: {target}')
    review = extension['review']
    require(review['commerce'] is True and review['commerce_description'].strip(), 'Commerce must be disclosed')
    for kind, count in [('positive', 5), ('negative', 3)]:
        cases = review['test_cases'][kind]
        require(len(cases) == count, f'Expected {count} {kind} cases')
        for case in cases:
            required = ('description', 'prompt', 'tools_triggered', 'expected_behavior') if kind == 'positive' else ('description', 'prompt')
            require(all(isinstance(case.get(key), str) and case[key].strip() for key in required), f'Invalid {kind} review case')
    return manifest


def source_files(root):
    files = {}
    for name in FILES:
        path = root / name
        require(path.is_file() and not path.is_symlink(), f'Missing or unsafe file: {name}')
        files[name] = path.read_bytes()
    for directory in DIRECTORIES:
        base = root / directory
        require(base.is_dir() and not base.is_symlink(), f'Missing or unsafe directory: {directory}')
        for path in sorted(base.rglob('*')):
            require(not path.is_symlink(), f'Symlink prohibited: {path}')
            if path.is_file():
                name = path.relative_to(root).as_posix()
                require(not any(p.startswith('.') or p in ('node_modules', '__pycache__') for p in path.relative_to(base).parts),
                        f'Unwanted packaged file: {name}')
                files[name] = path.read_bytes()
    market = json.loads((root / '.claude-plugin/marketplace.json').read_text())
    require(market['metadata']['version'] == json.loads(files['plugin.json'])['version'], 'Marketplace version mismatch')
    return files


def validate_archive(archive, tag=None):
    require(archive.stat().st_size <= 100 * 1024 * 1024, 'Archive exceeds 100 MiB')
    with zipfile.ZipFile(archive) as zipped:
        require(zipped.testzip() is None, 'Corrupt ZIP')
        require(0 < len(zipped.infolist()) <= 5000, 'Invalid ZIP entry count')
        files, normalized = {}, set()
        for entry in zipped.infolist():
            name = entry.filename
            require(name == name.strip() and '\\' not in name and not name.startswith('/'), f'Unsafe ZIP path: {name}')
            require(all(p not in ('', '.', '..') for p in name.split('/')) and len(name.split('/')) <= 20
                    and len(name.encode('utf-8')) <= 1024, f'Unsafe ZIP path: {name}')
            key = unicodedata.normalize('NFC', name).casefold()
            require(key not in normalized, f'Duplicate ZIP path: {name}')
            normalized.add(key)
            require(stat.S_ISREG(entry.external_attr >> 16) and not entry.is_dir(), f'Non-regular ZIP file: {name}')
            require(not entry.flag_bits & 1 and entry.file_size <= 100 * 1024 * 1024, f'Unsupported ZIP entry: {name}')
            require(name in FILES or any(name.startswith(d + '/') for d in DIRECTORIES), f'Unrelated ZIP entry: {name}')
            require(not any(p.startswith('.') for p in name.split('/')) or name in FILES, f'Hidden ZIP entry: {name}')
            files[name] = zipped.read(entry)
        return validate_files(files, tag)


def build(root, output, tag=None):
    require(not any(output.resolve().is_relative_to((root / d).resolve()) for d in DIRECTORIES), 'Output cannot be inside packaged components')
    files = source_files(root)
    manifest = validate_files(files, tag)
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f'{manifest["name"]}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipped:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zipped.writestr(info, data)
    validate_archive(archive, tag)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / 'SHA256SUMS').write_text(f'{digest}  {archive.name}\n')
    return archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--tag', help='Require this release tag to match every version')
    parser.add_argument('--validate', type=Path, metavar='ZIP', help='Validate an existing archive')
    args = parser.parse_args()
    if args.validate:
        manifest = validate_archive(args.validate, args.tag)
        print(f'Validated {args.validate}: {manifest["name"]} v{manifest["version"]}')
    else:
        print(f'Built and validated {build(args.root, args.output, args.tag)}')
    print('Package checks passed. OpenAI policy approval, live MCP checks and portal review are separate.')


if __name__ == '__main__':
    main()
