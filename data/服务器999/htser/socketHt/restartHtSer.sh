#!/bin/sh
kill 9 `lsof -t -i:999`
nohup python3 -u /ht/ht/data/服务器999/htser/socketHt/serHt.py> /dev/null 2>&1 &

