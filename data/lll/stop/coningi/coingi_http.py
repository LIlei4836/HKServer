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
    B = {'trxusdt':['mkeusdt',185,0],'eosusdt':['thpusdt',4,1],'etcusdt':['cgbusdt',6.5,0]}
    threadList = list()
    for symbol in B:
        t1 = threading.Thread(target=getdata, args=(symbol,time1,B.get(symbol)))
        threadList.append(t1)
    for t1 in threadList:
        t1.start()
    for t1 in threadList:
        t1.join()

def getdata(symbol,period,platform):
    while 1:
        try:
            # url = "http://api.huobiasia.vip/market/history/kline?symbol="+symbol+"&size=600&period="+period
            # url = "http://api.huobi.me/market/history/kline?symbol="+symbol+"&size=1&period="+period
            urlDict = ["http://api.huobiasia.vip/market/history/kline?symbol=", symbol, '&size=600&period=',period]
            url = ''.join(urlDict)
            result = get_html_bytes(url)
            if result == None:
                time.sleep(5)
                continue
            result = str(result, encoding='utf-8')
            if result[1:5] in 'html':
                # getdata(symbol,period)
                time.sleep(2)
                continue
                pass
            else:
                result=json.loads(result)
                k = platform[1]
                b = platform[2]
                for res in result['data']:
                    res['open']=res['open']*k+b
                    res['close']=res['close']*k+b
                    res['high']=res['high']*k+b
                    res['low']=res['low']*k+b
                r.set('market:'+platform[0]+':'+period, json.dumps(result))
                # print(json.dumps(result))
                print(r.get('market:'+platform[0]+':'+period))
            timeDict = {'1min': 30 * 1, '5min': 30 * 5, '15min': 30 * 15, '30min': 30 * 30, '60min': 30 * 60,
                        '1day': 30 * 60 * 24, '1mon': 30 * 60 * 24 * 30, '1week': 30 * 60 * 24 * 7,
                        '1year': 30 * 60 * 24 * 36}
            time.sleep(timeDict[period])
        except Exception as e:
            print(e)
            time.sleep(30)

if __name__ == '__main__':
    #多进程，每个时间段的行情一个进程
    A = ['1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year']
    threadList = list()
    for a in A:
        t1 = threading.Thread(target=getname, args=(a,))
        threadList.append(t1)
    for t1 in threadList:
        t1.start()
    for t1 in threadList:
        t1.join()


    # A = ['1day',]
    # p = Pool(len(A))
    # for i in A:
    #     p.apply_async(getname, args=(i,))
    #     print('进程' + i + '启动成功！')
    # p.close()
    # p.join()







