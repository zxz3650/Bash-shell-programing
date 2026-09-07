# 05-2. awk·sed·sort·uniq로 로그 집계

텍스트 처리 도구는 서로 다른 역할을 가진다. 행 선택, 열 추출, 치환, 정렬, 집계를 작은 단계로 나누면 결과가 틀린 위치를 찾기 쉽다.

{% hint style="info" %}
### 🧭 학습 목표

- awk 레코드·필드·패턴·동작을 설명한다.
- sort와 uniq의 입력 조건을 이해한다.
- 로케일과 정렬 기준을 고정한다.
- 불완전한 행을 정상 데이터와 구분한다.
{% endhint %}

## 0. 샘플과 정답

```bash
lab_dir=$(mktemp -d)
printf '%s\n' 'INFO api' 'ERROR db' 'WARN api' 'ERROR db' 'ERROR api' > "$lab_dir/events.txt"
```

ERROR는 3행이며 db 2행, api 1행이다. 작업 전 정답을 손으로 계산한다.

## 1. 필드 추출

```bash
awk '$1 == "ERROR" { print $2 }' "$lab_dir/events.txt"
```

```text
db
db
api
```

기본 필드 구분은 공백이며 `$1`은 첫 필드, `$NF`는 마지막 필드, NR은 현재 레코드 번호다. awk 코드의 작은따옴표는 Bash가 `$1`을 자기 위치 인자로 확장하지 못하게 한다.

## 2. 정렬 후 인접 중복 집계

```bash
awk '$1 == "ERROR" { print $2 }' "$lab_dir/events.txt" |
    LC_ALL=C sort |
    uniq -c |
    LC_ALL=C sort -k1,1nr -k2,2
```

2 db, 1 api 순이다. uniq는 인접한 같은 행만 묶으므로 먼저 sort가 필요하다. 빈도 내림차순 뒤 이름 오름차순을 두어 동률에서도 순서가 정해지게 한다.

## 3. awk에서 직접 집계

```bash
awk '
    NF != 2 { bad++; next }
    $1 == "ERROR" { count[$2]++ }
    END {
        for (service in count)
            printf "%s\t%d\n", service, count[service]
        if (bad > 0) exit 2
    }
' "$lab_dir/events.txt" | LC_ALL=C sort
```

awk 연관 배열의 순회 순서는 보장하지 않는다. 표시 순서는 뒤에서 정한다. 오류 상태까지 필요하면 pipefail을 설정하거나 awk 결과를 먼저 파일에 저장하고 상태를 확인한다.

## 4. sed와 cut의 경계

```bash
sed -n '1,3p' "$lab_dir/events.txt"
sed 's/ERROR/REVIEW/g' "$lab_dir/events.txt"
```

첫 명령은 3행 미리보기, 둘째는 stdout 치환 결과다. 원본은 바뀌지 않는다. sed -i는 GNU와 BSD 옵션 차이가 있고 원본을 변경하므로 교재에서는 임시 결과 후 교체를 사용한다.

cut은 명확한 단일 문자 구분 형식에 적합하다. 따옴표 안에 쉼표가 있는 일반 CSV는 cut -d,로 올바르게 처리할 수 없다.

## 실패 사례와 실습

1. db·api가 교대로 등장하도록 바꾸고 sort 없는 uniq 결과를 확인한다.
2. 서비스 이름만 있는 잘못된 행을 추가한다.
3. 정상 행 집계와 오류 상태가 모두 유지되도록 변경한다.

### 해설

잘못된 행을 빈 서비스 이름으로 집계하면 데이터가 오염된다. 형식 검사와 집계는 순서를 나눠 작성한다.

## ✅ 완료 기준

- [ ] 각 단계의 예상 결과와 실제 결과를 비교한다.
- [ ] 출력 순서와 집계 정확성을 따로 검증한다.
- [ ] 입력 구분 규칙이 복잡해지는 전환 시점을 설명한다.

다음: [05-3. JSON과 형식 선택](05-3-json-data-contracts.md)
