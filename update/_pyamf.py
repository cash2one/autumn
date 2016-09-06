import pyamf

# from pyamf.remoting
# from pyamf.amf3 import

from pyamf import tests
from pyamf.tests.gateway import *
# from pyamf.amf3 import

import requests
from pyamf import remoting
response = requests.get('http://jgsb.agri.gov.cn/flexapps/hqApp.swf').content

# print remoting.decode(response.encode('u8'))
ins = pyamf.decode(response)
# print dir(ins)
# print ins.context
# # print ins.stream, type(ins.stream)
# print dir(ins.stream)
# data = ins.stream.read()
# print type(data)

print [elem[k] for elem in ins for k in elem]


