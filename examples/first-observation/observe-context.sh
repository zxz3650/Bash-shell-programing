#!/usr/bin/env bash
# Chapter 01: local self-context only; no network, sudo, or filesystem writes.
# stdout: human-readable observation. stderr: errors. Status: 0/1/2.
set -u

if (( $# != 0 )); then
    printf 'usage: bash observe-context.sh\n' >&2
    exit 2
fi

observed_at=$(TZ=Asia/Seoul date '+%Y-%m-%dT%H:%M:%S%z') || {
    printf 'observation failed: date\n' >&2
    exit 1
}
case $observed_at in
    *+0900) ;;
    *) printf 'observation failed: Asia/Seoul offset is not +0900\n' >&2; exit 1 ;;
esac
host_name=$(hostname) || { printf 'observation failed: hostname\n' >&2; exit 1; }
os_name=$(uname -s) || { printf 'observation failed: uname -s\n' >&2; exit 1; }
kernel_release=$(uname -r) || { printf 'observation failed: uname -r\n' >&2; exit 1; }
user_id=$(id -u) || { printf 'observation failed: id -u\n' >&2; exit 1; }
group_id=$(id -g) || { printf 'observation failed: id -g\n' >&2; exit 1; }
process_info=$(ps -p "$$" -o pid=,ppid=,comm=) || {
    printf 'observation failed: ps\n' >&2
    exit 1
}
if [[ -z $host_name || -z $os_name || -z $kernel_release || -z $process_info ]]; then
    printf 'observation failed: required output is empty\n' >&2
    exit 1
fi
if [[ ! $user_id =~ ^[0-9]+$ || ! $group_id =~ ^[0-9]+$ ]]; then
    printf 'observation failed: numeric UID/GID required\n' >&2
    exit 1
fi

# Buffering these small values prevents an earlier collection failure from
# emitting a report marked complete. This is not a system-wide atomic snapshot.
printf 'source_type=live_self\n'
printf 'observed_at_kst=%s\n' "$observed_at"
printf 'display_timezone=Asia/Seoul (UTC+09:00)\n'
printf 'host=%s\nos=%s\nkernel=%s\n' "$host_name" "$os_name" "$kernel_release"
printf 'effective_uid=%s\neffective_gid=%s\n' "$user_id" "$group_id"
printf 'bash_version=%s\nshell_pid=%s\nshell_ppid=%s\n' "$BASH_VERSION" "$$" "$PPID"
printf 'process_pid_ppid_comm=%s\n' "$process_info"
printf 'collection_status=complete\n'
