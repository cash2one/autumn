#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import time
import traceback
from functools import wraps


def cached(timeout, logged=False):
    """Decorator to cache the result of a function call.
        Cache expires after timeout seconds.
    """
    def decorator(func):
        if logged:
            print "-- Initializing cache for", func.__name__
        cache = {}

        @wraps(func)
        def decorated_function(*args, **kwargs):
            if logged:
                print "-- Called function", func.__name__
            key = (args, frozenset(kwargs.items()))
            result = None
            if key in cache:
                if logged:
                    print "-- Cache hit for", func.__name__, key

                (cache_hit, expiry) = cache[key]
                if time.time() - expiry < timeout:
                    result = cache_hit
                elif logged:
                    print "-- Cache expired for", func.__name__, key
            elif logged:
                print "-- Cache miss for", func.__name__, key

            # No cache hit, or expired
            if result is None:
                result = func(*args, **kwargs)

            cache[key] = (result, time.time())
            return result

        return decorated_function

    return decorator


# @cached(10, True)
def fib(n):
    """Returns the n'th Fibonacci number."""
    if n == 0 or n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


# ##################### metaclass #############################
def log_everything_metaclass(class_name, parents, attributes):
    print "Creating class", class_name, parents, attributes
    myattributes = {}
    for name, attr in attributes.items():
        myattributes[name] = attr
        if hasattr(attr, '__call__'):
            myattributes[name] = attr
    return type(class_name, parents, myattributes)


frametype_class_dict = {}


class ID3v2FrameClass(object):
    def __init__(self, frame_id):
        self.frame_id = frame_id

    def __call__(self, cls):
        print "Decorating class", cls.__name__
        # Here we could add some helper methods or attributes to c
        if self.frame_id:
            frametype_class_dict[self.frame_id] = cls
        return cls

    # def __call__(self, *args, **kwargs):
    #     pass

    @staticmethod
    def get_class_from_frame_identifier(frame_identifier):
        return frametype_class_dict.get(frame_identifier)


# @ID3v2FrameClass(None)
class ID3v2Frame(object):
    pass


# @ID3v2FrameClass("TIT2")
class ID3v2TitleFrame(ID3v2Frame):
    pass


# @ID3v2FrameClass("COMM")
class ID3v2CommentFrame(ID3v2Frame):
    pass


class PyWith(object):
    def __init__(self):
        self._data = range(20)

    def __enter__(self):
        return self._data

    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'typ:', exc_type
        print 'val:', exc_val
        print 'tb:', exc_tb, traceback.print_tb(exc_tb)


if __name__ == '__main__':
    print '----start-----'
    with PyWith() as pw:
        print pw
        print pw[20]
    print '------end------'
