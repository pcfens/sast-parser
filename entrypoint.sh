#!/bin/sh

set -e

# Run command if exists in PATH
if command -v "$1" >/dev/null 2>&1; then
    exec "$@"
else
    python /app/parse-sast.py $@
fi
