#!/usr/bin/env python3
"""Validate book structure, local links, shell syntax and optional notebook execution."""
from __future__ import annotations

import argparse
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


def validate_notebooks(execute: bool) -> None:
    import nbformat
    from nbclient import NotebookClient

    paths = sorted((ROOT / "jupyter-book/labs").glob("*.ipynb"))
    for path in paths:
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        for cell in notebook.cells:
            if cell.cell_type == "code":
                assert cell.execution_count is None and not cell.outputs, f"committed output: {path.name}"
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
    validate_notebooks(args.execute_notebooks)


if __name__ == "__main__":
    main()
