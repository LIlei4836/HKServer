#!/bin/sh
kill -9 $(netstat -tlnp | grep :999 | awk '{print $7}' | awk -F '/' '{print $1}')
nohup python3 -u /ht/ht/data/999/htser/socketHt/serHt.py> /dev/null 2>&1 &

