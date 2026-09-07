# 04-3. 표준 스트림과 원자적 결과 저장

프로그램을 연결할 때는 결과 데이터와 오류 메시지를 구분해야 한다. stdout에는 결과 데이터, stderr에는 진단을 출력하면 결과 파일을 다른 명령이 안정적으로 읽을 수 있다. 저장 도중 실패해도 기존 결과를 보존하려면 임시 파일을 거친다.

{% hint style="info" %}
### 🧭 학습 목표

- 파일 디스크립터 0·1·2를 연결한다.
- 리다이렉션 순서를 설명한다.
- here-document에서 확장 여부를 선택한다.
- 임시 파일에 결과를 쓴 뒤 이름을 바꾸어 최종 파일로 저장하는 절차를 설명한다.
{% endhint %}

## 0. 학습 전 확인

`>all.txt 2>&1`과 `2>&1 >out.txt`는 같은가? 기존 파일에 `>`를 사용하면 언제 내용이 사라지는가?

## 1. 스트림을 따로 기록

```bash
lab_dir=$(mktemp -d)
{
    printf 'result=42\n'
    printf 'diagnostic\n' >&2
} > "$lab_dir/result.txt" 2> "$lab_dir/error.txt"
cat "$lab_dir/result.txt"
cat "$lab_dir/error.txt"
```

두 파일은 각각 한 행이다. `>`는 실행 전에 파일을 열고 기존 내용을 비운다. 입력 파일과 출력 파일을 같게 지정한 `sort data > data`는 정렬 전에 원본을 비울 수 있다.

## 2. 순서 읽기

| 표현 | 결과 |
|---|---|
| `>all.txt 2>&1` | stdout을 파일로, stderr를 그 stdout에 연결 |
| `2>&1 >out.txt` | stderr를 원래 stdout에, stdout만 파일로 연결 |
| `>>out.txt` | 기존 끝에 추가 |
| `<input.txt` | 파일을 stdin으로 연결 |

리다이렉션은 왼쪽부터 처리된다. FD 복제는 나중에 연결된 경로를 계속 따라가는 변수가 아니다.

## 3. here-document

```bash
label=demo
cat <<'TEXT'
$label remains literal
TEXT
cat <<TEXT
label=$label
TEXT
```

첫 출력은 달러 문자를 보존하고 둘째는 label=demo다. 코드·설정 샘플을 생성할 때 의도치 않은 확장을 피하려면 구분자를 인용한다.

## 4. 임시 파일 후 교체

```bash
(
    umask 077
    report="$lab_dir/report.txt"
    temporary=$(mktemp "$lab_dir/.report.XXXXXX") || exit 1
    trap 'rm -f -- "$temporary"' EXIT
    if printf 'status=complete\n' > "$temporary"; then
        mv -- "$temporary" "$report" || exit 1
    else
        exit 1
    fi
    cat "$report"
)
```

임시 파일을 최종 결과와 같은 파일시스템에 만든다. 이름 교체가 원자적으로 이루어지면 독자는 이전 파일 또는 완성된 새 파일을 읽는다. 이는 전원 장애에서의 영구 저장 보장이나 다중 작성자 충돌 해결과는 다르다. 네트워크 파일시스템은 실제 동작을 확인해야 한다.

## 실패 사례와 실습

1. 두 리다이렉션 순서를 각각 실행하여 stderr의 위치를 확인한다.
2. 임시 파일 생성 후 실패하도록 수정하고 기존 report가 보존되는지 확인한다.
3. 기존 파일 덮어쓰기 허용과 거부 중 수업 프로젝트 정책을 정한다.

### 해설

실패 중 임시 파일만 정리하고 기존 결과는 유지하는지가 핵심이다. trap은 SIGKILL이나 전원 장애에는 실행되지 않으므로 다음 실행에서 남은 임시 파일을 다루는 정책도 필요하다.

## ✅ 완료 기준

- [ ] stdout과 stderr를 별도 파일로 검증한다.
- [ ] 입력과 출력 충돌을 피한다.
- [ ] 임시 저장·검증·최종 교체 순서를 설명한다.

다음: [05. 파이프라인과 텍스트 처리](../05-text-processing.md)
