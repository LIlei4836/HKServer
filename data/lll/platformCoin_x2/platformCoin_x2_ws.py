from coreX2 import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            paramDict = {'TRX':['5gch',15,0],'AKRO':['cht',5,0]}

            # ok,币安没有ARKO
            # paramDict = {'TRX': ['5gch', 15, 0]}

            currency=Currency()
            currency.name=name
            currency.name2 = paramDict[name][0]
            # currency.sub_bian(k=paramDict[name][1],b=paramDict[name][2])
            # currency.sub_ok(k=paramDict[name][1],b=paramDict[name][2])
            currency.sub_huobi(k=paramDict[name][1],b=paramDict[name][2])
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=['TRX','AKRO']
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


