# -*- coding: UTF-8 -*-

import os
import os.path
import sqlite3


class Sqlite3(object):
    def __init__(self, db_path=None):
        self.__db_path = db_path
        self.__conn = None

    def connect(self):
        if self.__conn is not None:
            try:
                self.__conn.close()
                self.__conn = None
            except Exception, e:
                print 'sqlite db connect() error:', e
        if self.__db_path is not None:
            db_name, path = self.__db_path.split('\\')[-1] + '.db', self.__db_path[:self.__db_path.rfind('\\') + 1]
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        self.__conn = sqlite3.connect(db_name)

    def disconnect(self):
        try:
            self.__conn.close()
            self.__conn = None
        except Exception, e:
            print 'self__conn close() exception:', e

    def get(self, sql, *args):
        """
            return a dict from matching one line
        """
        if self.__conn is None:
            self.connect()
        params = tuple(args[0]) if args and isinstance(args[0], (tuple, list)) else args
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql, params)
            data = cursor.fetchone()
            return data
        except Exception, e:
            print 'execute sql statement error:', e
            self.disconnect()

    def query(self, sql, *args):
        """
            return a list include dicts from matching all lines.
        """
        if self.__conn is None:
            self.connect()
        params = tuple(args[0]) if args and isinstance(args[0], (tuple, list)) else args
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql, params)
            data = cursor.fetchall()
            return data
        except Exception, e:
            print 'execute sql statement error:', e
            self.disconnect()

    def execute(self, sql, *args):
        """
            fit create , insert, update_, delete sql statement. here one item to execute to insert,
            if massive data, should pay attention to the storage speed, could use 'executemany()'
        """
        if self.__conn is None:
            self.connect()
        params = tuple(args[0]) if args and isinstance(args[0], (tuple, list)) else args
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql, params)
            self.__conn.commit()
        except Exception, e:
            print 'execute sql statement error:', e
            self.disconnect()

    def executemany(self, sql, values):
        """
            fit create , insert, update_, delete sql statement. here massive data to more operation,
            use 'Transaction' to speed up the storage speed
            eg: values is list include tuple,[(...), (...), ...]
        """
        if self.__conn is None:
            self.connect()
        try:
            cursor = self.__conn.cursor()
            cursor.executemany(sql, values)
            self.__conn.commit()
        except Exception, e:
            print 'executemany sql statement error:', e
            self.disconnect()

    def info(self):
        pass


if __name__ == '__main__':
    sq = Sqlite3('D:\sqlite\db\mydb')
    # sq.execute('create table catalog ( id integer primary key, pid integer, name varchar(10) UNIQUE )')
    # sq.execute("insert into catalog values(?, ?, ?)", str(3), str(1), 'name' + str(3))
    # data = sq.execute('select *from catalog where id=10')
    # print data


    # start = time()
    # values = []
    # for i in range(0, 10000):
    #     values.append((str(i), str(i), 'name' + str(i)))
    # sq.executemany("insert into catalog values(?, ?, ?)", values)
    #     print '%.8f%%' % (i / 5000.0 * 100)
    # print time() - start
    # data = sq.query('select * from catalog')
    # sq.execute('delete  from catalog')
    # print len(data), data
    # db.execute("""create table if not exists ?(
    #                         id int(4) primary key,
    #                         name varchar(512),
    #                         pub_no varchar(128) primary key,
    #                         pub_date varchar(16),
    #                         apply_no varchar(25),
    #                         apply_date varchar(16),
    #                         apply_date varchar(16),
    #                         inventor varchar(512),
    #                         address varchar(512),
    #                         category_no varchar(256),
    #                         agency varchar(512),
    #                         agent_person varchar(512),
    #                         abstract text
    #                     )""", select[0])