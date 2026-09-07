# 03-7. 반복문과 입력 스트리밍

배열을 순회하는 것과 파일을 한 줄씩 읽는 것은 다른 작업이다. 입력의 경계가 인수인지, 행인지, 파일명인지 먼저 정하면 올바른 반복 패턴을 선택할 수 있다.

{% hint style="info" %}
### 🧭 학습 목표

- for·while·break·continue를 사용한다.
- 공백·백슬래시·마지막 개행이 없는 행을 보존한다.
- 파이프 내부 변수 변경의 범위를 설명한다.
- 파일 목록과 텍스트 행을 다르게 처리한다.
{% endhint %}

## 선행 지식

[배열](03-4-arguments-arrays.md), [조건문](03-6-conditions.md). 실습은 [노트북 03](../jupyter-book/labs/03-conditions-loops-functions.ipynb)이다.

## 0. 학습 전 확인

`for item in $(cat file)`은 행을 보존하는가? 파이프로 연결한 while 안의 count는 밖에서도 증가하는가?

## 1. 배열 순회

```bash
levels=(INFO DEBUG ERROR)
for level in "${levels[@]}"; do
    [[ $level == DEBUG ]] && continue
    printf '%s\n' "$level"
done
```

INFO와 ERROR를 출력한다. continue는 이번 반복만 건너뛰고 break는 가장 가까운 반복문을 끝낸다.

## 2. 횟수 기반 반복

```bash
for ((index=0; index<3; index++)); do
    printf 'index=%s\n' "$index"
done
```

C 스타일 for는 Bash 전용이다. `{1..$limit}`는 변수 확장 전에 중괄호 확장이 처리되어 동적 범위를 만들지 못한다. 변수 범위는 산술 for를 사용한다.

## 3. 행 보존

```bash
lab_dir=$(mktemp -d)
printf '  leading spaces\npath\\name\nlast without newline' > "$lab_dir/lines.txt"
count=0
while IFS= read -r line || [[ -n $line ]]; do
    count=$((count + 1))
    printf '%s=<%s>\n' "$count" "$line"
done < "$lab_dir/lines.txt"
printf 'count=%s\n' "$count"
```

count는 3이다. IFS=는 앞뒤 공백을 보존하고 -r은 백슬래시를 이스케이프로 소비하지 않는다. EOF 직전 마지막 행에 개행이 없어도 read가 읽은 값이 있으면 처리한다.

생성한 경로는 출력해 확인한 뒤 실습 종료 시 해당 파일과 빈 디렉터리만 정리한다.

## 4. 파이프와 변수 범위

```bash
count=0
printf 'a\nb\n' | while IFS= read -r line; do
    count=$((count + 1))
done
printf 'parent count=%s\n' "$count"
```

기본 Bash 설정에서는 반복문이 서브셸에서 실행되어 부모 count는 0이다. lastpipe 같은 옵션에 따라 달라질 수 있으므로 부모 누적이 필요하면 `< file` 리다이렉션을 사용한다.

`done < <(producer)`는 프로세스 치환으로 입력을 받을 수 있지만 생산자 실패 상태가 자동으로 반복문 상태에 합쳐지지 않는다. 실패를 정확히 검증해야 할 때는 생산 결과를 임시 파일에 저장하고 상태를 확인한 뒤 읽는다.

## 5. 파일명은 행이 아니다

파일명에는 개행이 들어갈 수 있다. find 출력은 NUL 구분자로 전달하고 `read -r -d ''`로 읽는다. 상세 예제는 [04-2](../04-file-io/04-2-safe-filenames.md)에 있다.

## 🧪 직접 해보기

1. 위 lines.txt에 빈 행을 추가하고 count를 예상한다.
2. 빈 행과 `#`로 시작하는 행을 건너뛰는 조건을 추가한다.
3. 파이프를 파일 리다이렉션으로 바꾸어 부모 count를 비교한다.

### 해설

빈 행도 입력 레코드다. 건너뛰기 전에 증가하면 전체 행 수이고, 건너뛴 뒤 증가하면 유효 레코드 수다. 카운터 의미를 먼저 정한다.

## ✅ 완료 기준

- [ ] 행의 공백과 백슬래시를 보존한다.
- [ ] 마지막 개행 없는 입력을 처리한다.
- [ ] 반복문 변수의 프로세스 범위를 설명한다.

다음: [03-8. 함수와 스코프](03-8-functions.md)
