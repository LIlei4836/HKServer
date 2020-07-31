
import json
from ws4py.client.threadedclient import WebSocketClient
import gzip

class CG_Client(WebSocketClient):
    def opened(self):
        req = 'handicap:btcusdt:1min' #发送相应格式
        self.send(req)

    def closed(self, code, reason=None):
        connect_wss()

    def received_message(self, resp):
        resp = str(resp.data, encoding='utf-8')
        # resp = gzip.decompress(resp.data).decode('utf-8')
        if 'ping' in resp:
            result = json.loads(resp)
            pong = {}
            pong['pong'] = result['ping']
            self.send(json.dumps(pong))
        print(json.loads(resp))

def connect_wss():
    url = 'ws://127.0.0.1:888/getData'
    try:  # 这里是订阅，一定要先订阅，一定要先订阅
        ws = CG_Client(url)
        ws.connect()
        ws.run_forever()  # 执行命令
    except KeyboardInterrupt:
        ws.close()


if __name__ == '__main__':
    connect_wss()
