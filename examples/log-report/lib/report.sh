#!/usr/bin/env bash
# Contract: stdin = LEVEL SERVICE records, stdout = validated summary TSV.
# Empty input is valid. Malformed records fail without emitting a summary.
summarize_events() {
    LC_ALL=C awk '
        NF != 2 || $1 !~ /^(INFO|WARN|ERROR)$/ || $2 !~ /^[A-Za-z0-9_.-]+$/ {
            printf "invalid record at line %d\n", NR > "/dev/stderr"
            bad = 1
            next
        }
        { count[$1]++ }
        END {
            if (bad) exit 2
            printf "level\tcount\nINFO\t%d\nWARN\t%d\nERROR\t%d\n", count["INFO"], count["WARN"], count["ERROR"]
        }
    '
}
