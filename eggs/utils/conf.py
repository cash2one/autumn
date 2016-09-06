# -*- coding: UTF-8 -*-

import re
from datetime import date


confs = {'backup':            '\\backup\\',
         'daily_news':        '\\daily_news\\',
         'data_update':      '\\data_update\\',
         'excel':             '\\excel\\',
         'data_db':           '\\data_db\\'
         }


NEWS_PATH = r'D:\csf_news' + '\\'
HOT_NEWS_PATH = '/home/daily_news/hot_news/'

db_path = 'D:/temp/' + ''.join(str(date.today()).split('-')[:2]) + '.db'

#################### myself qiniu #######################
# bucket_name = 'bond'
# access_key = 'AvMYWH2lv0k7AQT1YPxDmXxHwQhp535edzOO4IdJ'
# secret_key = 't8JtkLOXrpDgqGUK9ENwq3P3tET7utI1gSwGf5qd'

##################### company qiniu #######################
bucket_name = 'csf-eos'
access_key = 'QjhFzM91UMoA0BrxuoubEld64Wvb3rXr7yMaop4q'
secret_key = 'RqrUk8S-h-Kne1gWrPO0iVdP1XCeyscqalIvmUsQ'

proxy_ips = [
    '111.184.237.70:8088',
    '221.209.235.74:80',
    '218.252.18.98:8088',
    '120.197.53.197:8080',
    '61.10.232.188:8088',
    '120.198.230.31:80',
    '210.14.138.102:80',
    '120.198.230.93:80',
    '120.198.230.30:80',
    '111.1.36.22:80',
    '111.205.122.222:80',
    '120.198.244.15:80',
    '116.228.55.217:80',
    '211.151.50.179:81',
    '211.138.121.36:80',
    '211.138.121.37:80',
]