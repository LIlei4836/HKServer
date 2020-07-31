#!/usr/bin/python3
#coding: utf-8

#对redis中所需要的 有序集合更新初始化，本脚本运行一次即可，

#coding=utf-8
from userAgents import get_html,get_html_bytes
import sys
import redis
import time
import pymysql
from multiprocessing import Pool
import warnings
import json
import random
import threading


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
def getname(symbol,currsname):
    B = {'1':'1min','5':'5min','15':'15min','30':'30min','60':'60min','D':'1day','W':'1week','M':'1mon'}
    # B = {'60':'60min'}
    # B = {'1':'1min'}

    for resolution in B:
        t1 = threading.Thread(target=getdata, args=(resolution,symbol,currsname,B.get(resolution)))
        t1.start()
        t1.join()

def getdata(resolution,symbol,currsname,time_name):
    reso={'1':[60*1*500,40,10],'5':[60*5*500,200,50],'15':[15*60*500,600,150],'30':[30*60*500,1200,300],'60':[60*60*500,2400,600],
          'D':[60*60*24*500,57600,14400],'W':[60*60*24*7*300,403200,100800],'M':[60*60*24*30*150,1728000,432000]}
    # reso = {'1':[60*1*500,40,10]}
    #不同时间段 from的时间要不同，从上面的字典中设置
    time_len=int(reso.get(resolution)[0])

    a = int(reso.get(resolution)[1])
    b = int(reso.get(resolution)[2])
    time_stamp = int(time.time())
    url = "http://tvc4.forexpros.com/2b3e7c8c1966d9488b9b637c11017675/" \
          + str(time_stamp) + "/6/6/28/history?symbol=" + str(symbol) + "&resolution" \
                                                                        "=" + str(resolution) + "&from=" + str(
        time_stamp - time_len) + "&to=" + str(time_stamp)
    result = get_html_bytes(url)
    if result:
        try:
            result = str(result, encoding='utf-8')
        except Exception as e:
            print(url)
            print(result)
            print(currsname, time_name, 'baocuo')
        # 转化成dict
        result = eval(result)
        # 当停盘时候不更新数据
        if 'nextTime' in result.keys():
            # print('停盘中！')
            pass
        else:
            qihuo_dict = {}
            qihuo_list = []
            for i in range(len(result['t'])):
                res = {}
                res['id'] = result['t'][i]
                res['high'] = result['h'][i]
                res['open'] = result['o'][i]
                res['low'] = result['l'][i]
                res['close'] = result['c'][i]
                res['vol'] = random.random() * b + a
                qihuo_list.append(res)
            qihuo_dict['data'] = qihuo_list[::-1]
            result = json.dumps(qihuo_dict)
            if len(result) > 40:
                res = json.loads(result)
                for data in res['data']:
                    # 删除指定  分数  区间内的所有成员
                    r.zremrangebyscore("market:" + currsname + ":" + time_name + ":redisSortset3.2.12", data['id'],
                                       data['id'])
                    r.zadd("market:" + currsname + ":" + time_name + ":redisSortset3.2.12",
                           {json.dumps(data): data['id']})
            # 删除分数值最小的前10个，避免有垃圾数据（根据分数排名删除）
            r.zremrangebyrank("market:" + currsname + ":" + time_name + ":redisSortset3.2.12", 0, 10)
            print(currsname, time_name, 'ok')



if __name__ == '__main__':
    A = {'1':'eurusdt','8832':'kcusdt'}
    p = Pool(len(A))
    for symbol in A:
        p.apply_async(getname, args=(symbol,A.get(symbol),))
        print('进程' + symbol + '启动成功！')
    p.close()
    p.join()








