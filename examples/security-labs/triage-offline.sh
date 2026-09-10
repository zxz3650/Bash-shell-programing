#!/usr/bin/env bash
# Collect a fixed allowlist of classroom evidence copies; no live host queries.
set -u
usage() { printf 'usage: bash triage-offline.sh -d DATA_DIR -o NEW_OUTPUT_DIR [-n]\n' >&2; }
data_dir='' output_dir='' dry_run=0 seen_data=0 seen_output=0
while getopts ':d:o:n' option; do
    case $option in
        d) (( seen_data == 0 )) || { usage; exit 2; }; data_dir=$OPTARG; seen_data=1 ;;
        o) (( seen_output == 0 )) || { usage; exit 2; }; output_dir=$OPTARG; seen_output=1 ;;
        n) dry_run=1 ;;
        *) usage; exit 2 ;;
    esac
done
shift "$((OPTIND - 1))"
if (( $# || !seen_data || !seen_output )) || [[ -z $data_dir || -z $output_dir ]]; then usage; exit 2; fi
if [[ ! -d $data_dir || -L $data_dir || -e $output_dir || -L $output_dir ]]; then
    printf 'invalid source directory or output already exists\n' >&2; exit 2
fi
for required in provenance.txt auth.log; do
    if [[ ! -f $data_dir/$required || ! -r $data_dir/$required || -L $data_dir/$required ]]; then
        printf 'required input unavailable: %s\n' "$required" >&2; exit 2
    fi
done
command -v python3 >/dev/null || { printf 'python3 required\n' >&2; exit 2; }
python3 - "$data_dir" "$output_dir" <<'PY' || exit 2
from pathlib import Path
import sys
source, destination = (Path(value).resolve() for value in sys.argv[1:])
if source == destination or source in destination.parents:
    print('output must be outside the source directory', file=sys.stderr)
    raise SystemExit(1)
PY
if (( dry_run )); then
    printf 'dry_run=validated required inputs; optional availability checked during collection\n'
    exit 0
fi
observed_at=$(TZ=Asia/Seoul date '+%Y-%m-%dT%H:%M:%S%z') || exit 2
case $observed_at in *+0900) ;; *) printf 'Asia/Seoul tzdata required\n' >&2; exit 2 ;; esac
umask 077
mkdir -- "$output_dir" || exit 2
printf 'category\tfile\tstatus\n' > "$output_dir/manifest.tsv" || exit 1
partial=0
collect_file() {
    local category=$1 name=$2 status
    if [[ ! -f $data_dir/$name || ! -r $data_dir/$name || -L $data_dir/$name ]]; then
        status=unavailable; partial=1
    elif cp -- "$data_dir/$name" "$output_dir/$name"; then
        status=copied
    else
        status=failed; partial=1
    fi
    printf '%s\t%s\t%s\n' "$category" "$name" "$status" >> "$output_dir/manifest.tsv" || return 1
}
collect_system() { collect_file system provenance.txt; }
collect_users() { collect_file users passwd.sample && collect_file permissions permissions.psv; }
collect_processes() { collect_file process processes.psv; }
collect_network() { collect_file network sockets.psv; }
collect_persistence() {
    collect_file persistence persistence.psv && collect_file persistence service-review.txt
}
collect_logs() {
    local name
    for name in auth.log login-review.psv journal-review.psv audit.log access.log; do
        collect_file logs "$name" || return 1
    done
}
collect_system && collect_users && collect_processes && collect_network && collect_persistence && collect_logs || exit 1
printf 'source_type=offline_classroom_copy\ncollected_at_kst=%s\n' "$observed_at" > "$output_dir/context.txt" || exit 1
if (( partial )); then completion=partial; else completion=complete; fi
printf 'collection_status=%s\n' "$completion" >> "$output_dir/context.txt" || exit 1
python3 - "$output_dir" <<'PY' || exit 1
import hashlib
from pathlib import Path
import sys
directory = Path(sys.argv[1])
lines = [f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n'
         for p in sorted(directory.iterdir()) if p.is_file()]
with (directory / 'SHA256SUMS').open('x', encoding='utf-8') as stream:
    stream.writelines(lines)
PY
printf '%s\n' "$completion" > "$output_dir/COLLECTION_FINISHED" || exit 1
printf 'collection_status=%s\n' "$completion"
exit "$partial"
