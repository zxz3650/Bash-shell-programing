#!/usr/bin/env python3
"""Execute offline teaching steps and verify fixture immutability."""
import hashlib
import os
import shutil
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "examples/security-labs/data"


def digests():
    return {str(p.relative_to(DATA)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in DATA.rglob("*") if p.is_file()}


before = digests()
scripts = sorted((ROOT / "examples/security-labs").glob("ch[0-9][0-9].sh"))
assert scripts
for script in scripts:
    with tempfile.TemporaryDirectory(prefix=f"course-{script.stem}-") as out:
        env = dict(os.environ, COURSE_DATA=str(DATA), COURSE_OUT=out,
                   COURSE_TOOLS=str(ROOT / 'examples/security-labs'))
        result = subprocess.run(["bash", str(script)], env=env, cwd=ROOT,
                                text=True, capture_output=True, timeout=60)
        assert result.returncode == 0, f"{script.name}\n{result.stdout}\n{result.stderr}"
        assert before == digests(), f"fixture modified: {script.name}"
        if script.stem == 'ch12':
            report = Path(out) / 'report'
            for line in (report / 'SHA256SUMS').read_text().splitlines():
                expected, name = line.split('  ', 1)
                assert hashlib.sha256((report / name).read_bytes()).hexdigest() == expected
        print(f"PASS: {script.stem} expected results and source preservation")
print(f"All {len(scripts)} security lab workflows passed.")

TOOLS = ROOT / 'examples/security-labs'
def run(tool, args):
    return subprocess.run(['bash', str(TOOLS / tool), *map(str, args)],
                          text=True, capture_output=True, timeout=30)

with tempfile.TemporaryDirectory(prefix='course-cli-check-') as temporary:
    work = Path(temporary)
    spaced = work / 'file with spaces.log'
    shutil.copyfile(DATA / 'ioc.log', spaced)
    cases = [
        (['-f', spaced, '-i', 'indicator.example'], 0),
        (['-f', spaced, '-i', 'not-present'], 1),
        (['-f', spaced, '-i', '-n'], 1),
        (['-f', spaced, '-i', ''], 2),
        (['-f', spaced, '-i', 'one\ntwo'], 2),
        (['-f', spaced, '-i', 'x', '-i', 'y'], 2),
        (['-f', work / 'missing', '-i', 'x'], 2),
        (['-f', spaced], 2),
    ]
    for args, expected in cases:
        result = run('ioc-search.sh', args)
        assert result.returncode == expected, result
    print('PASS: IOC CLI match/no-match/errors, quoting, duplicate and newline rejection')

    source = work / 'source'
    shutil.copytree(DATA, source)
    result = run('triage-offline.sh', ['-d', source, '-o', work / 'dry', '-n'])
    assert result.returncode == 0 and not (work / 'dry').exists()
    result = run('triage-offline.sh', ['-d', source, '-o', source / 'nested'])
    assert result.returncode == 2 and not (source / 'nested').exists()
    # Remove only this test's copy, never repository evidence.
    (source / 'sockets.psv').unlink()
    result = run('triage-offline.sh', ['-d', source, '-o', work / 'partial'])
    assert result.returncode == 1
    assert (work / 'partial/COLLECTION_FINISHED').read_text().strip() == 'partial'
    assert 'network\tsockets.psv\tunavailable' in (work / 'partial/manifest.tsv').read_text()
    (source / 'auth.log').unlink()
    result = run('triage-offline.sh', ['-d', source, '-o', work / 'missing-required'])
    assert result.returncode == 2 and not (work / 'missing-required').exists()
    (source / 'auth.log').symlink_to(DATA / 'auth.log')
    result = run('triage-offline.sh', ['-d', source, '-o', work / 'linked-required'])
    assert result.returncode == 2 and not (work / 'linked-required').exists()
    print('PASS: triage dry-run, source boundary, partial status, required and symlink rejection')
assert before == digests()
