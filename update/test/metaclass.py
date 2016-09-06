#!/usr/bin/env python
# -*- coding: utf-8 -*-


def upper_attr(future_class_name, future_class_parents, future_class_attr):
    print 'foo4:', future_class_name, future_class_parents, future_class_attr
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    return type(future_class_name, future_class_parents, uppercase_attr)


class UpperAttrMetaClass(type):
    # __new__ 是在__init__之前被调用的特殊方法
    # __new__是用来创建对象并返回之的方法
    # 而__init__只是用来将传入的参数初始化给对象
    # 你很少用到__new__，除非你希望能够控制对象的创建
    # 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写__new__
    # 如果你希望的话，你也可以在__init__中做些事情
    # 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
    def __new__(mcs, future_class_name, future_class_parents, future_class_attr):
        print mcs.__name__, mcs
        print future_class_name, future_class_parents, future_class_attr
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return super(UpperAttrMetaClass, mcs).__new__(mcs, future_class_name, future_class_parents, uppercase_attr)


class SuperMeta(type):
    def __call__(meta, classname, supers, classdict):
        print('In SuperMeta.call: ', meta, classname, supers, classdict)
        return type.__call__(meta, classname, supers, classdict)


class SubMeta(type):
    # __metaclass__ = SuperMeta

    def __new__(meta, classname, supers, classdict):
        print('In SubMeta.new: ', meta, classname, supers, classdict)
        return type.__new__(meta, classname, supers, classdict)

    def __init__(Class, classname, supers, classdict):
        print('In SubMeta init:', Class, classname, supers, classdict)
        print('...init class object:', list(Class.__dict__.keys()))

if __name__ == '__main__':
    print '$' * 100

    class Meat(type):
        def __new__(mcs, class_name, bases, namespace):
            print 'In Meta:', mcs, class_name, bases, namespace
            super_new = super(Meat, mcs).__new__
            new_class = super_new(mcs, class_name, bases, namespace)
            p = [b for b in bases if isinstance(b, Meat)]
            print 'p:', p
            print 'new_class:', new_class, ' to->', new_class.__name__, id(new_class)
            return new_class

        def abc(self):
            print 'abc'

    print '1' * 100

    class FKV(Meat):
        __metaclass__ = Meat

        def foo(self):
            print 'in foo!'

    print '2' * 100

    class Mtk(FKV):
        meta = []

        class ccs:
            pass

    print '3' * 100

    # class SubMtk(Mtk):
    #     def smtk(self):
    #         pass

    # print 'FKV:', FKV, id(FKV)
    print 'Mtk:', Mtk, id(Mtk)
    # print 'SubMtk:', SubMtk, id(SubMtk)
