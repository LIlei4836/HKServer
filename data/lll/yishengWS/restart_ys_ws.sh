#!/bin/sh

kill 9 `lsof -t -i:8800`
nohup python3 /root/lll/data/yishengWS/manage.py runserver 0.0.0.0:8800 >/root/lll/data/yishengWS/error.log  2>&1 &

