#!/usr/bin/python3
#coding: utf-8
from flask import Flask
import json
import redis

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

app = Flask(__name__)
@app.route('/symbol2/<symbol>/period/<period>/size/<int:size>')
def get_hongbao2(symbol, period, size):
    data = []
    data_youxu = r.zrange('market:' + symbol + ':' + period + ':redisSortset3.2.12', 0, size - 1, desc=True)
    # 由于有序集中存储的是dic，故应将每一部分转化成json再通过接口给返回
    # print(data_youxu)
    for str1 in data_youxu:
        #字典形式的字符串  转字典，eval()
        # print(str1)
        data_dict = eval(str(str1))
        #字典直接压入数组中
        data.append(data_dict)
    #将数组用json.dumps 转化即可形成标准json串
    data = json.dumps(data)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)