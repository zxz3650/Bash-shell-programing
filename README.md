# 표지

Linux 시스템을 조사하고 로그를 분석하며 반복 점검을 자동화하는 **Bash Shell Programming** 실습 교재입니다.

보안 질문에서 출발해 필요한 명령과 Bash 문법을 익힙니다. 출력의 의미와 한계를 확인하고 원본을 보존하며 근거 있는 조사 기록을 만듭니다.

## 이 교재에서 배우는 내용

- 셸 실행 모델과 Linux 명령 사용법을 먼저 학습합니다.
- Shell Programming, 셸 명령 언어, `sh`, Bash와 터미널의 관계를 구분합니다.
- IOC 검색, 파일·계정·프로세스·네트워크 조사, 인증·Journal·Audit·웹 로그 분석에 필요한 문법을 사용합니다.
- 각 장은 개요, 학습 목표, 최소 예제, 실패 사례, 실습, 완료 기준 순서로 구성합니다.
- 레드팀 관련 예제는 소유하거나 명시적으로 허가받은 랩에서만 수행합니다.
- 원본 데이터를 보존하면서 조사하고, 테스트로 스크립트의 동작을 확인합니다.

## 학습 순서

[Bash 문법 찾아보기](bash-syntax-index.md)에서 변수·인용·배열·조건문·반복문·함수의 상세 교안으로 바로 이동할 수 있습니다. [학습 안내와 실습 연결표](course-guide.md)에 따라 12개 장·49개 상세 절의 기본 설명과 문법 실습을 학습한 뒤 같은 장의 보안 적용 실습으로 연결합니다. 기본 문법 교안과 기존 프로젝트는 독립적인 학습 경로로 계속 제공합니다.

Red Team의 목적·권한 경계를 Blue Team의 아티팩트·로그·탐지·완화와 같은 사례에서 비교합니다. [GTFOBins 해설](07-secure-scripting/07-4-gtfobins-review.md)은 정상 도구의 기능과 실제 설정을 구분하는 법을 다룹니다.

1. [01. Bash와 Shell Programming 소개](01-bash-intro.md)
2. [02. 개발 및 실습 환경](02-bash-setup.md)
3. [03. Bash 기초 문법](03-bash-basics.md)
4. [04. 파일 입출력과 권한](04-file-io.md)
5. [05. 파이프라인과 텍스트 처리](05-text-processing.md)
6. [06. 프로세스와 시스템 조사](06-system-inspection.md)
7. [07. 안전한 Shell Script](07-secure-scripting.md)
8. [08. 시스템 자동화](08-system-automation.md)
9. [09. 테스트와 디버깅](09-testing-debugging.md)
10. [10. 프로그램 구조화](10-program-architecture.md)
11. [11. 병렬 작업과 대량 처리](11-parallel-jobs.md)
12. [12. Bash 활용 종합 프로젝트](12-capstone.md)

## 실습용 Jupyter Book

설명을 읽는 것에서 끝나지 않도록 실행 가능한 노트북 실습을 제공합니다. 기본 Python 커널에서 `%%bash` 셀을 실행하므로 별도의 Bash 커널 없이 JupyterLab에서 바로 따라 할 수 있습니다.

- [Bash 실습용 Jupyter Book 안내](jupyter-book/index.md)
- 기존 기초·심화 노트북 12개와 02~12장 보안 실습 11개, 총 23개 노트북
- 모든 파일 생성 작업은 임시 실습 디렉터리 안에서 수행
- 각 실습은 목표, 설정, 단계별 실행, 자체 점검, 다음 학습 순서로 구성

## 학습 산출물

완성 예제는 [로그 보고서 프로젝트](examples/log-report/README.md), 프로젝트 요구사항과 평가 기준은 [12. Bash 활용 종합 프로젝트](12-capstone.md)에 있습니다. 저장소 루트에서 `bash tests/test-course.sh`를 실행하면 정상 입력과 잘못된 입력을 처리하는 동작을 확인할 수 있습니다.

- 실행 가능한 Bash 프로그램과 명령줄 인터페이스
- 로그·파일·프로세스·네트워크 상태 수집 기능
- 안전한 입력 검증, 임시 파일 및 종료 처리
- ShellCheck·shfmt·Bats 품질 검사
- 수집한 로그와 시스템 정보를 정리하는 보안 조사 프로젝트

학습한 내용은 보안 사고 조사에 필요한 정보 수집과 반복 점검을 자동화하는 데 활용할 수 있습니다.
