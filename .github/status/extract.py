#!/usr/bin/env python3
"""Reads what a Vania-Metrics repository publishes from its sources, for the documentation site.

    extract.py DIR > catalog.json

DIR is a checkout of the core or of a collector. What comes out:
  metrics      every family declared through MetricRegistry: full name, type, help, labels
  config       every key read through Config, with its default and its environment variable
  collector    the class implementing Collector: registered name, target, interval, javadoc
  contract     for the core, the families of each capability profile, from the contract files

Plain Java parsing, no compiler: every declaration names its metric with a string literal (the
registry refuses anything else at runtime anyway), and help texts are literals joined with '+'.
Anything that is not a literal is kept as its source text rather than guessed.
"""
import json
import pathlib
import re
import sys

PREFIX = 'mc_'
DECLARATION = re.compile(r'\.(gauge|counter|histogram)\(')
CONFIG = re.compile(r'\.get(String|Int|Long|Double|Boolean|Seconds)\(')


def returned(src, method):
    """The literal a no-argument method returns: String name() { return "grim"; } is grim."""
    m = re.search(r'\b' + method + r'\(\)\s*\{\s*return\s+([^;]+);\s*\}', src)
    return m.group(1).strip() if m else None


COLLECTOR_CLASS = re.compile(r'class\s+(\w+)\s+implements\s+(?:[\w.]+\s*,\s*)*Collector\b')


def call_args(src, start):
    """The top-level arguments of the call whose '(' is at start, as source slices."""
    args, depth, i, begin = [], 0, start, start + 1
    while i < len(src):
        c = src[i]
        if c in '"\'':
            i = skip_literal(src, i)
            continue
        if src.startswith('//', i):
            i = src.index('\n', i)
            continue
        if src.startswith('/*', i):
            i = src.index('*/', i) + 2
            continue
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
            if depth == 0:
                args.append(src[begin:i].strip())
                return args
        elif c == ',' and depth == 1:
            args.append(src[begin:i].strip())
            begin = i + 1
        i += 1
    return args


def skip_literal(src, i):
    if src.startswith('"""', i):
        return src.index('"""', i + 3) + 3
    quote, i = src[i], i + 1
    while src[i] != quote:
        i += 2 if src[i] == '\\' else 1
    return i + 1


def literal(expr):
    """The value of "a" + "b", or None if the expression is not made of string literals only."""
    parts = re.split(r'\s*\+\s*(?=")', expr.strip())
    out = []
    for part in parts:
        m = re.fullmatch(r'"((?:[^"\\]|\\.)*)"', part.strip())
        if not m:
            return None
        out.append(unescape(m.group(1)))
    return ''.join(out)


JAVA_ESCAPES = {'n': '\n', 't': '\t', 'r': '\r', 'b': '\b', 'f': '\f', '"': '"', "'": "'", '\\': '\\'}


def unescape(body):
    return re.sub(r'\\(u+[0-9a-fA-F]{4}|.)',
                  lambda e: chr(int(e.group(1).lstrip('u'), 16)) if e.group(1).startswith('u')
                  else JAVA_ESCAPES.get(e.group(1), e.group(1)), body)


def javadoc_text(doc):
    """A javadoc comment as Markdown: paragraphs kept, {@code x} and {@link x} as code."""
    lines = [re.sub(r'^\s*\*\s?', '', line) for line in doc.strip('/*').split('\n')]
    text = '\n'.join(lines).strip()
    text = re.sub(r'\{@(?:code|link|linkplain)\s+([^}]*)\}', r'`\1`', text)
    text = re.sub(r'</?(?:b|strong)>', '**', text)
    text = re.sub(r'</?(?:i|em)>', '*', text)
    text = re.sub(r'<li>\s*', '\n- ', text)
    text = re.sub(r'</?(?:ol|ul|li)>', '', text)
    text = re.sub(r'<p>\s*', '\n\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    paragraphs = [' '.join(p.split()) if not p.lstrip().startswith('- ') else p.strip()
                  for p in text.split('\n\n')]
    return '\n\n'.join(p for p in paragraphs if p)


