# 07. 안전한 Shell Script

## 기본 학습과 보안 실습 연결

07-1·07-2의 입력 검증·데이터 경계·dry-run·원본 보존을 학습합니다. 이어서 [07-3. 계정·권한 위험 검토](07-secure-scripting/07-3-account-permission-review.md)에서 특수 비트·sudo·capability·변경 권한을 비교합니다. 점검 스크립트에도 배운 안전 설계를 적용합니다.

이어서 [07-4. GTFOBins와 권한 경계 검토](07-secure-scripting/07-4-gtfobins-review.md)에서 정상 도구의 기능·권한 문맥·업무 범위를 비교합니다. Red Team의 위험 질문과 Blue Team의 실행 근거를 연결하고, 네 개의 합성 검토 카드로 등재·설정·행위 판정이 다른 이유를 연습합니다.

## 개요

외부에서 받은 입력을 검증하고, 옵션 주입을 방지하며, 임시 파일과 비밀정보를 안전하게 관리하는 방법을 배웁니다. 파일 삭제와 덮어쓰기 전에는 대상 경로와 변경 내용을 확인합니다.

## 학습 순서와 질문

1. [07-1. 입력 검증과 데이터·코드 경계](07-secure-scripting/07-1-input-boundaries.md)
2. [07-2. dry-run·멱등성·실패 시 보존](07-secure-scripting/07-2-dry-run-idempotency.md)

검증한 값이면 인용을 생략해도 되는가? dry-run에서 폴더를 만들면 어떤 문제가 있는가? 같은 요청을 다시 실행하면 결과가 유지되는가? 03장의 인수 경계, 04장의 경로·저장, 06장의 정리를 연결해 답합니다. 아래 mode·pattern·file 등의 조각 예제는 호출자가 입력을 전달한 상황을 가정합니다.

{% hint style="info" %}
## 🧭 학습 목표

- allowlist와 명시적 종료 상태로 입력을 검증한다.
- `eval`과 문자열 기반 명령 조립을 피한다.
- dry-run과 멱등성을 변경 작업에 적용한다.
{% endhint %}

## 권장 시작 구조

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

readonly program_name=${0##*/}

usage() {
    printf 'usage: %s INPUT_FILE\n' "$program_name" >&2
}

main() {
    (($# == 1)) || { usage; return 2; }

    local input=$1
    [[ -r $input ]] || {
        printf 'error: cannot read: %s\n' "$input" >&2
        return 1
    }

    wc -l -- "$input"
}

main "$@"
```

`set -e`만으로 모든 오류가 처리되는 것은 아닙니다. 예상 가능한 실패는 `if`, `||`, 명시적 종료 상태로 처리하고 반드시 테스트합니다.

## 입력 검증

```bash
is_valid_ipv4_text() {
    [[ $1 =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]
}

case $mode in
    collect|analyze) ;;
    *) printf 'invalid mode: %s\n' "$mode" >&2; exit 2 ;;
esac
```

위 IPv4 정규식은 모양만 검사하므로 999.999.999.999도 통과합니다. 주소 유효성 검증기로 사용하지 않습니다. 실제 주소 검증은 각 옥텟 범위까지 확인하거나 Python ipaddress 같은 전용 파서를 사용합니다. 가능한 값이 정해져 있다면 allowlist를 사용합니다. 검증된 데이터도 인용하고 해당 명령이 지원하는 옵션 종료 규칙을 사용합니다.

## 피해야 할 패턴

```bash
# 위험: 문자열을 다시 셸 코드로 해석
eval "$user_input"

# 위험: 다운로드와 실행을 한 단계로 연결
curl https://example.invalid/install.sh | bash

# 위험: 변수가 비면 예상 밖의 경로가 될 수 있음
rm -rf "$target/"*
```

대신 명령과 인수를 배열로 분리하고 다운로드한 파일은 출처·해시·내용을 검토한 뒤 실행합니다.

```bash
cmd=(grep -nF -- "$pattern" "$file")
"${cmd[@]}"
```

## 로그와 비밀정보

- `set -x`가 토큰과 비밀번호를 출력할 수 있습니다.
- 비밀을 명령행 인수나 URL에 넣지 않습니다.
- 보고서 파일에는 `umask 077`을 적용합니다.
- 오류 메시지에 전체 환경 변수나 원문 자격증명을 출력하지 않습니다.

## 멱등성과 dry-run

반복 실행해도 같은 결과가 되도록 설계하고, 변경 작업에는 미리보기 모드를 둡니다.

```bash
if [[ $dry_run == true ]]; then
    printf 'would move: %q -> %q\n' "$source" "$destination"
else
    mv -- "$source" "$destination"
fi
```

## 🧪 직접 해보기

1. `eval` 없이 옵션 배열로 `grep` 명령을 구성하세요.
2. 빈 대상 경로에서 반드시 실패하는 정리 함수를 작성하세요.
3. 실제 변경 없이 수행 내용을 출력하는 `--dry-run` 옵션을 구현하세요.

## ✅ 완료 기준

- 빈 경로와 하이픈 입력에서 안전하게 실패한다.
- 명령과 인수를 배열로 분리한다.
- 비밀정보가 로그와 명령행에 노출되지 않는다.
