#coding: utf-8
from websocket import create_connection
import requests
import gzip
import json
import redis
import time
import random
import threading


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def m(i):
    while 1:
        fk={'btcusdt':1, 'bchusdt':11, 'ethusdt':2, 'ltcusdt':6, 'etcusdt':9, 'xrpusdt':10, 'eosusdt':4}
        try:

            tradeStr = """{"sub": "market.""" + i + """.kline.1min","id": "id1"}"""
            ws = create_connection("wss://api.huobi.br.com/ws", timeout=10)
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
                    except :
                        data = data['tick']
                        result1 = {}
                        try:
                            url = "http://www.cebar.top/api/Riskmanagement/fkMethod?cid=" + str(fk.get(i))
                            print(url)
                            response = requests.get(url)
                            response = float(response.content.decode())
                            r.set('hlg:cebar:fk:'+i,response)
                        except:
                            pass
                        response=float(r.get('hlg:cebar:fk:'+i))
                        result1["id"] = data['id']
                        result1["vol"] = data['vol']
                        result1["high"] =data['high'] + float(response)
                        result1["open"] =data['open'] + float(response)
                        result1["low"] = data['low'] + float(response)
                        result1["close"] = data['close'] + float(response)
                        data = json.dumps(result1)
                        r.set('sub:cebar:'+i+':1min', data)
                        print(r.get('sub:cebar:'+i+':1min'))
        except Exception as e:
            time.sleep(10)

if __name__ == '__main__':
        currnames = ['btcusdt','bchusdt','ethusdt','ltcusdt','etcusdt','xrpusdt','eosusdt']
        for i in currnames:
            t1 = threading.Thread(target=m,args = (i,))
            t1.start()
        t1.join()


