# 06-2. 백그라운드 작업·시그널·정리

명령 뒤의 &는 기다리지 않고 다음 단계로 진행하게 한다. 작업을 시작했다는 사실은 성공적으로 끝났다는 뜻이 아니다. PID와 wait를 통해 완료와 결과를 회수한다.

{% hint style="info" %}
### 🧭 학습 목표

- `$!`로 자식 PID를 저장한다.
- wait의 결과를 회수한다.
- INT·TERM·EXIT의 역할을 구분한다.
- 자신이 생성한 자원만 정리한다.
{% endhint %}

## 0. 학습 전 확인

백그라운드 명령 바로 다음의 `$?`는 자식의 최종 결과인가? SIGKILL에도 trap이 실행되는가?

## 1. 완료 회수

```bash
bash -c 'exit 7' &
worker_pid=$!
if wait "$worker_pid"; then
    printf 'worker succeeded\n'
else
    status=$?
    printf 'worker failed=%s\n' "$status"
fi
```

결과는 worker failed=7이다. wait가 없으면 실패를 놓치기 쉽다. 부모가 직접 시작한 자식을 추적하고, 모르는 PID에 명령을 보내지 않는다.

## 2. 종료 요청 관찰

```bash
sleep 30 &
worker_pid=$!
kill -TERM "$worker_pid"
if wait "$worker_pid"; then
    printf 'completed\n'
else
    printf 'terminated status=%s\n' "$?"
fi
```

위 코드는 바로 만든 sleep에만 TERM을 보낸다. Bash에서는 시그널 종료 상태를 보통 128+시그널 번호로 표현한다. TERM은 15여서 보통 143이다. 프로그램 자체가 0이 아닌 종료 상태로 종료한 경우와 원인을 함께 확인한다.

## 3. 임시 파일과 trap

다음을 `cleanup-demo.sh`로 저장한다.

```bash
#!/usr/bin/env bash
temporary=$(mktemp) || exit 1
cleanup() {
    local status=$?
    rm -f -- "$temporary"
    return "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
printf 'temporary=%s\n' "$temporary"
printf 'ready\n' > "$temporary"
sleep 10
```

정상 종료와 Ctrl+C 후 표시한 임시 파일이 사라지는지 확인한다. cleanup은 진입 시 상태를 저장한다. 정리 과정의 성공으로 원래 실패가 덮이지 않아야 한다.

## 4. 한계와 설계

EXIT는 실제 OS 시그널이 아니라 셸 종료 훅이다. SIGKILL과 전원 장애에서는 정리 코드를 실행할 수 없다. 자식 프로세스가 있는 스크립트라면 임시 파일뿐 아니라 자식 종료와 wait도 설계해야 한다. 한 PID 종료가 전체 자손 트리 종료를 보장하지는 않는다.

## 🧪 직접 해보기

1. 상태 0과 7로 끝나는 자식을 각각 시작하고 wait한다.
2. cleanup-demo의 정상 종료와 Ctrl+C 결과를 비교한다.
3. cleanup에 진단 출력을 추가하고 원래 종료 상태가 유지되는지 확인한다.

### 해설

“백그라운드 시작 성공”, “작업 완료”, “자원 회수”는 별도 단계다. 어떤 단계가 끝났는지 로그에 정확히 기록한다.

## ✅ 완료 기준

- [ ] 모든 직접 자식의 결과를 회수한다.
- [ ] cleanup이 원래 상태를 보존한다.
- [ ] trap이 실행되지 않는 종료 상황을 설명한다.

다음: [07. 안전한 Shell Script](../07-secure-scripting.md)
