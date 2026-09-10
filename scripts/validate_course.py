#!/usr/bin/env python3
"""Validate book structure, local links, shell syntax and optional notebook execution."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def validate_documents() -> None:
    summary = (ROOT / "SUMMARY.md").read_text(encoding="utf-8")
    pages = [ROOT / path for path in re.findall(r"\]\(([^)]+\.md)\)", summary)]
    assert len(pages) == len(set(pages)), "duplicate SUMMARY entry"
    blocks = 0
    for page in pages:
        assert page.is_file(), f"missing page: {page}"
        text = page.read_text(encoding="utf-8")
        assert text.startswith("# "), f"missing title: {page}"
        assert text.count("{% hint ") == text.count("{% endhint %}"), f"hint imbalance: {page}"
        fences = re.findall(r"^```.*$", text, re.M)
        assert len(fences) % 2 == 0, f"fence imbalance: {page}"
        plain = re.sub(r"^```[^\n]*\n.*?^```\s*$", "", text, flags=re.M | re.S)
        for target in re.findall(r"\]\(([^)]+)\)", plain):
            link = urlsplit(target)
            if link.scheme or not link.path or link.path.startswith("/"):
                continue
            resolved = (page.parent / unquote(link.path)).resolve()
            assert resolved.exists(), f"broken link: {page.relative_to(ROOT)} -> {target}"
        for code in re.findall(r"^```bash\n(.*?)^```\s*$", text, re.M | re.S):
            if code.startswith("#!/usr/bin/env bats"):
                continue
            checked = subprocess.run(["bash", "-n"], input=code, text=True, capture_output=True)
            assert checked.returncode == 0, f"shell syntax: {page}\n{checked.stderr}"
            blocks += 1
    for script in list((ROOT / "examples").rglob("*.sh")) + list((ROOT / "tests").glob("*.sh")):
        subprocess.run(["bash", "-n", str(script)], check=True)
    print(f"Documents: {len(pages)} SUMMARY pages, {blocks} Bash blocks, local links and executable syntax OK")


def validate_foundation_preservation() -> None:
    baseline = json.loads((ROOT / 'tests/fixtures/bash-foundations.json').read_text(encoding='utf-8'))
    summary = (ROOT / 'SUMMARY.md').read_text(encoding='utf-8')
    index = (ROOT / 'bash-syntax-index.md').read_text(encoding='utf-8')
    assert '* [03. Bash 기초 문법](03-bash-basics.md)' in summary
    assert 'Bash 문법 찾아보기' in summary
    positions = []
    for name, expected in baseline['sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, f'original syntax lesson changed: {name}'
        assert name in index, f'syntax index missing: {name}'
        positions.append(summary.index('](' + name + ')'))
    assert len(positions) == 9 and positions == sorted(positions), 'syntax lesson sequence changed'
    assert max(positions) < summary.index('](03-bash-basics/03-10-ioc-search.md)'), 'IOC precedes foundational lessons'
    toc = (ROOT / 'jupyter-book/myst.yml').read_text(encoding='utf-8')
    assert toc.index('file: labs/03-conditions-loops-functions.ipynb') < toc.index('file: labs/security-03-ioc.ipynb')
    print('Foundations: nine original lessons byte-identical; syntax index and foundation-first navigation OK')


def validate_security_coverage() -> None:
    # Structural regression guard, not a substitute for educational review.
    from security_notebooks import CHAPTERS, perspective_section
    required = {details[2] for number, details in CHAPTERS.items() if number >= '03'}
    required.update({
        '06-system-inspection/06-4-network-investigation.md',
        '07-secure-scripting/07-4-gtfobins-review.md',
        '10-program-architecture/10-3-journal-analysis.md',
    })
    summary = (ROOT / 'SUMMARY.md').read_text(encoding='utf-8')
    for page in required:
        assert page in summary, f'perspective page not published: {page}'
        section = perspective_section(ROOT, page)
        for term in ('Red Team', 'Blue Team', 'Artifact', 'Detection', 'Mitigation'):
            assert term in section, f'missing {term}: {page}'
    gtfo = (ROOT / '07-secure-scripting/07-4-gtfobins-review.md').read_text(encoding='utf-8')
    for term in ('https://gtfobins.org/', 'Sudo', 'SUID', 'Capabilities', 'R01', 'R02', 'R03', 'R04'):
        assert term in gtfo, f'missing GTFOBins learning anchor: {term}'
    print(f'Security coverage: {len(required)} linked perspective sections and GTFOBins learning anchors OK')


def validate_notebooks(execute: bool) -> None:
    import nbformat
    from nbclient import NotebookClient
    from build_jupyter_book import NOTEBOOKS

    paths = sorted((ROOT / "jupyter-book/labs").glob("*.ipynb"))
    toc = (ROOT / 'jupyter-book/myst.yml').read_text(encoding='utf-8')
    toc_paths = re.findall(r'file:\s+(\S+\.ipynb)', toc)
    assert len(toc_paths) == len(set(toc_paths)), 'duplicate notebook TOC entry'
    assert {str(p.relative_to(ROOT / 'jupyter-book')) for p in paths} == set(toc_paths), 'notebook TOC mismatch'
    for path in paths:
        assert json.loads(path.read_text(encoding="utf-8")) == NOTEBOOKS[path.name], f"regenerate notebook: {path.name}"
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        for cell in notebook.cells:
            if cell.cell_type == 'markdown':
                for target in re.findall(r'\]\(([^)]+)\)', cell.source):
                    link = urlsplit(target)
                    if not link.scheme and link.path and not link.path.startswith('/'):
                        assert (path.parent / unquote(link.path)).resolve().exists(), f'notebook link: {path.name} -> {target}'
            if cell.cell_type == "code":
                assert cell.execution_count is None and not cell.outputs, f"committed output: {path.name}"
                if cell.source.startswith("%%bash\n"):
                    checked = subprocess.run(["bash", "-n"], input=cell.source.split("\n", 1)[1],
                                             text=True, capture_output=True)
                    assert checked.returncode == 0, f"notebook Bash syntax: {path.name}\n{checked.stderr}"
                else:
                    ast.parse(cell.source, filename=f"{path.name}:{cell.id}")
        if execute:
            # Execute an in-memory copy; do not store host names or local paths in Git.
            NotebookClient(notebook, timeout=120, kernel_name="python3",
                           resources={"metadata": {"path": str(ROOT)}}).execute()
            print(f"Notebook executed: {path.name}", flush=True)
    print(f"Notebooks: {len(paths)} valid, outputs cleared; executed={execute}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute-notebooks", action="store_true")
    args = parser.parse_args()
    validate_documents()
    validate_foundation_preservation()
    validate_security_coverage()
    validate_notebooks(args.execute_notebooks)


if __name__ == "__main__":
    main()
