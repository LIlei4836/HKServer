#coding: utf-8
from websocket import create_connection
import zlib
import json
import redis
import requests
from utils import UTC_to_timeStamp
import gzip
import queue


q = queue.Queue()

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
class Currency(object):
    #构造函数
    def __init__(self):
        self.data={}         #最终数据
        self.name=None       #真名
        self.name2=None      #别名
        self.projectName=None#项目名称
        self.riskUrl=None    #风控接口

    #OK数据解压缩
    def inflate(self,data):
        decompress = zlib.decompressobj(-zlib.MAX_WBITS)
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated

    #得到风控数据
    def get_riskNum(self):
        if not self.name2:
            self.name2=self.name
        if self.riskUrl:
            try:
                response = requests.get(self.riskUrl)
                response = float(response.content.decode())
                r.set('hlg:' + self.projectName + ':' + self.name2 + ':riskNum', response)
                # print(('hlg:' + self.projectName + ':' + self.name2 + ':riskNum'))
            except:
                pass
            c = float(r.get('hlg:' + self.projectName + ':' + self.name2 + ':riskNum'))
        else:
            c = 0
        return c

    #将数据存入redis
    def save_data(self):
        sub_name = self.name2.lower() + 'usdt'
        if self.riskUrl:
            r.set('sub:' + self.projectName + ':' + sub_name + ':1min', self.data)
            # print('sub:' + self.projectName + ':' + sub_name + ':1min')

            print(r.get('sub:' + self.projectName + ':' + sub_name + ':1min'))
        else:
            r.set('sub:' + sub_name + ':1min', self.data)
            # print('sub:' + sub_name + ':1min')
            print(sub_name, r.get('sub:' + sub_name + ':1min'))

    #订阅OK数据源
    def sub_ok(self,k=1,b=0):
        tradeStr = """{"op": "subscribe", "args": ["spot/candle60s:"""+self.name+"""-USDK"]}"""
        ws = create_connection("wss://okexcomreal.bafang.com:8443/ws/v3")
        ws.send(tradeStr)
        while 1:
            compressData = ws.recv()
            data_unzip = self.inflate(compressData).decode(encoding='utf-8')
            data_list = json.loads(data_unzip).get('data')
            if data_list :
                #如果风控地址不存在则c=0
                c=self.get_riskNum()
                data = data_list[0]
                result = {}
                result["id"] = UTC_to_timeStamp(data['candle'][0])
                result["open"] = float(data['candle'][1])*k+b+c
                result["high"] = float(data['candle'][2])*k+b+c
                result["low"] = float(data['candle'][3])*k+b+c
                result["close"] = float(data['candle'][4])*k+b+c
                result["vol"] = float(data['candle'][5])/100
                result["name"]=self.name2
                self.data=json.dumps(result)
                self.save_data()


    #订阅火币数据源
    def sub_huobi(self,k=1,b=0):
        tradeStr = """{"sub": "market.""" + self.name.lower() + """husd.kline.1min","id": "id1"}"""
        ws = create_connection("wss://api.huobiasia.vip/ws")
        ws.send(tradeStr)
        while (1):
            compressData = ws.recv()
            result_dic = json.loads(gzip.decompress(compressData).decode('utf-8'))
            if 'ping' in result_dic.keys():
                ts = result_dic['ping']
                data={}
                data['pong']=ts
                ws.send(json.dumps(data))
            else:
                if 'status' in result_dic.keys():
                    pass
                else:
                    result_dic = result_dic['tick']
                    del result_dic['count'], result_dic['vol']
                    c=self.get_riskNum()
                    result_dic["vol"] = result_dic.pop("amount")/10
                    result_dic['open']=result_dic['open']* k + b + c
                    result_dic['high']=result_dic['high']* k + b + c
                    result_dic['low']=result_dic['low']* k + b + c
                    result_dic['close']=result_dic['close']* k + b + c
                    result_dic["name"] = self.name2
                    self.data=json.dumps(result_dic)
                    self.save_data()
    #订阅币安数据
    def sub_bian(self,k=1,b=0):
        ws = create_connection("wss://stream2.binance.cloud/ws/"+self.name.lower()+"usdt@kline_1m.b10")
        while 1:
            resp = json.loads(str(ws.recv()))
            resp = resp['k']
            c=self.get_riskNum()
            L = {}
            L['id'] = int(resp['t'] / 1000)
            L['high'] = float(resp['h'])* k + b + c
            L['open'] = float(resp['o'])* k + b + c
            L['low'] = float(resp['l'])* k + b + c
            L['close'] = float(resp['c'])* k + b + c
            L['vol'] = float(resp['v'])
            L['name']=self.name2
            self.data = json.dumps(L)
            self.save_data()
