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
import pytz

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# okex ，币安均无HT

def getname(time1):
    B = ['QTUM', 'XMR', 'ATOM', 'NEO', 'DCR', 'LAMB', 'BTM', 'ONT',]
    threadlist = list()
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname,time1,))
        threadlist.append(t1)

    for t1 in threadlist:
        t1.start()

    for t1 in threadlist:
        t1.join()


newDict = {'qtumusdt': ['miscusdt'], 'xmrusdt': ['mrdusdt'], 'atomusdt': ['xzctusdt'], 'neousdt': ['hecusdt'],
           'dcrusdt': ['xttcusdt'],'lambusdt': ['lambusdt'], 'btmusdt': ['btmusdt'],'ontusdt': ['ontusdt'],}

def getdata(currsname,time1,):
    while 1:
        try:
            tradeStr = """{"op": "subscribe", "args": ["spot/ticker:""" + currsname + """-USDT"]}"""
            ws = create_connection("wss://okexcomreal.bafang.com:8443/ws/v3")
            ws.send(tradeStr)
            while 1:
                compressData = ws.recv()
                data_unzip = inflate(compressData).decode(encoding='utf-8')
                data_list = json.loads(data_unzip).get('data')
                if data_list:
                    data = data_list[0]
                    result = {}


                    result["time"] = utc_to_local(data['timestamp'])
                    result['sell'] = data['best_ask']
                    result['buy'] = data['best_bid']
                    result['sellmount'] = data['best_ask_size']
                    result['buymount'] = data['best_bid_size']

                    data = json.dumps(result)

                    symbol = currsname.lower()+'usdt'
                    r.set('handicap:' + symbol + ':1min', data)
                    # print(symbol,data)
                    # print('handicap:' + symbol + ':1min')
                    # print(r.get('handicap:' + symbol+ ':1min'))


                    # 添加别名
                    newNames = newDict.get(symbol)
                    if newNames:
                        for newName in newNames:
                            r.set('handicap:' + newName + ':1min', data)
                            # print(r.get('handicap:' + newName + ':1min'))
                            # print('handicap:' + newName + ':1min')

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

# UTCS时间转换为时间戳 2018-07-13T16:00:00Z
def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S.%fZ'):
    local_tz = pytz.timezone('Asia/Chongqing')      #定义本地时区
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)       #讲世界时间的格式转化为datetime.datetime格式
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)     #想将datetime格式添加上世界时区，然后astimezone切换时区：世界时区==>本地时区
    return int(time.mktime(local_dt.timetuple()))


if __name__ == '__main__':
    A = {'1min'}
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
    p.close()
    p.join()

