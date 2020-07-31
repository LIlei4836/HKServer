#!/usr/bin/python3
#coding: utf-8
from userAgents import get_html,get_html_bytes,get_html_bytes_no_daili
import redis
import time
from multiprocessing import Pool
import threading
import json

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
def getname(time1):
    #多线程，每个货币对儿一个线程
    B = {'bichkc':['trxusdt','jtbusdt']}
    for symbol in B:
        t1 = threading.Thread(target=getdata, args=(symbol,time1, B.get(symbol)))
        t1.start()
    t1.join()

def getdata(symbol,period,currency):
    while 1:
        try:
            #url = "http://api.huobiasia.vip/market/history/kline?symbol="+currency[0]+"&size=600&period="+period
            url = "http://api.huobi.br.com/market/history/kline?symbol=" + currency[0] + "&size=600&period=" + period
            result = get_html_bytes(url)

            result = str(result, encoding='utf-8')
            if result[1:5] in 'html':
                getdata(symbol,period)
            else:
                response = float(r.get('lll:'+symbol+':fk:'+currency[0]))
                result = json.loads(result)
                count = 144
                multiplier = 10000

                for res in result['data']:
                    res['open']=abs(res['open']*multiplier-count)+response
                    res['close']=abs(res['close']*multiplier-count)+response
                    res['high']=abs(res['high']*multiplier-count)+response
                    res['low']=abs(res['low']*multiplier-count)+response
                r.set('market:'+'xueusdt'+':'+period, json.dumps(result))
                print('market:' + 'xueusdt' + ':' + period, json.dumps(result))
            time.sleep(30)
        except :
            time.sleep(30)

if __name__ == '__main__':
    #多进程，每个时间段的行情一个进程
    A = ['1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year']
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()







