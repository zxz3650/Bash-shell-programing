"""Mirror the reviewed non-privileged boundary experiments into chapter 07."""
import re


def build_gtfobins_cells(md, code, root):
    page = root / '07-secure-scripting/07-4-gtfobins-review.md'
    text = page.read_text(encoding='utf-8')
    section = text.split('<!-- gtfo-notebook:start -->', 1)[1].split('<!-- gtfo-notebook:end -->', 1)[0]
    impact = '## 기능이 악용되면 어떤 영향이 생기는가' + text.split('## 기능이 악용되면 어떤 영향이 생기는가', 1)[1].split('## 확장 실습 환경', 1)[0]
    cells = [md(impact), md('## 확장 실험 Setup\n\nUbuntu 일반 사용자 환경에서 실행합니다. '
                'root로 동작하는 Colab에서는 이 실험을 실행하지 않습니다. '
                'sudo·SUID·Capability 부여 없이 자신의 더미 파일만 사용합니다. '
                '앞의 Setup부터 실행한 뒤 아래 셀을 실행하세요. 결과는 COURSE_OUT 안의 새 폴더에 남습니다.'),
             code("import os\nimport platform\nimport tempfile\n"
                  "if platform.system() != 'Linux' or os.geteuid() == 0:\n"
                  "    raise RuntimeError('이 확장 실험은 Ubuntu 일반 사용자 환경에서 실행하세요.')\n"
                  "os.environ['GTFO_LAB'] = tempfile.mkdtemp(prefix='gtfo-boundary-', dir=os.environ['COURSE_OUT'])\n"
                  "print('GTFO 실습용 임시 폴더 준비 완료')")]
    parts = re.split(r'^```bash\n(.*?)^```\s*$', section, flags=re.M | re.S)
    for number, part in enumerate(parts):
        if not part.strip():
            continue
        cells.append(code('%%bash\n' + part) if number % 2 else md(part))
    assert sum(c['cell_type'] == 'code' for c in cells) == 7
    return cells
