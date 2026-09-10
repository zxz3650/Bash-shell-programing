# Bash 문법 찾아보기

변수·인용·조건문·반복문·함수부터 단계별로 배우는 기본 학습 경로입니다. 각 링크는 요약이 아니라 예제·출력 해석·실패 사례·직접 해보기·완료 기준을 담은 상세 교안으로 연결됩니다. 보안 실습은 이 기본기를 사용하는 적용 과제입니다.

## 1. 시작과 실행 환경

- [01. Bash와 Shell Programming 소개](01-bash-intro.md): Shell·Bash·터미널의 관계, Bash가 적합한 업무, Python과의 역할 구분
- [02. 개발 및 실습 환경](02-bash-setup.md): Ubuntu·WSL·Jupyter 준비, shebang, 스크립트 실행과 도움말
- [03. Bash 기초 문법](03-bash-basics.md): 아래 아홉 절의 전체 학습 순서

## 2. 기본 문법 아홉 절

| 순서 | 상세 교안 | 다루는 내용 |
|---|---|---|
| 03-1 | [명령 실행과 종료 상태](03-bash-basics/03-1-execution-model.md) | 명령·인수, stdout/stderr, `$?`, 명령 연결 |
| 03-2 | [변수와 환경 변수](03-bash-basics/03-2-variables-environment.md) | 대입·참조, export, 자식 프로세스, 명령 치환 |
| 03-3 | [인용과 확장 순서](03-bash-basics/03-3-quoting-expansion.md) | 작은/큰따옴표, word splitting, glob, 확장 순서 |
| 03-4 | [위치 인자와 배열](03-bash-basics/03-4-arguments-arrays.md) | `$1`, `$@`, `$#`, shift, 배열과 인수 경계 |
| 03-5 | [문자열 처리와 산술식](03-bash-basics/03-5-strings-arithmetic.md) | 매개변수 확장, 문자열 비교·추출, 정수 계산 |
| 03-6 | [조건문과 case](03-bash-basics/03-6-conditions.md) | if·elif·else, 파일·문자열·숫자 조건, case |
| 03-7 | [반복문과 입력 스트리밍](03-bash-basics/03-7-loops.md) | for·while, break·continue, read, 행과 파일명 경계 |
| 03-8 | [함수와 스코프](03-bash-basics/03-8-functions.md) | 함수 정의·호출, local, stdout·return, 스코프 |
| 03-9 | [문법 종합 실습](03-bash-basics/03-9-syntax-project.md) | 배운 문법으로 이벤트 분류기 구현·검증 |

처음 배우는 학생은 03-1부터 순서대로 읽습니다. 예제를 실행하고 출력과 종료 상태를 예상한 뒤 직접 해보기 문제를 풉니다. 문법을 이미 아는 학생은 필요한 절을 복습하면서 적용 실습으로 이동할 수 있습니다.

## 3. 파일·파이프라인·프로그램 작성

| 기본 학습 | 다음 보안 적용 |
|---|---|
| [04. 파일 입출력과 권한](04-file-io.md) | [04-4. 의심 파일 조사](04-file-io/04-4-filesystem-investigation.md) |
| [05. 파이프라인과 텍스트 처리](05-text-processing.md) | [05-4. SSH 인증 로그 분석](05-text-processing/05-4-auth-pipeline.md) |
| [06. 프로세스와 시스템 조사](06-system-inspection.md) | [06-3. 호스트·프로세스·서비스 연결](06-system-inspection/06-3-host-process-investigation.md) |
| [07. 안전한 Shell Script](07-secure-scripting.md) | [07-3. 계정·권한 검토](07-secure-scripting/07-3-account-permission-review.md), [07-4. GTFOBins](07-secure-scripting/07-4-gtfobins-review.md) |
| [08. 시스템 자동화](08-system-automation.md) | [08-3. 지속성 위치 검토](08-system-automation/08-3-persistence-review.md) |
| [09. 테스트와 디버깅](09-testing-debugging.md) | [09-3. 로그인 아티팩트 검증](09-testing-debugging/09-3-login-artifacts.md) |
| [10. 프로그램 구조화](10-program-architecture.md) | [10-3. Journal](10-program-architecture/10-3-journal-analysis.md), [10-4. Audit](10-program-architecture/10-4-audit-analysis.md) |
| [11. 병렬 작업과 대량 처리](11-parallel-jobs.md) | [11-3. 웹 로그 분석](11-parallel-jobs/11-3-web-log-analysis.md) |
| [12. Bash 활용 종합 프로젝트](12-capstone.md) | [12-3. DFIR Capstone](12-capstone/12-3-dfir-capstone.md) |

## 4. 기본 문법을 실행하는 노트북

- [00. 환경 확인](jupyter-book/labs/00-orientation-and-safety.ipynb)
- [01. Bash 선택과 Shell 실행 모델](jupyter-book/labs/01-when-to-use-bash.ipynb)
- [02. 인자·변수·배열·인용](jupyter-book/labs/02-arguments-variables-arrays.ipynb)
- [03. 조건문·반복문·함수](jupyter-book/labs/03-conditions-loops-functions.ipynb)
- [04. 파일·권한·파이프라인](jupyter-book/labs/04-files-permissions-pipelines.ipynb)
- [05. 텍스트 처리](jupyter-book/labs/05-text-processing.ipynb)

노트북 번호와 교안 장 번호는 항상 같지 않습니다. [전체 실습 연결표](jupyter-book/labs/README.md)에서 확인합니다. 기본 노트북의 Setup부터 순서대로 실행하고, 학습한 문법을 같은 장의 security 노트북에 적용합니다. 어느 노트북도 코드 검토 없이 운영 시스템에 적용하지 않습니다.
