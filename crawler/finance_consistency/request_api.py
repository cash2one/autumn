# -*- coding: UTF-8 -*-

import os
import time
import simplejson
import datetime
import requests
from multiprocessing.dummy import Lock

lock = Lock()
path = os.path.dirname(__file__) + '/log/'


def save_file(file_name, message):
    with lock:
        with open(''.join((path, file_name)), 'a') as fd:
            fd.write(message + '\n')


def request_interface(typ_query_string):
    url = 'http://192.168.250.206:17010/dataentry/fin/fin?' \
          'secu={1}&y={2}&ctyp={6}&rpt={0}&range=all&fp={3}&q={4}'

    typ, (query_string, ids) = typ_query_string
    today = ''.join(str(datetime.date.today()).split('-'))
    message = '{1}, [_id: {0}] '.format(ids, time.strftime('%Y-%m-%d %H:%M:%S %A'))
    filename = '_'.join((typ, 'log', today + '.txt'))

    if query_string.split('#')[3] == 'None':
        save_file(filename, '{0} info: fp is None'.format(message))
        print('\t[id:{0}]: fp is None.'.format(ids))
        return None

    for k in range(3):
        try:
            url_res = url.format(*query_string.split('#'))
            print url_res
            data = requests.get(url_res, timeout=30).content
            if simplejson.loads(data).get('code', None) == '200':
                print('\t[{1}->id:{0}]: request to 192.168.250.206 is ok'.format(ids, typ))
                return ids
        except Exception as e:
            message += e.message
        if k == 2:
            save_file(filename, 'info: {0}'.format(message))
            print('\t[id:{0}]: 3 times request fail.'.format(ids))
