# 06. 호스트·프로세스·네트워크 조사

## 보안 질문에서 시작하기

[호스트·프로세스·서비스](06-system-inspection/06-3-host-process-investigation.md)를 먼저 연결하고 [네트워크 상태](06-system-inspection/06-4-network-investigation.md)를 해석합니다. 필수 실습은 합성 스냅샷이며, 아래 라이브 조회는 승인된 자기 환경에서만 수행합니다. 조회를 실행하지 않은 범위도 기록합니다.

## 개요

프로세스 계보, `/proc`, 백그라운드 작업, 시그널과 로컬 네트워크 상태를 읽기 전용으로 조사합니다.

## 학습 순서

1. [06-1. 프로세스와 로컬 시스템 상태](06-system-inspection/06-1-processes-observation.md)
2. [06-2. 백그라운드 작업·시그널·정리](06-system-inspection/06-2-jobs-signals.md)

03장의 종료 상태와 04장의 임시 자원 처리를 연결합니다. 시작 성공과 완료 성공의 차이, PID 재사용, trap이 실행되지 않는 종료 상황을 먼저 생각합니다. [노트북 06](jupyter-book/labs/06-system-inspection-secure-scripting.ipynb)으로 로컬 상태를 읽습니다. 아래 /proc·ss·ip·ps --sort 예제는 Linux 전용이며 macOS 대안은 상세 절에서 설명합니다.

{% hint style="info" %}
## 🧭 학습 목표

- PID·PPID·사용자·시작 시각·명령행을 함께 수집한다.
- 백그라운드 프로세스의 종료 상태를 회수한다.
- `trap`으로 인터럽트 시 임시 자원을 정리한다.
{% endhint %}

## 프로세스 조사

```bash
ps -ef
ps -eo pid,ppid,user,lstart,comm,args --sort=ppid
pgrep -a ssh
```

조사 시에는 PID뿐 아니라 PPID, 사용자, 시작 시간과 전체 인수를 함께 기록합니다. 명령행에는 민감정보가 포함될 수 있으므로 보고서 공유 범위를 제한합니다.

Linux에서는 `/proc`에서 실행 파일과 열린 파일 등의 정보를 확인할 수 있습니다.

```bash
pid=$$
readlink -f "/proc/$pid/exe"
tr '\0' ' ' <"/proc/$pid/cmdline"
printf '\n'
```

## 백그라운드 작업

```bash
sleep 1 &
task_pid=$!
printf 'pid=%s\n' "$task_pid"
wait "$task_pid"
status=$?
```

`$!`는 가장 최근 백그라운드 프로세스의 PID입니다. `wait`로 종료를 회수하지 않으면 결과와 실패를 놓치기 쉽습니다.

## 시그널과 정리

```bash
#!/usr/bin/env bash

work_dir=$(mktemp -d)

cleanup() {
    rm -rf -- "$work_dir"
}

trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
```

`trap`을 사용하면 정상 종료와 오류, 인터럽트 상황에서 임시 파일과 디렉터리를 정리할 수 있습니다. 생성한 경로를 기록해 두고, 삭제 전에 변수가 비어 있지 않은지와 정확한 실습 경로인지 확인합니다.

## 네트워크 상태 확인

```bash
ss -lntup
ip address show
ip route show
```

이 명령들은 로컬 상태 확인용입니다. 외부 시스템을 대상으로 한 연결이나 스캔은 소유자 승인이 있을 때만 수행합니다.

## 🧪 직접 해보기

1. 현재 셸의 부모 프로세스 트리를 조사하세요.
2. 두 개의 백그라운드 작업을 실행하고 각각의 종료 상태를 수집하세요.
3. Ctrl+C를 눌러도 임시 디렉터리가 남지 않는 스크립트를 작성하세요.

## ✅ 완료 기준

- 프로세스와 부모 프로세스의 관계를 설명한다.
- 읽기 전용 시스템 스냅샷을 제한된 권한으로 저장한다.
