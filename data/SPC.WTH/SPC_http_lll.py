
#coding=utf-8
from userAgents import get_html
import redis
import time
from multiprocessing import Pool
import json
import random
import threading

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
def getname(i,iu):
    #多线程，每个货币对儿一个线程
    B = ['1min','5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year']
    for time1 in B:
        t1 = threading.Thread(target=getdata, args=(i,iu,time1,))
        t1.start()
    t1.join()

def getdata(i,iu,time1):
    while 1:
        try:
            url = 'http://api.huobiasia.vip/market/history/kline?symbol=' + i + '&size=500&period=' + time1
            result = get_html(url)
            if result[1:5] in 'html':
                pass
            else:
                result = json.loads(result)['data']
                if i == 'htusdt':
                    P = []
                    for index, resp in enumerate(result):
                        L={}
                        try:
                            response = float(r.get('hlg:spc:SPC:riskNum'))
                        except:
                            response = 0
                        k = 1.88
                        b = 0
                        L['id'] = resp['id']
                        L['high'] = resp['high'] * k + b + response
                        L['open'] = resp['open'] * k + b + response
                        L['low'] = resp['low'] * k + b + response
                        L['close'] = resp['close'] * k + b + response
                        L['vol'] = resp['vol']
                        del resp['count'], resp['amount']
                        P.append(L)
                    if P:
                        P= '{"data":'+json.dumps(P)+'}'
                        r.set('market:'+iu+':'+time1, P)
                        # print(r.get('market:'+iu+':'+time1))
                if i == 'ethusdt':
                    P = []
                    for index, resp in enumerate(result):
                        L = {}
                        try:
                            response = float(r.get('hlg:spc:WTH:riskNum'))
                        except:
                            response = 0
                        k = 0.175438
                        b = 0
                        L['id'] = resp['id']
                        L['high'] = resp['high'] * k + b + response
                        L['open'] = resp['open'] * k + b + response
                        L['low'] = resp['low'] * k + b + response
                        L['close'] = resp['close'] * k + b + response
                        L['vol'] = resp['vol']
                        del resp['count'], resp['amount']
                        P.append(L)
                    if P:
                        P = '{"data":' + json.dumps(P) + '}'
                        r.set('market:' + iu + ':' + time1, P)
                        # print(r.get('market:' + iu + ':' + time1))
                time.sleep(30)
        except:
            time.sleep(30)
if __name__ == '__main__':
    A ={'htusdt': 'spcusdt', 'ethusdt':'wthusdt'}
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,A.get(i),))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()













