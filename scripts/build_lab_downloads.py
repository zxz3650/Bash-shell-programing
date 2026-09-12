#!/usr/bin/env python3
"""Build deterministic, self-contained notebook ZIPs; never package local outputs."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / 'jupyter-book/labs'
RAW = 'https://github.com/zxz3650/Bash-shell-programing/raw/refs/heads/master/downloads'
BLOB = 'https://github.com/zxz3650/Bash-shell-programing/blob/master/'
BOOK = 'https://zxz3650.gitbook.io/bash-shell-programing/'
CHAPTERS = [
    ('01-bash-intro', ['00-orientation-and-safety', '01-when-to-use-bash']),
    ('02-bash-setup', ['00-orientation-and-safety', 'security-02-evidence']),
    ('03-bash-basics', ['02-arguments-variables-arrays', '03-conditions-loops-functions', 'security-03-ioc']),
    ('04-file-io', ['04-files-permissions-pipelines', 'security-04-files']),
    ('05-text-processing', ['05-text-processing', 'security-05-auth']),
    ('06-system-inspection', ['06-system-inspection-secure-scripting', 'security-06-process-network']),
    ('07-secure-scripting', ['06-system-inspection-secure-scripting', 'security-07-permissions']),
    ('08-system-automation', ['07-automation-testing', 'security-08-persistence']),
    ('09-testing-debugging', ['09-error-contracts', 'security-09-login']),
    ('10-program-architecture', ['10-modules-contracts', 'security-10-journal-audit']),
    ('11-parallel-jobs', ['11-bounded-parallel', 'security-11-web']),
    ('12-capstone', ['08-capstone-triage-collector', 'security-12-triage']),
]
LABELS = {
    '00-orientation-and-safety': '환경·안전',
    '01-when-to-use-bash': 'Bash 활용과 첫 조사',
    '02-arguments-variables-arrays': '인자·변수·배열',
    '03-conditions-loops-functions': '조건·반복·함수',
    '04-files-permissions-pipelines': '파일·권한·파이프',
    '05-text-processing': '텍스트 처리',
    '06-system-inspection-secure-scripting': '안전한 시스템 조사',
    '07-automation-testing': '자동화·테스트',
    '08-capstone-triage-collector': '로컬 조사 수집기',
    '09-error-contracts': '오류·종료 상태',
    '10-modules-contracts': '모듈·함수',
    '11-bounded-parallel': '제한된 병렬 처리',
    'security-02-evidence': '증거·KST',
    'security-03-ioc': 'IOC 검색',
    'security-04-files': '의심 파일 조사',
    'security-05-auth': 'SSH 로그 분석',
    'security-06-process-network': '프로세스·네트워크',
    'security-07-permissions': '계정·권한·GTFOBins 검토',
    'security-08-persistence': '지속성 흔적 검토',
    'security-09-login': '로그인 아티팩트',
    'security-10-journal-audit': 'Journal·Audit',
    'security-11-web': '웹 로그 분석',
    'security-12-triage': 'DFIR 종합 실습',
}


def encoded(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def notebook_bytes(name: str) -> bytes:
    path = LABS / (name + '.ipynb')
    notebook = json.loads(path.read_text())
    # Keep all code, fixtures and ordering unchanged. Links in the standalone
    # distribution point to the online source instead of absent textbook files.
    def online_link(match: re.Match) -> str:
        target = match[1]
        url = urlsplit(target)
        if url.scheme or not url.path or url.path.startswith('/'):
            return match[0]
        resolved = (path.parent / unquote(url.path)).resolve()
        assert resolved.is_file(), target
        relative = resolved.relative_to(ROOT).as_posix()
        suffix = ('#' + url.fragment) if url.fragment else ''
        return '](' + BLOB + quote(relative) + suffix + ')'
    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            source = cell['source']
            source = ''.join(source) if isinstance(source, list) else source
            cell['source'] = re.sub(r'\]\(([^)]+)\)', online_link, source)
        else:
            assert cell['execution_count'] is None and not cell['outputs']
    return encoded(notebook)


def start_here(title: str, names: list[str]) -> bytes:
    order = '\n'.join(f'{i}. `notebooks/{name}.ipynb`' for i, name in enumerate(names, 1))
    return f'''# {title} — 실습 시작하기

이 ZIP은 JupyterLab에서 실행하는 학습용 노트북 묶음입니다. 완성된 HTML 웹사이트가 아닙니다.
노트북 안에 예제 코드와 합성 입력 자료가 포함되어 있습니다. 기본 문법 실습을 먼저 마친 뒤 보안 적용 실습을 진행합니다.

## 실행 순서

Ubuntu VM 또는 WSL2 Ubuntu에서 Python 3.10 이상과 Bash를 준비합니다.
압축을 푼 뒤 이 파일과 `requirements.txt`가 있는 폴더에서 터미널을 엽니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

JupyterLab에서 `notebooks/`를 열고 Python 3 커널을 선택합니다. `%%bash` 셀은 그대로 실행합니다.
설정 셀부터 위에서 아래로 Shift+Enter로 실행하고, Checks의 결과를 확인합니다.
서로 다른 Bash 셀 사이에서 일반 셸 변수나 `cd` 상태는 유지되지 않습니다.

{order}

전체 묶음에서는 노트북 번호와 교안 장 번호가 다를 수 있으므로 [장별 연결표]({BOOK}downloads)를 함께 봅니다.
01·02장의 환경 실습, 06·07장의 안전한 조사 실습은 여러 장에서 함께 사용합니다.

## 보관과 안전

- 개인 풀이를 다른 이름으로 저장합니다. 새 버전은 새 폴더에 풀어 기존 풀이를 보존합니다.
- 임시 실습 디렉터리는 영구 보관 장소가 아닙니다. Cleanup 전에 필요한 결과를 따로 저장합니다.
- 일반 사용자로 실행하고, Jupyter 서버를 외부에 공개하지 않습니다.
- 합성 자료를 사용하는 필수 실습과 실제 Linux 로그를 읽는 선택 VM 실습을 구분합니다.
- 터미널 프로젝트 전체 소스는 [저장소]({BLOB})에서 확인합니다. 이 ZIP은 노트북 실습용입니다.
- MANIFEST.json의 version은 자료 묶음의 내용 식별자이며 설치 패키지를 고정하는 값은 아닙니다.

[설치·실행·문제 해결 안내]({BOOK}practice) · [온라인 교안]({BOOK})
'''.encode()


def package(key: str, title: str, names: list[str]) -> tuple[bytes, dict]:
    files = {'requirements.txt': b'jupyterlab>=4,<5\nipykernel>=6,<7\n',
             'START-HERE.md': start_here(title, names)}
    files.update({f'notebooks/{name}.ipynb': notebook_bytes(name) for name in names})
    hashes = {name: digest(data) for name, data in sorted(files.items())}
    version = digest(encoded(hashes))[:12]
    files['MANIFEST.json'] = encoded({'version': version, 'sha256': hashes, 'notebooks': names})
    output = io.BytesIO()
    folder = f'bash-{key}-{version}'
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(f'{folder}/{name}', date_time=(2020, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    data = output.getvalue()
    return data, {'file': key + '.zip', 'title': title, 'version': version,
                  'bytes': len(data), 'sha256': digest(data), 'notebooks': names}


def build() -> dict[str, bytes]:
    artifacts = {}
    entries = []
    for slug, names in CHAPTERS:
        title = (ROOT / (slug + '.md')).read_text().splitlines()[0].removeprefix('# ')
        data, entry = package('chapter-' + slug[:2], title, names)
        artifacts[entry['file']] = data
        entries.append(entry)
    all_names = sorted(path.stem for path in LABS.glob('*.ipynb'))
    assert set(all_names) == {name for _, names in CHAPTERS for name in names}
    data, all_entry = package('all-labs', 'Bash 전체 실습', all_names)
    artifacts[all_entry['file']] = data
    artifacts['index.json'] = encoded({'chapters': entries, 'all': all_entry})
    rows = []
    for entry in entries:
        names = ' → '.join(LABELS[name] for name in entry['notebooks'])
        rows.append(f"| {entry['title']} | [ZIP 받기]({RAW}/{entry['file']}) | {names} | `{entry['version']}` | {entry['bytes'] / 1024:.1f} KiB |")
    artifacts['README.md'] = (f'''# 학습용 Jupyter 노트북 다운로드

**수강할 장의 ZIP을 내려받고, 압축을 푼 뒤 START-HERE.md부터 읽으세요.** Git이나 GitHub 계정 없이 받을 수 있습니다.

[전체 실습 ZIP 받기 — 노트북 {len(all_names)}개]({RAW}/all-labs.zip) · [처음 실행하는 방법](../PRACTICE.md)

전체 자료 버전: `{all_entry['version']}` · {all_entry['bytes'] / 1024:.1f} KiB

## 장별 다운로드

기본 문법 노트북을 먼저, `security-` 노트북을 나중에 실행합니다. 노트북 파일 번호는 교안 장 번호와 다릅니다. 같은 노트북을 공유하는 장도 있습니다.

| 교안 | 다운로드 | 포함 실습 — 실행 순서 | 자료 버전 | ZIP 크기 |
| --- | --- | --- | --- | --- |
''' + '\n'.join(rows) + '''

## 어떤 자료가 들어 있나요?

- `notebooks/`: 해당 장의 `.ipynb` 파일. 예제 코드와 합성 입력 데이터는 노트북 안에 포함됩니다.
- `requirements.txt`: JupyterLab과 Python 커널 설치 목록. Bash는 운영체제에서 준비합니다.
- `START-HERE.md`: 압축 해제 후 실행 방법과 노트북 순서.
- `MANIFEST.json`: 자료 버전과 파일별 SHA256.

이 ZIP은 **JupyterLab 실행용 실습 자료**이며 오프라인 HTML Jupyter Book은 아닙니다. 교안 본문과 터미널 프로젝트 전체 소스는 포함하지 않습니다. 노트북의 교안 참고 링크는 온라인 저장소로 연결됩니다. 패키지 최초 설치와 온라인 참고 자료 열기에는 인터넷 연결이 필요합니다.

## 새 버전으로 바꿀 때

현재 폴더의 MANIFEST.json과 위 자료 버전을 비교합니다. 같으면 다시 받지 않아도 됩니다. 달라졌다면 필요한 장만 **새 폴더**에 풀고 개인 풀이를 비교해 옮깁니다. 기존 폴더를 덮어쓰지 않습니다.

[배포 목록과 ZIP SHA256](index.json)에서 무결성을 확인할 수 있습니다. 자료 버전은 노트북 묶음의 식별자이며 설치 패키지의 버전 고정을 뜻하지 않습니다.
''').encode()
    return artifacts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    destination = ROOT / 'downloads'
    outputs = build()
    if args.check:
        for name, data in outputs.items():
            assert (destination / name).read_bytes() == data, f'stale download: {name}'
        assert {p.name for p in destination.iterdir()} == set(outputs), 'unexpected distribution file'
    else:
        destination.mkdir(exist_ok=True)
        for name, data in outputs.items():
            (destination / name).write_bytes(data)
    print(f'Downloads: {len(CHAPTERS)} chapter ZIPs + 23-notebook full ZIP; deterministic files OK')


if __name__ == '__main__':
    main()
