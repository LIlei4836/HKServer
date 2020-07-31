#!/usr/bin/python3
#coding: utf-8
from websocket import create_connection
import gzip
import time
import json
import redis
import requests
import random
from multiprocessing import Pool
import threading

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def getname(time1):
    B = {'btcusdt':'BTC', 'ethusdt':'ETH', 'ltcusdt':'LTC', 'bchusdt':'BCH', 'eosusdt':'EOS', 'xrpusdt':'XRP', 'etcusdt':'ETC','trxusdt':'TRX'}
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname,B.get(currsname),time1,))
        t1.start()
    t1.join()

def getdata(currsname,codeName,time1):
    while 1:
        try:
            time.sleep(2)
            url = "http://www.silvercontract.top/api/System/getFkData?coinName="+str(codeName)
            resp = float(requests.get(url,timeout=2).content.decode())
            r.set('hlg:yixin:fk:'+codeName,resp)
        except Exception as e:
            print(e)
if __name__ == '__main__':
    A = ['1min']
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()



