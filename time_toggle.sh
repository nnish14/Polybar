#!/bin/bash

MODE_FILE="${XDG_CACHE_HOME:-$HOME/.cache}/polybar_time_mode"

# Initialize mode safely
mkdir -p "$(dirname "$MODE_FILE")"

if [[ ! -f "$MODE_FILE" || -z "$(cat "$MODE_FILE" 2>/dev/null)" ]]; then
    echo "short" > "$MODE_FILE"
fi

while true; do
    MODE=$(cat "$MODE_FILE" 2>/dev/null)

    # Failsafe fallback
    if [[ -z "$MODE" ]]; then
        MODE="short"
    fi

    if [[ "$MODE" == "short" ]]; then
        date "+%H:%M"
    else
        date "+%A, %d %B %Y | %H:%M:%S"
    fi

    sleep 1
done

