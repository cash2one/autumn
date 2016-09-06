# -*- coding: UTF-8 -*-

import chardet
import requests


class RequestHtml(object):
    """ class get html source by url"""

    def get_html(self, url, data=None):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0', }
        for _ in range(0, 6):
            try:
                if data is None:
                    r = requests.get(url, params={}, timeout=30.0, headers=headers)
                else:
                    r = requests.post(url, data=data, timeout=30.0, headers=headers)
                # return self.to_utf8(r.content)
                return r.content
            except Exception as e:
                pass
        return 'None'

    def to_utf8(self, string):
        """ To different text types of transcoding centrally """
        charset = chardet.detect(string)['encoding']
        if charset is None:
            return string
        if charset != 'utf-8' and charset == 'GB2312':
            charset = 'gb18030'
        try:
            return string.decode(charset).encode('utf-8')
        except Exception, e:
            print 'chardet error:', e
        return ''
