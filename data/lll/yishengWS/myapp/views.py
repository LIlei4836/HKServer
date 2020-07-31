import json
import time
import datetime
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse
import redis

import logging


fmt = '%(asctime)s , %(levelname)s , %(filename)s %(funcName)s line %(lineno)s , %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S %a'
logging.basicConfig(level=logging.ERROR,
format=fmt,
datefmt=datefmt,
filename="log.txt")

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

clients = []
@accept_websocket
def getData(request):
    # 判断是不是websocket连接
    if not request.is_websocket():
        pass
    else:
        clients.append(request.websocket)
        time.sleep(3)
        while True:
            if request.websocket.count_messages() > 0:

                for message in request.websocket:
                    print(clients,message)
                    if request.websocket.is_closed():
                        print('连接关闭了',request.websocket)
                        clients.remove(request.websocket)
                        time.sleep(5)
                        return HttpResponse('连接断开')
                    else:
                        message = str(message, encoding='utf-8')
                        global flag
                        flag = True
                        lastClose = float(0)
                        while flag:
                            if request.websocket.is_closed():
                                for client in clients:
                                    client.close()
                                    try:
                                        clients.remove(client)
                                    except:
                                        pass
                                # print(clients)
                                print('连接关闭',request.websocket)
                                flag = False
                                return HttpResponse('连接断开')
                            else:
                                try:
                                    data = r.get(message)
                                    if not data:
                                        flag = False
                                        time.sleep(5)
                                        break
                                    data = json.loads(data)
                                    newClose = data.get('close')
                                    if newClose and lastClose != newClose:
                                        request.websocket.send(json.dumps(data))
                                        lastClose = data['close']
                                        t = time.time()
                                    elif time.time() - t > 28:
                                        request.websocket.send(json.dumps(data))
                                        t = time.time()
                                        # global_num = global_num + 1
                                except Exception as e:
                                    print(e)
                                    result = bytes('暂无此币种', encoding='utf-8')
                                    print(str(result, encoding='utf-8'))
                                    request.websocket.send(result, )
                                    request.websocket.close()
                                    time.sleep(5)
                                    # flag = False
                                    break
            time.sleep(0.1)





