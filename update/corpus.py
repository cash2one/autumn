# encoding: utf-8
from pymongo import MongoClient

coll = MongoClient('192.168.100.15')['log']['crawler_def']
data1 = {
    'name': '财经新闻',
    'table': 'log:category_stat',
    'freq': '实时抓取',
    'local': '54.223.37.5<mongodb>news:crawler_news',
    'def': '财经类新闻的实时抓取， 主要为京东，智投提供数据',
    'st': None,
    'et': None
}

data2 = {
    'name': '新三板公告',
    'table': 'log:corpus_stat',
    'freq': '实时抓取',
    'local': '122.144.134.95<mongodb>news:announcement_otc',
    'def': '新三板公告抓取， wenping.chen 需求',
    'st': None,
    'et': None
}

data3 = {
    'name': '研报',
    'table': 'log:corpus_stat',
    'freq': '实时抓取',
    'local': '122.144.134.95<mongodb>news:research_report_def',
    'def': '东方财富A股与港股研报抓取， wenping.chen 需求',
    'st': None,
    'et': None
}

data4 = {
    'name': '京东指数',
    'table': 'log:corpus_stat',
    'freq': '每日定时抓取 09:20AM',
    'local': '122.144.134.95<mongodb>ada:index_members_a',
    'def': '位京东提供600多家指数数据， wenping.chen 需求',
    'st': None,
    'et': None
}

data5 = {
    'name': '专利数据',
    'table': 'log:corpus_stat',
    'freq': '实时抓取',
    'local': '192.168.100.20<mongodb>py_crawl:patent',
    'def': '国家专利数据抓取',
    'st': None,
    'et': None
}

data6 = {
    'name': '雪球大V',
    'table': 'log:corpus_stat',
    'freq': '一次抓取',
    'local': '192.168.100.20<mongodb>py_crawl:bigv_cubes',
    'def': '抓取雪球大V与相关股票组合信息， Alex需求',
    'st': None,
    'et': None
}

data7 = {
    'name': '知乎股票评论',
    'table': 'log:corpus_stat',
    'freq': '实时抓取',
    'local': '192.168.100.20<mongodb>py_crawl:zhihu',
    'def': '抓取知乎中对股票的相关股评数据',
    'st': None,
    'et': None
}

data8 = {
    'name': 'ETF基金',
    'table': 'log:corpus_stat',
    'freq': '一次抓取',
    'local': '192.168.100.20<mongodb>py_crawl:etfund',
    'def': 'etf基金费率相关信息抓取， Andy Zhang需求',
    'st': None,
    'et': None
}


data9 = {
    'name': '东方财富股吧股票评论',
    'table': 'log:corpus_stat',
    'freq': '实时抓取',
    'local': '192.168.100.20<mongodb>py_crawl:guba',
    'def': '对东方财股相关股评数据的抓取',
    'st': None,
    'et': None
}

data10 = {
    'name': '知识图谱_问财',
    'table': 'log:corpus_stat',
    'freq': '实时抓取',
    'local': '54.223.37.5<mongodb>graph:nlp_event',
    'def': '为知识图谱提供实时抓取数据',
    'st': None,
    'et': None
}

data11 = {
    'name': '百度新闻',
    'table': 'log:corpus_stat',
    'freq': '实时抓取',
    'local': '192.168.100.20<mongodb>py_crawl:baidu',
    'def': '利用百度搜索引擎对相关股票咨询的抓取',
    'st': None,
    'et': None
}

data12 = {
    'name': '因果树',
    'table': 'log:corpus_stat',
    'freq': '每日定时抓取',
    'local': '192.168.100.20<mongodb>py_crawl:innotree',
    'def': '抓取创投相关信息',
    'st': None,
    'et': None
}

data13 = {
    'name': '大宗交易',
    'table': 'log:corpus_stat',
    'freq': '每日定时抓取',
    'local': '122.144.134.95<mongodb>ada:base_block_trade',
    'def': '抓取深交所、上交所大宗交易相关信息 Wenping.chen需求',
    'st': None,
    'et': None
}

data14 = {
    'name': '融资融券',
    'table': 'log:corpus_stat',
    'freq': '每日定时抓取',
    'local': '122.144.134.95<mongodb>ada:base_block_trade',
    'def': '抓取深交所、上交所融资融券相关信息 Wenping.chen需求',
    'st': None,
    'et': None
}

data15 = {
    'name': '高管增减持',
    'table': 'log:corpus_stat',
    'freq': '每日定时抓取',
    'local': '122.144.134.95<mongodb>ada:base_block_trade',
    'def': '抓取深交所、上交所高管增减持相关信息 Wenping.chen需求',
    'st': None,
    'et': None
}

data16 = {
    'name': '港股中文公告',
    'table': 'log:corpus_stat',
    'freq': '每日定时抓取',
    'local': '122.144.134.95<mongodb>ada:base_block_trade',
    'def': '抓取港交所之港股中文公告相关信息 Wenping.chen需求',
    'st': None,
    'et': None
}

data17 = {
    'name': '港股英文公告',
    'table': 'log:corpus_stat',
    'freq': '每日定时抓取',
    'local': '122.144.134.95<mongodb>ada:base_block_trade',
    'def': '抓取港交所之港股英文公告相关信息 Wenping.chen需求',
    'st': None,
    'et': None
}

data18 = {
    'name': '美股公告',
    'table': 'log:corpus_stat',
    'freq': '每日定时抓取',
    'local': '122.144.134.95<mongodb>ada:base_block_trade',
    'def': '抓取美股英文公告相关信息,与Wan.jun之前的抓取合并',
    'st': None,
    'et': None
}

data = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14,
        data15, data16, data17, data18]

for item in data:
    coll.insert(item)

