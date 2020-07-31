import requests
import threading
from multiprocessing import Pool
import time
import json
import redis

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def time1(i,iu):
    B = {'60':'1min','300':'5min','900':'15min','1800':'30min','3600':'60min','86400':'1day','604800':'1week','18144000':'1mon'}
    for b in B:
        t1 = threading.Thread(target=getdata, args=(i,iu,b,B.get(b),))
        t1.start()
    t1.join()


def getdata(i,iu,b,min):
    while 1:
        url = 'http://39.100.233.117:7000/python/symbol/' + iu + '/period/' + min + '/size/500'
        # url = 'http://localhost:7000/python/symbol/' + iu + '/period/' + min + '/size/1'
        html = requests.get(url, timeout =3)
        result = html.text
        result = json.loads(result)
        r.set('market:'+iu+':'+min,json.dumps(result))
        print(min, result)

        time.sleep(30)


if __name__ == '__main__':
    # A = {'BTC':'btcusdt','LTC':'ltcusdt','ETH':'ethusdt','EOS':'eosusdt','XRP':'xrpusdt','BCH':'bchusdt','BSV':'bsvusdt'}
    A = {'OKB':'okbusdt'}
    p = Pool(len(A))
    for i in A:
        p.apply_async(time1,args=(i,A.get(i),))
    p.close()
    p.join()