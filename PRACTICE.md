# 실습 자료 받기와 시작하기

**교안을 읽으며 직접 실행할 수 있도록 학습용 Jupyter 노트북을 제공합니다.** 수강할 장만 받거나, 전체 23개 노트북을 한 번에 받을 수 있습니다.

[장별 실습 ZIP 선택하기](downloads/README.md) · [전체 실습 ZIP 바로 받기](https://github.com/zxz3650/Bash-shell-programing/raw/refs/heads/master/downloads/all-labs.zip)

## 1. 다운로드하고 압축 풀기

1. 위 링크에서 ZIP을 받습니다. Git이나 GitHub 계정은 필요하지 않습니다.
2. ZIP을 새 폴더에 압축 해제합니다. `bash-chapter-03-자료버전/`처럼 장 번호와 버전이 붙은 폴더가 만들어집니다.
3. 폴더 안의 `START-HERE.md`를 읽습니다. 해당 장에서 실행할 노트북 순서가 적혀 있습니다.

ZIP에는 `.ipynb` 노트북, 패키지 설치 목록, 시작 안내, 파일별 해시가 들어 있습니다. 예제 코드와 합성 입력 자료는 노트북에 포함되어 있으므로 따로 복사하지 않습니다. 교안 본문과 터미널 프로젝트 전체 소스, 완성된 HTML 웹사이트는 이 ZIP에 포함되지 않습니다.

## 2. JupyterLab 시작하기

기준 환경은 **Ubuntu VM 또는 WSL2 Ubuntu, Python 3.10 이상, Bash**입니다. Windows 사용자는 PowerShell이 아니라 Ubuntu 터미널에서 아래 명령을 실행합니다. 자세한 환경 준비는 [02장](02-bash-setup.md)을 따릅니다. macOS에서도 기본 문법 노트북을 실행할 수 있지만 Linux 전용 조사 명령과 출력은 다를 수 있습니다.

압축을 푼 폴더 중 `requirements.txt`와 `START-HERE.md`가 있는 위치에서 터미널을 열고 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

패키지 최초 설치에는 인터넷 연결이 필요합니다. Ubuntu에서 `venv`를 만들 수 없다면 교육용 VM에 `python3-venv`가 준비되어 있는지 확인합니다. JupyterLab은 일반 사용자로 실행하고, 접속 토큰이나 주소를 다른 사람에게 공유하거나 서버를 외부에 공개하지 않습니다.

## 3. 노트북 열고 실습하기

1. 브라우저에 열린 JupyterLab 왼쪽 파일 목록에서 `notebooks/`를 엽니다.
2. `START-HERE.md`에 표시된 첫 `.ipynb` 파일을 엽니다. 처음 학습한다면 01장 ZIP의 `00-orientation-and-safety.ipynb`부터 시작합니다.
3. 커널은 **Python 3**를 선택합니다. 별도의 Bash 커널은 필요하지 않습니다.
4. 목표를 읽고 Setup부터 **Shift+Enter**로 위에서 아래로 실행합니다. `%%bash`는 지우지 않습니다.
5. 예상 결과와 자신의 출력을 비교하고 Checks를 확인합니다. 기본 문법 실습 후 같은 장의 `security-` 노트북을 진행합니다.
6. 다시 검증할 때는 커널을 재시작하고 처음부터 실행합니다. Cleanup 셀을 실행하기 전에 필요한 결과를 보관합니다.

JupyterLab은 노트북을 실행하는 도구이고, 이 과정의 Jupyter Book은 실습을 엮은 교재입니다. **ZIP만 압축 해제한다고 웹페이지가 실행되지는 않습니다.** 위 명령으로 JupyterLab을 시작한 뒤 `.ipynb`를 열어야 합니다.

## 4. 개인 풀이 보관하기

노트북을 다른 이름으로 복사하여 풀이를 저장합니다. 실습에서 만든 임시 디렉터리는 정리 셀 실행이나 시스템 정리로 없어질 수 있으므로, 제출할 결과는 별도 보관 폴더에 저장합니다. 원본 증거 파일은 수정하지 않습니다.

[다운로드 목록](downloads/README.md)의 자료 버전과 받은 폴더의 `MANIFEST.json`을 비교합니다. 버전이 달라지면 새 ZIP을 **새 폴더에** 풀고 개인 풀이를 옮깁니다. 기존 풀이 위에 압축을 풀지 않습니다.

## 막히기 쉬운 부분

| 증상 | 확인할 내용 |
| --- | --- |
| ZIP을 열었는데 실행 버튼이 없음 | 압축 해제 후 터미널에서 `jupyter lab`을 실행합니다. |
| `requirements.txt`를 찾을 수 없음 | 한 단계 안쪽의 START-HERE.md가 있는 폴더에서 실행합니다. |
| `%%bash`가 오류로 표시됨 | Python 3 커널인지, Bash가 설치되어 있는지 확인합니다. 셀 첫 줄의 매직 명령을 유지합니다. |
| 이전 셀에서 만든 변수가 없어짐 | 각 `%%bash` 셀은 새 프로세스입니다. Setup 셀의 환경 변수·파일을 통한 전달 방식을 따릅니다. |
| `BASH_LAB_DIR`가 없거나 입력 파일을 찾지 못함 | Setup부터 실행했는지, Cleanup 후 뒤쪽 셀만 다시 실행하지 않았는지 확인합니다. |
| systemd·audit 로그 관련 명령을 실행할 수 없음 | 합성 자료를 쓰는 노트북과 실제 Ubuntu VM에서 수행하는 선택 실습을 구분합니다. |

설치가 어려운 경우 [실습 목록](jupyter-book/labs/README.md)의 Colab 링크를 대안으로 사용할 수 있습니다. 로컬 저장·Linux VM 실습을 포함한 수업에서는 위 ZIP 경로를 기준으로 진행합니다.

참고: [JupyterLab 공식 실행 안내](https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html)
