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

def getname(i,iu):
    B = ['1min']
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname,i,iu,))
        t1.start()
    t1.join()

def getdata(time1,currsname,codeName):
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

                        try:
                            url = "http://bitflyex.wlnxx.top/api/System/getFkData?coinName="+str(codeName[0])
                            resp = requests.get(url).content.decode()
                            data['id'] = data['id']
                            data['high'] = data['high'] + float(resp)
                            data['open'] = data['open'] + float(resp)
                            data['low'] = data['low'] + float(resp)
                            data['close'] = data['close'] + float(resp)
                            r.set('bitf_fk:'+str(codeName[0]),float(resp))
                        except:
                            resp = r.get('bitf_fk:'+str(codeName[0]))
                            data['id'] = data['id']
                            data['high'] = data['high'] + float(resp)
                            data['open'] = data['open'] + float(resp)
                            data['low'] = data['low'] + float(resp)
                            data['close'] = data['close'] + float(resp)

                        del data['count'], data['vol'], data['amount']
                        data = json.dumps(dict(data))
                        b = r.lrange('fk:'+codeName[1]+':'+time1, 0, 0)
                        try:
                            if b:
                                if b != 't':
                                    b = b[0][19:-1]
                                if data != 't':
                                    c = data[19:-1]
                                if c != b :
                                    if json.loads((r.lrange('fk:'+codeName[1]+':'+time1, 0, 0))[0])['id'] == json.loads(data)['id']:
                                        r.lpop('fk:'+codeName[1]+':'+time1)
                                        r.lpush('fk:'+codeName[1]+':'+time1, data)
                                    else:
                                        r.lpush('fk:' + codeName[1] + ':' + time1, data)
                                else:
                                    pass
                            else:
                                r.lpush('fk:'+codeName[1]+':'+time1,data)

                            fk_data = r.lrange('fk:'+codeName[1]+':'+time1,0,0)[0]
                            fk_data = json.loads(fk_data)
                            fk_data["vol"] = random.random()*22+12

                            r.set('sub:risk:'+codeName[1]+':'+time1,json.dumps(fk_data))
                        except:
                            time.sleep(5)
                            break

        except Exception as e:
            print(codeName[1],time1,e)
            time.sleep(20)

if __name__ == '__main__':
    A = {'bchusdt':['HB10','hb10usdt'], 'etcusdt':['NAS','nasusdt']}
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,A.get(i),))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()

