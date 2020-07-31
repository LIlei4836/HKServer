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
    B = {'btcusdt':[['cgbusdt',10,0],['bhvusdt',100,0],]}
    for symbol in B:
        for time1 in A:
            t1 = threading.Thread(target=getdata, args=(symbol,time1,B.get(symbol)))
            threadlist.append(t1)
    for t1 in threadlist:
        t1.start()
    for t1 in threadlist:
        t1.join()



def getdata(symbol,period,platforms):

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


            # print(asks)

            for platform in platforms:

                bidList = list()
                for bid in range(len(bids)):
                    bidDetailList = list()
                    bidDetailList.append(bids[bid][0]*platform[1]+platform[2])
                    bidDetailList.append(bids[bid][1])
                    bidList.append(bidDetailList)

                askList = list()
                for ask in range(len(asks)):
                    askDetailList = list()
                    askDetailList.append(asks[ask][0] * platform[1] + platform[2])
                    askDetailList.append(asks[ask][1])
                    askList.append(askDetailList)


                dataDict = dict()

                dataDict['buy'] = bidList
                dataDict['sell'] = askList
                dataDict['t'] = int(ts/1000)
                # dataDict['key'] = 'depth:' + symbol + ':' + period

                keyDict = ['depth:', platform[0], ':', period]
                key = ''.join(keyDict)

                print(key)
                # r.set(key, json.dumps(dataDict))
                # print(r.get('depth:'+symbol+':'+period))
                # print('depth:' + symbol + ':' + period)
        except Exception as e:
            print(e)

        time.sleep(5)






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
