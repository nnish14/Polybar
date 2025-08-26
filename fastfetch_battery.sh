#!/bin/bash

charging_flag=-1
percent=0

while true; do
    # Every 5 seconds: poll real battery status
    battery_info=$(fastfetch --structure battery --logo none)
    new_percent=$(echo "$battery_info" | grep -oP '[0-9]+(?=%)')
    raw_status=$(echo "$battery_info" | grep -oP '\[(.*?)\]' | tr -d '[]' | tr '[:upper:]' '[:lower:]')

    percent=$new_percent

    if echo "$raw_status" | grep -qw "charging"; then
        charging_flag=1
    elif echo "$raw_status" | grep -qw "discharging"; then
        charging_flag=0
    else
        charging_flag=-1
    fi

    for i in {1..2}; do

        if (( charging_flag == 1 )); then
            # Charging animation
            icons=(󰂄 󰂆 󰂈 󰂉 󰂅)
            color="#A3BE8C"
            index=$(( $(date +%s) % ${#icons[@]} ))
            icon="${icons[$index]}"
        elif (( charging_flag == 0 )); then
            # Discharging ramp
            if (( percent <= 19 )); then
                icon="󰁺"; color="#BF616A"
            elif (( percent <= 39 )); then
                icon="󰁼"; color="#D08770"
            elif (( percent <= 59 )); then
                icon="󰁾"; color="#EBCB8B"
            elif (( percent <= 79 )); then
                icon="󰂀"; color="#88C0D0"
            else
                icon="󰁹"; color="#8FBCBB"
            fi
        else
            # Unknown state fallback
            icon="󰂄"; color="#FFFFFF"
        fi

        echo "%{F$color}$icon $percent%%{F-}"
        sleep 1
    done

done

