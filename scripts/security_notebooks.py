"""Build security companions from reviewed shell steps and synthetic fixtures."""
import re

CHAPTERS = {
    "11": ("web", "웹 로그와 제한된 배치", "11-parallel-jobs/11-3-web-log-analysis.md", "요청·상태를 분리하고 두 로컬 작업을 검증합니다.", "HTTP401=3, 200=2, 404=1; auth5행/access6행"),
    "12": ("triage", "오프라인 DFIR Capstone", "12-capstone/12-3-dfir-capstone.md", "고정 자료의 사본 수집·상태·해시와 사실/가설 인계를 통합합니다.", "complete, manifest 헤더+12항목, 기존 결과 보존, 사실2/가설1/미확인1"),
    "08": ("persistence", "지속성 위치와 승인 검토", "08-system-automation/08-3-persistence-review.md", "자동 시작 위치의 승인·실행 주체·수집 누락을 구분합니다.", "승인 미확인 1개, 알려진 기록 3개, 설치한 지속성 0개"),
    "09": ("login", "로그인 아티팩트 교차 검증", "09-testing-debugging/09-3-login-artifacts.md", "합성 로그인 요약을 교차 확인하고 잘못된 입력을 검출합니다.", "아티팩트 4행, 성공 1행, malformed 행 검출"),
    "10": ("journal-audit", "Journal·Audit 이벤트 연결", "10-program-architecture/10-4-audit-analysis.md", "서비스의 부팅 문맥과 Audit 레코드·이벤트 단위를 구분합니다.", "서비스 2행, Audit 6레코드/1이벤트, auid1000/euid0은 승인 여부와 별개"),
    "06": ("process-network", "프로세스·소켓 문맥 연결", "06-system-inspection/06-3-host-process-investigation.md", "합성 스냅샷을 연결하고 PID·시각·서비스 문맥의 한계를 설명합니다.", "프로세스 4행, PID 520의 서비스·목적지 연결, 판정은 추가 검토"),
    "07": ("permissions", "계정·권한 기준선 검토", "07-secure-scripting/07-3-account-permission-review.md", "UID 0·특수 비트·쓰기 권한을 정상 기준선과 비교합니다.", "UID 0 계정 2개, 기준선 SUID 1개, 검토 항목 1개, 악용 입증 아님"),
    "03": ("ioc", "IOC 검색과 입력 경계", "03-bash-basics/03-10-ioc-search.md", "문자열·정규식·필드 비교와 검색 실패를 구분합니다.", "literal=1 regex=2; substring=2 exact_field=1; no_match_status=1"),
    "04": ("files", "파일 조사와 경계 보존", "04-file-io/04-4-filesystem-investigation.md", "공백·개행 파일명을 보존하고 사본의 변경을 확인합니다.", "파일 4개, 줄 수 5, 원본 평문 보존"),
    "05": ("auth", "SSH 로그 파이프라인", "05-text-processing/05-4-auth-pipeline.md", "원문→실패 행→주소→빈도를 단계별로 확인합니다.", "실패 3건, 주소별 2/1건, 공개키 성공 1건, sudo 기록 1건"),
    "02": ("evidence", "환경과 증거 취급", "02-bash-setup/02-2-evidence-time.md",
           "합성 출처·KST·partial을 확인하고 작업 사본과 결과를 분리합니다.",
           "copy_matches=yes, original_and_analysis=separate; 미수집은 0건이 아닙니다."),
}


