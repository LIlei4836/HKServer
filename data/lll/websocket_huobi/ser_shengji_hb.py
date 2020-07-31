# -*- coding = utf-8  -*-
# @Time: 2020/6/1 14:36
# @Author: 李雷雷
# @File: socket_server.py

# @Motto:不积跬步无以至千里，不积小流无以成江海，程序人生的精彩需要坚持不懈地积累！


import sys
import socket
import time
import gevent
from gevent import socket, monkey
import redis
import threading
import json

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

monkey.patch_all()


def server(port):
    try:
        s = socket.socket()
        s.bind(('0.0.0.0', port))
        s.listen(1000)
        while True:
            cli, addr = s.accept()
            gevent.spawn(handle_request, cli)
    except KeyboardInterrupt as e:
        print(e)


def handle_request(conn):
    global_num = 1
    lastClose = float(0)
    try:
        data = conn.recv(1024)

        while True:
            if global_num > 0:
                if not data:
                    conn.close()
                else:
                    result = r.get(data)

                    try:
                        # 请求最新价
                        newClose = json.loads(result).get('close')
                        if newClose and lastClose != newClose:
                            result = result.encode('utf-8')
                            conn.send(result)
                            lastClose = json.loads(result)['close']
                        elif newClose and global_num>5000:
                            result = result.encode('utf-8')
                            conn.send(result)
                            global_num = 1
                        elif not newClose:
                            # 其他类型的key
                            result = result.encode('utf-8')
                            conn.send(result)
                            if global_num >500:
                                global_num = 1
                            time.sleep(0.1)
                        time.sleep(0.15)
                    except Exception as e:
                        try:
                            badkey = '订阅信息有误'
                            conn.sendall(badkey.encode('utf-8'))
                            time.sleep(5)

                        except Exception as e:
                            print(1,e)
                        finally:
                            conn.close()
                            break
                global_num = global_num + 1
            else:
                # 创建字典，内容为当前
                datas = {}
                datas['ping'] = int(time.time())
                time_stamp = datas['ping']
                datas = json.dumps(datas)
                conn.sendall(str(datas).encode('utf-8'))
                message = conn.recv(1024)
                message = message.decode('utf-8')
                message = json.loads(message)

                print(message)

                if int(message['pong']) == int(time_stamp):
                    global_num = 0
                else:
                    conn.close()
                    break

    except OSError as e:
        print("client has been closed")

    except Exception as ex:
        print(ex)
    finally:
        # print(22222222222222222222)
        time.sleep(5)
        conn.close()



if __name__ == '__main__':
    server(888)
