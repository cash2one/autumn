# -*- coding: utf-8 -*-

import bsddb
import os
import os.path


class PyBsddb(object):
    """
    Bsddb objects behave generally like dictionaries. Keys and values must be strings.
    Note: 网上使用这种方法， 但是这个类产生有像.001、.002等非数据库文件，并且在存储速度上有点慢。
    """
    def __init__(self, bsddb_path, mod):
        self.__path = os.path.dirname(bsddb_path)
        self.__db_name = os.path.basename(bsddb_path)
        self.__dic = {'b': bsddb.db.DB_BTREE, 'h': bsddb.db.DB_HASH, 'q': bsddb.db.DB_QUEUE, 'r': bsddb.db.DB_RECNO}
        self.__mod = self.__dic[mod]
        self.__dbenv = None
        self.__db = None

    def __open(self):
        self.close()
        self.__dbenv = bsddb.db.DBEnv()
        self.__dbenv.open(self.__path, bsddb.db.DB_CREATE | bsddb.db.DB_INIT_MPOOL)
        self.__db = bsddb.db.DB(self.__dbenv)
        self.__db.open(self.__db_name, self.__mod, bsddb.db.DB_CREATE, 0666)

    def put(self, key, value=''):
        self.close()
        self.__open()
        try:
            self.__db.put(key, value)
        except Exception as e:
            print 'put error:', e

    def get(self, key):
        self.close()
        self.__open()
        try:
            value = self.__db.get(key)
            return value
        except Exception as e:
            print 'get error:', e

    def has_key(self, key):
        self.close()
        self.__open()
        try:
            if key in self.__db:
                return 1
        except Exception as e:
            print 'has_key error:', e
        return 0

    def remove(self, key):
        self.close()
        self.__open()
        try:
            self.__db.remove(key)
        except Exception as e:
            print 'remove error:', e

    def close(self):
        if self.__dbenv is not None:
            try:
                self.__dbenv.close()
            except Exception as e:
                print 'close() error `__dbenv`:', e

        if self.__db is not None:
            try:
                self.__db.close()
            except Exception as e:
                print 'close() error `__db`:', e


class FileBsd(object):
    """
        key: Integer keys only allowed for Recno and Queue DB's, string is allowed.
        value: Data values must be of type string or None
    """
    def __init__(self, option, filename, flag='c', mode=0666):
        self.__db = None
        self.__option = option
        self.__filename = filename
        self.__flag = flag
        self.__mode = mode

    def __connect(self):
        if self.__db is not None:
            self.close()

        if self.__option == 'bt':
            self.__db = bsddb.btopen(self.__filename, self.__flag, self.__mode)
        if self.__option == 'hash':
            self.__db = bsddb.hashopen(self.__filename, self.__flag, self.__mode)

    def put(self, key, value=''):
        if self.__db is None:
            self.__connect()
        try:
            self.__db[key] = value
        except Exception as e:
            print 'FileBsd put error:', e

    def get(self, key):
        if self.__db is None:
            self.__connect()
        try:
            return self.__db[key]
        except KeyError:
            pass

    def has_key(self, key):
        if self.__db is None:
            self.__connect()
        if key in self.__db:
            return 1
        return 0

    def remove(self, key):
        if self.__db is None:
            self.__connect()
        try:
            self.__db.pop(key, default=None)
        except KeyError:
            pass

    def close(self):
        try:
            if self.__db is not None:
                self.__db.close()
                self.__db = None
        except Exception as e:
            print 'FileBsd close error:', e


if __name__ == '__main__':
    from eggs.utils.tools import md5
    import time
    from random import sample
    from string import letters, digits
    path = r'D:/temp/' + 'test3.db'
    start = time.time()
    db = FileBsd('hash', path)
    # for i in xrange(1000):
    #     tit = md5(''.join(sample(letters, 5) + sample(digits, 4) + sample(letters, 6)))
    #     db.put(tit)
    #     print tit
    print db.has_key('abf27b8164ff08a48e98665cdb2d2aad')
    print time.time() - start
    db.close()