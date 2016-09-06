# -*- coding: UTF-8 -*-

import re
import inspect
from datetime import date
from dis import dis
from functools import wraps

# for property
class CardHolder(object):
    acctlen = 8             # Class data
    retireage = 59.5

    def __init__(self, acct, name, age, addr):
        self.acct = acct    # Instance data
        self.name = name    # These trigger prop setters too
        self.age = age      # __X mangled to have class name
        self.addr = addr    # addr is not managed
                            # remain has no data

    def getName(self):
        return self.__name

    def setName(self, value):
        print 'set name enter!'
        value = value.lower().replace(' ', '_')
        self.__name = value
    name = property(getName, setName)

    def getAge(self):
        return self.__age

    def setAge(self, value):
        print 'set age enter!'
        if value < 0 or value > 150:
            raise ValueError('invalid age')
        else:
            self.__age = value
    age = property(getAge, setAge)

    def getAcct(self):
        return self.__acct[:-3] + '***'

    def setAcct(self, value):
        print 'set acct enter!'
        value = value.replace('-', '')
        if len(value) != self.acctlen:
            raise TypeError('invald acct number')
        else:
            self.__acct = value
    acct = property(getAcct, setAcct)

    def remainGet(self):  # Could be a method, not attr
        return self.retireage - self.age # Unless already using as attr
    remain = property(remainGet)
# for property

# for descriptor
class Name(object):
    def __get__(self, instance, owner):  # Class names: CardHolder locals
        return self.name

    def __set__(self, instance, value):
        value = value.lower().replace(' ', '_')
        self.name = value

class Age(object):
    def __get__(self, instance, owner):
        return self.age     # Use descriptor data

    def __set__(self, instance, value):
        if value < 0 or value > 150:
            raise ValueError('invalid age')
        else:
            self.age = value

class Acct(object):
    def __get__(self, instance, owner):
        return self.acct[:-3] + '***'

    def __set__(self, instance, value):
        value = value.replace('-', '')
        if len(value) != instance.acctlen:  # Use instance class data
            raise TypeError('invald acct number')
        else:
            self.acct = value

class Remain(object):
    def __get__(self, instance, owner):
        return instance.retireage - instance.age    # Triggers Age.__get__

    def __set__(self, instance, value):
        raise TypeError('cannot set remain')    # Else set allowed here

class CardHolder2(object):
    acctlen = 1             # Class data
    retireage = 59.5

    def __init__(self, acct, name, age, addr):
        self.acct = acct    # Instance data
        self.name = name    # These trigger __set__ calls too
        self.age = age      # __X not needed: in descriptor
        self.addr = addr    # addr is not managed
                            # remain has no data
    name = Name()
    age = Age()
    acct = Acct()
    remain = Remain()

if __name__ == '__main__':
    print CardHolder2('1', '2', 3, '4').name
