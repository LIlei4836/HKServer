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
    B = ['ETC','LINK','IOST','DCR','LAMB']
    threadlist = list()
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname,time1,))
        threadlist.append(t1)

    for t1 in threadlist:
        t1.start()

    for t1 in threadlist:
        t1.join()


newDict = {'etcusdt': [['hklusdt', 1, -4.83], ], 'linkusdt': [['grtusdt', 0.03, 0], ],'iostusdt': [['stbeusdt', 0.1, 0.16], ],
           'dcrusdt': [['jtbusdt', 1, float(r.get('hlg:jtb:fk:dcrusdt'))]],'lambusdt':[['fgcusdt', 10, 0.17]]}

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


                    symbol = currsname.lower() + 'usdt'
                    newNamesLists = newDict.get(symbol)


                    for newNameList in newNamesLists:

                        k = newNameList[1]
                        b = newNameList[2]

                        result = {}
                        result["time"] = utc_to_local(data['timestamp'])

                        result['sell'] = float(data['best_ask'])*k + b

                        result['buy'] = float(data['best_bid'])*k+b
                        result['sellmount'] = float(data['best_ask_size'])*k+b
                        result['buymount'] = float(data['best_bid_size'])*k+b
                        newData = json.dumps(result)



                        r.set('handicap:' + newNameList[0] + ':1min', newData)
                        # print(symbol,newData)
                        # print('handicap:' + newNameList[0] + ':1min')
                        # print(r.get('handicap:' + newNameList[0]+ ':1min'))

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

