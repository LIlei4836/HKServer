#coding: utf-8
from websocket import create_connection
import requests
import gzip
import json
import redis
import time
import random
import threading
from multiprocessing import Pool


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def getname(time1):
    #多线程，每个货币对儿一个线程
    B = {'bichkc':['trxusdt','jtbusdt']}
    for symbol in B:
        t1 = threading.Thread(target=getdata, args=(symbol,time1, B.get(symbol)))
        t1.start()
    t1.join()

def getdata(symbol,time1, currency):
    while 1:
        try:
            tradeStr = """{"sub": "market.""" + currency[0] + """.kline."""+time1+"""","symbol":""" + "\"" + time1 + "\"}"
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
                        try:
                            url = "http://www.bichkc.com/api/Riskmanagement/fkMethod?cid=9"
                            response = requests.get(url, timeout=2)
                            response = float(response.content.decode())
                            r.set('lll:'+symbol+':fk:'+currency[0],response)
                        except:
                            pass
                        response = float(r.get('lll:'+symbol+':fk:'+currency[0]))
                        data["id"] = data['id']
                        # result1["vol"] = random.random() * 10 + 4
                        count = 144
                        multiplier = 10000
                        data["high"] =abs(data['high']*multiplier-count) + response
                        data["open"] =abs(data['open']*multiplier-count) + response
                        data["low"] = abs(data['low']*multiplier-count) + response
                        data["close"] = abs(data['close']*multiplier-count)+ response
                        data = json.dumps(data)
                        r.set('sub:'+'xueusdt'+':'+time1, data)
                        print(currency[0],time1,r.get('sub:'+'xueusdt'+':'+time1))
        except Exception as e:
            time.sleep(10)

if __name__ == '__main__':
    A = ['1min']
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
    p.close()
    p.join()


