#!/bin/sh
kill 9 `lsof -t -i:888`
nohup python3 -u /ht/ht/data/lll/websocket_huobi/ser_shengji_hb.py> /dev/null 2>&1 &

