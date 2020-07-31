# -*- coding=utf-8  -*-
# @Time: 2020/7/3 10:56
# @Author: LeiLei Li
# @File: Demo01.py

# 当火币5分钟最新价不变化，自动切换成ok


import redis
import time
import json
import os
import logging
from twilio.rest import Client



fmt = '%(asctime)s , %(levelname)s , %(filename)s %(funcName)s line %(lineno)s , %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S %a'
logging.basicConfig(level=logging.INFO,
format=fmt,
datefmt=datefmt,
filename="log.txt")


# 短信配置
account_sid = 'AC35f3050ccc8b35000684434ada25ca9f'
auth_token = 'c27863fca9385f0fd59cc27c4e70c7ae'
client = Client(account_sid, auth_token)


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

oldClose = 0
oldTime = 0

while 1:
    data = r.get('sub:btcusdt:1min')
    data = json.loads(data)
    timeStamp = data.get('id')
    close = data.get('close')
    times = int(time.time())
    if oldClose != close:
        oldClose = close
        oldTime = timeStamp

    if times - oldTime > 300:
        logging.info(str(times) + ', '+ str(timeStamp)+', '+str(close))
        os.system('/ht/ht/data/lll/hb_ok/restart_hb_ok.sh')
        oldTime = times

        message = client.messages.create(
                              from_='+12029913273',
                              body='火币行情发生异常，请尽快处理',
                              to='+8615618022874'
                          )
        break

    print(times,oldTime,times-oldTime,close)
    time.sleep(10)