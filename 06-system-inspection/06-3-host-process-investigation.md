# 06-3. 호스트·프로세스·서비스를 연결해 조사하기

## 질문과 목표

“이 프로세스는 언제 누구의 권한으로 시작됐고 어떤 서비스와 관련이 있는가?” PID 하나가 아닌 호스트·부팅·시작 시각·부모·실행 파일·권한을 함께 봅니다. 01장의 자기 환경 관찰을 확장하되 필수 실습은 제공 스냅샷만 분석합니다.

## 호스트 정보의 목적

승인된 Ubuntu VM에서 다음을 조회할 수 있습니다. 아래 명령은 설치·업데이트를 하지 않습니다.

```bash
hostname
hostnamectl
uname -a
uname -r
cat /etc/os-release
```

| 출력 | 읽을 부분 | 주의 |
|---|---|---|
| hostname | 호스트 식별 표식 | 변경 가능, 유일한 증거 ID 아님 |
| hostnamectl | OS·커널·가상화 정보 | systemd 환경이 아닐 수 있음 |
| uname | 현재 실행 커널·아키텍처 | 배포판 패키지 패치 상태와 다름 |
| os-release | ID·VERSION_ID | 사용자 공간 배포판 정보 |

공격자는 환경과 보안 경계를 이해하려고 조사할 수 있습니다. 분석가는 수집 자료가 같은 시스템에서 나온 것인지, 적용해야 할 배포판 설명이 무엇인지 확인합니다. 오래된 버전 문자열만으로 취약점 존재를 확정하지 않고 벤더 보안 권고와 실제 패키지 상태를 비교합니다.

## 프로세스 목록

```bash
TZ=Asia/Seoul ps -eo pid,ppid,user,lstart,cmd
pgrep -a sshd
```

`ps aux`는 사용자·CPU·메모리·명령행, `ps -ef`는 UID·PID·PPID를 함께 보는 다른 출력 형식입니다. 같은 명령의 옵션 조합도 구현에 따라 달라지므로 GNU/Linux 기준과 macOS를 구분합니다. pgrep은 이름 선택 도구이며 이름을 신뢰성 있는 신원 증명으로 취급하지 않습니다.

교육용 자료의 한 행:

```text
520|1|collector|2026-09-10T09:05:00+09:00|/opt/collector/bin/report|report-helper.service
```

PID 520, PPID 1, collector 사용자, 09:05 시작, 지정 실행 경로와 서비스 문맥입니다. 부모 1은 서비스 또는 재부모화 등 여러 원인이 있으므로 악성이라는 뜻이 아닙니다. 명령행에는 비밀값이 들어갈 수 있어 수집·공유 범위를 제한합니다.

## /proc에서 확인할 것

아래는 Ubuntu VM에서 **자기 Bash**만 조회합니다.

```bash
pid=$$
readlink "/proc/$pid/exe"
tr '\0' '\n' < "/proc/$pid/cmdline"
ls -l "/proc/$pid/fd"
```

exe는 실행 파일 링크, cmdline은 NUL로 구분된 인수, fd는 열린 파일 디스크립터입니다. NUL을 줄바꿈으로 바꾼 화면은 원래 인수에 포함된 개행을 구분하지 못하므로 미리보기입니다. `/proc/PID/environ`에는 토큰 등이 있을 수 있어 기본 실습은 덤프하지 않습니다. 꼭 필요한 조사라면 승인·최소 수집·접근 제한이 먼저입니다.

접근 실패는 프로세스 종료·권한·hidepid·네임스페이스 제한 때문일 수 있습니다. `(deleted)` 실행 파일 표시는 업데이트 후 삭제된 구버전 파일에서도 나타날 수 있습니다. 위험 신호이지 악성 판결이 아닙니다.

## 서비스와 연결

Ubuntu systemd 환경의 조회 예입니다.

```bash
systemctl --type=service --state=running --no-pager
systemctl show ssh.service -p MainPID -p User -p FragmentPath
```

