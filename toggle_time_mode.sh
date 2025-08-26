#!/bin/bash

MODE_FILE="${XDG_CACHE_HOME:-$HOME/.cache}/polybar_time_mode"

mkdir -p "$(dirname "$MODE_FILE")"

if [[ ! -f "$MODE_FILE" ]]; then
    echo "short" > "$MODE_FILE"
    exit 0
fi

MODE=$(cat "$MODE_FILE")

if [[ "$MODE" == "short" ]]; then
    echo "long" > "$MODE_FILE"
else
    echo "short" > "$MODE_FILE"
fi

