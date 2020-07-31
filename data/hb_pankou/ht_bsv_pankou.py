from websocket import create_connection
import gzip
import time
import json
import redis
import threading

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def get_data(b):
    while 1:
        try:
            tradeStr = """{"sub":"market."""+b+""".bbo","id": "id10"}"""
            ws = create_connection("wss://api.huobi.br.com/ws")
            # ws = create_connection("wss://api.huobiasia.vip/ws")
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
                        r.set('handicap:'+b+':1min',json.dumps(res))
                        # print(b,r.get('handicap:'+b+':1min'))
        except:
            time.sleep(10)

if __name__ == '__main__':
    B = ['adausdt','htusdt','bsvusdt','dashusdt','zecusdt','elausdt','neousdt']
    for b in B :
        t1 = threading.Thread(target=get_data, args=(b,))
        t1.start()
    t1.join()


