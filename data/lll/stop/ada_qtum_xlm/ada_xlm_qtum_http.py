#!/usr/bin/python3
#coding: utf-8
from utils import get_html,get_html_bytes
import redis
import time
from multiprocessing import Pool
import threading
import json

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
def getname(time1):
    #多线程，每个货币对儿一个线程
    B = ['adausdt','xlmusdt','qtumusdt']
    for symbol in B:
        t1 = threading.Thread(target=getdata, args=(symbol,time1))
        t1.start()
    t1.join()

def getdata(symbol,period):
    while 1:
        try:
            url = "http://api.huobiasia.vip/market/history/kline?symbol="+symbol+"&size=600&period="+period
            # url = "http://api.huobi.io/market/history/kline?symbol="+symbol+"&size=500&period="+period
            # print(url)
            result = get_html_bytes(url)
            result = str(result, encoding='utf-8')
            if result[1:5] in 'html':
                getdata(symbol,period)
            else:
                result=json.loads(result)
                k = 1
                b = 0
                # print(result['data'])
                for res in result['data']:
                    res['open']=res['open']*k+b
                    res['close']=res['close']*k+b
                    res['high']=res['high']*k+b
                    res['low']=res['low']*k+b
                r.set('market:'+symbol+':'+period, json.dumps(result))
                # print(('market:'+symbol+':'+period))
                print(r.get('market:'+symbol+':'+period))
            time.sleep(30)
        except :
            time.sleep(30)

if __name__ == '__main__':
    #多进程，每个时间段的行情一个进程
    A = ['1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year']
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()







