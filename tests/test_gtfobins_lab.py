#!/usr/bin/env python3
"""Execute chapter 07 from its published-shape ZIP as a non-root Linux user."""
import argparse
from pathlib import Path
import tempfile
import zipfile

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--render-dir', type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='gtfo-package-test-') as temporary:
        with zipfile.ZipFile(ROOT / 'downloads/chapter-07.zip') as archive:
            archive.extractall(temporary)
        package = next(Path(temporary).iterdir())
        path = package / 'notebooks/security-07-permissions.ipynb'
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        NotebookClient(notebook, timeout=120, kernel_name='python3',
                       resources={'metadata': {'path': str(path.parent)}}).execute()
        output = '\n'.join(item.get('text', '') for cell in notebook.cells
                           for item in cell.get('outputs', []) if item.output_type == 'stream')
        for expected in ('denied_status=2', 'restored_mode=600 content_unchanged=yes',
                         'original_lines=1 copy_lines=2', 'roundtrip_equal=yes',
                         'encoded_mode=600', 'lab_suid_files=0',
                         'E01 aligned', 'E02 review', 'E03 unknown', '원본 내용 보존: PASS'):
            assert expected in output, expected
        print('GTFO extension: six experiments and ten expected results PASS')
        if args.render_dir:
            args.render_dir.mkdir(parents=True, exist_ok=True)
            nbformat.write(notebook, args.render_dir / 'chapter-07-executed.ipynb')
            print('Local executed notebook saved; convert with nbconvert for visual review. Not distributed.')


if __name__ == '__main__':
    main()
