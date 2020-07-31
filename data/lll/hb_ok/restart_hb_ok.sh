#!/bin/sh

# hb
ps -ef|grep hbRedisHlg.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/hlg/huobi_http/backup_ok/okRedisHlg.py > /dev/null 2>&1 &

ps -ef|grep hbRedisHlg_1.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/hlg/huobi_http/backup_ok/okRedisHlg_1.py > /dev/null 2>&1 &

ps -ef|grep hbRedisHlg_2.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/hlg/huobi_http/backup_ok/hb_other.py > /dev/null 2>&1 &


# qr
ps -ef|grep qr2_ws_ht.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/ht/data/qryh/backup_ok/qr2_ws_ok.py > /dev/null 2>&1 &


# spc
ps -ef|grep main_spc.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/ht/data/SPC.WTH/backup_ok/main_spc_hb.py > /dev/null 2>&1 &
nohup python3 -u /ht/ht/data/SPC.WTH/backup_ok/main_wth_ok.py > /dev/null 2>&1 &


#ect
ps -ef|grep ect_ws_lll.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/ht/data/lll/ect/backup_ok/ect_ws_lll_ok.py > /dev/null 2>&1 &




# platformCoin
ps -ef|grep platformCoin_ws.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/ht/data/lll/platformCoin/backup_ok/platformCoin_ws_ok.py > /dev/null 2>&1 &


ps -ef|grep platformCoin_one_ws.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/ht/data/lll/platformCoin_one/backup_ok/platformCoin_one_ws_ok.py > /dev/null 2>&1 &


ps -ef|grep platformCoin_two_ws.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/ht/data/lll/platformCoin_two/backup_ok/platformCoin_two_ws_ok.py > /dev/null 2>&1 &


ps -ef|grep platformCoin_three_ws.py | grep -v grep |cut -c 9-15|xargs kill -s 9
nohup python3 -u /ht/ht/data/lll/platformCoin_three/backup_ok/platformCoin_three_ws_ok.py > /dev/null 2>&1 &