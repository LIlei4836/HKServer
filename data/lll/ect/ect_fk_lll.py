# -*- coding = utf-8  -*-
# @Time: 2020/6/3 0:05
# @Author: 李雷雷
# @File: ect_fk_lll.py

import requests
import redis
import time
import threading
import logging


fmt = '%(asctime)s , %(levelname)s , %(filename)s %(funcName)s line %(lineno)s , %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S %a'
logging.basicConfig(level=logging.INFO,
format=fmt,
datefmt=datefmt,
filename="log.txt")


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


def get_fk(fk,id):
    while 1:
        try:
            urlDict = ["http://www.ectiolive.com/api/Riskmanagement/fkMethod?cid=", str(id)]
            url = ''.join(urlDict)
            # print(url)
            response = requests.get(url,timeout=3)
            response = float(response.content.decode())
            r.set('hlg:ect:fk:' + fk, response)
            print(response)
            # print(r.get('hlg:ect:fk:' + fk))
            # print('hlg:ect:fk:' + fk)
        except Exception as e:
            # logging.info(e)
            print(e)
            pass
        time.sleep(5)


if __name__ == '__main__':
    fks = {'btcusdt': 2, 'bchusdt': 6, 'ethusdt': 3, 'ltcusdt': 4, 'etcusdt': 5, 'xrpusdt': 8, 'eosusdt': 7,'ectio':9, 'bvt':10,'won':11}
    threadlist = []
    for fk in fks:
        t1 = threading.Thread(target=get_fk, args=(fk,fks.get(fk)))
        threadlist.append(t1)
    for t1 in threadlist:
        t1.start()
    for t1 in threadlist:
        t1.join()