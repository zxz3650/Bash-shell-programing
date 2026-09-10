# 02-2. 원본·해시·시간대를 보존하는 분석 준비

## 보안 질문과 목표

“이 결과는 어느 자료에서 나왔으며 분석 도중 바뀌지 않았는가?” Live Response와 Offline Analysis를 구분하고, 원본·작업 사본·결과를 분리합니다. 증거 관리의 입문 실습이며 조직의 포렌식 취급 절차를 대체하지 않습니다.

## 수집 시 남길 정보

| 항목 | 교육용 예 | 이유 |
|---|---|---|
| 사건 ID·출처 | COURSE-IR-002 / synthetic | 실제 증거와 합성 자료 구분 |
| 호스트·원본 경로·범위 | lab-web-01 / selected records | 누락 범위 명시 |
| 수집자·도구·버전 | course-author | 재현·인계 |
| 시작·종료·시간대 | 09:00~10:00 +09:00 | 타임라인 비교 |
| 파일별 크기·SHA-256 | 실제 계산 | 전달·분석 중 변경 확인 |
| 권한·실패·누락 | audit coverage partial | 0건과 미수집 구분 |

## 해시의 의미

Ubuntu에서 저장소 루트 기준으로 실행합니다.

```bash
sha256sum examples/security-labs/data/provenance.txt
```

출력은 `64자리 16진수  파일명`입니다. 실제 값을 직접 계산하고 사본과 비교합니다. 같으면 그 비교 시점의 바이트 내용이 같다는 근거입니다. 원래 경로·소유자·수집 전 변조·작성자의 정당성을 증명하지는 않습니다. 해시 목록의 보관과 출처도 기록해야 합니다.

macOS는 `shasum -a 256` 또는 노트북의 hashlib을 사용합니다. 실제 수집에서 단순 cp는 메타데이터 보존·포렌식 이미징의 대체 수단이 아닙니다.

## 라이브 조회와 오프라인 분석

라이브 조회는 휘발성 프로세스·소켓을 볼 수 있지만 조사 행위 자체가 상태에 영향을 줍니다. 파일 읽기는 마운트 정책에 따라 atime에 영향을 주고 명령 실행이 Audit에 기록될 수 있습니다. 오프라인 분석은 수집 사본의 시점과 범위만 해석합니다. 읽기 전용 마운트·작업 사본·접근 기록을 구분합니다.

사본이 읽기 전용이어도 안전한 내용이라는 뜻은 아닙니다. 의심 파일은 실행하지 않고 불필요한 미리보기도 피합니다. 공격자에 의한 삭제·변조 가능성과 정상 회전·보존 정책에 의한 누락을 모두 검토합니다.

## 시간대 실수

```text
원본 UTC: 2026-09-10T00:00:00Z
분석 KST: 2026-09-10T09:00:00+09:00
```

같은 순간입니다. `00:00:00Z`를 `00:00:00+09:00`으로 접미사만 바꾸면 9시간 다른 순간이 됩니다. 연도·시간대가 없는 syslog는 호스트 설정·수집 기간·시계 오차를 확인하고 추정값을 명시합니다.

### Bash Point — 읽기와 쓰기

```bash
cat "$COURSE_DATA/provenance.txt"
printf 'analysis_status=needs_more_evidence\n' > "$COURSE_OUT/analysis.txt"
```

`>`는 명령 실행 전에 파일을 열고 기존 내용을 비울 수 있습니다. 입력과 출력 경로를 동일하게 지정하지 않습니다. 변수를 인용해 공백 경로를 한 인수로 유지합니다.

## 실습과 예상 결과

[실행 안내](../examples/security-labs/README.md)에 따라 ch02.sh를 실행합니다. 출처 확인 → 사본 비교 → 별도 결과 → 누락 확인 순서입니다.

```text
source_type=synthetic
source_timezone=Asia/Seoul
audit_coverage=partial
copy_matches=yes
original_and_analysis=separate
not-collected=unavailable, not zero events
```

## 질문과 완료 기준

해시가 같아도 진짜 사건 당시 원본이라고 단정할 수 없는 이유, 누락을 0건으로 취급하면 안 되는 이유, KST 변환과 접미사 변경의 차이를 설명합니다. 원본 경로에 리다이렉션하지 않았고 실행 전후 내용 검사가 통과하면 완료입니다.

다음은 [노트북 실행](02-3-notebook-workflow.md)입니다.

## 참고 자료

- [NIST SP 800-86](https://csrc.nist.gov/pubs/sp/800/86/final)
- [GNU SHA-2 utilities](https://www.gnu.org/software/coreutils/manual/html_node/sha2-utilities.html)
