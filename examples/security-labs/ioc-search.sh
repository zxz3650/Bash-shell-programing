#!/usr/bin/env bash
# Literal line search only; does not connect to indicators or execute input.
set -u
usage() { printf 'usage: bash ioc-search.sh -f FILE -i LITERAL\n' >&2; }
input_file='' indicator='' seen_file=0 seen_indicator=0
while getopts ':f:i:' option; do
    case $option in
        f) (( seen_file == 0 )) || { usage; exit 2; }; input_file=$OPTARG; seen_file=1 ;;
        i) (( seen_indicator == 0 )) || { usage; exit 2; }; indicator=$OPTARG; seen_indicator=1 ;;
        *) usage; exit 2 ;;
    esac
done
shift "$((OPTIND - 1))"
if (( $# != 0 || seen_file != 1 || seen_indicator != 1 )) || [[ -z $input_file || -z $indicator || $indicator == *$'\n'* ]]; then
    usage; exit 2
fi
if [[ ! -f $input_file || ! -r $input_file ]]; then
    printf 'input is not a readable regular file\n' >&2; exit 2
fi
# grep: 0 match, 1 no match, 2 error. Read errors can follow partial stdout.
grep -nF -- "$indicator" "$input_file"
status=$?
if (( status > 1 )); then
    printf 'search failed; discard partial results\n' >&2
    exit 2
fi
exit "$status"
