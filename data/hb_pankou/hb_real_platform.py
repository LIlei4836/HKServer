from websocket import create_connection
import requests
import gzip
import time
import json
import redis
import threading


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def get_name(b,platformlist):
    threadinglist=list()
    for platform in platformlist:
        t1 = threading.Thread(target=get_data, args=(b,platform,))
        threadinglist.append(t1)
    for t1 in threadinglist:
        t1.start()
    for t1 in threadinglist:
        t1.join()


def get_data(b,platform):
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
                        data = data['tick']['data'][0]
                        res = {}
                        k = platform[1]
                        v = platform[2]

                        res['time'] = data['ts']
                        res['amount'] = data['amount']*k+v
                        res['price'] = data['price']*k+v
                        res['type'] = data['direction']
                        r.set('real:'+platform[0]+':1min',json.dumps(res))
                        print('real:'+platform[0]+':1min')
                        print(r.get('real:'+platform[0]+':1min'))

                    time.sleep(0.05)
        except Exception as e:
            print(e)
            time.sleep(10)
if __name__ == '__main__':
    B = {'etcusdt':[['hklusdt',1,-4.83]],'linkusdt':[['grtusdt',0.03,0],],'iostusdt':[['stbeusdt',0.1,0.16],],'lambusdt':[['fgcusdt',10,0.17]]}
    threadinglist = list()
    for b in B :
        t1 = threading.Thread(target=get_name, args=(b,B.get(b),))
        threadinglist.append(t1)
    for t1 in threadinglist:
        t1.start()
    for t1 in threadinglist:
        t1.join()
