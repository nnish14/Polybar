#!/usr/bin/env python3

import time
import os

MODE_FILE = f"{os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))}/polybar_time_mode"
SCROLL_FILE = f"{os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))}/polybar_date_scroll"

MAXLEN = 30
SPACER = "    "

def get_mode():
    if not os.path.exists(MODE_FILE):
        return "short"
    with open(MODE_FILE, "r") as f:
        return f.read().strip()

def get_scroll_position(text):
    if not os.path.exists(SCROLL_FILE):
        pos = 0
    else:
        try:
            with open(SCROLL_FILE, "r") as f:
                pos = int(f.read().strip())
        except:
            pos = 0

    pos = (pos + 1) % len(text)

    with open(SCROLL_FILE, "w") as f:
        f.write(str(pos))

    return pos

def main():
    mode = get_mode()

    if mode == "short":
        print(time.strftime("%H:%M"))
    else:
        date_str = ">>> " + time.strftime("%A, %d %B %Y") + " <<<" + SPACER
        pos = get_scroll_position(date_str)

        # Scroll logic
        if len(date_str) <= MAXLEN:
            output = date_str.ljust(MAXLEN)
        else:
            output = (date_str + date_str)[pos:pos+MAXLEN]

        print(output)

if __name__ == "__main__":
    main()

