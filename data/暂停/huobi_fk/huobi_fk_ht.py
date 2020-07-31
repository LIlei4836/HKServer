#!/usr/bin/python3
#coding: utf-8
from websocket import create_connection
import gzip
import time
import json
import redis
import requests
import random
from multiprocessing import Pool
import threading

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def getname(time1):
    B = {'btcusdt':'BTC', 'ethusdt':'ETH', 'ltcusdt':'LTC', 'bchusdt':'BCH', 'eosusdt':'EOS', 'xrpusdt':'XRP', 'etcusdt':'ETC','trxusdt':'TRX'}
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname,B.get(currsname),time1,))
        t1.start()
    t1.join()

def getdata(currsname,codeName,time1):
    while 1:
        try:
            tradeStr = """{"sub": "market."""+currsname+""".kline."""+time1+"""","id": "id1"}"""
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
                        # 对数据的处理
                        data=data['tick']
                        # try:
                        #     url = "http://www.silvercontract.top/api/System/getFkData?coinName="+str(codeName)
                        #     resp = float(requests.get(url,timeout=2).content.decode())
                        #     r.set('hlg:yixin:fk:'+codeName,resp)
                        # except:
                        #     pass
                        resp=float(r.get('hlg:yixin:fk:'+codeName))
                        data['id'] = data['id']
                        data['high'] = data['high'] + resp
                        data['open'] = data['open'] + resp
                        data['low'] = data['low'] + resp
                        data['close'] = data['close'] + resp
                        del data['count'], data['vol'], data['amount']
                        data = json.dumps(dict(data))
                        b = r.lrange('fk:'+currsname+':'+time1, 0, 0)
                        try:
                            if b:
                                if b != 't':
                                    b = b[0][19:-1]
                                if data != 't':
                                    c = data[19:-1]
                                if c != b :
                                    if json.loads((r.lrange('fk:'+currsname+':'+time1, 0, 0))[0])['id'] == json.loads(data)['id']:
                                        r.lpop('fk:'+currsname+':'+time1)
                                        r.lpush('fk:'+currsname+':'+time1, data)
                                    else:
                                        r.lpush('fk:' + currsname + ':' + time1, data)
                                else:
                                    pass
                            else:
                                r.lpush('fk:'+currsname+':'+time1,data)

                            fk_data = r.lrange('fk:'+currsname+':'+time1,0,0)[0]
                            fk_data = json.loads(fk_data)
                            fk_data["vol"] = random.random()*22+12

                            r.set('sub:risk:'+currsname+':'+time1,json.dumps(fk_data))
                            print('sub:risk:'+currsname+':'+time1)
                        except:
                            pass

        except Exception as e:
            print(currsname,time1,e)
            time.sleep(20)

if __name__ == '__main__':
    A = ['1min']
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()



