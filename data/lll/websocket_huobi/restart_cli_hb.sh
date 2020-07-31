#!/bin/sh
ps -ef | grep cli_shengji_hb.py | grep -v grep | cut -c 9-15 | xargs kill -s 9
nohup python3 -u /ht/ht/data/lll/websocket_huobi/cli_shengji_hb.py> /dev/null 2>&1 &

