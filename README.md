# 표지

보안엔지니어가 블루팀 조사·대응 자동화와 승인된 레드팀 실습에 활용하기 전에 필요한 Bash Shell Programming 기반을 학습하는 과정입니다.

## 과정 설계 원칙

- 셸 실행 모델과 Linux 명령 사용법을 먼저 학습합니다.
- 변수·제어문·함수에서 파일·텍스트·프로세스·자동화 순서로 적용 범위를 확장합니다.
- 각 장은 개요, 학습 목표, 최소 예제, 실패 사례, 실습, 완료 기준 순서로 구성합니다.
- 레드팀 관련 예제는 소유하거나 명시적으로 허가받은 랩에서만 수행합니다.
- destructive 명령보다 읽기 전용 조사와 재현 가능한 테스트를 우선합니다.

## 학습 순서

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
- 환경 확인부터 변수·제어문·파일·텍스트·시스템 조사·안전한 스크립팅·자동화·종합 프로젝트까지 9개 실습
- 모든 파일 생성 작업은 임시 실습 디렉터리 안에서 수행
- 각 실습은 목표, 설정, 단계별 실행, 자체 점검, 다음 학습 순서로 구성

## 학습 산출물

- 실행 가능한 Bash 프로그램과 명령줄 인터페이스
- 로그·파일·프로세스·네트워크 상태 수집 기능
- 안전한 입력 검증, 임시 파일 및 종료 처리
- ShellCheck·shfmt·Bats 품질 검사
- 재현 가능한 블루팀 triage 프로젝트

이 과정을 완료한 뒤 CSIRT 조사 자동화 또는 승인된 공격 검증 자동화 심화과정으로 분기합니다.
