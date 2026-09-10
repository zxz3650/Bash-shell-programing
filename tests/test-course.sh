#!/usr/bin/env bash
# Behavior tests use only synthetic fixtures and an isolated temporary directory.
set -uo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P) || exit 1
report="$root/examples/log-report/bin/log-report.sh"
parallel="$root/examples/parallel/run-workers.sh"
fixture="$root/examples/log-report/fixtures/events.log"
expected="$root/examples/log-report/fixtures/expected.tsv"
work=$(mktemp -d) || exit 1
trap 'rm -rf -- "$work"' EXIT
passed=0
fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
pass() { passed=$((passed + 1)); printf 'PASS: %s\n' "$*"; }
expect_status() {
    local expected_status=$1 status=0
    shift
    "$@" > "$work/stdout" 2> "$work/stderr" || status=$?
    [[ $status == "$expected_status" ]] || fail "expected=$expected_status actual=$status command=$1"
}

expect_status 0 bash "$report" --help
grep -q '^usage:' "$work/stdout" || fail 'help text'
pass 'help contract'
expect_status 2 bash "$report"
[[ -s $work/stderr ]] || fail 'usage diagnostic'
pass 'missing arguments'
expect_status 2 bash "$report" --input
pass 'missing option value'
expect_status 2 bash "$report" --unknown
pass 'unknown option'
expect_status 2 bash "$report" --input "$fixture" --input "$fixture" --output "$work/duplicate.tsv"
[[ ! -e $work/duplicate.tsv ]] || fail 'duplicate option created output'
pass 'duplicate input rejected'
expect_status 0 bash "$report" --input "$fixture" --output "$work/dry.tsv" --dry-run
[[ ! -e $work/dry.tsv ]] || fail 'dry-run created output'
pass 'dry-run no output'
expect_status 0 bash "$report" --input "$fixture" --output "$work/report.tsv"
cmp -s "$expected" "$work/report.tsv" || fail 'summary values'
[[ ! -s $work/stdout ]] || fail 'stdout contaminated'
pass 'exact summary and clean stdout'
expect_status 1 bash "$report" --input "$fixture" --output "$work/report.tsv"
cmp -s "$expected" "$work/report.tsv" || fail 'existing output changed'
pass 'existing output preserved'
expect_status 1 bash "$report" --input "$work/missing" --output "$work/missing.tsv"
[[ ! -e $work/missing.tsv ]] || fail 'missing input published'
pass 'missing input'
printf 'INFO api\nBROKEN\n' > "$work/bad.log"
expect_status 1 bash "$report" --input "$work/bad.log" --output "$work/bad.tsv"
[[ ! -e $work/bad.tsv ]] || fail 'malformed input published'
grep -q 'line 2' "$work/stderr" || fail 'missing bad line number'
pass 'malformed record is not published'
expect_status 1 bash "$report" --input "$work/bad.log" --output "$work/bad-dry.tsv" --dry-run
[[ ! -e $work/bad-dry.tsv ]] || fail 'bad dry-run output'
pass 'dry-run validates records'
touch "$work/empty.log"
expect_status 0 bash "$report" --input "$work/empty.log" --output "$work/empty.tsv"
printf 'level\tcount\nINFO\t0\nWARN\t0\nERROR\t0\n' > "$work/empty-expected.tsv"
cmp -s "$work/empty-expected.tsv" "$work/empty.tsv" || fail 'empty summary'
pass 'empty input is explicit zero summary'
cp "$fixture" "$work/two words.log"
expect_status 0 bash "$report" --input "$work/two words.log" --output "$work/two words.tsv"
cmp -s "$expected" "$work/two words.tsv" || fail 'space path'
pass 'space path'
printf 'ERROR api' > "$work/no-newline.log"
expect_status 0 bash "$report" --input "$work/no-newline.log" --output "$work/no-newline.tsv"
grep -q $'ERROR\t1' "$work/no-newline.tsv" || fail 'last record lost'
pass 'last record without newline'
ln -s "$work/nonexistent-target" "$work/link.tsv"
expect_status 1 bash "$report" --input "$fixture" --output "$work/link.tsv"
[[ -L $work/link.tsv && ! -e $work/nonexistent-target ]] || fail 'symlink changed'
pass 'dangling output symlink rejected'
expect_status 1 bash "$report" --input "$fixture" --output "$work/no-parent/report.tsv"
pass 'missing output parent'
for jobs in 1 2 4; do
    expect_status 0 bash "$parallel" "$jobs" "$fixture" "$work/two words.log" "$work/empty.log"
    printf '1\t5\n2\t5\n3\t0\n' > "$work/parallel-expected.tsv"
    cmp -s "$work/parallel-expected.tsv" "$work/stdout" || fail "ordered parallel jobs=$jobs"
done
pass 'parallel serial-equivalent output at 1 2 4 workers'
expect_status 1 bash "$parallel" 2 "$fixture" "$work/missing"
[[ ! -s $work/stdout ]] || fail 'partial parallel report emitted'
pass 'parallel failures propagated'
expect_status 2 bash "$parallel" 0 "$fixture"
pass 'worker bound validation'
cmp -s "$fixture" "$work/two words.log" || fail 'input changed'
pass 'source preserved'
if find "$work" -name '.log-report.*' | grep -q .; then
    fail 'temporary report leaked'
fi
pass 'temporary report cleanup'
bash "$root/tests/test-first-observation.sh" || fail 'first observation checks'
pass 'first observation companion'
printf 'All %s behavior checks passed.\n' "$passed"
