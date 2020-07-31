#!/usr/bin/python3
#coding: utf-8

from utils import  get_html_bytes,get_html
import redis
import time
from multiprocessing import Pool
import threading
import json

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def getname(time1):
    #多线程，每个货币对儿一个线程
    B = {'xrpusdt':['bvt',100,0],'trxusdt':['won',1000,20],'zecusdt':['ectio',1,50]}

    threadinglist= list()
    for symbol in B:
        t1 = threading.Thread(target=getdata, args=(symbol,time1,B.get(symbol)))
        threadinglist.append(t1)

    for t1 in threadinglist:
        t1.start()
    for t1 in threadinglist:
        t1.join()


def getdata(symbol,period,platForm):
    while 1:
        try:
            # url = "http://api.huobi.vn/market/history/kline?symbol=" + symbol + "&size=600&period=" + period
            urlDict = ["http://api.huobiasia.vip/market/history/kline?symbol=",symbol,"&size=600&period=",period]
            url = ''.join(urlDict)
            # print(url)

            result = get_html_bytes(url)

            result = str(result, encoding='utf-8')
            if result[1:5] in 'html':
                getdata(symbol, period)
            else:
                result = json.loads(result)
                try:
                    print(r.get('hlg:ect:fk:'+platForm[0]))
                    response = float(r.get('hlg:ect:fk:'+platForm[0]))
                except Exception as e:
                    response = float(0)
                k = platForm[1]
                b = platForm[2]
                for res in result['data']:
                    res['open'] = res['open'] * k + b + response
                    res['close'] = res['close'] * k + b + response
                    res['high'] = res['high'] * k + b + response
                    res['low'] = res['low'] * k + b + response
                # print(result)
                # print('market:ect:'+platForm[0]+'usdt:'+period)
                r.set('market:ect:'+platForm[0]+'usdt:'+period, json.dumps(result))
                print(symbol, r.get('market:ect:'+platForm[0]+'usdt:'+period ))
                time.sleep(30)
        except Exception as e:
            time.sleep(30)
            print(e)


if __name__ == '__main__':
    #多进程，每个时间段的行情一个进程
    A = ['1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year']
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()

