# 04-4. 의심 파일 조사와 파일명·시간·해시 해석

터미널 예제는 [공통 실습 준비](../examples/security-labs/README.md)를 먼저 수행합니다. lab_tree·file_path는 자신이 만든 실습 트리와 파일을 지정합니다.

## 보안 질문과 목표

“최근 생긴 파일인가, 실행된 파일인가, 단지 이름이 이상한가?” 검색 조건·메타데이터·내용·실행 흔적을 구분합니다. find로 범위를 제한하고 stat·file·strings·sha256sum으로 관찰하되 의심 파일을 실행하지 않습니다. 02장의 증거 분리, 03장의 인용과 종료 상태가 선수지식입니다.

## 단계별 조사

| 질문 | 관찰 | 해석 한계 |
|---|---|---|
| 어디에 있는가 | 경로·파일시스템·소유자 | /tmp나 숨김 이름 자체는 악성 아님 |
| 무엇이 바뀌었는가 | mtime·ctime·크기·권한 | ctime은 생성 시각이 아님 |
| 어떤 형식인가 | file 결과·실제 바이트 | 확장자·형식 판정만으로 안전성 확정 불가 |
| 같은 내용인가 | SHA-256 | 소유권·수집 전 진실성까지 증명하지 않음 |
| 실행됐는가 | 프로세스·Audit·서비스·로그 | 파일 존재·실행 권한만으로 실행을 증명 못 함 |

## find의 범위를 먼저 정하기

다음은 **승인된 Ubuntu VM에서만 하는 선택 조회**입니다. 전체 `/` 대신 필요한 경로와 기간을 정합니다. stderr를 버리지 않고 수집 제한을 기록합니다.

```bash
find /tmp /var/tmp -xdev -type f -mtime -1
```

`-mtime -1`은 조회 시점 기준 24시간 단위의 파일 내용 변경 시간 조건입니다. “오늘 자정 이후 생성”이 아닙니다. `-xdev`는 시작점의 파일시스템을 벗어나지 않으므로 별도 마운트는 누락될 수 있습니다. find가 성공해도 대상이 실행 중이면 일관된 단일 시점 스냅샷은 아닙니다.

Ubuntu GNU find에서 다음 조건을 읽고 목적을 설명합니다. `lab_tree`는 자신이 만든 실습 트리만 지정합니다.

```bash
find "$lab_tree" -type f -name '.*'
find "$lab_tree" -type f -size +10M
find "$lab_tree" -type f -perm /111
find "$lab_tree" -type d -perm -0002
```

숨김 이름, 큰 파일, 실행 비트 중 하나 이상, other 쓰기 비트가 있는 디렉터리를 각각 찾습니다. 실행 비트와 실제 실행 가능성은 마운트 noexec·ACL·실행 형식에 따라 다릅니다. 조건만으로 악성 분류하지 않습니다.

## 파일 하나를 자세히 보기

`file_path`는 검토할 실습 파일의 경로입니다. 다음은 GNU/Linux 기준입니다.

```bash
TZ=Asia/Seoul stat -- "$file_path"
file -- "$file_path"
strings -a -n 8 -- "$file_path" | head -n 20
sha256sum -- "$file_path"
```

교육용 stat 일부:

```text
Size: 15   regular file
Access: (0644/-rw-r--r--) Uid: (1000/analyst) Gid: (1000/analyst)
Modify: 2026-09-10 09:05:00.000000000 +0900
Change: 2026-09-10 09:05:00.000000000 +0900
```

Modify는 내용 변경, Change는 inode 상태 변경입니다. Birth는 파일시스템·도구에 따라 없을 수 있습니다. 문자열은 실행 코드의 동작이 아니라 출력 가능한 바이트 조각입니다. 개인정보·제어문자가 포함될 수 있으므로 공유·터미널 표시도 주의합니다. head로 미리보기한 결과를 전체 문자열 목록으로 제출하지 않습니다. pipefail에서는 조기 종료로 upstream SIGPIPE가 날 수 있으므로 보존용 수집과 미리보기는 분리합니다.

## Bash Point — 줄 대신 NUL

```bash
find "$lab_tree" -type f -print0 > "$COURSE_OUT/files.nul"
while IFS= read -r -d '' path; do
    printf 'review=%q\n' "$path"
done < "$COURSE_OUT/files.nul"
```

파일명은 개행을 포함할 수 있지만 NUL은 포함할 수 없습니다. `for path in $(find ...)`는 공백·개행을 쪼개고 glob도 확장하여 다른 파일을 처리할 수 있습니다. NUL 목록은 `xargs -0`과 연결할 수도 있습니다. `%q`는 Bash에서 경계를 읽기 쉽게 표시하는 용도이며 원래 파일명을 바꾸지 않습니다.

## Red / Blue 관점과 실패 사례

### 인코딩된 자료를 실행하지 않고 읽기

Base64는 바이트를 텍스트로 표현하는 인코딩이지 암호화나 악성 판정 기준이 아닙니다. Ubuntu의 작은 평문 예를 비교합니다.

```bash
printf '%s' 'review-note' | base64
printf '%s' 'cmV2aWV3LW5vdGU=' | base64 --decode
printf '\n'
```

인코딩 결과는 `cmV2aWV3LW5vdGU=`, 복원 결과는 `review-note`입니다. macOS의 decode 옵션은 -D 등 구현별 차이를 확인합니다. 실제 의심 자료는 크기 제한·원본/복원본 분리·해시·안전한 표시를 적용하고, 복원한 내용을 bash나 다른 인터프리터에 파이프로 전달하지 않습니다. 복원 성공은 내용의 안전성을 보증하지 않습니다.

공격자는 쓰기 가능한 경로와 실행 경계를 관심 있게 볼 수 있습니다. 방어자는 예상 소유자·권한·배포 이력과 실제 변경 흔적을 비교합니다. `/tmp` 파일을 발견했다고 삭제하면 실행 파일·열린 FD·원래 메타데이터를 잃을 수 있습니다. 수집과 영향 판단을 먼저 수행합니다. 비트 검색 결과를 권한 상승 성공으로 보고하지 않습니다.

## 실습·예상 결과

ch04.sh는 결과 폴더에만 공백·개행·숨김·하이픈 이름의 평문 파일 네 개를 만듭니다. 실행 권한을 추가하거나 시스템 경로를 수정하지 않습니다.

```text
created_files=4
nul_records=4
line_count=5 but file_count=4
copy_changed=yes source_text_preserved=yes
```

## 분석 질문·완료 기준

왜 find 출력 줄 수가 파일 수와 다른가? ctime을 생성 시각으로 해석하면 어떤 타임라인 오류가 생기는가? 해시 변경이 악성 행위를 입증하는가? 실행됐다는 결론에 어떤 자료가 더 필요한가? 파일 경계·메타데이터·내용·실행 증거를 구분해 제출하면 완료입니다. 다음 05장은 로그 행의 경계와 필드 의미를 다룹니다.

## 참고 자료

- [GNU findutils](https://www.gnu.org/software/findutils/manual/html_mono/find.html)
- [stat](https://man7.org/linux/man-pages/man1/stat.1.html)
- [GNU strings](https://sourceware.org/binutils/docs/binutils/strings.html)
