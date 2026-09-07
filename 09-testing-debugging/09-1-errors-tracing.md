# 09-1. 종료 상태·errexit·추적 디버깅

set -e는 예외 처리 체계가 아니다. 어떤 문맥에서 실행했는지에 따라 중단 여부가 달라진다. 필수 단계의 실패는 명시적으로 확인하고, 개발 중에는 상태를 재현하는 작은 실험을 만든다.

{% hint style="info" %}
### 🧭 학습 목표

- set -e·-u·pipefail을 구분한다.
- 조건문에서 호출한 함수의 오류 전파를 관찰한다.
- bash -n과 -x의 검증 범위를 구분한다.
- 상태를 바꾸지 않고 진단한다.
{% endhint %}

## 0. 학습 전 확인

함수 안에서 false가 실행되면 항상 중단되는가? 구문 검사가 성공하면 결과도 올바른가?

## 1. 옵션별 역할

| 옵션 | 기능 | 한계 |
|---|---|---|
| -e | 특정 문맥의 비영 상태에서 종료 | if·논리 목록 등 예외 있음 |
| -u | 미설정 변수 확장을 오류 처리 | 빈 값 검증을 대신하지 않음 |
| pipefail | 파이프 앞 단계 실패도 상태에 반영 | 정상적인 검색 없음도 비영 가능 |
| -E | ERR trap 상속을 확장 | ERR 적용 예외는 남음 |

프로젝트마다 필요한 옵션을 설명한다. 시작 줄을 복사했다는 이유만으로 오류 처리가 완성되지 않는다.

## 2. 조건부 호출의 함정

```bash
bash -e -c '
    work() { false; printf "continued\n"; }
    if work; then printf "reported success\n"; fi
'
```

continued와 reported success가 출력된다. 함수가 조건 위치에서 호출되어 내부 실패가 자동 중단을 일으키지 않고 마지막 printf의 성공이 반환된다.

```bash
bash -e -c '
    work() { false || return 1; printf "not reached\n"; }
    if work; then printf "success\n"; else printf "failure\n"; fi
'
```

이제 failure만 출력된다. 파일 수집·압축·결과 게시처럼 필수 단계에서는 명시적 상태 전달을 사용한다.

## 3. 부정 조건 뒤 상태

```bash
if ! false; then
    printf 'negated status=%s\n' "$?"
fi
```

출력은 0이다. `!`가 상태를 반전했기 때문이다. 원래 상태가 필요하면 `if command; then ...; else status=$?; ...; fi` 형태로 저장한다.

## 4. 구문과 추적

```bash
bash -n examples/log-report/bin/log-report.sh
bash -x examples/log-report/bin/log-report.sh --help
```

저장소 루트에서 실행한다. -n은 구문을 확인하고 -x는 실제 실행하며 확장된 명령을 stderr에 출력한다. 추적에는 인수와 데이터가 남을 수 있으므로 합성 실습 데이터에서만 사용한다.

여러 파일은 `for script in examples/log-report/bin/*.sh; do bash -n "$script" || break; done`처럼 각각 검사한다. `bash -n a.sh b.sh`는 두 파일을 모두 검사하는 명령이 아니다. b.sh는 a.sh의 인수다.

## 🧪 직접 해보기

1. 위 work를 직접 호출한 경우와 if에서 호출한 경우를 비교한다.
2. false 대신 상태 7의 자식 명령을 넣고 원래 상태를 전달한다.
3. 미설정·빈 값에 -u와 `${value:-default}`를 적용한다.

### 해설

호출 문맥이 달라져도 필수 단계 실패를 일관되게 전달하는지가 중요하다. 오류를 숨기기 위해 무조건 `|| true`를 붙이지 않는다.

## ✅ 완료 기준

- [ ] 오류 전파를 작은 재현 예로 설명한다.
- [ ] 각 실행 파일을 개별 구문 검사한다.
- [ ] 디버깅 출력과 업무 결과를 분리한다.

다음: [09-2. 테스트 설계와 회귀 검증](09-2-tests-quality.md)
