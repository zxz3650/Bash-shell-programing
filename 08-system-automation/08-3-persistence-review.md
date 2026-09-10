# 08-3. 자동 시작·예약·SSH 설정에서 지속성 흔적 조사하기

합성 자료 예제는 [공통 실습 준비](../examples/security-labs/README.md)를 먼저 수행합니다. 설정 내용은 실행하거나 설치하지 않습니다.

## 보안 질문과 목표

“재부팅·로그인·예약 시점에 실행되는 동작이 승인된 것인가?” 자동화 기능은 정상 운영과 지속성 악용 모두에 쓰일 수 있습니다. 등록 방법이나 악성 동작을 실습하는 대신 설정 사본·파일 변경·실행 기록·승인 이력을 연결합니다. 06장의 서비스, 07장의 변경 권한이 선수지식입니다.

## 조사 위치와 작동 조건

| 영역 | 검토할 자료 | 중요한 차이 |
|---|---|---|
| cron | 시스템 crontab·cron.d·사용자 crontab | 시스템 형식과 사용자 형식의 사용자 필드 차이 |
| systemd | system/user unit·timer·drop-in | 본 파일만 읽으면 override를 놓침 |
| rc.local·startup | 호환 서비스·실제 참조 여부 | 파일 존재만으로 부팅 실행 보장 못 함 |
| Bash 시작 파일 | .bashrc·.bash_profile·.profile | 로그인/비로그인·대화형 여부 |
| SSH | authorized_keys·sshd 설정·변경 이력 | 키 파일 경로·옵션·인증 방식이 다를 수 있음 |
| 동적 링커 | preload 관련 설정·라이브러리 기준선 | 설정 흔적과 실제 로드 상태 구분 |
| 커널 모듈 | 부팅 설정·모듈 목록·서명·패키지 | 로드된 모듈이 모두 악성인 것은 아님 |

이 표는 조사 범위 목록입니다. 악성 키·unit·시작 스크립트를 만들거나 설치하지 않습니다. 경로만 검사하는 자동화는 사용자별 설정·별도 마운트·컨테이너·정책 예외를 놓칠 수 있습니다.

## 설정을 실행하지 않고 읽기

합성 자료에서 필요한 필드를 선택합니다.

```bash
grep -E '^(User|ExecStart|DropInPaths|change_ticket)=' "$COURSE_DATA/service-review.txt"
```

```text
User=collector
ExecStart=/opt/collector/bin/report
DropInPaths=not_collected
change_ticket=unknown
```

서비스 실행 계정은 collector이고 실행 경로는 /opt 아래입니다. drop-in은 수집되지 않았고 승인 이력이 확인되지 않았습니다. unknown을 비인가 확정으로 바꾸지 않습니다. 07장의 파일 권한 목록과 비교하면 collector 그룹 쓰기 가능 설정을 검토할 이유가 생기지만, 서비스 설정 전체와 업무 기준선이 필요합니다.

## 선택 Ubuntu VM 조회

다음은 존재하는 ssh 서비스의 설정과 timer 목록을 읽는 예입니다. 실제 unit 이름을 확인합니다.

```bash
systemctl cat ssh.service
systemctl show ssh.service -p FragmentPath -p DropInPaths -p User -p ExecStart
systemctl list-timers --all --no-pager
crontab -l
```

crontab -l은 현재 사용자 범위입니다. “no crontab”과 접근 오류는 구분합니다. 이 명령으로 다른 모든 사용자의 예약 작업까지 조사했다고 보고하지 않습니다. systemctl cat은 파일을 보여줄 뿐 현재 메모리의 적용 상태·과거 실행을 모두 증명하지 않습니다. 서비스 시작·활성화·reload 명령은 이 실습에 없습니다.

## Shell 시작 파일 주의

`.bashrc`를 source로 읽으면 내용이 실행됩니다. 의심 사본은 cat·sed 등으로 데이터로 검토하고, 실제 로딩 조건과 참조 경로를 확인합니다. 비로그인 대화형 Bash와 로그인 Bash가 같은 시작 파일을 항상 읽는 것은 아닙니다. 적용 여부는 셸 종류·실행 옵션·호출 환경도 고려합니다.

SSH 키 파일도 원문 전체를 공개 보고서에 복사하지 않습니다. 키 소유자·승인·추가 시각·인증 성공 기록을 비교하고 지문 등 필요한 식별정보만 제한적으로 공유합니다. 공개키 파일 수정이 실제 인증 성공을 증명하지는 않습니다.

### Bash Point — 설정은 코드가 아니라 분석 입력

`grep -E '^(User|ExecStart)='`는 줄 시작과 선택 필드를 표현하는 정규식입니다. `source service-review.txt`처럼 데이터를 실행하는 방식은 사용하지 않습니다. 결과 파일에는 관찰값과 승인 상태를 분리하여 기록합니다. 등록 자동화와 조사 자동화는 별개입니다.

