# -*- coding: UTF-8 -*-

import re
import download
from pyquery import PyQuery

query_start_date = '2010.01.01'
query_end_date = '2015.06.30'

# there you need alert query date, selected, one of num* and pageNow
form_data = {
    'showType': '1',
    'strWord': "公开（公告）日=BETWEEN['{0}','{1}'] and 地址='上海市'".format(query_start_date, query_end_date),
    'numSortMethod': '',
    'strLicenseCode': '',
    'selected': '',
    'numFMGB': '',
    'numFMSQ': '',
    'numSYXX': '',
    'numWGSQ': '',
    'pageSize': '3',
    'pageNow': '1'
}


def get_form_data(typ=None):
    assert typ is not None, u'Must select one type of `fmgb`, `fmsq`, `syxx`, `wgsq`'

    form_data['num' + typ.upper()] = '0'
    num_typ = lambda t: re.compile(r'ksjs\.num{0}\.value.*?(\d+).*?;'.format(typ.upper()), re.S).findall(t)
    selected = lambda v: re.compile(r'ksjs\.selected\.value.*?([a-z]+).*?;', re.S).findall(v)

    html = download.RequestHtml().get_html('http://epub.sipo.gov.cn/patentoutline.action', form_data)
    form_data['num' + typ.upper()], form_data['numSortMethod'] = num_typ(html)[0], '0'
    form_data.update(selected=selected(html)[0], pageSize='10')
    return form_data
