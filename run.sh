#!/bin/bash

# rm /dev/shm/EvalBot.log || true
# rm /tmp/EvalBot.log || true
# touch /dev/shm/EvalBot.log
# ln -sf /dev/shm/EvalBot.log /tmp/EvalBot.log

cd /home/kuma/EvalBot
/opt/conda/bin/python3 /home/kuma/EvalBot/main.py
