# 02-3. Jupyter에서 재현 가능한 조사 실습하기

## 목표

새 커널에서 위에서 아래로 실행되는 조사 기록을 만듭니다. 이전 셀의 숨은 상태가 필요하거나 개인 서버 정보가 출력에 남으면 공유용 실습으로 적합하지 않습니다.

## Python 커널과 Bash 셀

이 과정은 Python 커널의 `%%bash`를 사용합니다. 셀마다 새 Bash가 시작하므로 첫 셀의 cd·일반 변수는 다음 Bash 셀에 남지 않습니다. Python 환경 변수 `COURSE_DATA`, `COURSE_OUT`과 파일로 상태를 명시합니다.

```text
Setup: 새 결과 디렉터리·합성 자료 준비
→ Bash 셀 1: 출처 확인
→ Bash 셀 2: 사본 비교
→ Checks: 원본 해시·결과 검증
```

## 시작 전 안전 확인

코드를 먼저 읽고 기본 로컬 접속 범위에서 Jupyter를 사용합니다. 서버 토큰·비밀번호를 끄지 않습니다. 가상환경은 OS 샌드박스가 아닙니다. 실제 운영 증거·인증정보를 온라인 노트북에 업로드하지 않습니다.

## 기대 결과의 종류

| 종류 | 평가 | 예 |
|---|---|---|
| 합성 자료 | 정확한 값 | partial, 실패 3건 |
| 자기 환경 | 구조·의미 | Bash 버전·KST 시각 |
| 오류 사례 | 상태·stderr | 없는 파일·잘못된 인수 |
| 보존 | 실행 전후 해시 | 입력 내용 미변경 |

### Bash Point — 실패를 확인하기

```bash
set -euo pipefail
test -r "$COURSE_DATA/provenance.txt"
grep -Fx 'source_type=synthetic' "$COURSE_DATA/provenance.txt"
```

예상 자료가 없으면 그냥 지나치지 않습니다. 다만 set -e는 모든 문맥에서 원하는 실패 정책을 자동 보장하지 않습니다. 예상 실패는 if 또는 상태 변수로 직접 처리하고 세부 예외는 09장에서 다룹니다.

## 실패 사례

- 셀 중간부터 실행해 경로가 없으면 Setup부터 다시 실행합니다.
- 기존 결과를 새 결과로 오인하지 않도록 매 실행마다 새 폴더를 씁니다.
- 오류 출력만 지우지 말고 예상 실패인지 코드 결함인지 구분합니다.
- 공개할 때 실행 출력을 비우고 교육용 기대값만 설명 셀에 남깁니다.

## 실습·질문·완료 기준

실습 목록의 02장 보안 실습을 새 커널에서 전체 실행합니다. 원본 해시와 각 STEP 검사를 확인합니다. 결과는 임시 폴더에 남지만 장기 보존을 보장하지 않습니다.

실행 환경, 재실행 여부, 예상·실제 결과, 누락을 제출합니다. 모든 셀이 성공했다는 사실이 침해 판단까지 맞다는 뜻은 아닙니다. 두 Bash 셀 사이에 어떤 값이 유지되는지, 왜 실제 호스트 정보를 그대로 공개하면 안 되는지 설명하면 완료입니다.

다음 03장은 IOC 표식 검색으로 인수·인용·조건·반복을 학습합니다.

## 참고 자료

- [IPython script magics](https://ipython.readthedocs.io/en/stable/interactive/magics.html#cellmagic-script)
- [Jupyter Server security](https://jupyter-server.readthedocs.io/en/latest/operators/security.html)
