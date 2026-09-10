#!/usr/bin/env bash
set -euo pipefail
test_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
python3 "$test_dir/test_security_labs.py"
