from core import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            paramDict = {'XRP':['ghb',3,0],'TRX': ['cwz', 1000, -3.9]}

            currency=Currency()
            currency.name=name
            currency.name2 = paramDict[name][0]
            # currency.sub_bian()
            # currency.sub_ok()
            currency.sub_huobi(k=paramDict[name][1],b=paramDict[name][2])
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=['XRP','TRX']
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


