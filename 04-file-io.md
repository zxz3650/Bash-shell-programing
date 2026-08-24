# 04. 파일 입출력과 권한

## 개요

경로, 파일 메타데이터, 권한과 안전한 파일명 처리를 학습합니다.

{% hint style="info" %}
## 🧭 학습 목표

- 절대 경로와 상대 경로를 구분한다.
- `mktemp`, `umask`, `find -print0`을 안전하게 사용한다.
- 공백·개행·하이픈이 포함된 파일명을 처리한다.
{% endhint %}

## 경로와 파일 확인

```bash
pwd
ls -la
file README.md
stat README.md
```

절대 경로는 `/`에서 시작하며, 상대 경로는 현재 디렉터리를 기준으로 합니다. 스크립트에서는 실행 위치와 스크립트 위치가 다를 수 있음을 기억해야 합니다.

```bash
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
printf '%s\n' "$script_dir"
```

## 안전한 실습 디렉터리

```bash
lab_dir=$(mktemp -d)
printf 'lab=%s\n' "$lab_dir"
touch -- "$lab_dir/file with spaces.log"
find "$lab_dir" -maxdepth 1 -type f -print
rm -r -- "$lab_dir"
```

`--`는 뒤에 오는 값을 옵션이 아닌 피연산자로 취급하도록 돕습니다. `-report.log`처럼 하이픈으로 시작하는 파일명을 처리할 때 중요합니다.

## 권한 이해

```bash
ls -l README.md
chmod u+x script.sh
umask
id
```

권한은 소유자(user), 그룹(group), 기타 사용자(other)의 읽기·쓰기·실행 비트로 구성됩니다. 수집 결과에 민감정보가 포함될 수 있다면 기본 권한을 제한합니다.

```bash
umask 077
report=$(mktemp)
printf 'private report\n' >"$report"
ls -l "$report"
```

## NUL 구분 파일 처리

파일명에는 공백과 개행이 포함될 수 있습니다. 안전하게 순회하려면 NUL 문자를 사용합니다.

```bash
find . -type f -name '*.log' -print0 |
    while IFS= read -r -d '' file; do
        printf '%q\n' "$file"
    done
```

## 🧪 직접 해보기

1. 공백과 하이픈으로 시작하는 파일명을 만들어 안전하게 출력하세요.
2. 소유자만 읽고 쓸 수 있는 임시 보고서를 만드세요.
3. `find` 결과를 `for file in $(find ...)`로 처리하면 왜 위험한지 설명하세요.

## ✅ 완료 기준

- 민감한 결과 파일의 기본 권한을 제한한다.
- 파일 경계를 손상하지 않고 검색 결과를 순회한다.
