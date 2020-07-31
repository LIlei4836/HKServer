from websocket import create_connection
import gzip
import time
import json
import redis
import threading

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def get_data(b,period):
    while 1:
        try:
            tradeStr = """{"sub":"market."""+b+""".bbo","id": "id1"}"""
            ws = create_connection("wss://api.huobi.br.com/ws",timeout=5)
            # ws = create_connection("wss://api.huobiasia.vip/ws",timeout=2)
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
                        data = data['tick']
                        res = {}
                        res['time'] = int(data['quoteTime']/1000)
                        res['sell'] = data['ask']
                        res['buy'] = data['bid']
                        res['sellmount'] = data['askSize']
                        res['buymount'] = data['bidSize']
                        # print(res)

                        r.set('handicap:' + b+ ':1min', json.dumps(res))
                        r.set('handicap:'+period+':1min',json.dumps(res))
                        # print(period,r.get('handicap:'+period+':1min'))
        except Exception as e:
            print(e)
            time.sleep(10)

if __name__ == '__main__':

    # B = {'lambusdt': 'lambusdt', 'btmusdt': 'btmusdt','ontusdt': 'ontusdt', 'wiccusdt': 'wiccusdt','bhdusdt':'acxusdt','xzcusdt':'axccusdt'}
    B = {'hb10usdt': 'ancdusdt', 'wiccusdt': 'wiccusdt', 'bhdusdt': 'acxusdt', 'xzcusdt': 'axccusdt'}
    threalist = list()
    for b in B :
        t1 = threading.Thread(target=get_data, args=(b,B.get(b)))
        threalist.append(t1)
    for t1 in threalist:
        t1.start()
    for t1 in threalist:
        t1.join()