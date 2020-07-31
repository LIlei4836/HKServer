from core_usdt import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            paramDict = {'USDT':['bfb',0.1,0.046],}

            currency=Currency()
            currency.name=name
            currency.name2 = paramDict[name][0]
            # 无币安
            # currency.sub_ok(k=paramDict[name][1],b=paramDict[name][2])
            currency.sub_huobi(k=paramDict[name][1],b=paramDict[name][2])
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=['USDT',]
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


