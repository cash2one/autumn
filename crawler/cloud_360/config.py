#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymongo


SEGMENT_NUM = 8000

account = 'shukuyun@163.com'
password = 'shukuYUN!'
db_name = 'shukuyun'
table_name_source = 'ee_comp_info'
table_name_insert = 'ee_comp_data'
table_gather_copy = 'ee_comp_gather_copy'

cookie_file = os.path.dirname(__file__) + os.sep + 'login_cookies.dat'
log_normal = os.path.dirname(__file__) + os.sep + 'normal.txt'
log_weibo = os.path.dirname(__file__) + os.sep + 'weibo.txt'
log_alexa = os.path.dirname(__file__) + os.sep + 'alexa.txt'
log_patent = os.path.dirname(__file__) + os.sep + 'patent.txt'

db = pymongo.MongoClient('192.168.250.200', 27017)