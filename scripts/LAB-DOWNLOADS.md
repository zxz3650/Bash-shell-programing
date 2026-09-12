# 학습용 ZIP 관리

학생용 안내는 [실습 자료 받기와 시작하기](../PRACTICE.md), 배포 목록은 [다운로드](../downloads/README.md)다.

1. 기존 노트북 생성 소스를 수정했다면 `python scripts/build_jupyter_book.py`로 갱신한다.
2. `python scripts/build_lab_downloads.py`로 장별 ZIP 12개, 전체 ZIP, 다운로드 표와 해시 목록을 갱신한다.
3. `python scripts/build_lab_downloads.py --check`와 `python tests/test_lab_downloads.py`로 파일 누락·해시·결정적 생성·코드 동일성·다운로드 연결을 확인한다.
4. `python tests/test_lab_downloads.py --execute`로 새 임시 폴더에 전체 ZIP을 풀어 23개 노트북을 처음부터 실행한다. Jupyter Python 커널과 해당 실습의 Linux 도구가 준비된 환경에서 실행한다.
5. `python scripts/validate_course.py`로 교안 링크·문법 원본 보존·노트북 생성 소스 일치를 검사한다.

07장 권한 실험은 Linux 일반 사용자 환경에서 `python tests/test_gtfobins_lab.py`로 별도 검증한다. `--render-dir /tmp/검토폴더`를 지정하면 실행본을 로컬 검토용으로 저장한다. nbconvert가 있는 검토 환경에서 `jupyter nbconvert --to html 실행본.ipynb`로 변환해 표시를 확인한다. 실행본은 배포하지 않는다. root 실행 Colab 및 macOS는 이 확장 실험의 실행 대상이 아니다.

장별 기본/보안 노트북 매핑은 `build_lab_downloads.py`의 CHAPTERS에서 관리한다. ZIP은 허용된 노트북·설치 목록·시작 안내만 넣으며 로컬 실행 결과, 가상환경, 개인 풀이, 인증 파일은 수집하지 않는다. 노트북 코드 셀과 입력 자료는 원본 그대로 보존하고, 배포본의 상대 Markdown 링크만 온라인 저장소 링크로 바꾼다.

ZIP 타임스탬프와 정렬은 고정한다. MANIFEST.json의 자료 버전은 포함 파일 내용에서 계산하며, 설치 패키지 버전 잠금을 뜻하지 않는다. downloads/README.md와 index.json은 자동 생성 파일이므로 직접 수정하지 않는다. 생성한 배포 파일과 소스를 함께 커밋한다.
