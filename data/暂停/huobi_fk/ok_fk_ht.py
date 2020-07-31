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
import zlib

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


def getname(time1):
    B = {'btcusdt':'BTC', 'ethusdt':'ETH', 'ltcusdt':'LTC', 'bchusdt':'BCH', 'eosusdt':'EOS', 'xrpusdt':'XRP', 'etcusdt':'ETC','trxusdt':'TRX'}
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname,B.get(currsname),time1,))
        t1.start()
    t1.join()

def getdata(currsname,codeName,time1):
    print(currsname,codeName,time1)
    while 1:
        try:
            tradeStr = """{"op": "subscribe", "args": ["spot/candle60s:"""+codeName+"""-USDT"]}"""
            ws = create_connection("wss://okexcomreal.bafang.com:8443/ws/v3")
            ws.send(tradeStr)
            while 1:
                compressData = ws.recv()
                b = inflate(compressData).decode(encoding='utf-8')
                b = json.loads(b)

                data = b.get('data')
                if data :
                    data = data[0]
                    time2 = str(int(time.time()))
                    try:
                        url = "http://www.silvercontract.top/api/System/getFkData?coinName=" + str(codeName)
                        resp = float(requests.get(url).content.decode())
                        r.set('hlg:yixin:fk:' + codeName, resp)
                    except:
                        pass
                    resp = float(r.get('hlg:yixin:fk:' + codeName))
                    result1 = {}
                    result1["id"] = int(time2)
                    result1["open"] = float(data['candle'][1])+resp
                    result1["high"] = float(data['candle'][2])+resp
                    result1["low"] = float(data['candle'][3])+resp
                    result1["close"] = float(data['candle'][4])+resp
                    result1["vol"] = float('%.2f' % (random.random() * 15 + 8.8))
                    data = json.dumps(result1)
                    b = r.lrange('fk:' + currsname + ':' + time1, 0, 0)
                    try:
                        if b:
                            if b != 't':
                                b = b[0][19:-1]
                            if data != 't':
                                c = data[19:-1]
                            if c != b:
                                if json.loads((r.lrange('fk:' + currsname + ':' + time1, 0, 0))[0])['id'] == \
                                        json.loads(data)['id']:
                                    r.lpop('fk:' + currsname + ':' + time1)
                                    r.lpush('fk:' + currsname + ':' + time1, data)
                                else:
                                    r.lpush('fk:' + currsname + ':' + time1, data)
                            else:
                                pass
                        else:
                            r.lpush('fk:' + currsname + ':' + time1, data)

                        fk_data = r.lrange('fk:' + currsname + ':' + time1, 0, 0)[0]
                        fk_data = json.loads(fk_data)
                        fk_data["vol"] = random.random() * 22 + 12

                        r.set('sub:risk:' + currsname + ':' + time1, json.dumps(fk_data))
                        print('sub:risk:' + currsname + ':' + time1)
                    except:
                        pass
        except Exception as e:
            print(e)
            time.sleep(10)


if __name__ == '__main__':
    A = ['1min']
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()



