#coding: utf-8
from multiprocessing import Pool
import json
import time
import redis
import datetime
import random
import threading
from utils import get_html

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def time1(i,iu):
    B = {'60':'1min','300':'5min','900':'15min','1800':'30min','3600':'60min','86400':'1day','604800':'1week','18144000':'1mon'}
    for b in B:
        t1 = threading.Thread(target=getdata, args=(i,iu,b,B.get(b),))
        t1.start()
    t1.join()

def getdata(i,iu,b,min):
    while 1:
        try:
            time1 = int(time.time()*1000)
            # url = "https://www.okex.me/v2/spot/instruments/"+i+"-USDT/candles?granularity="+b+"&size=500&t="+str(time1)
            url = "https://www.okex.me/api/index/v3/instruments/"+i+"-USD/candles?granularity="+b+"&size=500&t="+str(time1)
            res = get_html(url)
            res = json.loads(res)['data']
            P = []
            for index,q in enumerate(res):
                t = res[-index-1][0]
                t = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.000Z")
                t = time.strptime(str(t), "%Y-%m-%d %H:%M:%S")
                t = int(time.mktime(t))

                L= {}
                L['id'] = t + 3600*8
                L['open'] = float(res[-index-1][1])
                L['high'] = float(res[-index-1][2])
                L['low'] = float(res[-index-1][3])
                L['close'] = float(res[-index-1][4])
                L["vol"] = float('%.2f' % (random.random() * 15 + 8.8))
                P.append(L)
            P = '{"data":'+json.dumps(P)+'}'
            r.set('market:'+iu+':'+min,P)
            # print(P)
            print(r.get('market:'+iu+':'+min))
        except Exception as e:
            print(e)
        time.sleep(50)


if __name__ == '__main__':
    # A = {'BTC':'btcusdt','LTC':'ltcusdt','ETH':'ethusdt','EOS':'eosusdt','XRP':'xrpusdt','BCH':'bchusdt','BSV':'bsvusdt'}
    A = {'OKB':'okbusdt'}
    p = Pool(len(A))
    for i in A:
        p.apply_async(time1,args=(i,A.get(i),))
    p.close()
    p.join()




