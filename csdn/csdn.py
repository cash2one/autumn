# -*- coding: utf-8 -*-

import os
import os.path
from datetime import date
from time import time, strftime, sleep
from eggs.utils.up_server import UpServerWin


def csdn_server(path, us, cur_dir):
    local_path, remote_path = r'D:\csf_news\%s\%s', r'/home/daily_news/csf_news/%s/%s'
    for toot, dirs, files in os.walk(path):
        for k, file_name in enumerate(files):
            try:
                us.upload_server(local_path % (cur_dir, file_name), remote_path % (cur_dir, file_name))
                print 'upload file: %s ok' % file_name, k + 1
            except Exception as ex:
                print 'file %s upload err:[' % file_name, ex, ']continue'
                continue


if __name__ == '__main__':
    count = 0
    while 1:
        if strftime('%H%M') in ['']:
            cur_date, start = str(date.today()).replace('-', ''), time()
            server = UpServerWin('192.168.0.233', 'root', 'chinascope!@#', 22)
            server.exec_command('mkdir /home/daily_news/csf_news/' + cur_date)
            try:
                csdn_server(r'D:\csf_news\%s' % cur_date, server, cur_date)
            except Exception as e:
                server = UpServerWin('192.168.0.233', 'root', 'chinascope!@#', 22)
                print 'upload 233 server err:', e
            finally:
                server.disconnect()
            print (time() - start) / 3600
        else:
            count += 1
            sleep(10.0)
            print strftime('%Y-%m-%d %H:%M:%S %A')
        if count % 9 == 0:
            count = 0