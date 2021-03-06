import socketserver
import redis
import time
import json

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

class MyThreadingTCPServer(socketserver.ThreadingTCPServer):
    """重写socketserver.ThreadingTCPServer"""
    # 服务停止后即刻释放端口，无需等待tcp连接断开
    allow_reuse_address = True


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        # 创建一个链接,继承于socketserver中的BaseRequestHandler类
        conn = self.request
        global_num = 0
        message = conn.recv(1024)
        ss=message.decode('utf-8')

        while 1:
            if global_num<500:
                try:
                    # if 'handicap' in ss:
                    #     time.sleep(15)
                    #     conn.close()
                    #     break
                    response_text = r.get(ss)
                    # print(response_text)
                    if response_text == None:
                        # print(2,ss,conn)
                        time.sleep(15)
                        conn.close()
                        break
                    elif response_text:
                        try:
                            conn.sendall(response_text.encode('utf-8'))
                        except:
                            conn.close()
                            break
                except Exception as e:
                    print(e,conn)
                    badkey='订阅信息有误'
                    try:
                        conn.sendall(badkey.encode('utf-8'))
                    except Exception as e:
                        print(e)
                    print(3,ss,conn)
                    time.sleep(10)
                    # conn.shutdown(1)
                    conn.close()
                    break
                global_num=global_num+1
                time.sleep(0.25)
            else:
                #创建字典，内容为当前
                data={}
                data['ping']=int(time.time())
                time_stamp=data['ping']
                data=json.dumps(data)
                conn.sendall(str(data).encode('utf-8'))
                message = conn.recv(1024)
                message=message.decode('utf-8')
                message=json.loads(message)

                if int(message['pong'])==int(time_stamp):
                    global_num = 0
                else:
                    # conn.shutdown(2)
                    conn.close()
                    break

if __name__ == "__main__":
    server = MyThreadingTCPServer(('0.0.0.0', 999, ), MyServer)
    server.serve_forever()




