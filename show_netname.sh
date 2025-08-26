#!/bin/bash
# $1 = module name (network-wifi or network-eth)
# $2 = text to display

echo "$2"   # print name so Polybar shows it
sleep 5     # wait 5 seconds
polybar-msg hook "$1" 0 >/dev/null 2>&1
