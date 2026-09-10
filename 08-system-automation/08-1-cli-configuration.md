# 08-1. CLI·설정 우선순위·실행 로그

반복 작업을 도구로 만들려면 사용자가 입력과 결과를 예측할 수 있어야 한다. 명령줄 옵션, 환경 변수, 기본값의 우선순위와 종료 상태를 먼저 문서화한다.

{% hint style="info" %}
### 🧭 학습 목표

- getopts로 짧은 옵션과 필수 값을 처리한다.
- 옵션·환경·기본값 우선순위를 적용한다.
- 도움말과 오류의 출력 경로를 구분한다.
- 실행 로그와 결과 데이터를 분리한다.
{% endhint %}

## 학습 전 확인

환경 변수와 -o 옵션이 동시에 있으면 무엇을 쓰는가? 인수 순서나 누락에 따라 오류가 달라지는가?

## 1. 명령 사용법과 종료 상태

예제 도구의 형식은 `report.sh [-n] [-o DIR] INPUT`이다. -n은 dry-run, -o는 출력 위치다. 상태 0은 성공, 2는 사용법 오류, 1은 실행 실패다.

```bash
#!/usr/bin/env bash
usage() { printf 'usage: report.sh [-n] [-o DIR] INPUT\n'; }
dry_run=false
output_dir=${REPORT_OUTPUT:-./output}
while getopts ':hno:' option; do
    case $option in
        h) usage; exit 0 ;;
        n) dry_run=true ;;
        o) output_dir=$OPTARG ;;
        :) printf 'option -%s needs a value\n' "$OPTARG" >&2; exit 2 ;;
        \?) usage >&2; exit 2 ;;
    esac
done
shift "$((OPTIND - 1))"
(( $# == 1 )) || { usage >&2; exit 2; }
printf 'dry_run=%s output=%s input=%s\n' "$dry_run" "$output_dir" "$1"
```

이 예제는 파싱 결과만 출력하며 실제 보고서를 만들지 않는다. report.sh로 저장한 뒤 `bash report.sh -n -o 'two words' input.log`를 실행하면 세 설정이 보존된다.

## 2. getopts 해석

옵션 문자열 첫 콜론은 오류를 코드에서 처리하게 한다. o 뒤 콜론은 값이 필요하다는 뜻이다. OPTIND는 다음 처리 위치이며 파싱 후 shift로 옵션을 제거한다. 함수 안에서 여러 번 파싱하려면 OPTIND를 1로 재설정한다.

getopts는 긴 옵션을 직접 지원하지 않는다. --output 같은 인터페이스는 while과 case로 구현하고 누락 값·중복 옵션 정책을 테스트한다. GNU getopt와 BSD getopt를 동일하게 가정하지 않는다.

## 3. 설정 우선순위

```text
기본값 ./output → REPORT_OUTPUT 환경 변수 → -o 명령줄 옵션
```

최종 값은 뒤 단계가 덮어쓴다. 지원하는 설정만 읽는다. 환경 전체를 출력하면 토큰 등 업무와 무관한 정보가 드러날 수 있다.

## 4. 로그

```bash
log() {
    local level=$1
    shift
    printf '%s\t%s\t%s\n' "$(TZ=Asia/Seoul date '+%Y-%m-%dT%H:%M:%S%z')" "$level" "$*" >&2
}
log INFO 'validation completed'
```

stdout에는 다른 프로그램에 전달할 결과 데이터만 출력한다. 시각은 KST(+0900)로 표시하고 원본 시각과 구분한다. 로그 메시지의 탭·개행을 허용할지 정한다. 구조화 로그가 복잡해지면 jq나 Python으로 JSON을 생성한다.

## 🧪 직접 해보기

1. -h, -o 값 누락, 알 수 없는 옵션, 입력 없음의 상태를 기록한다.
2. REPORT_OUTPUT과 -o를 함께 지정하여 우선순위를 확인한다.
3. `--` 뒤의 하이픈으로 시작하는 입력을 보존한다.

### 해설

사용 오류는 파일 생성 전에 발견해야 한다. 도움말 요청은 stdout·상태 0, 잘못된 사용은 stderr·상태 2로 구분한다.

## ✅ 완료 기준

- [ ] 모든 옵션의 누락·정상 사례가 있다.
- [ ] 최종 설정의 출처를 설명한다.
- [ ] 로그가 결과 파일에 섞이지 않는다.

다음: [08-2. 예약 실행과 중복 방지](08-2-scheduling-locks.md)
