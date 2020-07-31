from core import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            paramDict = {'TRX':['nec',10000,-90],'ETC':['hkl',1,-4.83],'HT':['im',0.1,-0.24]}

            currency=Currency()
            currency.name=name
            currency.name2 = paramDict[name][0]
            # currency.sub_bian()
            # currency.sub_ok()
            currency.sub_huobi(k=paramDict[name][1],b=paramDict[name][2])
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=['TRX','ETC','HT']
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


