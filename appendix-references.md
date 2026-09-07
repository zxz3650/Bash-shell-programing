# 부록. 용어·공식 자료·호환성

## 용어 확인

| 용어 | 이 교안에서의 의미 |
|---|---|
| Shell Programming | 셸 명령 언어로 작업을 자동화하는 활동 |
| Bash | 명령 언어를 해석하는 GNU 셸 프로그램과 그 확장 문법 |
| Terminal | 입력·화면과 셸을 연결하는 프로그램 |
| argv | 프로그램에 전달한 인수 목록 |
| exit status | 명령의 정수 종료 상태 |
| stdout/stderr | 결과·진단을 전달하는 별도 스트림 |
| quoting | 확장과 인수 경계를 제어하는 인용 |
| glob | 파일명·문자열 패턴 확장 |
| subshell | 부모와 분리된 셸 실행 환경 |
| idempotency | 같은 요청을 반복해도 추가 효과가 달라지지 않는 성질 |
| atomic publication | 다른 프로그램이 작성 중인 파일을 읽지 않도록, 완성된 결과만 최종 경로에서 읽을 수 있게 하는 방식 |

## 플랫폼 표

| 기능 | 기본 지원 | 수업 적용 |
|---|---|---|
| 인덱스 배열·[[ ]]·프로세스 치환 | Bash 3.2 이상 | 공통 문법 |
| 연관 배열 | Bash 4 이상 | 버전 표시 후 선택 실습 |
| wait -n | Bash 4.3 이상 | 기본 예제는 배치 wait 사용 |
| /proc·ip·ss·flock | Linux 중심 | Linux 전용 표시 |
| stat -c·date -Is·sort -z | GNU 도구 계열 | macOS 기본 도구와 차이 확인 |
| jq·ShellCheck·shfmt·Bats | 별도 도구 | 설치 여부 기록 |

macOS의 /bin/sh가 Bash 확장을 일부 허용하더라도 POSIX sh 스크립트의 이식성을 의미하지 않는다. GNU/Linux의 작은 컨테이너도 Bash·도구가 모두 설치되어 있다고 가정하지 않는다.

## 공식 자료

- [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html): 실행 모델·변수·확장·조건·함수·작업 제어
- [GNU Shell Expansions](https://www.gnu.org/software/bash/manual/html_node/Shell-Expansions.html): 확장 순서
- [GNU The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html): errexit·nounset·pipefail
- [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html): 이식 가능한 셸 명령 언어
- [GNU Coreutils](https://www.gnu.org/software/coreutils/manual/coreutils.html): 파일·정렬·해시·상태 도구
- [GNU Findutils](https://www.gnu.org/software/findutils/manual/html_mono/find.html): find·xargs와 파일명 전달
- [GNU Grep](https://www.gnu.org/software/grep/manual/grep.html): 검색·정규식·상태
- [GNU Awk](https://www.gnu.org/software/gawk/manual/gawk.html): 레코드·필드·집계
- [jq manual](https://jqlang.org/manual/): JSON 변환·검증
- [ShellCheck wiki](https://www.shellcheck.net/wiki/): 정적 분석 진단의 의미
- [shfmt](https://github.com/mvdan/sh): 셸 코드 서식
- [Bats documentation](https://bats-core.readthedocs.io/en/stable/): 동작 테스트
- [Microsoft WSL 설치](https://learn.microsoft.com/en-us/windows/wsl/install): Windows 실습 환경

## 도구 확인 명령

```bash
bash --version
command -v bash awk grep find sort jq shellcheck shfmt bats
uname -s
```

매뉴얼과 현재 도구가 다르면 설치 버전과 해당 플랫폼 매뉴얼을 확인한다. 이 교안의 예제는 명령을 직접 실행하여 동작을 이해하기 위한 것으로, 운영 배포의 모든 환경을 보장하는 구성은 아니다.
