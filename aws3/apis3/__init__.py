from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from ..passage.ttypes import Strategy, Storage

from ..passage.PassageService import Client


class AwsCloud(object):
    """ This interface is only suitable for chinascope company """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
        self.transport = None

        self.__connect()

    def __connect(self):
        socket = TSocket.TSocket(self.host, self.port)
        self.transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Client(protocol)
        self.transport.open()

    def close(self):
        self.transport.close()

    def put(self):
        pass

    def get(self):
        pass



