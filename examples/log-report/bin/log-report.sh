#!/usr/bin/env bash
# Bash 3.2+, Linux/macOS. Input is never changed; output must be a new file.
set -uo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P) || exit 1
# shellcheck source=examples/log-report/lib/report.sh
source "$script_dir/../lib/report.sh" || exit 1

usage() {
    printf 'usage: log-report.sh --input FILE --output FILE [--dry-run]\n'
}

temporary=''
cleanup() {
    local status=$?
    if [[ -n $temporary ]]; then
        rm -f -- "$temporary"
    fi
    return "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

main() {
    local input='' output='' dry_run=false parent
    local input_seen=false output_seen=false
    while (( $# > 0 )); do
        case $1 in
            --help) usage; return 0 ;;
            --input)
                (( $# >= 2 )) || { usage >&2; return 2; }
                [[ $input_seen == false && -n $2 ]] || return 2
                input=$2; input_seen=true; shift 2 ;;
            --output)
                (( $# >= 2 )) || { usage >&2; return 2; }
                [[ $output_seen == false && -n $2 ]] || return 2
                output=$2; output_seen=true; shift 2 ;;
            --dry-run) dry_run=true; shift ;;
            *) usage >&2; return 2 ;;
        esac
    done
    [[ -n $input && -n $output ]] || { usage >&2; return 2; }
    [[ -f $input && -r $input ]] || {
        printf 'input must be a readable regular file\n' >&2; return 1;
    }
    parent=$(dirname -- "$output") || return 1
    [[ -d $parent && ! -e $output && ! -L $output ]] || {
        printf 'output parent must exist and output must be new\n' >&2; return 1;
    }
    if [[ $dry_run == true ]]; then
        summarize_events < "$input" > /dev/null || return 1
        printf 'would read=%q\nwould write=%q\n' "$input" "$output"
        return 0
    fi
    umask 077
    temporary=$(mktemp "$parent/.log-report.XXXXXX") || return 1
    summarize_events < "$input" > "$temporary" || {
        printf 'report not published: invalid or unreadable input\n' >&2; return 1;
    }
    # Same-directory hard link publishes a complete file and fails if output exists.
    # For filesystems without hard links this intentionally fails closed.
    ln -- "$temporary" "$output" || {
        printf 'could not publish new output\n' >&2; return 1;
    }
    printf 'report created: %s\n' "$output" >&2
}

main "$@"
