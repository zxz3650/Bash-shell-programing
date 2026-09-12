# Bash Shell Programming 실습 교재

이 Jupyter Book은 본 교안의 개념을 학생이 직접 실행하며 확인하는 실습 트랙입니다. Shell Programming은 셸 명령 언어로 자동화하는 방식이고, Bash는 그 언어를 해석하는 대표적인 셸 프로그램입니다. 모든 노트북은 기본 Python 커널에서 `%%bash` 셀을 실행하므로 별도의 Bash 커널을 설치하지 않아도 됩니다.

## 학습 목표

교안은 12개 장·49개 상세 절이며 노트북은 23개다. 00부터 11까지는 기본·심화 학습이고 security-02부터 security-12까지는 보안 적용 실습이다. 초심자는 [Bash 문법 찾아보기](../bash-syntax-index.md)와 기본 노트북에서 문법을 학습한 뒤 [학습 연결표](../course-guide.md)에 따라 보안 분석에 적용한다.

security-03부터 security-12까지는 교안의 Red Team ↔ Blue Team 사례와 역할별 분석 기록을 포함한다. 07장에는 GTFOBins 관련성·권한 검토·실행 자료를 구분하는 네 개의 합성 카드 실습이 있다. 실행 결과는 자동 검사하고, 위험 설명·탐지·완화 과제는 강사 또는 동료가 검토한다.

- Shell Programming, `sh`와 Bash 인터프리터의 관계를 구분한다.
- Bash가 적합한 문제와 Python이 적합한 문제를 구분한다.
- 변수, 인자, 배열, 조건문, 반복문, 함수를 작은 작업에 적용한다.
- 파일, 권한, 파이프라인, 텍스트 처리 명령을 안전하게 조합한다.
- 시스템 상태를 읽기 전용으로 조사하고 결과를 재현 가능하게 저장한다.
- 실패를 빠르게 감지하고 테스트 가능한 자동화 스크립트를 작성한다.

## 실습 자료 다운로드 — 학생용

**[장별 학습용 노트북 ZIP 받기](../downloads/README.md)** · [전체 노트북 23개 받기](https://github.com/zxz3650/Bash-shell-programing/raw/refs/heads/master/downloads/all-labs.zip)

Git 설치 없이 ZIP을 받아 시작할 수 있습니다. 압축을 푼 폴더의 `START-HERE.md`에서 노트북 실행 순서를 확인합니다. [실습 자료 받기와 시작하기](../PRACTICE.md)에 설치부터 첫 셀 실행, 개인 풀이 보관까지 안내되어 있습니다.

ZIP 안의 `requirements.txt`가 있는 폴더에서 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

JupyterLab의 `notebooks/`에서 `.ipynb`를 열고 **Python 3** 커널로 실행합니다. 다운로드 ZIP은 노트북 실습용이며 완성된 HTML Jupyter Book이 아닙니다.

## 전체 저장소로 시작하기 — 강사·프로젝트 학습용

터미널 프로젝트 소스와 교안까지 함께 필요한 경우 다음 방법을 사용합니다. 학생용 ZIP의 폴더 구조와 다르므로 위 실행 명령과 구분합니다.

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

단, 07장 GTFOBins 확장 실험은 파일 접근 거부를 관찰하므로 **Ubuntu 일반 사용자**가 필요합니다. root로 실행되는 Colab 대신 VM/WSL에서 진행합니다.

## 실습 규칙

1. 위에서 아래로 셀을 순서대로 실행합니다.
2. Setup에서 만든 `BASH_LAB_DIR` 또는 `COURSE_OUT` 안에서만 결과를 만들고 입력 자료는 보존합니다.
3. 명령을 실행하기 전에 입력값, 대상 경로, 예상 출력을 먼저 확인합니다.
4. 오류가 발생하면 출력과 종료 상태 `$?`를 함께 기록합니다.
5. 보안 관련 명령은 본인 소유 시스템이나 명시적으로 허가된 실습 환경에서만 사용합니다.

## 기본 학습에서 보안 실습으로

아래 기본·심화 노트북에서 Bash 문법을 먼저 학습하고, [장별 실습 목록](labs/README.md)의 security-02~12로 적용합니다. 합성 자료만 사용하는 필수 실습과 Linux 전용 도구를 사용하는 선택 VM 조사는 구분합니다. [다운로드 연결표](../downloads/README.md)에서 각 장의 기본 노트북과 보안 노트북을 함께 받을 수 있습니다.

| 순서 | 실습 | 결과물 |
|---:|---|---|
| 00 | 용어·인터프리터·환경과 안전 규칙 | `sh`/Bash 구분과 새 임시 실습 디렉터리 |
| 01 | Linux 보안 조사와 Shell 실행 모델 | 조사 기록·KST·사실/가설·Bash/Python 판단 |
| 02 | 인자·변수·배열 | 입력 검증 스크립트 |
| 03 | 조건·반복·함수 | 파일 분류 함수 |
| 04 | 파일·권한·파이프라인 | 안전한 파일 처리 흐름 |
| 05 | 텍스트 처리 | 로그 요약 보고서 |
| 06 | 시스템 조사·안전한 스크립팅 | 읽기 전용 상태 스냅샷 |
| 07 | 자동화·테스트 | 종료 상태 기반 테스트 |
| 08 | 종합 프로젝트 | 로컬 triage 수집기 |
| 09 | 오류 전파·종료 상태 | 정상 출력·오류 출력·종료 상태 검사 |
| 10 | 모듈·함수의 입력과 출력 | 불러올 때 파일을 변경하거나 작업을 실행하지 않는 라이브러리 |
| 11 | 제한된 병렬 처리 | 직렬·병렬 결과 일치 검증 |

세부 파일과 운영 방법은 [실습 목록](labs/README.md)을 참고합니다.
