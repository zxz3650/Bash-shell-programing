# 02. 개발 및 실습 환경

**[02장 학습용 노트북 ZIP 받기](https://github.com/zxz3650/Bash-shell-programing/raw/refs/heads/master/downloads/chapter-02.zip)** · [처음 실행하는 방법](PRACTICE.md) · [포함 노트북과 자료 버전](downloads/README.md)

압축을 푼 뒤 `START-HERE.md`의 순서대로 기본 실습부터 실행하고 보안 적용 실습으로 이어갑니다.

## 개요

Windows WSL 2 또는 Linux에 Bash 실습 환경을 구성하고 명령 탐색, shebang, 종료 상태와 도움말 사용법을 익힙니다. 기본 환경과 첫 스크립트 실행을 확인한 뒤 원본·결과 분리와 증거 취급 실습으로 연결합니다.

## 보안 실습 순서

1. [02-1. 조사 환경과 실습 범위 정하기](02-bash-setup/02-1-lab-boundaries.md)
2. [02-2. 원본·해시·시간대를 보존하는 분석 준비](02-bash-setup/02-2-evidence-time.md)
3. [02-3. Jupyter에서 재현 가능한 조사 실습하기](02-bash-setup/02-3-notebook-workflow.md)

처음 배우는 학생은 아래 설치·명령 탐색·첫 스크립트 실행을 먼저 진행한 뒤 위의 보안 실습으로 이동합니다.

## 학습 전 확인

터미널 창, Bash 프로세스, .sh 파일을 구분할 수 있는지 [01장](01-bash-intro.md)에서 확인합니다. 아래 PowerShell 명령은 Windows에서, bash 명령은 Linux·WSL·macOS의 Bash에서 실행합니다.

## 환경 선택과 설치

| 환경 | 준비 | 이 교안에서의 범위 |
|---|---|---|
| Windows | WSL2 Ubuntu 설치 | Bash·파일 분석, 서비스는 지원 여부 확인 |
| Linux | 별도 Ubuntu VM·GNU 도구 | 기준 환경, 로그·권한별 준비 필요 |
| macOS | 기본 Bash 또는 별도 Bash | 공통 문법·프로젝트, Linux 전용 제외 |
| Colab | 노트북 링크 열기 | 셀 실행, 영구 예약 작업 제외 |

### Windows: PowerShell에서 WSL 준비

관리자 PowerShell에서 실행하고 요청되면 재부팅합니다.

```powershell
wsl --install -d Ubuntu
wsl --list --verbose
```

Ubuntu를 열어 사용자 계정을 만든 뒤 다음 Linux 명령을 실행합니다. 이미 WSL이 있다면 재설치하지 않고 배포판과 버전을 확인합니다. [Microsoft 공식 설치 안내](https://learn.microsoft.com/en-us/windows/wsl/install)를 기준으로 합니다.

### Ubuntu: 과정 도구

```bash
sudo apt update
sudo apt install bash git coreutils findutils grep gawk sed jq shellcheck bats shfmt python3-venv python3-pip tzdata procps
bash --version
```

설치는 관리자 권한이 필요하지만 교재 실습은 일반 사용자로 진행합니다. 배포판 버전에 따라 패키지 제공 여부가 다를 수 있습니다. 설치 실패 시 해당 패키지와 배포판 버전을 먼저 확인합니다.

선택 Linux 조회에 필요한 패키지는 iproute2(ip·ss), lsof, file, binutils(strings), libcap2-bin(getcap), auditd(ausearch·aureport), systemd(journalctl)입니다. 실습 VM의 구성과 패키지 제공 여부를 먼저 확인합니다. 특히 auditd 설치는 서비스 상태에 영향을 줄 수 있으므로 운영 증거 시스템에서 설치하지 않습니다. 필수 오프라인 노트북에는 이런 서비스 설정이 필요하지 않습니다.

01장의 자기 환경 관찰에는 `procps`의 ps와 `tzdata`의 Asia/Seoul 데이터가 필요합니다. `TZ=Asia/Seoul date '+%z'`가 `+0900`인지 확인합니다. 최소 컨테이너에서 시간대 데이터가 빠지면 잘못된 오프셋이 나올 수 있으며, 관찰 도구는 이 경우 성공 보고서를 만들지 않습니다. 이 설정은 명령의 표시 시간대를 지정하며 시스템 시계를 바꾸지 않습니다.

### macOS: 실행 파일 구분

```bash
/bin/bash --version
command -v bash
```

기본 /bin/bash는 보통 3.2 계열입니다. Homebrew를 사용하는 경우 다음 도구를 별도로 설치할 수 있습니다.

```bash
brew install bash jq shellcheck shfmt bats-core
bash --version
```

설치 후에도 /bin/bash가 자동 교체되는 것은 아닙니다. `command -v bash`와 `type -a bash`로 실제 선택된 경로를 확인합니다. GNU stat -c·date -Is·sort -z와 Linux /proc·ss·ip 예제는 [호환성 표](appendix-references.md)를 참고합니다.

## 저장소와 실습 폴더

```bash
git clone https://github.com/zxz3650/Bash-shell-programing.git
cd Bash-shell-programing
lab_dir=$(mktemp -d)
printf 'practice directory=%s\n' "$lab_dir"
```

이미 저장소가 있다면 해당 폴더를 사용합니다. GitBook용 Markdown은 저장소에서 읽고, 파일 변경 실습은 별도의 lab_dir 안에서 진행합니다. 샘플 코드에서 lab_dir를 사용하면 같은 터미널의 앞 준비 블록을 먼저 실행해야 합니다.

## JupyterLab 실습 환경

저장소 루트에서 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r jupyter-book/requirements.txt
jupyter lab jupyter-book/labs
```

노트북의 Python 커널에서 `%%bash` 셀을 실행합니다. 각 Bash 셀은 새 프로세스이므로 `cd`나 셸 변수가 다음 셀로 이어지지 않습니다. 교재는 Python 셀에서 설정한 BASH_LAB_DIR와 파일로 상태를 전달합니다. Python 가상환경은 Python 패키지를 격리하며 Bash 자체를 가상화하지 않습니다.

[실습 목록](jupyter-book/labs/README.md)의 Colab 링크를 사용하면 설치 없이 시작할 수 있습니다. Colab의 파일과 런타임은 영구 보존을 보장하지 않으므로 필요한 결과는 별도로 저장합니다.

{% hint style="info" %}
## 🧭 학습 목표

- Bash 버전과 현재 셸 프로세스를 확인한다.
- VS Code WSL과 필수 품질 도구를 준비한다.
- 첫 스크립트를 실행하고 종료 상태를 판독한다.
{% endhint %}

---

## 2.1 셸이란 무엇인가

셸은 사용자의 명령을 해석해 운영체제의 프로그램을 실행하는 인터페이스입니다. Bash는 대화형 명령 실행과 스크립트 실행을 모두 지원합니다.

```bash
printf 'shell=%s\n' "$SHELL"
bash --version
pwd
```

`$SHELL`은 로그인 셸을 나타내므로 현재 실행 중인 프로세스와 다를 수 있습니다. 정확한 현재 프로세스는 다음처럼 확인합니다.

```bash
ps -p "$$" -o pid,ppid,comm,args
```

## 명령 탐색 순서

alias는 입력을 읽을 때 치환되며 비대화형 셸에서는 기본적으로 확장되지 않습니다. 명령 실행은 함수·builtin·PATH의 실행 파일 등을 찾습니다. [03-1 실행 모델](03-bash-basics/03-1-execution-model.md)에서 두 단계를 구분합니다.

```bash
type cd
type printf
type -a bash
command -v jq
```

자동화에서는 `which`보다 셸 builtin과 함수까지 판별하는 `command -v`를 권장합니다.

## 첫 번째 스크립트

```bash
#!/usr/bin/env bash

printf 'user=%s\n' "$(id -un)"
printf 'host=%s\n' "$(hostname)"
printf 'time=%s\n' "$(TZ=Asia/Seoul date '+%Y-%m-%dT%H:%M:%S%z')"
```

위 내용을 실습 폴더의 `system_info.sh`로 저장한 뒤 그 폴더에서 실행합니다.

```bash
bash -n system_info.sh
bash system_info.sh
chmod u+x system_info.sh
./system_info.sh
echo "$?"
```

사용자·호스트·KST 시각 세 행과 마지막 상태 0을 확인합니다. 값은 환경마다 달라집니다. bash로 파일을 읽어 실행할 때와 실행 권한을 주어 직접 실행할 때를 구분합니다.

## 첫 실행 오류 해결

| 증상 | 확인할 원인 | 조치 |
|---|---|---|
| command not found | 실행 파일·PATH | command -v·type 확인 |
| Permission denied | 실행 권한·디렉터리 권한 | bash로 읽기 실행과 직접 실행 비교 |
| bad interpreter 또는 CR 문자 | shebang·CRLF 줄바꿈 | UTF-8, LF로 저장 |
| 파일 없음 | 현재 위치·상대 경로 | pwd와 실제 파일명 확인 |
| 배열 구문 오류 | sh로 Bash 코드 실행 | bash 또는 올바른 shebang 사용 |

## 환경 확인 제출

OS 종류, Bash 경로·버전, Python 버전, Jupyter 커널 이름, 첫 실행의 상태를 기록합니다. 전체 환경 변수를 덤프하지 않습니다. `bash tests/test-course.sh`는 저장소 루트에서 제공 프로젝트를 검증합니다.

첫 줄은 shebang이며 사용할 인터프리터를 지정합니다. 종료 상태 `0`은 일반적으로 성공, 그 외 값은 실패를 뜻합니다.

## 도움말을 찾는 순서

```bash
help printf        # Bash builtin
man find           # 외부 명령 매뉴얼
find --help        # GNU find의 옵션 요약, macOS는 man find 사용
type -a command    # 명령의 정체 확인
```

## 🧪 직접 해보기

1. 현재 Bash의 PID와 부모 PID를 출력해 보세요.
2. `cd`, `test`, `grep`이 builtin인지 외부 명령인지 확인하세요.
3. 존재하지 않는 명령의 종료 상태를 확인하세요.

## ✅ 완료 기준

- `bash --version`, `command -v`, `type`을 사용할 수 있다.
- 실행 권한과 shebang의 역할을 설명할 수 있다.
