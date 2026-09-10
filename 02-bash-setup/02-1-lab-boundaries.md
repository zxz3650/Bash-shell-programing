# 02-1. 조사 환경과 실습 범위 정하기

## 개요와 목표

“명령이 실행된다”와 “조사 결과가 믿을 만하다”는 다릅니다. 컨테이너에서 보이는 PID·네트워크·사용자는 호스트 전체와 다를 수 있습니다. 01장의 관찰 범위를 복습하고, 조사 대상·실행 환경·수집 권한을 구분합니다.

## 환경 선택

| 환경 | 적합한 과제 | 해석의 한계 |
|---|---|---|
| Ubuntu VM | 프로세스·systemd·로그 관찰 | 기본 이미지에 로그·auditd가 없을 수 있음 |
| WSL2 Ubuntu | Bash·GNU 도구·파일 분석 | 서비스·부팅 기록이 일반 서버와 다를 수 있음 |
| 컨테이너 | 고정 자료 처리·테스트 | 네임스페이스·최소 도구·Journal 부재 |
| macOS | 공통 Bash·오프라인 분석 | BSD 옵션, /proc·systemd 부재 |
| Jupyter/Colab | 단계별 실습·결과 검사 | 커널의 환경이며 조사 대상 서버가 아님 |

기준은 별도 Ubuntu VM과 일반 사용자입니다. 스냅샷은 실습 복구용이며 증거 출처·해시·인계 기록을 대체하지 않습니다. 개인 인증정보나 운영 증거를 실습 VM·온라인 노트북에 넣지 않습니다.

## 준비 확인

설치는 [02장](../02-bash-setup.md)을 참고합니다. 아래는 변경 없는 확인입니다.

```bash
command -v bash python3 ps date
bash --version
TZ=Asia/Seoul date '+%Y-%m-%dT%H:%M:%S%z'
```

교육용 출력 일부:

```text
/usr/bin/bash
/usr/bin/python3
/usr/bin/ps
/usr/bin/date
GNU bash, version 5.2...
2026-09-10T09:00:00+0900
```

경로·버전은 실제 환경을 기록합니다. 설치 경로를 찾았다는 사실은 실행 파일의 무결성을 검증한 것이 아닙니다. 의심 시스템의 명령 결과를 무조건 신뢰하지 말고 신뢰 가능한 수집 도구와 오프라인 분석을 검토합니다.

### Bash Point — 명령별 환경 변수

`TZ=Asia/Seoul date ...`는 date의 표시 시간대를 지정합니다. `export TZ=Asia/Seoul`은 이후 자식에게도 전달합니다. 원본 로그나 시스템 시계는 바뀌지 않습니다. +0900이 아니면 tzdata 설치 여부를 확인합니다.

## Red / Blue 관점과 흔적

공격자는 사용 가능한 환경을 파악하려 하고 분석가는 관찰 범위를 입증해야 합니다. 이 수업에서는 공격 실행 대신 범위 오인으로 생기는 판단 오류를 검토합니다. 프로세스가 몇 개만 보인다고 서버 전체가 조용하다고 단정하지 않습니다. 컨테이너·권한·시각 차이를 확인합니다.

정상 조사 명령도 프로세스·접근·감사 흔적을 남길 수 있습니다. 조사 시작·종료 시각과 사용 명령을 기록해 사건 행위와 분석가 행위를 구분합니다. 기록 여부는 감사 설정과 수집 범위에 달려 있습니다.

## 실패 사례와 수정

| 오해 | 원인 | 수정 |
|---|---|---|
| venv가 시스템을 격리한다 | Python 패키지 환경일 뿐 | VM·접근 범위와 구분 |
| systemctl 오류는 침해다 | PID 1이 systemd가 아닐 수 있음 | 실행 환경 확인 |
| 거부되면 sudo로 재실행 | 수집 범위를 임의 확대 | 승인·필요 권한 확인 |
| 명령이 없으면 0건 | 조회하지 못함 | unavailable로 기록 |

## 실습·분석 질문·완료 기준

OS, Bash 경로·버전, VM/컨테이너 여부, 실행 사용자, KST 표시를 제출합니다. `/proc`, Journal, Audit 중 무엇을 사용할 수 있는지 적고, **설치됨 / 실행 가능 / 접근 허용 / 자료 존재**가 다른 조건인 이유를 설명합니다. 운영 증거 원본에 도구를 설치하지 않습니다.

관찰하지 못한 범위까지 명시하면 완료입니다. 다음은 [증거와 시간대](02-2-evidence-time.md)입니다.

## 참고 자료

- [Microsoft WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Python venv](https://docs.python.org/3/library/venv.html)
- [GNU date](https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html)