def build_security_notebooks(md, code, notebook, root):
    data_dir = root / "examples/security-labs/data"
    fixtures = {str(p.relative_to(data_dir)): p.read_text(encoding="utf-8")
                for p in sorted(data_dir.rglob("*")) if p.is_file()}
    all_fixtures = fixtures
    selected_inputs = {
        '02': ['provenance.txt'], '03': ['ioc.log'], '04': ['provenance.txt'],
        '05': ['auth.log'], '06': ['processes.psv', 'sockets.psv'],
        '07': ['passwd.sample', 'permissions.psv'],
        '08': ['persistence.psv', 'service-review.txt'],
        '09': ['login-review.psv', 'auth.log'], '10': ['journal-review.psv', 'audit.log'],
        '11': ['access.log', 'auth.log'], '12': list(all_fixtures),
    }
    tools = {name: (root / 'examples/security-labs' / name).read_text(encoding='utf-8')
             for name in ('ioc-search.sh', 'triage-offline.sh')}
    result = {}
    for number, (slug, title, page, goal, expected) in sorted(CHAPTERS.items()):
        fixtures = {name: all_fixtures[name] for name in selected_inputs[number]}
        source = (root / f"examples/security-labs/ch{number}.sh").read_text(encoding="utf-8")
        chunks = re.split(r"^# STEP: (.+)\n", source, flags=re.M)
        cells = [md(f"## Goal\n\n{goal}\n\n[교안과 분석 질문](../../{page})을 먼저 읽습니다."),
                 md("## Setup\n\nPython 커널의 %%bash를 사용합니다. 새 임시 폴더에 합성 자료와 결과 경로를 준비합니다. 외부 접속·서비스 등록·원본 서버 조사는 하지 않습니다. 코드를 검토하고 Setup부터 순서대로 실행합니다. Bash 셀 사이의 상태는 환경 변수와 파일로 전달합니다."),
                 code("from pathlib import Path\nimport hashlib\nimport os\nimport tempfile\n\n"
                      f"lab = Path(tempfile.mkdtemp(prefix='bash-security-{number}-'))\n"
                      "data = lab / 'data'\noutput = lab / 'output'\ndata.mkdir()\noutput.mkdir()\n"
                      f"fixtures = {fixtures!r}\n"
                      "for name, content in fixtures.items():\n"
                      "    path = data / name\n    path.parent.mkdir(parents=True, exist_ok=True)\n"
                      "    path.write_text(content, encoding='utf-8')\n"
                      "before = {name: hashlib.sha256((data / name).read_bytes()).hexdigest() for name in fixtures}\n"
                      "tools_dir = lab / 'tools'\ntools_dir.mkdir()\n"
                      "os.environ['COURSE_TOOLS'] = str(tools_dir)\n"
                      "os.environ['COURSE_DATA'] = str(data)\nos.environ['COURSE_OUT'] = str(output)\n"
                      "print('합성 자료와 새 결과 폴더 준비 완료')"),
                 md(f"## Steps\n\n예상 결과: {expected}\n\n명령을 실행하기 전에 입력·출력·실패 조건을 표시합니다. 자료의 상세 필드 해석과 정상 행위 대안은 연결된 교안에서 확인합니다.")]
        if number in ('03', '12'):
            tool_name = 'ioc-search.sh' if number == '03' else 'triage-offline.sh'
            cells += [md("### 제공 도구 준비\n\n아래 구현을 읽고 입력 검증·실패 처리·출력 경계를 표시합니다. 실행 중 다운로드하지 않으며 실습 폴더에만 저장합니다."),
                      code('%%bash\nset -euo pipefail\ncat > "$COURSE_TOOLS/' + tool_name + '" <<\'COURSE_TOOL\'\n' + tools[tool_name] + 'COURSE_TOOL\n')]
        for i in range(1, len(chunks), 2):
            cells += [md(f"### {(i + 1) // 2}. {chunks[i]}"),
                      code("%%bash\nset -euo pipefail\n"
                           ': "${COURSE_DATA:?}" "${COURSE_OUT:?}"\n' + chunks[i + 1])]
        cells += [md("## Checks\n\n각 STEP의 test는 고정 자료의 계산 결과를 검사합니다. 아래는 원본 내용 보존을 확인합니다. 실행 성공과 침해 판정은 다릅니다. 어떤 결과가 사실이고 어떤 결론이 가설인지 교안 질문에 답합니다."),
                  code("after = {name: hashlib.sha256((data / name).read_bytes()).hexdigest() for name in fixtures}\n"
                       "assert before == after\nprint('원본 내용 보존: PASS')\n"
                       "print('분석 결과 파일 수:', sum(p.is_file() for p in output.rglob('*')))"),
                  md("## Next Steps\n\n교안의 완료 기준에 따라 근거·정상 행위 가능성·누락·추가 확인을 제출합니다. 결과는 검토용 임시 폴더에 남습니다. 재실행은 Setup부터 새 폴더에서 시작하며 실제 증거를 공개 저장소에 올리지 않습니다.")]
        result[f"security-{number}-{slug}.ipynb"] = notebook(f"{number}장 보안 실습 — {title}", cells)
    return result
