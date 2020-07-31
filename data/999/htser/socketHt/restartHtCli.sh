#!/bin/sh
ps -ef | grep cliHt.py | grep -v grep | cut -c 9-15 | xargs kill -s 9
nohup python3 -u /ht/ht/data/999/htser/socketHt/cliHt.py> /dev/null 2>&1 &

