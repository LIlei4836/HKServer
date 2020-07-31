from core import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            paramDict = {'LTC': ['cib', 4,10],'LAMB':['fgc',10,0.17],'ZIL':['usk',20,0],'LINK':['grt',0.03,0],'IOST':['stbe',0.1,0.16]}

            currency=Currency()
            currency.name=name
            currency.name2 = paramDict[name][0]
            # currency.sub_bian()
            # currency.sub_ok(k=paramDict[name][1],b=paramDict[name][2] )
            currency.sub_huobi(k=paramDict[name][1],b=paramDict[name][2])
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=['LTC','LAMB','ZIL','LINK','IOST']
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


