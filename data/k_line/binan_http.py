
from multiprocessing import Pool
import json
import time
import redis
import datetime
import random
import threading
from utils import get_html
pool = redis.ConnectionPool(host='127.0.0.1')  # 实现一个连接池
r = redis.Redis(connection_pool=pool,db=1)

def time1(i):
    B = {'1m':'1min','5m':'5min','15m':'15min','30m':'30min','1h':'60min','1d':'1day','1w':'1week','1M':'1mon'}
    for b in B:
        t1 = threading.Thread(target=getdata, args=(i,b,B.get(b),))
        t1.start()
    t1.join()


def getdata(i,b,min):
    while 1:
        try:
            url = "https://api.yshyqxx.com/api/v1/klines?symbol="+i+"&interval="+b+"&limit=300"
            # url = "https://api.urbn1w.cn/api/v1/klines?symbol="+i+"&interval="+b+"&limit=300"
            # print(url)
            res = get_html(url)
            res = json.loads(res)
            L = []
            bizhong = {'BNBUSDT':'bnbusdt'}
            bi = bizhong.get(i)
            for index,re in enumerate(res):
                P = {}
                # print(re)
                P['id'] = int(res[-index-1][0]/1000)
                P['open'] = float('%2f' % float(res[-index-1][1]))
                P['high'] = float('%2f' % float(res[-index-1][2]))
                P['low'] = float('%2f' % float(res[-index-1][3]))
                P['close'] = float('%2f' % float(res[-index-1][4]))
                P['vol'] = float('%.2f' % float(res[-index-1][5]))
                L.append(P)
            L = '{"data":' + json.dumps(L) + '}'
            r.set('market:'+bi+':'+min,L)
            print(r.get('market:'+bi+':'+min))
            time.sleep(30)
        except Exception as e:
            print(e)
            time.sleep(30)
        time.sleep(30)

if __name__ == '__main__':
    A = ['BNBUSDT']

    p = Pool(len(A))

    for i in A:
        p.apply_async(time1,args=(i,))
    p.close()
    p.join()




