#!/usr/bin/python3
#coding: utf-8
import sys
import redis
import time
import json
import threading

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def getdata(symbol):
    while 1:
        try:
            da = r.lrange('fk:'+symbol+':1min',0,500)
            data = {}
            data['data'] = da
            r.set('market:risk:'+symbol + ':1min', json.dumps(data))
            time.sleep(60)
        except:
            pass


if __name__ == '__main__':

    B = ['btcusdt', 'ltcusdt', 'ethusdt', 'eosusdt', 'xrpusdt', 'bchusdt', 'htusdt', 'bsvusdt', 'htusdt','nasusdt','hb10usdt']
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname,))
        t1.start()
    t1.join()