서비스 이름은 실제 환경에서 확인합니다. RHEL 계열은 sshd.service일 수 있습니다. 상태 running은 정당성·무결성 검증이 아닙니다. unit 파일·drop-in·실행 경로·계정·승인 변경 기록을 비교합니다. 08장에서 지속성 흔적 검토로 이어집니다.

### Bash Point — 연관 배열은 awk 안의 데이터 구조

실습에서 `exe[pid]`로 프로세스 경로를 기억한 뒤 소켓 자료와 연결합니다. 이것은 awk 배열이며 Bash 배열이 아닙니다. Bash는 두 입력 파일과 출력 경로를 전달합니다. 데이터 조인과 실행 조정의 역할을 구분합니다.

## 흔적·탐지·완화

환경 조사 → 프로세스 실행 가능 흔적 → Audit의 exec 기록(설정된 경우)·명령 실행 시각 → 계정·세션·부모와 비교합니다. 정상 관리 도구의 동일 명령을 오탐하지 않도록 승인 작업과 비교하고, 이상 프로세스는 증거 수집 전 무조건 종료하지 않습니다.

## 실습·완료 기준

ch06.sh에서 프로세스 4행과 소켓 3행을 읽고 PID 520을 collector/report-helper.service에 연결합니다. `.7:443` 연결을 보고 즉시 C2라고 표시하지 않습니다. 두 스냅샷의 수집 시차·PID 재사용 가능성, 목적지 승인 목록, 서비스 변경 이력을 추가 질문으로 제출합니다.

다음은 [네트워크 상태 해석](06-4-network-investigation.md)입니다.

## Red Team ↔ Blue Team 사례 분석

### 사례: 익숙한 서비스 이름이 신뢰의 근거인가

**Red Team 질문:** 프로세스·서비스 정보에서 권한 경계나 운영상의 노출을 이해할 수 있는가? 실행 이름이 아니라 사용자·실행 파일·설정 출처가 중요하며, 버전 정보만으로 취약점 악용 가능성을 확정하지 않습니다.

| 연결 단계 | 분석 내용 |
|---|---|
| Goal / Boundary | 환경과 실행 권한을 이해하려는 목적. 관찰 범위·네임스페이스·읽기 권한이 전제 |
| Command / Observation | ps·pgrep·/proc·systemctl 정보를 비교. 합성 PID 520은 collector로 09:05 시작 |
| System Change / Artifact | 프로세스 생성·부모 관계·실행 파일·FD. 종료된 프로세스는 현재 /proc에 없을 수 있음 |
| Log prerequisite | 사전 exec 감사/EDR와 서비스 Journal. 프로세스 스냅샷은 과거 실행 전부가 아님 |
| Blue Team Investigation | report-helper.service의 unit·drop-in·실행 경로·배포 이력을 PID와 비교 |
| Detection | 예상 사용자·실행 경로·부모·시간대에서 벗어난 조합을 검토. 이름만 차단하지 않음 |
| Mitigation | 서비스별 최소 권한·신뢰된 배포 경로·필요한 실행 기록. 중지 전 휘발성 근거와 영향 검토 |

**반례와 해설:** PPID 1은 정상 서비스에도 나타납니다. PID 520이라는 숫자는 다음 부팅에서 다른 프로세스가 재사용할 수 있습니다. 지금 실행 중인 파일의 해시와 과거 사건 시점 파일의 해시를 같은 사실로 취급하지 않습니다.

**제출 과제:** PID 520에 대해 사용자·시작 시각·실행 경로·서비스 네 필드를 제시합니다. Red Team은 추가 확인할 경계 하나, Blue Team은 필요한 자료 두 개를 적습니다. 프로세스 명령행 전체를 공개 보고서에 복사하기 전에 민감정보 검토 필요성도 설명합니다.

## 참고 자료

- [Linux /proc](https://www.kernel.org/doc/html/latest/filesystems/proc.html)
- [ps](https://man7.org/linux/man-pages/man1/ps.1.html)
- [systemctl](https://man7.org/linux/man-pages/man1/systemctl.1.html)
