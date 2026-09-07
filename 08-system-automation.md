# 08. 시스템 자동화

## 개요

반복되는 점검과 수집 작업을 옵션, 로그, dry-run을 갖춘 명령줄 도구로 만듭니다.

## 학습 순서

1. [08-1. CLI·설정 우선순위·로그](08-system-automation/08-1-cli-configuration.md)
2. [08-2. 비대화형 실행·예약·잠금](08-system-automation/08-2-scheduling-locks.md)

환경 변수와 옵션 중 무엇이 우선인가, 도움말과 사용 오류는 같은 상태인가, 작업이 겹치면 어떻게 되는가를 먼저 생각합니다. 노트북 07로 자동화의 상태 계약을 검증한 뒤 Linux 환경에서 예약·잠금 설정을 학습합니다. 스케줄을 실제 등록하는 것과 설정 예제를 읽는 것을 구분합니다.

{% hint style="info" %}
## 🧭 학습 목표

- `getopts`로 명령줄 옵션을 처리한다.
- 설정, 실행 로직과 출력 형식을 분리한다.
- cron과 systemd timer에 적합한 비대화형 스크립트를 작성한다.
{% endhint %}

## 선행 지식

- 03장 함수와 종료 상태
- 04장 파일과 권한
- 07장 입력 검증과 안전한 정리

## 1. 옵션 처리

```bash
usage() { printf 'usage: %s [-n] [-o DIR] INPUT\n' "${0##*/}" >&2; }

dry_run=false
output_dir=./output

while getopts ':no:' option; do
    case $option in
        n) dry_run=true ;;
        o) output_dir=$OPTARG ;;
        *) usage; exit 2 ;;
    esac
done
shift "$((OPTIND - 1))"
```

## 2. 비대화형 실행

예약 실행에서는 현재 디렉터리, PATH, 터미널이 다를 수 있습니다. 절대 경로를 사용하고 사용자 입력을 기다리지 않으며 stdout과 stderr의 의미를 구분합니다.

```bash
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
readonly config_file="$script_dir/config.env"
```

## 3. 실행 로그

```bash
log() {
    local level=$1
    shift
printf '%s\t%s\t%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$level" "$*" >&2
}
```

비밀번호·토큰·원문 개인정보는 로그에 남기지 않습니다.

## 🧪 종합 실습

지정한 디렉터리의 파일 수, 전체 크기, 최근 변경 파일을 TSV로 출력하는 `inventory.sh`를 작성합니다. `-n`, `-o DIR`, `-h`를 지원하고 읽기 오류를 기록합니다.

## ✅ 완료 기준

- 옵션 오류와 실행 오류가 서로 다른 종료 상태를 반환한다.
- 어느 디렉터리에서 실행해도 동일하게 동작한다.
- dry-run에서는 파일시스템을 변경하지 않는다.
