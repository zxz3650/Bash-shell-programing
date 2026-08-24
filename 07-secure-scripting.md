# 07. 안전한 Shell Script

## 개요

신뢰할 수 없는 입력, 옵션 주입, 임시 파일, 비밀정보와 destructive 작업을 안전하게 처리합니다.

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

가능한 값이 정해져 있다면 denylist보다 allowlist를 사용합니다. 검증된 데이터도 항상 인용하고 옵션 앞에는 `--`를 사용합니다.

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
