# -*- coding: utf-8 -*-

import re
from pymongo import Connection

# amazon_conn = Connection('10.0.250.10', 27017)
# coll_hotnews = amazon_conn.news.hotnews_analyse
# coll_subnews = amazon_conn.news.subnews_analyse
# crawler = amazon_conn.news.crawler_news


def update_news_table():

    for _index, _docs in enumerate(crawler.find()):
        d = _docs['d']
        _id = _docs['_id']

        title = _docs['title']
        date = _docs['dt']
        author = _docs['auth']
        source = _docs['cat']
        url = _docs['url']
        ratio = _docs['ratio']
        crt = _docs['crt']
        content = _docs['text']

        news_docs = {'d': d, 'title': title, 'crt': crt, 'date': date, 'author': author, 'source': source,
                     'url': url, 'ratio': ratio, 'content': content}

        crawler.remove({'_id': _id})
        if d[:4] <= '2016':
            print crawler.insert(news_docs)
        break


if __name__ == '__main__':
    update_news_table()
    # update_news_table(coll_subnews)

