# 로그 보고서 프로젝트

저장소 루트에서 아래 순서로 실행한다. Bash 3.2 이상, awk, mktemp, ln이 필요하며 Linux/macOS의 로컬 파일시스템을 대상으로 한다. awk 진단은 /dev/stderr를 사용한다.

```bash
lab_dir=$(mktemp -d)
bash examples/log-report/bin/log-report.sh \
    --input examples/log-report/fixtures/events.log \
    --output "$lab_dir/report.tsv" --dry-run
bash examples/log-report/bin/log-report.sh \
    --input examples/log-report/fixtures/events.log \
    --output "$lab_dir/report.tsv"
diff -u examples/log-report/fixtures/expected.tsv "$lab_dir/report.tsv"
bash tests/test-course.sh
```

입력 계약: 한 행에 LEVEL SERVICE 두 필드. LEVEL은 INFO/WARN/ERROR, SERVICE는 영문자·숫자·밑줄·점·하이픈이다. 공백으로 필드를 구분하며 빈 행과 잘못된 행은 거부한다. 빈 파일은 유효하며 모든 집계가 0이다.

출력 계약: 헤더와 INFO/WARN/ERROR 순서의 TSV. 상태 0은 성공, 2는 사용 오류, 1은 입력·출력·실행 오류다. 정상 실행의 진행 메시지는 stderr, 결과 데이터는 출력 파일이다. dry-run의 계획은 stdout이다.

기존 결과와 깨진 심볼릭 링크는 덮어쓰지 않는다. 같은 디렉터리의 임시 파일에 검증된 결과를 쓴 뒤 하드 링크로 새 이름을 게시하여 검사 후 충돌에도 기존 파일을 덮지 않는다. 하드 링크 미지원 파일시스템은 실패한다. 악의적으로 교체되는 공유 디렉터리나 전원 장애의 내구성을 보장하는 도구는 아니다.

학생은 먼저 [12-1 교안](../../12-capstone/12-1-log-report-project.md)의 요구사항과 검증표로 구현하고 이 코드를 비교용 해설로 사용한다.
