#!/usr/bin/env bash
# Synthetic data, local self-observation and temporary command doubles only.
set -uo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P) || exit 1
observer="$root/examples/first-observation/observe-context.sh"
bash_bin=$(command -v bash) || exit 1
work=$(mktemp -d) || exit 1
trap 'rm -rf -- "$work"' EXIT
passed=0
fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
pass() { passed=$((passed + 1)); printf 'PASS: %s\n' "$*"; }
expect_status() {
    local wanted=$1 actual=0
    shift
    "$@" > "$work/out" 2> "$work/err" || actual=$?
    [[ $actual == "$wanted" ]] || fail "expected status=$wanted actual=$actual"
}

expect_status 0 "$bash_bin" "$observer"
for field in source_type observed_at_kst display_timezone host os kernel effective_uid effective_gid bash_version shell_pid shell_ppid process_pid_ppid_comm collection_status; do
    grep -q "^$field=." "$work/out" || fail "missing field: $field"
done
[[ ! -s $work/err ]] || fail 'normal observation emitted errors'
grep -q '^source_type=live_self$' "$work/out" || fail 'source type'
pass 'self-context structure and separated streams'
grep -Eq '^observed_at_kst=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\+0900$' "$work/out" || fail 'KST offset'
grep -Fq 'display_timezone=Asia/Seoul (UTC+09:00)' "$work/out" || fail 'timezone label'
pass 'KST timestamp and timezone label'
expect_status 2 "$bash_bin" "$observer" 'unexpected argument'
[[ ! -s $work/out && -s $work/err ]] || fail 'usage streams'
pass 'unexpected arguments rejected'

mkdir "$work/failing" "$work/wrong-zone" "$work/empty" || exit 1
printf '#!/bin/sh\nexit 7\n' > "$work/failing/uname"
printf '#!/bin/sh\nprintf "2026-09-10T00:00:00+0000\\n"\n' > "$work/wrong-zone/date"
printf '#!/bin/sh\nexit 0\n' > "$work/empty/hostname"
chmod 700 "$work/failing/uname" "$work/wrong-zone/date" "$work/empty/hostname"
probe_status=0
"$work/failing/uname" > "$work/probe-out" 2> "$work/probe-err" || probe_status=$?
[[ $probe_status == 7 ]] || fail 'temporary directory must allow execution of test doubles (check noexec)'
expect_status 1 env PATH="$work/failing:$PATH" "$bash_bin" "$observer"
[[ ! -s $work/out ]] || fail 'failed collection emitted report'
grep -q 'uname -s' "$work/err" || fail 'failed command not identified'
pass 'collection failure is not a completed report'
expect_status 1 env PATH="$work/wrong-zone:$PATH" "$bash_bin" "$observer"
[[ ! -s $work/out ]] || fail 'wrong timezone emitted report'
grep -q 'offset' "$work/err" || fail 'timezone failure not explained'
pass 'wrong timezone rejected'
expect_status 1 env PATH="$work/empty:$PATH" "$bash_bin" "$observer"
[[ ! -s $work/out ]] || fail 'empty required data emitted report'
pass 'empty required observation rejected'

value='case 01'
printf '<%s>\n' "$value" > "$work/quoted"
printf '<case 01>\n' > "$work/quoted-expected"
cmp -s "$work/quoted" "$work/quoted-expected" || fail 'quoting'
pass 'quoted label keeps its boundary'
expect_status 7 "$bash_bin" -c 'printf "data\n"; printf "diagnostic\n" >&2; exit 7'
[[ $(< "$work/out") == data && $(< "$work/err") == diagnostic ]] || fail 'stream contents'
pass 'stdout stderr and failure are independent'

printf 'original\n' > "$work/existing"
# shellcheck disable=SC2016 # $1 is deliberately expanded by the child Bash.
expect_status 1 "$bash_bin" -c 'set -C; printf "replacement\n" > "$1"' bash "$work/existing"
[[ $(< "$work/existing") == original ]] || fail 'existing result overwritten'
pass 'noclobber preserves existing regular file'
fixture="$root/examples/first-observation/fixtures/case.txt"
grep -q '^source_type=synthetic$' "$fixture" || fail 'fixture provenance'
grep -q '^audit_coverage=unknown$' "$fixture" || fail 'fixture limitation'
grep -q '^observed_at=2026-09-10T09:00:00+09:00$' "$fixture" || fail 'fixture time'
pass 'fixture distinguishes provenance and unknown coverage'
printf 'All %s first-observation checks passed.\n' "$passed"
