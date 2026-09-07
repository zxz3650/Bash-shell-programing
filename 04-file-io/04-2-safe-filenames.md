# 04-2. 파일명 경계와 안전한 목록 처리

파일명에는 공백, 탭, 개행, 별표가 들어갈 수 있다. 줄바꿈으로 나열한 목록은 모든 파일명을 손실 없이 표현하지 못한다. 파일 목록의 구분자는 NUL을 사용한다.

{% hint style="info" %}
### 🧭 학습 목표

- find -print0과 read -d의 조합을 설명한다.
- 명령 결과 문자열을 for로 분리하는 문제를 관찰한다.
- 인용·옵션 종료·빈 목록을 각각 처리한다.
- 파일 순회 중 오류의 의미를 정한다.
{% endhint %}

## 학습 전 확인

`for file in $(find ...)`는 파일명이 아니라 무엇을 순회하는가? [03-3](../03-bash-basics/03-3-quoting-expansion.md)의 단어 분리를 적용한다.

## 1. 재현 가능한 파일 집합

```bash
lab_dir=$(mktemp -d)
mkdir "$lab_dir/input"
printf 'A\n' > "$lab_dir/input/one.log"
printf 'B\n' > "$lab_dir/input/two words.log"
printf 'C\n' > "$lab_dir/input/-draft.log"
printf 'D\n' > "$lab_dir/input/line
break.log"
printf 'lab=%s\n' "$lab_dir"
```

파일은 네 개다. 마지막 이름에는 실제 개행이 들어 있다. ls 화면의 행 수를 파일 개수로 해석하지 않는다.

## 2. NUL 목록 생성과 상태 확인

```bash
if find "$lab_dir/input" -type f -name '*.log' -print0 > "$lab_dir/list.bin"; then
    count=0
    while IFS= read -r -d '' file; do
        count=$((count + 1))
        printf '%s: %q\n' "$count" "$file"
    done < "$lab_dir/list.bin"
    printf 'count=%s\n' "$count"
else
    printf 'cannot build file list\n' >&2
fi
```

count=4다. `%q`는 Bash에서 읽을 수 있는 이스케이프 표현으로 사람이 경계를 확인하도록 돕는다. 다른 프로그램에 전달할 데이터 형식 대신 사용하지 않는다.

목록을 먼저 파일에 저장하여 find의 실패를 확인했다. 목록은 특정 시점의 이름이며 이후 파일이 바뀔 수 있다는 점은 남는다.

## 3. 빈 목록과 glob

```bash
(
    shopt -s nullglob
    files=("$lab_dir/input"/*.missing)
    printf 'empty count=%s\n' "${#files[@]}"
)
```

기본 glob은 일치가 없으면 패턴 문자열을 남긴다. nullglob은 일치 없음에서 단어를 제거한다. 옵션 변경은 서브셸로 범위를 제한했다.

## 4. 인용과 옵션 경계

`"$file"`은 공백 보존, `--`는 옵션 해석 종료다. 두 가지는 다른 문제다. cat·cp 등 지원하는 명령에는 `--`를 쓰고, 입력 경로를 `./-name`처럼 경로로 명확히 표현할 수도 있다.

## 실패 사례

`for file in $(find ...)`는 명령 치환, 단어 분리, 파일명 확장을 거쳐 원래 파일 경계를 잃는다. `ls | wc -l`도 개행 파일명과 출력 형식 때문에 파일 개수 측정의 일반 해법이 아니다.

## 🧪 직접 해보기

1. 네 파일의 이름과 개수를 유지한 채 순회한다.
2. 확장자를 missing으로 바꿔 빈 목록의 동작을 비교한다.
3. 목록 생성 뒤 파일 하나가 없어지면 전체 작업을 중단할지, 나머지 파일을 처리하고 누락을 알릴지 정한다.

### 해설

좋은 루프는 네 파일에 네 번 실행된다. 오류 정책은 누락을 조용히 무시하는 대신 상태와 진단에 드러나야 한다.

## ✅ 완료 기준

- [ ] 공백·개행·하이픈 파일명을 보존한다.
- [ ] NUL 목록을 셸 변수에 담지 않는다.
- [ ] 검색 실패와 빈 목록을 구분한다.

다음: [04-3. 스트림과 안전한 저장](04-3-streams-atomic-output.md)
