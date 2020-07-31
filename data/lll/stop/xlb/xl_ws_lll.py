from core import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            paramDict = {'btc': ['btc', 'xl', '2',1],'eth': ['eth', 'xl', '3',1],'ltc': ['ltc', 'xl', '4',1],'etc': ['etc', 'xl', '5',1],
                         'bch': ['bch', 'xl', '6',1],'eos': ['eos', 'xl', '7',1],'xrp': ['xrp', 'xl', '8',1],}
            riskManageUrl = 'http://www.xlbex.net/api/Riskmanagement/fkMethod?cid='
            currency=Currency()
            currency.name=name
            currency.name2 = paramDict[name][0]
            currency.projectName = paramDict[name][1]
            #   currency.riskUrl = riskManageUrl+paramDict[name][2]
            # currency.sub_bian()
            # currency.sub_ok()
            currency.sub_huobi(paramDict[name][3])
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=['btc','eth','ltc','etc','bch','eos','xrp']
# currency_list=['eos']
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


