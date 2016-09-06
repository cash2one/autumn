# -*- coding: UTF-8 -*-

import gridfs
import StringIO
from PIL import Image


class GFS(object):
    def __init__(self, db=None, collection=None):
        if db is None or collection is None:
            raise ValueError('db and collection is None, valid value.')

        self.__gfs = gridfs.GridFS(db, collection)

    def put(self, img_name, fmt=None):
        gf, image, fmts = None, None, ['png', 'jpeg', 'jpg', 'gif', 'bmp']

        if img_name.rfind('.') == -1:
            raise NameError('img_name: %s have not extension' % img_name)

        fmt = img_name[img_name.rfind('.') + 1:].lower() if fmt is None else fmt
        try:
            sio = StringIO.StringIO()
            image = Image.open(img_name)
            fmt = 'jpeg' if fmt == 'jpg' else fmt
            try:
                image.save(sio, fmt)
            except IOError:
                image.convert('RGB').save(sio, fmt)
            gf = self.__gfs.put(sio.getvalue(), filename=img_name, format=fmt)
        except Exception as e:
            print 'write image error:', e
        return gf

    def get(self):
        pass
