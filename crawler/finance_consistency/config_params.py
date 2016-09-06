# -*- coding: UTF-8 -*-

from pymongo import MongoClient

HOST = '192.168.250.200'
PORT = 27017
NAME = 'fin'
TABLE_TPL_LTM = 'fin_rpt_tpl_ltm'
TABLE_TPL_YTD = 'fin_rpt_tpl_ytd'
TABLE_ASREP_LTM = 'fin_rpt_asrep_ext_ltm'
TABLE_ASREP_YTD = 'fin_rpt_asrep_ext_ytd'

CONN = MongoClient(HOST, PORT)
DATABASE = CONN[NAME]

coll_tpl_ltm = DATABASE[TABLE_TPL_LTM]
coll_tpl_ytd = DATABASE[TABLE_TPL_YTD]
coll_asrep_ltm = DATABASE[TABLE_ASREP_LTM]
coll_asrep_ytd = DATABASE[TABLE_ASREP_YTD]

