#coding=utf-8
from utils import get_html,get_html_bytes,get_html_bytes_no_daili
import redis
import time
from multiprocessing import Pool
import json
import threading
import websockets
import asyncio


newWebsocket = asyncio.new_event_loop()
"""
获取各个币种历史数据存入redis中
"""
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
def getname(time1):
    #多线程，每个货币对儿一个线程
    B = {'hb10usdt': 'sancusdt', 'qtumusdt': 'miosusdt', 'xmrusdt': 'xmrcusdt', 'atomusdt': 'ztcyusdt','neousdt': 'hexcusdt', 'dcrusdt': 'hxtcusdt',
         'lambusdt': 'lambusdt', 'btmusdt': 'btmusdt','ontusdt': 'ontusdt', 'wiccusdt': 'wiccusdt','bhdusdt':'acxusdt','xzcusdt':'axccusdt'}
    thread_lists = list()
    for currsname in B:
        t1 = threading.Thread(target=getdata, args=(currsname, time1,B.get(currsname),))
        t1.start()
        thread_lists.append(t1)
    for thread_list in thread_lists:
        thread_list.join()

async def hello(res):
    try:
        async with websockets.connect('ws://47.52.18.210:7000')as websocket:
        # async with websockets.connect('ws://localhost:7000')as websocket:
            await websocket.send(json.dumps(res))
                # time.sleep(3)

    except Exception as e:

        time.sleep(10)


newDict = {'hb10usdt':'ancdusdt','qtumusdt':'miscusdt','neousdt':'hecusdt','dcrusdt':'xttcusdt','atomusdt':'xzctusdt','xmrusdt':'mrdusdt'}

def getdata(symbol,period,iu):
    while 1:
        try:
            # url = "https://api.huobi.me/market/history/kline?symbol="+symbol+"&size=300&period="+period
            url = "http://api.huobi.br.com/market/history/kline?symbol="+symbol+"&size=300&period="+period
            result = get_html(url)

            if result[1:5] in 'html':
                pass
            else:
                result = json.loads(result)['data']
                for res in result:
                    res['open']=res['open']
                    res['close']=res['close']
                    res['high']=res['high']
                    res['low']=res['low']

                data = {}
                data['data']= json.dumps(result)
                data['key'] = 'market:'+iu+':'+period
                result = '{"data":'+json.dumps(result)+'}'

                r.set('market:'+iu+':'+period, result)

                newName = newDict.get(symbol)
                if newName:
                    r.set('market:' + newName +':' +period, result)
                    # print(('market:' + newName + ':' + period))

                # print(('market:'+iu+':'+period))
                # print(r.get('market:'+iu+':'+period))

                # newWebsocket.run_until_complete(hello(data))
                # print(data)
        except:
            pass
        time.sleep(30)


if __name__ == '__main__':
    #多进程，每个时间段的行情一个进程
    A = ['1min', '5min', '15min', '30min', '60min', '1day', '1mon', '1week', '1year']
    p = Pool(len(A))
    for i in A:
        p.apply_async(getname, args=(i,))
        print('进程' + i + '启动成功！')
    p.close()
    p.join()













