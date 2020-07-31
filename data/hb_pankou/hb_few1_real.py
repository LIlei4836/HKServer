from websocket import create_connection
import requests
import gzip
import time
import json
import redis
import threading


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def get_data(b,period):
    while 1:
        try:
            tradeStr = """{"sub": "market."""+b+""".trade.detail","id": "id1"}"""
            ws = create_connection("wss://api.huobi.br.com/ws",timeout=5)
            ws.send(tradeStr)
            while 1:
                compressData = ws.recv()
                result = gzip.decompress(compressData).decode('utf-8')
                if result[:7] == '{"ping"':
                    ts = result[8:21]
                    pong = '{"pong":' + ts + '}'
                    ws.send(pong)
                    ws.send(tradeStr)
                else:
                    data = json.loads(result)
                    try:
                        if data['status']:
                            pass
                    except:
                        data = data['tick']['data'][0]
                        res = {}
                        res['time'] = data['ts']
                        res['amount'] = data['amount']
                        res['price'] = data['price']
                        res['type'] = data['direction']

                        r.set('real:'+b+':1min',json.dumps(res))
                        r.set('real:'+period+':1min',json.dumps(res))
                        # print(r.get('real:'+b+':1min'))

                    time.sleep(0.05)
        except Exception as e:
            time.sleep(5)
if __name__ == '__main__':
    # B = {'hb10usdt': 'ancdusdt', 'qtumusdt': 'miscusdt', 'xmrusdt': 'mrdusdt', 'atomusdt': 'xzctusdt','neousdt': 'hecusdt', 'dcrusdt': 'xttcusdt', }
    B = {'qtumusdt': 'miscusdt', 'xmrusdt': 'mrdusdt', 'atomusdt': 'xzctusdt', 'neousdt': 'hecusdt',
         'dcrusdt': 'xttcusdt', 'lambusdt': 'lambusdt', 'btmusdt': 'btmusdt', 'ontusdt': 'ontusdt', }
    threalist = list()
    for b in B :
        t1 = threading.Thread(target=get_data, args=(b,B.get(b)))
        threalist.append(t1)
    for t1 in threalist:
        t1.start()
    for t1 in threalist:
        t1.join()