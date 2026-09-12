# 05. 파이프라인과 텍스트 처리

**[05장 학습용 노트북 ZIP 받기](https://github.com/zxz3650/Bash-shell-programing/raw/refs/heads/master/downloads/chapter-05.zip)** · [처음 실행하는 방법](PRACTICE.md) · [포함 노트북과 자료 버전](downloads/README.md)

압축을 푼 뒤 `START-HERE.md`의 순서대로 기본 실습부터 실행하고 보안 적용 실습으로 이어갑니다.

## 기본 학습과 보안 실습 연결

05-1부터 05-3까지 파이프라인·텍스트 도구·입력 형식을 학습한 뒤 [05-4. SSH 인증 로그 실습](05-text-processing/05-4-auth-pipeline.md)에 적용합니다. 원문→행 선택→주소→빈도의 각 단계가 배운 명령과 종료 상태에 어떻게 대응하는지 확인합니다.

## 개요

표준 스트림과 파이프라인으로 로그를 필터링·정규화·집계하고 JSON을 구조적으로 처리합니다.

## 학습 순서와 선행 지식

04장의 스트림·파일 보존을 바탕으로 단계별 입력 형식과 종료 상태를 검증합니다.

1. [05-1. 파이프라인과 grep](05-text-processing/05-1-pipelines-grep.md)
2. [05-2. awk·sed·정렬·집계](05-text-processing/05-2-awk-sed-aggregation.md)
3. [05-3. JSON의 구조와 입력 검증](05-text-processing/05-3-json-data-contracts.md)

학습 전 질문: 검색 결과가 없다는 것은 실행 오류인가? uniq 앞에 sort가 필요한 이유는 무엇인가? JSON을 cut으로 처리하면 어떤 입력에서 실패하는가? [노트북 05](jupyter-book/labs/05-text-processing.ipynb)의 고정 로그를 손으로 집계한 뒤 결과를 비교합니다. 아래 명령 조각의 auth.log·access.log 등은 해당 형식의 입력을 준비한 뒤 사용하는 복습 예제입니다.

{% hint style="info" %}
## 🧭 학습 목표

- stdout과 stderr를 분리한다.
- `pipefail`로 중간 단계 실패를 탐지한다.
- grep, awk, sed, sort, uniq와 jq의 역할을 구분한다.
{% endhint %}

## 표준 스트림

프로세스는 표준 입력(0), 표준 출력(1), 표준 오류(2)를 사용합니다.

```bash
command >output.txt
command 2>error.txt
command >all.txt 2>&1
command </path/to/input.txt
```

오류 메시지는 표준 오류로 보냅니다.

```bash
printf 'error: file not found: %s\n' "$file" >&2
exit 1
```

## 파이프라인

```bash
printf '%s\n' alpha beta alpha |
    sort |
    uniq -c |
    sort -nr
```

각 단계가 한 가지 작업만 담당하도록 구성합니다. 긴 파이프라인은 중간 결과를 확인할 수 있게 여러 줄로 작성합니다.

```bash
set -o pipefail
grep -F 'Failed password' auth.log | sort | uniq -c
status=$?
```

`pipefail`을 사용하지 않으면 앞 단계의 실패가 마지막 명령의 성공에 가려질 수 있습니다.

## 주요 텍스트 처리 도구

```bash
grep -nF -- 'Failed password' auth.log
awk '{print $1, $NF}' access.log
sed -n '1,20p' report.txt
cut -d: -f1 /etc/passwd
sort data.txt | uniq -c
jq -r '.events[] | [.time, .source] | @tsv' events.json
```

정규식이 필요하지 않다면 `grep -F`를 사용합니다. JSON은 정규식 대신 `jq`로 구조적으로 처리합니다.

## here-document

```bash
cat <<'REPORT'
Incident summary
$HOME is not expanded here.
REPORT
```

구분자를 작은따옴표로 감싸면 본문의 변수와 명령 치환이 실행되지 않습니다.

## 🧪 직접 해보기

1. 파일에서 중복된 IP를 빈도순으로 출력하세요.
2. 성공 결과와 오류를 서로 다른 파일에 저장하세요.
3. 파이프라인의 첫 명령이 실패하는 예를 만들고 `pipefail`의 차이를 확인하세요.

## ✅ 완료 기준

- 긴 파이프라인을 단계별로 설명하고 오류를 확인한다.
- JSON을 정규식이 아닌 `jq`로 처리한다.
