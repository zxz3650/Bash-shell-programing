# 02. 개발 및 실습 환경

## 개요

Windows WSL 2 또는 Linux에 Bash 실습 환경을 구성하고 명령 탐색, shebang, 종료 상태와 도움말 사용법을 익힙니다.

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

Bash는 명령을 alias, function, builtin, 실행 파일 등의 순서로 탐색합니다.

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
printf 'time=%s\n' "$(date -Is)"
```

```bash
chmod +x system_info.sh
./system_info.sh
echo "$?"
```

첫 줄은 shebang이며 사용할 인터프리터를 지정합니다. 종료 상태 `0`은 일반적으로 성공, 그 외 값은 실패를 뜻합니다.

## 도움말을 찾는 순서

```bash
help printf        # Bash builtin
man find           # 외부 명령 매뉴얼
find --help        # 짧은 옵션 요약
type -a command    # 명령의 정체 확인
```

## 🧪 직접 해보기

1. 현재 Bash의 PID와 부모 PID를 출력해 보세요.
2. `cd`, `test`, `grep`이 builtin인지 외부 명령인지 확인하세요.
3. 존재하지 않는 명령의 종료 상태를 확인하세요.

## ✅ 완료 기준

- `bash --version`, `command -v`, `type`을 사용할 수 있다.
- 실행 권한과 shebang의 역할을 설명할 수 있다.