## Attack → Artifact → Detection → Mitigation

자동 실행 유지라는 목적 → 설정/키/파일 변경 → 메타데이터·무결성 기준선·Audit → 서비스 실행 Journal·인증 로그 → 변경 요청과 비교 → 불필요한 변경 권한 제한·정상 구성 복원·키 수명 관리로 이어집니다. 먼저 삭제하면 변경 주체·실행 파일·후속 행위를 조사하기 어려워질 수 있습니다.

관련 ATT&CK는 [Cron T1053.003](https://attack.mitre.org/techniques/T1053/003/), [Systemd Service T1543.002](https://attack.mitre.org/techniques/T1543/002/), [Unix Shell Configuration Modification T1546.004](https://attack.mitre.org/techniques/T1546/004/), [SSH Authorized Keys T1098.004](https://attack.mitre.org/techniques/T1098/004/)입니다. 정상 기능 사용 자체에 공격 기법 판정을 붙이지 않습니다.

## 실습·예상 결과

ch08.sh는 승인 미확인 1개와 알려진 기준선/승인 기록 3개를 분리합니다.

```text
unknown_approval=1 known_records=3 installed_by_lab=0
```

## 분석 질문·완료 기준

unknown과 unauthorized의 차이, unit 파일과 실제 실행의 차이, drop-in 미수집의 영향, 정상 백업 cron을 오탐하지 않을 근거를 제출합니다. 추가 수집 요청에는 경로·기간·목적·민감정보를 적습니다. 어떤 지속성도 실제 설치하지 않고 자료 기반 검토를 완료하면 통과입니다.

## Red Team ↔ Blue Team 사례 분석

### 사례: 자동 시작 구성의 승인과 실행은 같은가

**Red Team 질문:** 재부팅·예약·로그인 시 실행되는 구성의 변경 권한이 적절히 제한되어 있는가? 지속성은 동작을 계속 실행시키려는 목적이며, cron이나 systemd가 설치되어 있다는 사실 자체가 약점은 아닙니다.

| 연결 단계 | 분석 내용 |
|---|---|
| Goal / Boundary | 자동 실행의 연속성에 영향을 줄 수 있는 설정·코드의 통제 권한 검토 |
| Command / Observation | grep으로 User·ExecStart·DropInPaths·change_ticket을 선택. 현재 drop-in 미수집·승인 미확인 |
| System Change / Artifact | unit·timer·crontab·시작 파일·키의 변경. 존재·활성화·실행은 각각 별도 사실 |
| Log prerequisite | 사전 파일 변경 감사·배포 이력, 서비스 Journal·인증 로그. 모든 시작 파일 읽기가 자동 기록되지는 않음 |
| Blue Team Investigation | 등록된 위치→실제 참조 구성→실행 계정→파일 변경 주체→동일 기간 실행 기록 비교 |
| Detection | 승인되지 않은 구성 변화와 후속 실행을 연결. 미수집을 비인가 확정으로 바꾸지 않음 |
| Mitigation | 구성·코드의 쓰기 권한 제한, 변경 승인, 키 관리. 보존 후 승인된 정상 구성으로 복구 |

**반례와 해설:** 정상 백업 cron도 반복 실행되고 모니터링 unit도 부팅 때 시작됩니다. 합성 collector는 실행 계정이 collector이므로 root 지속성이라고 쓸 수 없습니다. DropInPaths=not_collected이면 본 파일만 보고 최종 실행 옵션을 완전히 확인했다는 표현도 틀립니다.

### 조사 위치별 다음 질문

| 위치 | 추가 확인 | 방어 측 검증 |
|---|---|---|
| cron·timer | 어떤 사용자와 시간 조건인가? | 예약과 실제 실행·변경 승인을 비교 |
| Shell 시작 파일 | 어느 셸 모드에서 참조되는가? | source로 실행하지 않고 참조 관계·수집 범위 확인 |
| authorized_keys | 실제 설정의 키 경로와 승인 주체는? | 지문·변경 이력·인증 방식·성공 기록 비교 |
| 동적 링커 | 구성·라이브러리가 배포 기준선과 맞는가? | 파일 신원·변경 이력·수집된 로드 정보 구분 |
| 커널 모듈 | 배포 패키지·서명·허용 목록과 맞는가? | 현재 로드 정보와 부팅 기록 비교. 이름만으로 악성 판정하지 않음 |

**제출 과제:** 승인 미확인 1건에 대해 필요한 자료 두 개와 가능한 정상 사유를 적습니다. “지속성 설치 확인” 대신 현재 확인된 설정·실행·승인 상태를 각각 기술합니다. 실습에서 어떤 구성도 설치하지 않았음을 결과에 남깁니다.

## 참고 자료

- [systemd.service](https://man7.org/linux/man-pages/man5/systemd.service.5.html)
- [Bash startup files](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html)
- [OpenSSH sshd_config](https://man.openbsd.org/sshd_config)
