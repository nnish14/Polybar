#!/usr/bin/env python3

import subprocess
import os
import time

STATE_FILE = "/tmp/ytmusic_scroll_state"

MAXLEN = 35      # Width of the scrolling window
SPACER = " "  # Spaces between scroll loops

def get_track_info():
    try:
        title = subprocess.check_output(
            ["playerctl", "-p", "firefox", "metadata", "xesam:title"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        artist = subprocess.check_output(
            ["playerctl", "-p", "firefox", "metadata", "xesam:artist"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return f"{artist} - {title}"
    except subprocess.CalledProcessError:
        return None

def get_scroll_position(text):
    """Read and update scroll position from a temp file"""
    if not os.path.exists(STATE_FILE):
        pos = 0
    else:
        try:
            with open(STATE_FILE, "r") as f:
                pos = int(f.read().strip())
        except:
            pos = 0

    # Update position
    pos = (pos + 1) % len(text)

    with open(STATE_FILE, "w") as f:
        f.write(str(pos))

    return pos

def main():
    track = get_track_info()

    if not track:
        print("No Track Playing")
        return

    full_text = track + SPACER
    pos = get_scroll_position(full_text)

    # Create scrolling window
    if len(full_text) < MAXLEN:
        output = full_text.ljust(MAXLEN)
    else:
        # Wrap-around
        output = (full_text + full_text)[pos:pos+MAXLEN]

    print(output)

if __name__ == "__main__":
    main()

