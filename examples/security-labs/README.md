# Linux 보안 분석 실습 자료

`data/`의 모든 자료는 교육용 합성 자료입니다. 실제 사건 증거·인증정보가 아니며 문서용 IP는 접속 대상이 아닙니다. 필수 실습은 오프라인 분석으로 진행하고, 실제 Journal·Audit·wtmp를 읽는 선택 Ubuntu VM 조사는 교안에서 따로 구분합니다.

## 실행

저장소 루트의 Bash 터미널에서 실행합니다. `02`를 해당 장 번호로 바꿉니다.

```bash
export COURSE_DATA="$PWD/examples/security-labs/data"
export COURSE_OUT="$(mktemp -d)"
bash examples/security-labs/ch02.sh
```

입력은 COURSE_DATA, 결과는 매 실행마다 새로 만든 COURSE_OUT입니다. 원본을 편집하거나 같은 결과 폴더를 재사용하지 않습니다. 임시 폴더는 OS 샌드박스가 아니므로 코드를 먼저 읽습니다. Bash 3.2 이상, 일반 텍스트 도구, Python 3이 기준이며 Linux 전용 조회는 본문에서 표시합니다.

각 STEP은 예상 결과를 검사합니다. 테스트와 노트북은 실행 전후 입력 내용의 해시도 비교합니다. 내용이 같다는 것이 읽기로 인한 atime 변화나 실행 흔적까지 없다는 뜻은 아닙니다. 결과는 검토를 위해 임시 폴더에 남지만 장기 보존은 보장되지 않습니다.

시스템 전체 수집, 외부 접속, 의심 파일 실행, 권한 변경, 서비스 등록은 자동 수행하지 않습니다. 운영 환경 수집·조치는 승인과 영향 평가가 먼저입니다.

## 검증

```bash
bash tests/test-security-labs.sh
```

자동 채점은 합성 자료의 계산 결과만 검증합니다. 침해 여부나 행위자의 의도를 확정하지 않습니다. 각 장의 질문에 정상 관리 작업, 누락 자료, 추가 확인을 설명해야 합니다.

## Red Team·Blue Team과 GTFOBins 연결

03장부터 12장까지의 주요 보안 절과 노트북에서 같은 관찰을 목적·전제·흔적·로깅 조건·조사·탐지·완화로 설명합니다. 서술 과제는 자동 계산 검사와 별도로 평가합니다.

07장의 tool-review.psv는 별도 가상 검토 카드입니다. reference_listed는 GTFOBins 등재를 가정한 교육 필드이며 실제 목록을 내려받거나 시스템 바이너리에 대조하지 않습니다. scope_fit는 제공된 설정 검토 요약이고 telemetry는 실행 자료 제공 여부입니다. 자동화가 정책을 해석해 취약점을 판정하는 자료가 아닙니다. 12장의 사건 증거·고정 수집 12항목과도 구분합니다.

ch07.sh는 카드의 형식과 허용값을 확인한 뒤 aligned=2/review=1/unknown=1, telemetry_present=2/telemetry_not_collected=2를 각각 출력합니다. 목록 등재와 위험 판정을 혼동하지 않는지는 [07-4 분석 질문](../../07-secure-scripting/07-4-gtfobins-review.md)으로 평가합니다.
