from websocket import create_connection
import requests
import gzip
import time
import json
import redis
import threading


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def get_data(b):
    while 1:
        try:
            tradeStr = """{"sub": "market."""+b+""".trade.detail","id": "id10"}"""
            ws = create_connection("wss://api.huobi.br.com/ws")
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
                        response = float(r.get('hlg:jtb:fk:jtbusdt'))
                        data = data['tick']['data'][0]
                        res = {}
                        res['time'] = data['ts']
                        res['amount'] = data['amount']
                        res['price'] = data['price']*10000-123+response
                        res['type'] = data['direction']
                        r.set('real:cebar:jtbusdt:1min',json.dumps(res))
        except:
            time.sleep(10)

if __name__ == '__main__':
    B = ['trxusdt']
    for b in B :
        t1 = threading.Thread(target=get_data, args=(b,))
        t1.start()
    t1.join()
