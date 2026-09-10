# 실습 목록과 운영 방법

## 장별 보안 실습

다음 노트북은 해당 교안 장과 함께 실행합니다. 합성 자료가 포함되어 별도 다운로드가 필요하지 않습니다. 실제 wtmp·Journal 바이너리 검증과 라이브 시스템 조사는 교안에 표시된 별도 Ubuntu VM 선택 실습입니다.

| 장 | 주제 | 노트북 | 바로 실행 |
|---|---|---|---|
| 02 | 환경·증거·KST | [보기](security-02-evidence.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-02-evidence.ipynb) |
| 03 | IOC·입력 경계 | [보기](security-03-ioc.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-03-ioc.ipynb) |
| 04 | 파일 조사 | [보기](security-04-files.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-04-files.ipynb) |
| 05 | SSH 로그 | [보기](security-05-auth.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-05-auth.ipynb) |
| 06 | 프로세스·네트워크 | [보기](security-06-process-network.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-06-process-network.ipynb) |
| 07 | 계정·권한·GTFOBins 검토 | [보기](security-07-permissions.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-07-permissions.ipynb) |
| 08 | 지속성 흔적 | [보기](security-08-persistence.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-08-persistence.ipynb) |
| 09 | 로그인 아티팩트 | [보기](security-09-login.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-09-login.ipynb) |
| 10 | Journal·Audit | [보기](security-10-journal-audit.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-10-journal-audit.ipynb) |
| 11 | 웹 로그·배치 | [보기](security-11-web.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-11-web.ipynb) |
| 12 | DFIR Capstone | [보기](security-12-triage.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/security-12-triage.ipynb) |

## 기초·심화 참고 노트북

위 security-03부터 security-12까지는 계산 뒤 Red Team ↔ Blue Team 사례와 분석 기록을 작성합니다. 07장의 GTFOBins 검토 카드는 실제 시스템 점검 결과가 아닌 별도 합성 훈련입니다. 12장에서는 인증·권한·지속성 사건 카드 세 개로 역할을 교대하고 근거·정상 반례·탐지·완화를 평가합니다.

| 순서 | 주제 | GitHub | 바로 실행 |
|---:|---|---|---|
| 00 | 환경 확인과 안전한 임시 디렉터리 | [노트북 보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/00-orientation-and-safety.ipynb) | [Colab에서 실행](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/00-orientation-and-safety.ipynb) |
| 01 | Linux 보안 조사·Shell 실행 모델·도구 선택 | [노트북 보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/01-when-to-use-bash.ipynb) | [Colab에서 실행](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/01-when-to-use-bash.ipynb) |
| 02 | 인자, 변수, 배열과 인용 | [노트북 보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/02-arguments-variables-arrays.ipynb) | [Colab에서 실행](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/02-arguments-variables-arrays.ipynb) |
| 03 | 조건문, 반복문, 함수 | [노트북 보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/03-conditions-loops-functions.ipynb) | [Colab에서 실행](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/03-conditions-loops-functions.ipynb) |
| 04 | 파일, 권한, 리다이렉션과 파이프 | [노트북 보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/04-files-permissions-pipelines.ipynb) | [Colab에서 실행](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/04-files-permissions-pipelines.ipynb) |
| 05 | `grep`, `cut`, `sort`, `uniq`, `awk` | [노트북 보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/05-text-processing.ipynb) | [Colab에서 실행](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/05-text-processing.ipynb) |
| 06 | 읽기 전용 조사와 안전 옵션 | [노트북 보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/06-system-inspection-secure-scripting.ipynb) | [Colab에서 실행](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/06-system-inspection-secure-scripting.ipynb) |
| 07 | 자동화와 종료 상태 기반 테스트 | [노트북 보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/07-automation-testing.ipynb) | [Colab에서 실행](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/07-automation-testing.ipynb) |
| 08 | 로컬 시스템 triage 수집기 | [노트북 보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/08-capstone-triage-collector.ipynb) | [Colab에서 실행](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/08-capstone-triage-collector.ipynb) |

## 수업 운영 권장안

아래 09·10·11 노트북은 오류 처리·모듈화·병렬 처리를 더 연습할 때 사용하는 참고 실습입니다. 장별 보안 수업은 위의 security 노트북 연결표를 따릅니다. 12장 종합 실습은 security-12-triage를 사용하고 기존 08 노트북은 별도 참고 자료로 활용합니다.

| 번호 | 주제 | 노트북 | 바로 실행 |
|---|---|---|---|
| 09 | 오류 전파와 종료 상태 | [보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/09-error-contracts.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/09-error-contracts.ipynb) |
| 10 | 모듈과 함수의 입력과 출력 | [보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/10-modules-contracts.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/10-modules-contracts.ipynb) |
| 11 | 제한된 병렬 처리 | [보기](https://github.com/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/11-bounded-parallel.ipynb) | [Colab](https://colab.research.google.com/github/zxz3650/Bash-shell-programing/blob/master/jupyter-book/labs/11-bounded-parallel.ipynb) |

- 강사는 먼저 예상 결과를 질문한 뒤 코드 셀을 실행합니다.
- 학생은 실행 결과를 확인하고 코드의 한 부분을 바꾸어 다시 실행합니다.
- 각 노트북의 `Checks`를 통과한 뒤 다음 실습으로 이동합니다.
- 종합 프로젝트는 결과 디렉터리, 로그, 체크섬을 함께 제출합니다.

## 실행 환경

- Linux 또는 macOS
- Bash 3.2 이상
- Python 3.10 이상
- JupyterLab 4

Windows 사용자는 WSL2의 Ubuntu 환경에서 실행하는 것을 권장합니다.
