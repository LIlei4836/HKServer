from huobi.client.account import AccountClient
from huobi.constant import *
from huobi.utils import LogInfo

account_client = AccountClient(api_key='9080b14c-e5301376-bg2hyw2dfg-d3382',
                               secret_key='d120aab4-a632d31e-0598cbd0-446c6')
LogInfo.output("====== (SDK encapsulated api) not recommend for low performance and frequence limitation ======")
account_balance_list = account_client.get_account_balance()
if account_balance_list and len(account_balance_list):
    for account_obj in account_balance_list:
        account_obj.print_object()
        print()