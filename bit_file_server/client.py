#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmlrpclib


def client(file_name, ip_port=None):
    if ip_port is None:
        ip_port = 'http://localhost:8000/'

    proxy = xmlrpclib.ServerProxy(ip_port)
    reader = proxy.file_reader(file_name)
    return reader


if __name__ == '__main__':
    ret = client(r"d:/temp/temp.txt")
    print ret
