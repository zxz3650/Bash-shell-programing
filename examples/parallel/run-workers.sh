#!/usr/bin/env bash
# Bounded batches, Bash 3.2+. stdout: input index and newline count, in input order.
set -o pipefail

usage() { printf 'usage: run-workers.sh JOBS FILE...\n' >&2; }
(( $# >= 2 )) || { usage; exit 2; }
[[ $1 =~ ^[1-8]$ ]] || { usage; exit 2; }
jobs=$1
shift
work_dir=$(mktemp -d) || exit 1
pids=()
cleanup() {
    local status=$? pid
    # Active entries are only children started by this script, not arbitrary PIDs.
    for pid in "${pids[@]}"; do
        kill -TERM "$pid" 2>/dev/null || :
    done
    for pid in "${pids[@]}"; do
        wait "$pid" 2>/dev/null || :
    done
    rm -rf -- "$work_dir"
    return "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

wait_batch() {
    local index status=0 pid
    for index in "${!pids[@]}"; do
        pid=${pids[$index]}
        wait "$pid" || status=1
        unset 'pids[index]'
    done
    pids=()
    return "$status"
}

index=0
failed=0
for input in "$@"; do
    index=$((index + 1))
    (
        [[ -f $input && -r $input ]] || exit 1
        wc -l < "$input" > "$work_dir/$index.txt"
    ) &
    pids+=("$!")
    if (( ${#pids[@]} >= jobs )); then
        wait_batch || failed=1
    fi
done
wait_batch || failed=1
if (( failed != 0 )); then
    printf 'one or more inputs failed; no merged result emitted\n' >&2
    exit 1
fi
for ((item=1; item<=index; item++)); do
    count=$(< "$work_dir/$item.txt")
    printf '%s\t%d\n' "$item" "$count"
done
