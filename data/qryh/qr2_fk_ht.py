import requests
import redis
import json
import time
import threading
"""
获取风控值放入redis中
"""
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def qr2():
    while 1:
        try:
            currnames = {'hb10usdt': 'sancusdt', 'qtumusdt': 'miosusdt', 'xmrusdt': 'xmrcusdt', 'atomusdt': 'ztcyusdt',
                         'neousdt': 'hexcusdt', 'dcrusdt': 'hxtcusdt', 'lambusdt': 'lambusdt', 'btmusdt': 'btmusdt',
                         'ontusdt': 'ontusdt', 'wiccusdt': 'wiccusdt'}
            for i in currnames:
                dict2 = {'hb10usdt': 9, 'qtumusdt': 10, 'xmrusdt': 12, 'atomusdt': 13, 'neousdt': 14, 'dcrusdt': 15, 'lambusdt': 16,'btmusdt': 17, 'ontusdt': 18, 'wiccusdt': 19}
                url = "http://47.57.110.229/api/Riskmanagement/fkMethod?cid="+str(dict2.get(i))
                res =float(requests.get(url).content.decode('utf-8'))
                r.set('hlg5:qryh:fk:'+currnames.get(i),res)
                print(r.get('hlg5:qryh:fk:'+currnames.get(i)))

        except Exception as e:
            print(e)
        time.sleep(5)
        print('')
if __name__ == '__main__':
    t1 = threading.Thread(target=qr2, args=())
    t1.start()
    t1.join()



