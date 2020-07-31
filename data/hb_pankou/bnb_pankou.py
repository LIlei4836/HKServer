from websocket import create_connection
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
            url = 'https://api.yshyqxx.com/api/v1/depth?limit=50&symbol=BNBUSDT'
            html = get_html(url)

            result = json.loads(html)

            bids = result['bids']
            asks = result['asks']
            res = {}
            res['time'] = int(time.time())
            res['sell'] = asks[0][0]
            res['buy'] = bids[0][0]
            res['sellmount'] = asks[0][1]
            res['buymount'] = bids[0][1]
            # print(asks, dids)
            r.set('handicap:' + b + ':1min', json.dumps(res))
            # print(b,r.get('handicap:'+b+':1min'))
            time.sleep(0.5)
        except:
            time.sleep(10)

if __name__ == '__main__':
    B = ['bnbusdt']
    for b in B :
        t1 = threading.Thread(target=get_data, args=(b,))
        t1.start()
    t1.join()
