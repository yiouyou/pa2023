#!/bin/bash

while true; do
    source /home/sz/pa2023/venv/bin/activate
    python ui_clean.py 7788
    echo "ui_clean crashed with exit code $?. Respawning..." >&2
    sleep 1
done
