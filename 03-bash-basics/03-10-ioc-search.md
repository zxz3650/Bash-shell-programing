# 03-10. IOC 검색으로 배우는 인수·인용·조건·반복

터미널 예제는 [공통 실습 준비](../examples/security-labs/README.md)를 먼저 수행합니다. 노트북은 Setup부터 실행합니다.

## 개요와 목표

분석가가 받은 표식을 로그에서 찾습니다. 표식은 조사 단서이지 악성 판정 자체가 아닙니다. 원본 자료·검색 방식·결과 없음·실행 오류를 구분하면서 변수, 인용, 위치 인수, getopts, 조건, while, 함수를 배웁니다. 01장의 종료 상태와 02장의 원본 분리가 선수지식입니다.

## 필요한 정보

검색 입력은 로그 사본 한 개, 표식은 문자열 한 개입니다. 이 실습의 src 필드는 교육용 형식이며 모든 인증 로그의 두 번째 필드가 주소라는 뜻이 아닙니다. 명령은 데이터를 읽을 뿐 표식 주소에 접속하지 않습니다.

```bash
grep -F '192.0.2.10' "$COURSE_DATA/ioc.log"
```

출력에는 `.10`과 `.100` 두 행이 있습니다. `-F`는 정규식 해석을 끄지만 **부분 문자열 검색**입니다. 정확한 IP 필드 비교가 필요하면 자료 형식을 먼저 확인해야 합니다.

```bash
awk '$2 == "src=192.0.2.10" {print}' "$COURSE_DATA/ioc.log"
```

```text
2026-09-10T09:01:00+09:00 src=192.0.2.10 action=failed
```

이 비교는 제공 형식에만 맞습니다. JSON·인용된 필드·IPv6가 있으면 해당 형식의 파서를 사용합니다. 주소 단독 출현은 성공한 접속이나 동일 행위자를 입증하지 않습니다.

## Bash Point — 인용과 정규식

`indicator.example`의 점은 정규식에서 임의 문자 하나입니다. `grep 'indicator.example'`은 `indicatorXexample`도 찾습니다. `grep -F -- "$indicator" "$input_file"`은 표식을 고정 문자열로 전달하고, `--`는 하이픈으로 시작하는 표식이 옵션이 되는 일을 막습니다.

따옴표는 셸의 단어 분리·파일명 확장을 막습니다. grep의 정규식 의미를 바꾸는 것은 -F입니다. 두 문제는 별개입니다. glob은 파일명 패턴이고 regex는 선택한 도구의 문자열 패턴이므로 혼동하지 않습니다.

## CLI로 발전시키기

저장소 루트에서 제공 도구를 실행합니다.

```bash
bash examples/security-labs/ioc-search.sh \
  -f examples/security-labs/data/ioc.log -i 'indicator.example'
```

```text
3:2026-09-10T09:03:00+09:00 note=indicator.example
```

| 상태 | 뜻 | 다음 판단 |
|---|---|---|
| 0 | 한 행 이상 일치 | 원문과 문맥 확인 |
| 1 | 일치 없음 | 수집 범위·형식·기간 검토 |
| 2 | 인수·읽기 오류 | 분석 결과로 사용하지 않음 |

getopts가 -f와 -i를 읽고 OPTARG에서 값을 받습니다. `$#`는 남은 인수 수, `$@`는 각 인수, `$0`는 실행 이름입니다. `shift "$((OPTIND - 1))"` 뒤 남은 인수를 거부합니다. 중복 옵션·빈 문자열·여러 줄 표식도 거부합니다. 파일 내용은 source/eval로 실행하지 않습니다.

## 실패 사례

```bash
# 잘못된 예: 공백·확장이 인수 경계를 바꿈
grep $indicator $input_file
```

예를 들어 공백 파일명이 여러 파일로 분리되면 일부 오류와 일부 결과가 섞일 수 있습니다. 수정은 인용과 -F·--이며, 읽기 중 오류가 발생할 가능성도 있으므로 비정상 종료 때 부분 stdout을 완성 결과로 취급하지 않습니다. 인용만으로 심볼릭 링크·동시 변경·접근 권한 문제까지 해결되지는 않습니다.

## 반복과 분기

`while IFS= read -r indicator`는 한 줄을 읽고 백슬래시와 선행 공백을 보존합니다. `for indicator in $(cat list)`는 공백으로 단어를 쪼개므로 부적합합니다. 표식마다 grep 상태를 즉시 보존하고 case로 일치·없음·오류를 나눕니다. 마지막 줄에 개행이 없는 자료는 별도 처리하거나 입력 형식에서 개행을 요구해야 합니다.

## Red / Blue 관점

공격자는 계정·호스트·환경의 의미 있는 문자열을 찾으려 할 수 있습니다. 방어자는 흔적의 문맥과 일관성을 확인합니다. 같은 문자열의 존재만으로 행위 목적을 알 수 없습니다. 자료 접근 자체가 감사 기록에 남을 수 있으므로 조사 기록을 남기고 수집 사본을 사용합니다. 검색어에 비밀정보를 넣으면 명령행이나 노트북 출력으로 노출될 수 있습니다.

## 실습·출력·완료 기준

[실행 안내](../examples/security-labs/README.md)의 ch03.sh를 실행합니다.

```text
literal=1 regex=2
substring=2 exact_field=1
no_match_status=1
found=indicator.example
not_found=absent-marker
```

문자열 검색과 의미적 필드 비교의 차이, 상태 1과 2의 차이, 따옴표와 -F의 차이를 설명합니다. 정답 건수뿐 아니라 원본 행 번호와 시간대를 근거로 제시하면 완료입니다. 다음 04장은 이 원칙을 파일명과 파일 내용 조사에 적용합니다.

## 참고 자료

- [GNU grep](https://www.gnu.org/software/grep/manual/grep.html)
- [Bash getopts](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html)
- [ShellCheck SC2086](https://www.shellcheck.net/wiki/SC2086)
