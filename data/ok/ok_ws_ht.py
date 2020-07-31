#coding: utf-8
from websocket import create_connection
import zlib
import json
import time
import redis
import random
import threading

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

def getdata(i,iu):
    while 1:
        try:
            tradeStr = """{"op": "subscribe", "args": ["spot/candle60s:"""+i+"""-USDT"]}"""
            ws = create_connection("wss://okexcomreal.bafang.com:8443/ws/v3")
            ws.send(tradeStr)
            while 1:
                compressData = ws.recv()
                b = inflate(compressData).decode(encoding='utf-8')
                b = json.loads(b)

                data = b.get('data')
                if data :
                    data = data[0]
                    time1 = str(int(time.time()))
                    result1 = {}
                    result1["id"] = int(time1)
                    result1["open"] = float(data['candle'][1])
                    result1["high"] = float(data['candle'][2])
                    result1["low"] = float(data['candle'][3])
                    result1["close"] = float(data['candle'][4])
                    result1["vol"] = float('%.2f' % (random.random() * 15 + 8.8))
                    red = json.dumps(result1)
                    r.set('sub:'+iu+':1min',red)
                    # print(r.get('sub:'+iu+':1min'))
                    time.sleep(0.1)
        except Exception as e:
            print(e)
            time.sleep(10)

if __name__ == '__main__':
    #htusdt
    A = {'OKB':'okbusdt'}
    for i in A:
        t1 = threading.Thread(target=getdata,args=(i,A.get(i),))
        t1.start()
    t1.join()






