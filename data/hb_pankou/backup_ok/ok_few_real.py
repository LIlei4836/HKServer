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
import datetime

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# okex ，币安均无HT

def getname(time1,timeNum):
    B = ['QTUM', 'XMR', 'ATOM', 'NEO', 'DCR', 'LAMB', 'BTM', 'ONT', ]
    threadlist = list()
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname,time1,timeNum))
        threadlist.append(t1)

    for t1 in threadlist:
        t1.start()

    for t1 in threadlist:
        t1.join()


newDict = {'qtumusdt': ['miscusdt'], 'xmrusdt': ['mrdusdt'], 'atomusdt': ['xzctusdt'], 'neousdt': ['hecusdt'],
           'dcrusdt': ['xttcusdt'],'lambusdt': ['lambusdt'], 'btmusdt': ['btmusdt'],'ontusdt': ['ontusdt'],}

def getdata(currsname,time1,timeNum):
    while 1:
        try:
            tradeStr = """{"op": "subscribe", "args": ["spot/trade:""" + currsname + """-USDT"]}"""
            ws = create_connection("wss://okexcomreal.bafang.com:8443/ws/v3")
            ws.send(tradeStr)
            while 1:
                compressData = ws.recv()
                data_unzip = inflate(compressData).decode(encoding='utf-8')
                data_list = json.loads(data_unzip).get('data')
                if data_list:
                    data = data_list[0]
                    result = {}

                    result["time"] = UTC_to_timeStamp(data['timestamp'])
                    result['amount'] = data['size']
                    result['price'] = data['price']
                    result['type'] = data['side']

                    data = json.dumps(result)


                    symbol = currsname.lower()+'usdt'
                    r.set('real:' + symbol + ':1min', data)
                    # print('real:' + symbol + ':1min')
                    # print(r.get('real:' + symbol+ ':1min'))



                    # 添加别名
                    newNames = newDict.get(symbol)
                    if newNames:
                        for newName in newNames:
                            r.set('real:' + newName + ':1min', data)
                            # print(r.get('real:' + newName + ':1min'))
                            # print('real:' + newName + ':1min')


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
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    utcTime = datetime.datetime.strptime(timeUtc, UTC_FORMAT)
    localtime = utcTime + datetime.timedelta(hours=8)
    ret_stamp = int(time.mktime(localtime.timetuple()) * 1000.0 + localtime.microsecond / 1000.0)
    return ret_stamp




if __name__ == '__main__':
    A = {'1min':'trade'}
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,A.get(i)))
    p.close()
    p.join()

