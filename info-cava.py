#!/usr/bin/env python3

import argparse
import subprocess
import signal
import tempfile
import sys
import os

# Ramp characters
BASE_BARS = [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

def build_ramp(extra_colors):
    ramp = BASE_BARS.copy()
    for color in extra_colors:
        color = color.strip(' #')
        ramp.append(f'%{{F#{color}}}█%{{F-}}')
    return ramp

def create_cava_config(framerate, bars, ascii_max_range, channels):
    conf = "[general]\n"
    conf += f"framerate={framerate}\n"
    conf += f"bars={bars}\n"
    conf += "[output]\n"
    conf += "method=raw\n"
    conf += "data_format=ascii\n"
    conf += f"ascii_max_range={ascii_max_range}\n"
    conf += "bar_delimiter=32\n"

    if channels != 'stereo':
        conf += "channels=mono\n"
        conf += f"mono_option={channels}\n"

    return conf

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--framerate', type=int, default=60)
    parser.add_argument('-b', '--bars', type=int, default=8)
    parser.add_argument('-e', '--extra_colors', default='fdd,fcc,fbb,faa')
    parser.add_argument('-c', '--channels', choices=['stereo', 'left', 'right', 'average'], default='stereo')

    args = parser.parse_args()

    extra_colors = args.extra_colors.split(',')
    ramp = build_ramp(extra_colors)

    ascii_max_range = len(ramp)

    with tempfile.NamedTemporaryFile('w', delete=False, prefix='polybar-cava-conf.') as tmp_conf:
        tmp_conf.write(create_cava_config(args.framerate, args.bars, ascii_max_range, args.channels))
        cava_conf_path = tmp_conf.name

    cava_proc = subprocess.Popen(['cava', '-p', cava_conf_path], stdout=subprocess.PIPE, text=True)

    def cleanup(sig, frame):
        try:
            cava_proc.kill()
        except:
            pass
        os.remove(cava_conf_path)
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        for line in cava_proc.stdout:
            bars = [int(x) for x in line.strip().split()]
            out = ''.join(ramp[min(bar, len(ramp)-1)] for bar in bars)
            print(out, flush=True)
    except KeyboardInterrupt:
        cleanup(None, None)

if __name__ == "__main__":
    main()

