#!/usr/bin/env python3
"""Verify ZIP contents, source fidelity, links and optional isolated execution."""
import argparse
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from urllib.parse import urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_lab_downloads import CHAPTERS, LABS, build, digest  # noqa: E402


def validate(execute=False):
    outputs = build()
    assert outputs == build(), 'non-deterministic output'
    assert set(outputs) == {p.name for p in (ROOT / 'downloads').iterdir()}
    for name, data in outputs.items():
        assert data == (ROOT / 'downloads' / name).read_bytes(), name
    index = json.loads(outputs['index.json'])
    assert len(index['chapters']) == 12
    assert len(index['all']['notebooks']) == 23
    for entry in index['chapters'] + [index['all']]:
        data = outputs[entry['file']]
        assert digest(data) == entry['sha256']
        assert len(data) == entry['bytes']
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            assert archive.testzip() is None
            names = archive.namelist()
            assert len(names) == len(set(names))
            folder = names[0].split('/')[0] + '/'
            for name in names:
                path = PurePosixPath(name)
                assert not path.is_absolute() and '..' not in path.parts
                assert name.startswith(folder)
                assert (archive.getinfo(name).external_attr >> 16) & 0o170000 == 0o100000
            manifest = json.loads(archive.read(folder + 'MANIFEST.json'))
            assert manifest['version'] == entry['version']
            assert manifest['notebooks'] == entry['notebooks']
            assert set(names) == {folder + name for name in manifest['sha256']} | {folder + 'MANIFEST.json'}
            for name, expected in manifest['sha256'].items():
                assert digest(archive.read(folder + name)) == expected
            for name in entry['notebooks']:
                notebook = json.loads(archive.read(folder + 'notebooks/' + name + '.ipynb'))
                original = json.loads((LABS / (name + '.ipynb')).read_text())
                assert notebook['metadata'] == original['metadata']
                assert len(notebook['cells']) == len(original['cells'])
                for cell, source in zip(notebook['cells'], original['cells']):
                    assert cell['id'] == source['id']
                    if cell['cell_type'] == 'code':
                        assert cell == source, f'changed code: {name}'
                        assert not cell['outputs'] and cell['execution_count'] is None
                    else:
                        for target in re.findall(r'\]\(([^)]+)\)', cell['source']):
                            url = urlsplit(target)
                            assert url.scheme or not url.path, f'non-portable link: {name}: {target}'
    summary = (ROOT / 'SUMMARY.md').read_text()
    for page in ('downloads/README.md', 'PRACTICE.md'):
        assert page in summary
    for slug, _ in CHAPTERS:
        assert f'downloads/chapter-{slug[:2]}.zip' in (ROOT / (slug + '.md')).read_text()
    print('Downloads: 13 ZIPs, hashes, exact code cells, cleared outputs, portable links and 12 chapter entry points OK', flush=True)
    if execute:
        import nbformat
        from nbclient import NotebookClient
        # A fresh extracted ZIP is the only working directory: no source repo,
        # hidden input files or previously executed cells are available here.
        with tempfile.TemporaryDirectory(prefix='bash-download-validation-') as temporary:
            with zipfile.ZipFile(io.BytesIO(outputs['all-labs.zip'])) as archive:
                archive.extractall(temporary)
            package = next(Path(temporary).iterdir())
            for path in sorted((package / 'notebooks').glob('*.ipynb')):
                notebook = nbformat.read(path, as_version=4)
                nbformat.validate(notebook)
                NotebookClient(notebook, timeout=120, kernel_name='python3',
                               resources={'metadata': {'path': str(path.parent)}}).execute()
                # Execution outputs may contain live local paths; do not publish them.
                print('Extracted notebook executed: ' + path.name, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    validate(parser.parse_args().execute)
