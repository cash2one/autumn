# -*- coding: UTF-8 -*-

import os
import itertools
import os.path
import hashlib
from random import sample
from string import letters, digits
from multiprocessing.dummy import Lock
from eggs.utils.xlsx import XlsxWriter

lock = Lock()


def md5(md5_str):
    if not isinstance(md5_str, basestring):
        raise ValueError('md5 must string!')
    m = hashlib.md5()
    try:
        m.update(md5_str)
    except UnicodeEncodeError:
        m.update(md5_str.encode('u8'))
    return m.hexdigest()


def get_precision(a, b, prec=2):
        a, b = float(a), float(b)
        integer, decimal_part = str(a / b).split('.')
        decimal_zero = list(itertools.takewhile(lambda _s: not bool(int(_s)), decimal_part))
        print integer, '|', decimal_part, '|', decimal_zero

        decimal_part += '0' * 10
        pos_number = int(decimal_part[prec])
        integer_from_decimal = int(decimal_part[len(decimal_zero):prec])
        if pos_number >= 5:
            prec_pos_integer = integer_from_decimal + 1
            if prec_pos_integer > 9:
                supplement = ''.join(decimal_zero[: -1]) + str(prec_pos_integer)
            else:
                supplement = ''.join(decimal_zero) + str(prec_pos_integer)
        else:
            supplement = ''.join(decimal_zero) + str(integer_from_decimal)
        return '.'.join([integer, supplement])


def write(dir_path, filename, lines, repl='\n'):
    """
    :param dir_path: string, data store path
    :param filename: string, file name
    :param lines: list or tuple, content of data
    :param repl: string, how to join with param `lines`
    """
    is_exist_path(dir_path)
    base_path = [dir_path, filename, '_']
    filename_path = ''.join(base_path + sample(letters, 8) + sample(digits, 6) + ['.txt'])

    with lock:
        with open(filename_path, 'a') as fp:
            if isinstance(lines, (tuple, list)):
                lines_seq = repl.join(lines).encode('u8')
            else:
                lines_seq = lines

            try:
                fp.writelines(lines_seq)
            except Exception as e:
                print('Write Error:[{0}], in file "{1}"'.format(e.message, __file__))


def is_exist_path(file_or_dir_path):
    if os.path.basename(file_or_dir_path):
        file_path = os.path.dirname(file_or_dir_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    else:
        if not os.path.exists(file_or_dir_path):
            os.makedirs(file_or_dir_path)


def read(file_path):
    """ open web or re search fail, you need to open and re search """
    file_name, path = (file_path.split('\\')[-1] + '.txt', file_path[:file_path.rfind('\\') + 1])
    os.chdir(path)
    with open(file_name, 'r') as fd:
        it = iter(list(set(fd.readlines())))
    return it


def to_excel(backup_path, excel_path, headers):
    """
        backup_path: source file include '.txt' data file
        excel_path: generate xls file path and file name.
        headers: one or more sheets have the same title, it is list tuple or iterable, but string.
    """
    excel_name, path = backup_path.split('\\')[-1] + '.xls', backup_path[:backup_path.rfind('\\') + 1]
    if not os.path.exists(excel_path):
        os.makedirs(excel_path)

    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)

    list_dirs = [file_name for file_name in os.listdir(path) if file_name.endswith(r'.txt')]
    for file_name in list_dirs:
        print file_name
        workbook = XlsxWriter(excel_path + file_name.replace('.txt', '.xls'), file_name, headers)
        with open(file_name) as fd:
            for j, line in enumerate(fd):
                data = [item.strip() for item in line.strip().split('$*$*$') if item.strip()]
                workbook.write(data)
        workbook.save()


if __name__ == '__main__':
    url = 'http://fund.eastmoney.com/news/1591,20160516624237583.html'
    print md5(url)

