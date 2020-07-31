# coding: utf-8
from websocket import create_connection
import gzip
import json
import redis
from multiprocessing import Pool
import random
import time
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


newDict = {'hb10usdt':'ancdusdt','qtumusdt':'miscusdt','neousdt':'hecusdt','dcrusdt':'xttcusdt','atomusdt':'xzctusdt','xmrusdt':'mrdusdt'}

def m(i, iu):
    while 1:
        try:
            tradeStr = """{"sub": "market.""" + i + """.kline.1min","id": "id1"}"""
            ws = create_connection("wss://api.huobi.br.com/ws", timeout=10)
            # ws = create_connection("wss://api.huobiasia.vip/ws")
            ws.send(tradeStr)
            while 1:
                try:

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
                            result1={}
                            result1["id"] = data['id']
                            result1["vol"] = float('%.4f' % float(random.random() * 10 + 4))
                            result1["high"] = data['high']
                            result1["open"] = data['open']
                            result1["low"] = data['low']
                            result1["close"] = data['close']
                            r.set('sub:' + iu + ':1min', json.dumps(result1))
                            newName = newDict.get(i)
                            if newName:
                                r.set('sub:' + newName + ':1min', json.dumps(result1))
                                print(newName, r.get('sub:' + newName + ':1min'))
                                # print('sub:' + newName + ':1min')
                            # print(iu,r.get('sub:' + iu + ':1min'))
                except:
                    time.sleep(10)
                    break
        except:
            time.sleep(5)
            pass


if __name__ == '__main__':
    currnames = {'hb10usdt': 'sancusdt', 'qtumusdt': 'miosusdt', 'xmrusdt': 'xmrcusdt', 'atomusdt': 'ztcyusdt',
                 'neousdt': 'hexcusdt', 'dcrusdt': 'hxtcusdt', 'lambusdt': 'lambusdt', 'btmusdt': 'btmusdt',
                 'ontusdt': 'ontusdt', 'wiccusdt': 'wiccusdt','bhdusdt':'acxusdt','xzcusdt':'axccusdt'}
    p = Pool(len(currnames))
    for i in currnames:
        res = p.apply_async(m, args=(i, currnames.get(i),))
    p.close()
    p.join()