def extract(root):
    metrics, config, description = {}, {}, None
    for path in sorted(root.glob('**/src/main/java/**/*.java')):
        rel = str(path.relative_to(root))
        # A collector's build keeps a clone of the core under .gradle/: not its sources. The
        # testkit runs the tests, it is not part of the plugin.
        parts = pathlib.Path(rel).parts
        if parts[0] == 'testkit' or any(part.startswith('.') or part == 'build' for part in parts):
            continue
        src = path.read_text(encoding='utf-8')
        for m in DECLARATION.finditer(src):
            args = call_args(src, m.end() - 1)
            name = literal(args[0]) if args else None
            if not name:
                continue
            kind = m.group(1)
            labels = args[3:] if kind == 'histogram' else args[2:]
            metrics[PREFIX + name] = {
                'name': PREFIX + name,
                'type': kind,
                'help': literal(args[1]) if len(args) > 1 else None,
                'labels': [literal(a) or a for a in labels],
                'source': rel,
            }
        for m in CONFIG.finditer(src):
            args = call_args(src, m.end() - 1)
            key = literal(args[0]) if args else None
            if not key or '.' not in key:
                continue
            default = args[1] if len(args) > 1 else None
            config.setdefault(key, {
                'key': key,
                'type': m.group(1).lower(),
                'default': literal(default) if default and default.startswith('"') else default,
                'env': 'VANIA_METRICS_' + key.upper().replace('.', '_'),
                'source': rel,
            })
        c = COLLECTOR_CLASS.search(src)
        if c and description is None and 'vaniametrics/module/' in rel:
            docs = list(re.finditer(r'/\*\*(.*?)\*/', src[:c.start()], re.S))
            interval = returned(src, 'intervalSeconds')
            description = {
                'class': c.group(1),
                # The name the collector registers under: collector.<name> keys, the collector label.
                'name': literal(returned(src, 'name') or '') or None,
                'source': literal(returned(src, 'source') or '') or None,
                'background': returned(src, 'isBackground') == 'true',
                'interval': int(interval) if interval and interval.isdigit() else None,
                'text': javadoc_text(docs[-1].group(0)) if docs else '',
            }

    catalog = {
        'metrics': sorted(metrics.values(), key=lambda x: x['name']),
        'config': sorted(config.values(), key=lambda x: x['key']),
    }
    if description:
        catalog['collector'] = description
    contract = root / 'common' / 'src' / 'test' / 'resources' / 'contract'
    if contract.is_dir():
        catalog['contract'] = {}
        for f in sorted(contract.glob('*.txt')):
            families = {}
            for line in f.read_text(encoding='utf-8').splitlines():
                if line.strip() and not line.startswith('#'):
                    name, kind, *labels = line.split()
                    families[name] = {'type': kind, 'labels': labels[0].split(',') if labels else []}
            catalog['contract'][f.stem] = families
    # What each real platform publishes once idle (+) and must not publish (-), as the testkit
    # checks it: finer than the profiles, e.g. Geyser has no backend, so no mc_proxy_backend_*.
    expected = root / 'testkit' / 'src' / 'integrationTest' / 'resources' / 'expected'
    if expected.is_dir():
        catalog['expected'] = {}
        for f in sorted(expected.glob('*.txt')):
            lines = [l.strip() for l in f.read_text(encoding='utf-8').splitlines()]
            catalog['expected'][f.stem] = {
                'present': sorted(l[1:] for l in lines if l.startswith('+')),
                'absent': sorted(l[1:] for l in lines if l.startswith('-')),
            }
    return catalog


if __name__ == '__main__':
    json.dump(extract(pathlib.Path(sys.argv[1])), sys.stdout, indent=2, ensure_ascii=False)
    print()
