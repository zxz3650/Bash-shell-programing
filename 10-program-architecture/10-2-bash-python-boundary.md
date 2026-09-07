# 10-2. Bash와 Python의 역할 분담

Bash는 운영체제 도구를 연결하는 작업에 강하다. Python은 구조화 데이터, 복잡한 오류 복구, 자료형과 모듈 기반 테스트가 필요한 작업에 적합하다. 코드 줄 수보다 데이터와 상태의 복잡도를 기준으로 선택한다.

{% hint style="info" %}
### 🧭 학습 목표

- Bash 대신 Python을 사용하는 편이 적합한 상황을 설명한다.
- 스트림·파일·종료 상태로 프로그램을 연결한다.
- 여러 파서가 겹치는 인용 문제를 줄인다.
- Bash를 계속 사용할 부분을 구체화한다.
{% endhint %}

## 학습 전 확인

중첩 JSON 검증과 UTC 시각 변환을 Bash 문자열 연산으로 구현하면 어떤 테스트가 필요해지는가?

## 1. 선택표

| 요구 | 우선 선택 | 이유 |
|---|---|---|
| 명령 세 개를 순서대로 실행 | Bash | 프로세스·상태 연결 |
| 파일 목록 전달·해시 도구 호출 | Bash | 기존 도구 조합 |
| 단순 필드별 집계 | awk 또는 Python | 데이터 크기와 처리 규칙에 따라 선택 |
| 중첩 JSON 스키마 검증 | Python | 구조화 자료와 테스트 |
| 시간대·날짜 계산 | Python | 전용 라이브러리 |
| 장기 실행 서버·복잡한 병렬 상태 | Python 등 | 수명·동시성 관리 |

## 2. Bash와 Python 사이의 데이터 전달

```text
Bash: 입력 경로·옵션 확인
→ Python: 레코드 파싱·자료형 검증·변환
→ Bash: 종료 상태 확인·결과 저장
```

Python 프로그램이 실패했는데도 Bash가 결과를 저장하면 불완전한 파일이 남을 수 있다. Bash에서는 Python의 종료 상태를 확인하고, 성공했을 때만 정해진 형식의 결과를 저장해야 한다.

## 3. 최소 실습

다음을 `normalize.py`로 저장한다.

```python
import json
import sys

try:
    value = json.load(sys.stdin)
    if not isinstance(value, dict) or not isinstance(value.get("name"), str):
        raise ValueError("name must be a string")
    print(json.dumps({"name": value["name"].strip()}, ensure_ascii=False))
except (ValueError, TypeError) as exc:
    print(f"invalid input: {exc}", file=sys.stderr)
    sys.exit(2)
```

```bash
printf '%s\n' '{"name":"  analyst  "}' | python3 normalize.py
```

예상 결과는 `{"name": "analyst"}`다. name이 숫자이면 stderr 진단과 상태 2다. 이 작은 예제는 역할 분담 설명용이며 전체 업무 스키마는 추가해야 한다.

## 4. 인용 계층 줄이기

긴 Python 코드를 `python -c "..."` 안에 넣고 Bash 변수까지 삽입하면 Bash·Python·JSON의 세 문법이 겹친다. 코드는 파일, 값은 인수 또는 stdin으로 분리한다. subprocess를 Python에서 호출할 때도 인수 목록을 사용한다.

## 5. 실패 사례

숫자처럼 보이는 문자열을 자동 변환하여 원래 의미를 잃거나, 오류 출력까지 정상 JSON 파일에 합치면 후속 파서가 실패한다. 출력 형식에는 각 필드의 자료형, 필수 항목, 오류 메시지를 보낼 위치까지 명시해야 한다.

## 🧪 직접 해보기

1. 정상 문자열·빈 문자열·숫자·name 없음·잘못된 JSON을 비교한다.
2. Bash에서 Python의 상태를 저장한다.
3. 기존 로그 보고서에서 Bash로 남길 부분과 Python으로 바꿀 부분을 설명한다.

## ✅ 완료 기준

- [ ] 전환 이유를 코드 길이보다 데이터·상태로 설명한다.
- [ ] 프로그램 사이 출력 형식과 상태가 명시돼 있다.
- [ ] 언어 사이에 값을 코드로 삽입하지 않는다.

다음: [11. 병렬 작업과 대량 처리](../11-parallel-jobs.md)
