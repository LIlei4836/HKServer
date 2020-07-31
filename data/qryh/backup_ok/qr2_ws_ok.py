#!/usr/bin/python3
#coding: utf-8

#从redis中取值格式    sub:btcusdt:1min
from websocket import create_connection
import gzip
import time
import json
import redis
from multiprocessing import Pool
import threading
import zlib

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# okex ，币安均无ELA

def getname(time1,timeNum):
    B=['QTUM','XMR','ATOM','NEO','DCR','LAMB','BTM','ONT']
    threadlist = list()
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname,time1,timeNum))
        threadlist.append(t1)

    for t1 in threadlist:
        t1.start()

    for t1 in threadlist:
        t1.join()


newDict = {'qtumusdt': ['miosusdt','miscusdt'], 'xmrusdt': ['xmrcusdt','mrdusdt'], 'atomusdt': ['ztcyusdt','xzctusdt'],'neousdt': ['hexcusdt','hecusdt'],
           'dcrusdt': ['hxtcusdt','xttcusdt'], 'lambusdt': ['lambusdt'], 'btmusdt': ['btmusdt'],'ontusdt': ['ontusdt'],}


def getdata(currsname,time1,timeNum):
    while 1:
        try:
            tradeStr = """{"op": "subscribe", "args": ["spot/"""+timeNum+""":""" + currsname + """-USDT"]}"""
            ws = create_connection("wss://okexcomreal.bafang.com:8443/ws/v3")
            ws.send(tradeStr)
            while 1:
                compressData = ws.recv()
                data_unzip = inflate(compressData).decode(encoding='utf-8')
                data_list = json.loads(data_unzip).get('data')
                if data_list:

                    data = data_list[0]
                    result = {}
                    result["id"] = UTC_to_timeStamp(data['candle'][0])
                    result["open"] = float(data['candle'][1])
                    result["high"] = float(data['candle'][2])
                    result["low"] = float(data['candle'][3])
                    result["close"] = float(data['candle'][4])
                    result["vol"] = float(data['candle'][5])
                    data = json.dumps(result)
                    # print(timeNum, data)

                    symbol = currsname.lower()+'usdt'
                    r.set('sub:' + symbol + ':' + time1, data)
                    # print('sub:' + symbol + ':' + time1)
                    # print(r.get('sub:' + symbol+ ':' + time1))
                    # 添加别名
                    newNames = newDict.get(symbol)
                    if newNames:
                        for newName in newNames:
                            r.set('sub:' + newName + ':' + time1, data)
                            # print(r.get('sub:' + newName + ':' + time1))
                            # print('sub:' + newName + ':' + time1)


                        # print(data)
        except Exception as e:
            print(currsname,time1,e)
            time.sleep(20)
            pass


# OK数据解压缩
def inflate(data):
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


def UTC_to_timeStamp(timeUtc):
    timeArray = time.strptime(timeUtc, "%Y-%m-%dT%H:%M:%S.000z")
    # 转换为时间戳:
    timeStamp = int(time.mktime(timeArray))+8 * 60 * 60
    return timeStamp



if __name__ == '__main__':
    # A = {'1min':'candle60s','1day':'candle86400s'}
    A = {'1min':'candle60s'}
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,A.get(i)))
    p.close()
    p.join()

