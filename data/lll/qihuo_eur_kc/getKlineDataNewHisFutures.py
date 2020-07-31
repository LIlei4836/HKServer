#!/usr/bin/python3
#coding: utf-8
"""
通过对期货接口获取最新价格存入redis，为ser提供期货推送数据
同时对redis中有序集合数据进行更新，插入。为http接口返回历史数据，提供数据支持

"""


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


"""
根据币种名称每个进程，起多个线程:
symbol     期货数据接口链接中 期货代号
currsname  期货对儿名称（存入redis）
"""
def getname(symbol,currsname):
    B = {'1':'1min','5':'5min','15':'15min','30':'30min','60':'60min','D':'1day','W':'1week','M':'1mon'}
    for resolution in B:
        t1 = threading.Thread(target=getdata, args=(resolution,symbol,currsname,B.get(resolution)))
        t1.start()
    t1.join()

"""
进行redis有序集合存储：
data           获取最新数据内容，
currsname      币对儿名称
time_name      时间名
有序集合键名称：market:wtiusdt:1min:redisSortset3.2.12
"""
def saveRedisSorted(data,currsname,time_name):
    # 删除当前时间戳的数据，然后再插入一条，作为更新，下面则为插入
    r.zremrangebyscore("market:" + currsname + ":" + time_name + ":redisSortset3.2.12", data['id'], data['id'])
    # 有序集合内容为json串，分数必须为int类型
    r.zadd("market:" + currsname + ":" + time_name + ":redisSortset3.2.12", {json.dumps(data): data['id']})
    # 只保留有序集合最近2018条
    r.zremrangebyrank("market:" + currsname + ":" + time_name + ":redisSortset3.2.12", 0, -2018)


"""
拼接请求地址，请求最新数据存入redis，同时更新历史数据中有序集合数据：
resolution 链接中的时间参数
symbol     链接中期货代号
currsname  期货对儿名称（存入redis）
time_name  期货对儿时间名称（存入redis）

"""
def getdata(resolution,symbol,currsname,time_name):
    reso={'1':[60*2,40,10],'5':[60*10,200,50],'15':[15*60*2,600,150],'30':[30*60*2,1200,300],'60':[60*60*2,2400,600],
          'D':[60*60*24*2,57600,14400],'W':[60*60*24*7*2,403200,100800],'M':[60*60*24*30*2,1728000,432000]}
    #不同时间段 from的时间要不同，从上面的字典中设置
    time_len=int(reso.get(resolution)[0])

    while 1:
        try:
            a=int(reso.get(resolution)[1])
            b=int(reso.get(resolution)[2])
            time_stamp=int(time.time())
            url = "http://tvc4.forexpros.com/2b3e7c8c1966d9488b9b637c11017675/"\
                  +str(time_stamp)+"/6/6/28/history?symbol="+str(symbol)+"&resolution" \
                  "="+str(resolution)+"&from="+str(time_stamp-time_len)+"&to="+str(time_stamp)
            # print(url)
            result = get_html_bytes(url)
            result = str(result, encoding='utf-8')
            #转化成dict
            result=eval(result)
            #当停盘时候不更新数据
            if 'nextTime' in result.keys():
                pass
            else:
                #只取接口中最后一条数据，
                res={}
                res['id']=result['t'][-1]
                res['high'] = result['h'][-1]
                res['open'] = result['o'][-1]
                res['low'] = result['l'][-1]
                res['close'] = result['c'][-1]
                res['vol'] = random.random() * b+a
                result = json.dumps(res)
                # print(result)
                #存进redis中的值必须为json，
                r.set('sub:' + currsname + ':' + time_name, result)
                print(currsname, time_name, r.get('sub:' + currsname + ':' + time_name))
                #但是进入有序集合之前需要使用字典，
                saveRedisSorted(res, currsname, time_name)
                time.sleep(0.5)
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':

    A = {'1':'eurusdt','8832':'kcusdt'}
    p = Pool(len(A))
    for symbol in A:
        p.apply_async(getname, args=(symbol,A.get(symbol),))
        print('进程' + symbol + '启动成功！')
    p.close()
    p.join()







