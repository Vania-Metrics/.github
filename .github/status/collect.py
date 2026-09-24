#!/usr/bin/env python3
"""Reads one CI run of a Vania-Metrics repository and prints it as a status record, in JSON.

    collect.py --repo collector-chunky --run-id 123 [--attempt 1] [--workflow ci]
               [--result success] [--collector-test collector-test.yml] > run.json

The outcome of every test cell comes from the job logs, the Gradle lines
"SmokeIT > platforms() > paper PASSED": the testkit's Markdown report only reaches the job
summary, which the API cannot read. The token needs actions:read on the repository: GH_TOKEN or
GITHUB_TOKEN, else the one `gh auth token` prints.

Without --result, the run's own conclusion is used. That is right for a finished run, but the run
calling this from its status job is still going and has none yet, hence the flag.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ORG = 'Vania-Metrics'
API = 'https://api.github.com/'
# "2026-09-23T19:21:03.1234567Z CorePlatformIT > platforms() > velocity-3.5.1 PASSED". Only
# classes named *IT: a unit test's dynamic test would print the same shape.
CELL = re.compile(r'\b\w+IT > \w+\(\) > ([a-z][a-z0-9.-]*) (PASSED|FAILED|SKIPPED)$')


class _Stay(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_Stay)
_TOKEN = None


def get(path, text=False):
    global _TOKEN
    if _TOKEN is None:
        _TOKEN = (os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
                  or subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip())
    headers = {'Authorization': f'Bearer {_TOKEN}', 'Accept': 'application/vnd.github+json',
               'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'vania-metrics-status'}
    for attempt in range(4):
        try:
            try:
                with _OPENER.open(urllib.request.Request(API + path, headers=headers), timeout=60) as r:
                    body = r.read()
            except urllib.error.HTTPError as e:
                if e.code not in (301, 302, 303, 307, 308):
                    raise
                # A log is served from a signed storage URL, which rejects our Authorization header.
                req = urllib.request.Request(e.headers['Location'], headers={'User-Agent': headers['User-Agent']})
                with urllib.request.urlopen(req, timeout=120) as r:
                    body = r.read()
            return body.decode('utf-8', 'replace') if text else json.loads(body)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            error = e
            # A job's log may take a few seconds to be available once the job is over.
            time.sleep(5 * (attempt + 1))
    sys.exit(f'GET {path}: {error}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--run-id', required=True, type=int)
    ap.add_argument('--attempt', type=int)
    ap.add_argument('--workflow')
    ap.add_argument('--result')
    ap.add_argument('--collector-test')
    a = ap.parse_args()

    base = f'repos/{ORG}/{a.repo}/actions'
    run = get(f'{base}/runs/{a.run_id}')
    attempt = a.attempt or run['run_attempt']
    jobs = get(f'{base}/runs/{a.run_id}/attempts/{attempt}/jobs?per_page=100')['jobs']

    cells, finished = {}, []
    for job in jobs:
        # The status job itself, still running, and anything that did not run.
        if job['name'].startswith('status') or job['status'] != 'completed':
            continue
        finished.append(job['completed_at'])
        for line in get(f'{base}/jobs/{job["id"]}/logs', text=True).splitlines():
            m = CELL.search(line.rstrip())
            if m:
                cells[m.group(1)] = m.group(2).lower()

    record = {
        'repo': a.repo,
        'workflow': a.workflow or run['name'],
        'run_id': a.run_id,
        'run_attempt': attempt,
        'url': f'https://github.com/{ORG}/{a.repo}/actions/runs/{a.run_id}',
        'event': run['event'],
        'branch': run['head_branch'],
        'sha': run['head_sha'],
        'result': a.result or run['conclusion'] or 'unknown',
        'finished': max(finished) if finished else run['updated_at'],
        'cells': dict(sorted(cells.items())),
    }
    if a.collector_test:
        import yaml  # only collectors have one
        with open(a.collector_test, encoding='utf-8') as f:
            runtime = (yaml.load(f, Loader=yaml.BaseLoader) or {}).get('runtime')
        if runtime:
            record['runtime'] = runtime
    json.dump(record, sys.stdout, indent=2)
    print()


if __name__ == '__main__':
    main()
