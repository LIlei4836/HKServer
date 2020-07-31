# -*- coding=utf-8  -*-
# @Time: 2020/6/12 10:13
# @Author: LeiLei Li
# @File: hb_depth.py

import requests
from utils import get_html,get_html_bytes
import json
from multiprocessing import Pool
import threading
import redis
import time



r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)


def getname():
    #多线程，每个货币对儿一个线程
    threadlist = list()

    A = ['step0', 'step1', 'step2', 'step3', 'step4', 'step5', ]
    B = {'btcusdt', 'ethusdt', 'htusdt', 'xrpusdt', 'ltcusdt', 'eosusdt', 'etcusdt', 'trxusdt','bchusdt'}
    for symbol in B:
        for time1 in A:
            t1 = threading.Thread(target=getdata, args=(symbol,time1))
            threadlist.append(t1)
    for t1 in threadlist:
        t1.start()
    for t1 in threadlist:
        t1.join()



def getdata(symbol,period):
    while 1:
        try:
            urlDict = ['http://api.huobiasia.vip/market/depth?symbol=', symbol, '&type=', period, '&depth=10']
            url = ''.join(urlDict)
            # print(url)

            res = get_html(url,)
            if res == None:
                time.sleep(1)
                continue
            result = json.loads(res)
            ts = result.get('ts')
            data = result.get('tick')
            bids = data.get('bids')
            asks = data.get('asks')

            dataDict = dict()

            # bidslist = dict()
            # for bid in bids:
            #     bidslist[bid[0]] = bid[1]
            #
            #
            # askslist = dict()
            # for ask in asks:
            #     askslist[ask[0]] = ask[1]

            dataDict['buy'] = bids
            dataDict['sell'] = asks
            dataDict['t'] = int(ts/1000)
            # dataDict['key'] = 'depth:' + symbol + ':' + period

            keyDict = ['depth:', symbol, ':', period]
            key = ''.join(keyDict)
            r.set(key, json.dumps(dataDict))
            # print(r.get('depth:'+symbol+':'+period))
            # print('depth:' + symbol + ':' + period)
        except Exception as e:
            print(e)

        time.sleep(1)






if __name__ == '__main__':
    getname()
    # #多进程，每个时间段的行情一个进程
    # A = ['step0','step1', 'step2', 'step3', 'step4', 'step5',]
    # # A = ['step1']
    # p = Pool(len(A))
    # for i in A:
    #     p.apply_async(getname, args=(i,))
    #     print('进程' + i + '启动成功！')
    # p.close()
    # p.join()
