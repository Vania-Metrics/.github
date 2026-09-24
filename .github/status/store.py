#!/usr/bin/env python3
"""Stores one CI run of a repository in the data branch the documentation site is built from.

    store.py DATA_DIR --record run.json --manifest compatibility.yml [--catalog catalog.json]

Writes, under DATA_DIR/<repo>/:
  <workflow>.json   the run, as collect.py read it
  manifest.json     compatibility.yml, every value a string: "yes", "no" and "on" stay words
  catalog.json      what the sources declare, as extract.py read it

A run older than the one already recorded changes nothing: a slow run finishing after a newer one
must not put the site back in time.
"""
import argparse
import json
import pathlib

import yaml


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('dir', type=pathlib.Path)
    ap.add_argument('--record', required=True)
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--catalog')
    a = ap.parse_args()

    rec = json.loads(pathlib.Path(a.record).read_text(encoding='utf-8'))
    d = a.dir / rec['repo']
    d.mkdir(parents=True, exist_ok=True)
    target = d / f'{rec["workflow"]}.json'
    if target.exists() and json.loads(target.read_text(encoding='utf-8'))['finished'] > rec['finished']:
        print(f'{target}: a newer run is already recorded, keeping it')
        return
    write(target, rec)
    with open(a.manifest, encoding='utf-8') as f:
        write(d / 'manifest.json', yaml.load(f, Loader=yaml.BaseLoader) or {})
    if a.catalog:
        write(d / 'catalog.json', json.loads(pathlib.Path(a.catalog).read_text(encoding='utf-8')))


if __name__ == '__main__':
    main()
