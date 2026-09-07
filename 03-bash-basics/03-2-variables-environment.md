# 03-2. 변수와 환경 변수

Bash의 일반 변수는 기본적으로 문자열을 보관한다. `count=10`은 Python의 정수 객체 생성과 같지 않다. 계산 문맥에서 값을 산술식으로 해석한다. 일반 변수, 환경 변수, 위치 인자는 전달 범위가 다르다.

{% hint style="info" %}
### 🧭 학습 목표

- 대입과 명령 호출 문법을 구분한다.
- 빈 문자열과 설정되지 않은 변수를 구분한다.
- 부모·자식 사이의 환경 전달을 관찰한다.
- 환경 설정과 비밀정보를 구분한다.
{% endhint %}

## 선행 지식과 연결

[03-1](03-1-execution-model.md)의 명령과 인수를 사용한다. 실습은 [노트북 02](../jupyter-book/labs/02-arguments-variables-arrays.ipynb)와 연결된다.

## 0. 학습 전 확인

`name=student`와 `name = student`는 같은가? 자식 Bash에서 변수를 바꾸면 부모도 바뀌는가?

## 1. 대입 문법

```bash
course='Shell Programming'
count=10
printf 'course=%s, count=%s\n' "$course" "$count"
```

`course = value`라고 쓰면 셸은 course라는 명령에 `=`와 value라는 인수를 전달하려 한다. 이름은 영문자·숫자·밑줄로 구성하되 숫자로 시작하지 않는다. 대소문자도 구분한다.

`$name`은 값을 사용하고 `name=value`는 값을 설정한다. 값 확인에는 printf를 사용한다.

## 2. 미설정과 빈 값

```bash
unset lab_label
printf 'unset=%s\n' "${lab_label-default}"
lab_label=''
printf 'empty=%s\n' "${lab_label-default}"
printf 'empty-or-unset=%s\n' "${lab_label:-default}"
```

```text
unset=default
empty=
empty-or-unset=default
```

콜론이 있는 `:-`는 미설정과 빈 문자열을 모두 기본값으로 처리한다. 콜론 없는 `-`는 미설정만 처리한다. 빈 값을 명시했는지 구분해야 하는 설정에서 중요하다.

## 3. export와 자식 프로세스

```bash
lab_local='parent only'
export LAB_SHARED='initial'
bash -c 'printf "local=<%s> shared=<%s>\n" "${lab_local-unset}" "$LAB_SHARED"'
bash -c 'LAB_SHARED=child; printf "child=%s\n" "$LAB_SHARED"'
printf 'parent=%s\n' "$LAB_SHARED"
```

자식의 첫 출력에서 lab_local은 unset, LAB_SHARED는 initial이다. 자식이 바꿔도 부모의 마지막 출력은 initial이다. 환경은 시작 시 전달되는 사본이며 양방향 공유 메모리가 아니다.

```text
부모의 export된 값 → 자식 시작 시 사본 전달 → 자식 변경은 부모에 반영되지 않음
```

## 4. 한 명령에만 환경 지정

```bash
unset LAB_MODE
LAB_MODE=demo bash -c 'printf "child=%s\n" "$LAB_MODE"'
printf 'parent=%s\n' "${LAB_MODE-unset}"
```

마지막 출력은 unset이다. 테스트·로케일·로그 수준을 한 번만 바꿀 때 유용하다.

## 5. readonly와 이름 선택

```bash
readonly course_version='1'
printf '%s\n' "$course_version"
```

readonly는 이후 재대입을 막는다. PATH, HOME, SHELL, IFS처럼 셸 동작에 영향을 주는 이름을 업무 변수로 재사용하지 않는다. `lab_dir`, `input_file`, `report_path`처럼 목적을 표현한다.

## 실패 사례와 해석

export는 비밀 보호 기능이 아니라 자식에게 전달하는 기능이다. env 전체 출력이나 set -x는 환경과 확장된 인수를 노출할 수 있다. 필요한 이름만 확인한다.

`source config.sh`는 설정 읽기가 아니라 현재 셸에서 코드 실행이다. 설정 경계는 [07-1](../07-secure-scripting/07-1-input-boundaries.md)에서 다룬다.

## 🧪 직접 해보기

1. 미설정·빈 문자열·debug에 대해 `${LAB_LEVEL:-info}`를 예측한다.
2. 일반 변수와 export 변수를 자식에 전달한다.
3. 자식에서 수정한 뒤 부모 값이 유지되는지 확인한다.

### 해설

기본값 결과는 info, info, debug다. 부모와 자식의 출력을 함께 기록해야 전달 방향을 검증할 수 있다.

## ✅ 완료 기준

- [ ] 대입 주변 공백이 오류가 되는 이유를 설명한다.
- [ ] 미설정과 빈 값에 맞는 기본값 문법을 선택한다.
- [ ] export의 방향과 범위를 설명한다.

다음: [03-3. 인용과 확장](03-3-quoting-expansion.md)
