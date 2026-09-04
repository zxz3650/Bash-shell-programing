# Bash Shell Programming 실습 교재

이 Jupyter Book은 본 교안의 개념을 학생이 직접 실행하며 확인하는 실습 트랙입니다. 모든 노트북은 기본 Python 커널에서 `%%bash` 셀을 실행하므로 별도의 Bash 커널을 설치하지 않아도 됩니다.

## 학습 목표

- Bash가 적합한 문제와 Python이 적합한 문제를 구분한다.
- 변수, 인자, 배열, 조건문, 반복문, 함수를 작은 작업에 적용한다.
- 파일, 권한, 파이프라인, 텍스트 처리 명령을 안전하게 조합한다.
- 시스템 상태를 읽기 전용으로 조사하고 결과를 재현 가능하게 저장한다.
- 실패를 빠르게 감지하고 테스트 가능한 자동화 스크립트를 작성한다.

## 시작하기

```bash
git clone https://github.com/zxz3650/Bash-shell-programing.git
cd Bash-shell-programing
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r jupyter-book/requirements.txt
jupyter lab jupyter-book/labs
```

Jupyter Book 웹 미리보기는 저장소 루트에서 다음과 같이 실행합니다.

```bash
jupyter book start jupyter-book
```

설치가 어려운 학생은 [실습 목록](labs/README.md)의 **Colab에서 실행** 링크를 사용합니다. Colab에서도 각 노트북의 `%%bash` 셀을 위에서 아래로 실행할 수 있습니다.

## 실습 규칙

1. 위에서 아래로 셀을 순서대로 실행합니다.
2. `BASH_LAB_DIR`로 표시되는 임시 디렉터리 밖의 파일을 변경하지 않습니다.
3. 명령을 실행하기 전에 입력값, 대상 경로, 예상 출력을 먼저 확인합니다.
4. 오류가 발생하면 출력과 종료 상태 `$?`를 함께 기록합니다.
5. 보안 관련 명령은 본인 소유 시스템이나 명시적으로 허가된 실습 환경에서만 사용합니다.

## 권장 학습 순서

| 순서 | 실습 | 결과물 |
|---:|---|---|
| 00 | 환경과 안전 규칙 | 격리된 실습 디렉터리 |
| 01 | Bash를 선택하는 기준 | Bash/Python 판단표 |
| 02 | 인자·변수·배열 | 입력 검증 스크립트 |
| 03 | 조건·반복·함수 | 파일 분류 함수 |
| 04 | 파일·권한·파이프라인 | 안전한 파일 처리 흐름 |
| 05 | 텍스트 처리 | 로그 요약 보고서 |
| 06 | 시스템 조사·안전한 스크립팅 | 읽기 전용 상태 스냅샷 |
| 07 | 자동화·테스트 | 종료 상태 기반 테스트 |
| 08 | 종합 프로젝트 | 로컬 triage 수집기 |

세부 파일과 운영 방법은 [실습 목록](labs/README.md)을 참고합니다.
