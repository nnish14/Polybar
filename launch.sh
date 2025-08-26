#!/bin/bash

LOCKFILE="/tmp/polybar-launch.lock"

# Check for lock
if [ -e "$LOCKFILE" ]; then
    echo "Polybar launch already in progress. Exiting."
    exit 1
fi

# Create lock
touch "$LOCKFILE"

# Kill existing polybars
pkill -x polybar

# Wait for polybar to actually quit
while pgrep -x polybar >/dev/null; do
    sleep 0.2
done

# Launch the bar
polybar mybar &

# Cleanup lockfile when done
rm -f "$LOCKFILE"

echo "Polybar launched cleanly."
