# -*- coding: utf-8 -*-

import re
import xlsxwriter
from pymongo import MongoClient
from eggs.utils.xlsx_writer import XlsxWriter

path = 'D:/temp/data/'
conn_new = MongoClient('192.168.250.208', 27017)
conn_rr = MongoClient('192.168.250.200', 27017)
conn_stock = MongoClient('192.168.250.200', 27017)


coll_new = conn_new.news.research_report_new
coll_rr = conn_rr.ada.rr_researcher
coll_stock = conn_stock.ada.base_stock


def save_excel(excel_name, headers, book_values):
    workbook = xlsxwriter.Workbook(path + excel_name)
    worksheet = workbook.add_worksheet('data')
    print 'book_values:', len(book_values)

    for k, values in enumerate([headers] + book_values):
        for i, item in enumerate(values):
            worksheet.write(k, i, item)
    workbook.close()


def check_requirement_11():
    """ research_report_new中aut不为空在rr_researcher中code不存在 """
    new_set = []
    rr_set = []
    book_values = []

    new_fields = {'aut': 1, 'src': 1, 'titl': 1}
    for k, dct in enumerate(coll_new.find({}, new_fields).sort([('_id', 1)])):
        item = dct.get('aut') and dct['aut'][0]
        if not item:
            continue
        new_set.append(dct)

    rr_fields = {'code': 1}
    for i, dct_to in enumerate(coll_rr.find({}, rr_fields).sort([('_id', 1)])):
        temp = dct_to.get('code')
        if not temp:
            continue
        rr_set.append(temp)

    count = len(new_set)
    print 'new_set count', count
    print 'rr_set count', len(rr_set)

    for j, each_dct in enumerate(new_set):
        ids = str(each_dct['_id'])
        aut = each_dct['aut'][0]
        print 'percent: [{1:.4f}%]'.format(ids, (j + 1) * 1.0 / count * 100)
        if aut not in rr_set:
            book_values.append([ids, aut, each_dct['src'], each_dct['titl']['szh']])

    save_excel('11.xlsx', ['_id', 'aut', 'src', 'titl'], book_values)


def check_requirement_10_and_09():
    """
    10:rr_researcher中name.szh，name.en存在数字，或name.szh左边或右边空格
    09:rr_researcher中name.en为空or不存在
    """
    rr_empty_list = []
    rr_space_digit_list = []
    is_digit = lambda s: re.compile(r'\d+').search(s)

    for data in coll_rr.find({}, {'name': 1, 'code': 1}):
        name = data.get('name', {})
        name_szh = name.get('szh')
        name_en = name.get('en')
        ids = str(data['_id'])

        if not name or not name.get('en'):
            rr_empty_list.append([ids, name_en, name_szh, data.get('code')])

        name_szh_en = name_szh + name_en
        if name_szh.startswith(' ') or name_szh.endswith(' ') or is_digit(name_szh_en):
            rr_space_digit_list.append([ids, name_en, name_szh, data.get('code')])

    save_excel('10.xlsx', ['_id', 'name.en', 'name.szh', 'code'], rr_space_digit_list)
    save_excel('09.xlsx', ['_id', 'name.en', 'name.szh', 'code'], rr_empty_list)


def check_requirement_08():
    """ research_report_new中secu在base_stock中code不存在,secu为空或不存在 """
    stock_code_list = []
    new_list = []
    book_values = []

    for item in coll_new.find({}, {'secu': 1}):
        new_list.append(item)

    for data in coll_stock.find({}, {'code': 1}):
        stock_code_list.append(data['code'])

    for each_dict in new_list:
        ids = str(each_dict['_id'])
        secu = each_dict.get('secu')
        print 'id:', ids
        if not secu or secu not in stock_code_list:
            book_values.append([ids, secu])

    save_excel('08.xlsx', ['_id', 'secu'], book_values)


def check_requirement_07():
    """ research_report_new：rdt,vn为空或不存在,rdt与vn中日期不一致，secu非_HK_EQ结尾 """
    book_values = []
    get_date = lambda d: re.compile(r'\d{4}-\d\d-\d\d').search(d)

    for data in coll_new.find({}, {'titl': 1, 'rdt': 1, 'vn': 1, 'secu': 1}):
        rdt = data.get('rdt')
        vn = data.get('vn', '')
        s_vn_date = get_date(vn)
        vn_date = '' if s_vn_date is None else s_vn_date.group()

        if not data['secu'].endswith('_HK_EQ') and (not rdt or not vn or vn_date != rdt):
            print 'vn_date:', vn_date, data['_id'], rdt
            book_values.append([str(data['_id']), data['titl']['szh'], data['secu'], rdt, vn])

    save_excel('07.xlsx', ['_id', 'titl.szh', 'rdt', 'vn'], book_values)


def check_requirement_06():
    """
    research_report_new：csfr为空或不存在，vn为空或不存在,vn含有“买入or增持or中性or减持or卖出”该字段，
    secu非_HK_EQ结尾
    """
    book_values = []
    for data in coll_new.find({}, {'titl': 1, 'rdt': 1, 'vn': 1, 'secu': 1, 'csfr': 1}):
        csfr = data.get('csfr')
        secu = data.get('secu')
        vn = data.get('vn')

        flag = csfr is None and (u'买入' in vn or u'增持' in vn or u'中性' or u'减持' in vn or u'卖出' in vn)
        if not secu.endswith('_HK_EQ') and (not vn or flag):
            print str(data['_id']), secu, csfr
            book_values.append([str(data['_id']), csfr, data['titl']['szh'], data['secu'], data['rdt'], vn])

    save_excel('06.xlsx', ['_id', 'csfr', 'titl.szh', 'secu', 'rdt', 'vn'], book_values)

if __name__ == '__main__':
    check_requirement_06()
