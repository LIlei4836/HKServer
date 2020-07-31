from websocket import create_connection
import requests
import gzip
import time
import json
import redis
import threading
from utils import get_html,get_html_bytes

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def get_data(b):
    while 1:
        try:
            url = 'https://api.yshyqxx.com/api/v1/aggTrades?limit=50&symbol=BNBUSDT'
            html = get_html(url)
            result = json.loads(html)

            res = {}
            res['time'] = int(round(time.time()*1000))
            res['amount'] =result[-1]['q']
            res['price'] = result[-1]['p']
            if result[-1]['m'] ==1:
                 type= 'sell'
            else:
                type = 'buy'
            res['type'] = type

            r.set('real:' + b + ':1min', json.dumps(res))
            # print(r.get('real:' + b + ':1min'))
            time.sleep(0.5)
        except Exception as e:
            time.sleep(10)
if __name__ == '__main__':
    B = ['bnbusdt']
    for b in B :
        t1 = threading.Thread(target=get_data, args=(b,))
        t1.start()
    t1.join()
