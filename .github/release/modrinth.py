#!/usr/bin/env python3
"""Publishes the jars of a release on Modrinth, in the project of the repository: the core in
vania-metrics, collector-<name> in vania-metrics-<name>. Called by the jars job of
.github/workflows/release.yml, once the jars are attached to the GitHub release.

Everything but the jars comes from compatibility.yml, the manifest CI checks on real servers:
the Minecraft version, the platforms (Modrinth's loaders: only those that passed), and for a
collector the plugin it targets. The core gets one version per platform jar, a collector one
version, which requires the core and its plugin when that plugin is on Modrinth.

A version number already on Modrinth is left as it is: running this again publishes nothing twice.

  modrinth.py --repo collector-luckperms --tag v0.6.1 --dist dist \\
              --manifest compatibility.yml --notes notes.md [--dry-run]

The token, in MODRINTH_TOKEN, must read projects and create versions. It reaches curl through
its config on stdin, never on the command line."""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

import yaml

API = 'https://api.modrinth.com/v2'
USER_AGENT = 'Vania-Metrics/release (github.com/Vania-Metrics)'
CORE = 'vania-metrics'
# The core's platform jars, as compatibility.yml names them, and how their versions are called.
# The API jar is for plugin authors, not for servers: it stays on GitHub.
CORE_JARS = {
    'vania-metrics-bukkit': 'Bukkit',
    'vania-metrics-sponge': 'Sponge',
    'vania-metrics-velocity': 'Velocity',
    'vania-metrics-bungee': 'BungeeCord',
    'vania-metrics-geyser': 'Geyser',
}
MODRINTH_PAGE = re.compile(r'^https://modrinth\.com/(?:plugin|mod)/([^/?#]+)')


def call(method, path, form=()):
    config = (f'header = "Authorization: {os.environ["MODRINTH_TOKEN"]}"\n'
              f'header = "User-Agent: {USER_AGENT}"\n')
    cmd = ['curl', '-sS', '-K', '-', '-X', method, '-w', '\n%{http_code}', API + path]
    for part in form:
        cmd += ['-F', part]
    out = subprocess.run(cmd, input=config, capture_output=True, text=True, check=True).stdout
    body, _, code = out.rpartition('\n')
    return int(code), body


def get(path):
    code, body = call('GET', path)
    if code != 200:
        sys.exit(f'GET {path}: HTTP {code} {body[:300]}')
    return json.loads(body)


def passed(cell):
    # compatibility.yml says yes; YAML 1.1, hence PyYAML, reads it as true.
    return cell is True or cell == 'yes'


def versions(repo, version, manifest, dist):
    """What to publish: one entry per Modrinth version."""
    if repo == 'core':
        loaders = {}
        for platform, cell in manifest['platforms'].items():
            if cell.get('status') == 'tested':
                loaders.setdefault(cell['jar'], []).append(platform)
        for jar, platforms in loaders.items():
            if jar not in CORE_JARS:
                sys.exit(f'compatibility.yml names a jar this script does not know: {jar}')
            yield {
                'file': dist / f'{jar}-{version}.jar',
                'number': f'{version}+{jar.removeprefix("vania-metrics-")}',
                'name': f'{version} for {CORE_JARS[jar]}',
                'loaders': platforms,
                'dependencies': [],
            }
        return
    dependencies = [{'project_id': get(f'/project/{CORE}')['id'], 'dependency_type': 'required'}]
    page = MODRINTH_PAGE.match(str((manifest.get('plugin') or {}).get('source', '')))
    if page:
        dependencies.append({'project_id': get(f'/project/{page[1]}')['id'],
                             'dependency_type': 'required'})
    yield {
        'file': dist / f'vania-metrics-{repo}-{version}.jar',
        'number': version,
        'name': version,
        'loaders': [p for p, cell in manifest['platforms'].items() if passed(cell.get('collector'))],
        'dependencies': dependencies,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', required=True, help='core, or collector-<name>')
    parser.add_argument('--tag', required=True, help='vX.Y.Z')
    parser.add_argument('--dist', required=True, type=pathlib.Path, help='the jars of the release')
    parser.add_argument('--manifest', required=True, type=pathlib.Path, help='compatibility.yml')
    parser.add_argument('--notes', type=pathlib.Path, help='the changelog, in Markdown')
    parser.add_argument('--dry-run', action='store_true', help='print what would be published')
    args = parser.parse_args()

    version = args.tag.removeprefix('v')
    manifest = yaml.safe_load(args.manifest.read_text())
    slug = CORE if args.repo == 'core' else f'{CORE}-{args.repo.removeprefix("collector-")}'
    project = get(f'/project/{slug}')
    published = {v['version_number'] for v in get(f'/project/{project["id"]}/version')}
    notes = args.notes.read_text() if args.notes else ''

    for v in versions(args.repo, version, manifest, args.dist):
        if v['number'] in published:
            print(f'{slug} {v["number"]}: already on Modrinth')
            continue
        if not v['file'].is_file():
            sys.exit(f'{slug} {v["number"]}: missing jar {v["file"]}')
        if not v['loaders']:
            sys.exit(f'{slug} {v["number"]}: no platform passed, nothing to publish it for')
        data = {
            'project_id': project['id'],
            'name': v['name'],
            'version_number': v['number'],
            'changelog': notes,
            'dependencies': v['dependencies'],
            'game_versions': [str(manifest['minecraft'])],
            'loaders': v['loaders'],
            'version_type': 'release',
            'featured': True,
            'status': 'listed',
            'file_parts': ['jar'],
            'primary_file': 'jar',
        }
        if args.dry_run:
            print(f'{slug} {v["number"]}: would publish {v["file"].name}',
                  json.dumps({k: data[k] for k in ('name', 'loaders', 'game_versions', 'dependencies')}))
            continue
        data_file = args.dist.parent / f'modrinth-{v["number"]}.json'
        data_file.write_text(json.dumps(data))
        code, body = call('POST', '/version', [f'data=<{data_file};type=application/json',
                                               f'jar=@{v["file"]};type=application/java-archive'])
        data_file.unlink()
        if code != 200:
            sys.exit(f'{slug} {v["number"]}: HTTP {code} {body[:400]}')
        print(f'{slug} {v["number"]}: published, https://modrinth.com/plugin/{slug}/version/{json.loads(body)["id"]}')


if __name__ == '__main__':
    main()
