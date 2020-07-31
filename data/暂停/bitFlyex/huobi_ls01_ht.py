#!/usr/bin/python3
#coding: utf-8
from userAgents import get_html
import redis
import time
from multiprocessing import Pool
import json
import threading

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
def getname(time1):
    #多线程，每个货币对儿一个线程
    B = ['etcusdt', 'hb10usdt', 'nasusdt']
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname, time1,))
        t1.start()
    t1.join()

def getdata(symbol,period):
    while 1:
        try:
            url = "http://api.huobi.io/market/history/kline?symbol="+symbol+"&size=500&period="+period
            result = get_html(url)
            if result[1:5] in 'html':
                pass
            else:
                result = json.loads(result)['data']
                result = '{"data":'+json.dumps(result)+'}'
                r.set('market:risk:'+symbol+':'+period, result)
                time.sleep(60)
        except Exception as e:
            time.sleep(30)

if __name__ == '__main__':
    #多进程，每个时间段的行情一个进程
    A = ['1min','5min', '15min', '30min', '60min', '1day', '1mon', '1week']
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()













