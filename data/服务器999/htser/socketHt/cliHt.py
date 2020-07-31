# 就是一个简单的TCP客户端
import socket
import time
import json
import os
import sys
os.chdir(sys.path[0])
# 连接服务端
while 1:
    try:
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sock = socket.socket()
        sock.connect(('127.0.0.1', 999, ))
        message='sub:btcusdt:1min'
        sock.sendall(message.encode('utf-8'))
        while True:
            try:
                data = sock.recv(1024)
                data=data.decode('utf-8')
                if data[2:6]=='ping':
                    data = json.loads(data)
                    data0={}
                    data0['pong']=data['ping']
                    data0=json.dumps(data0)
                    sock.sendall(data0.encode('utf-8'))
                elif len(data)<2:
                    sock.close()
                    break
                else:
                    # print(data)
                    data=json.loads(data)

                    # print(data)
            except ConnectionResetError as e:
                #断线重连
                localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print('neibu',localtime)
                break
    #再次重连则需要触发重启server端的逻辑。
    except ConnectionRefusedError as e:
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('调用shell脚本重启server端',localtime)
        os.system('./restartHtSer.sh')
        time.sleep(10)



