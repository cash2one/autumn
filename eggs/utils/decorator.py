# -*- coding: utf-8 -*-

import os


def decorator_tools(param):
    """
        decorator with argument, eg:
            @log_tools('aaa')
            def func(...): pass => func = log_tools('aaa')(func)
    """
    def decorator_argument(method):
        def wrapper(*args, **kwargs):
            path = os.path.dirname(__file__) + os.sep + param + '.log'
            with open(path, 'a') as fd:
                pass
            return method(*args, **kwargs)
        return wrapper
    return decorator_argument

