from eggs.utils.xlsx import XlsxReader
import xlrd


def read_from_excel():
    path = 'D:/temp/pdf_html/dest/000687_p21.xlsx'

    open_book = xlrd.open_workbook(path)
    table = open_book.sheet_by_name('Table 17')
    print table.nrows, table.name, table.ncols, table.number

    for row in range(table.nrows):
        tt = []
        for it in table.row_values(row):
            if isinstance(it, (int, float)):
                tt.append(str(it))
            else:
                tt.append(it.replace('\n', ''))
        print row, '|'.join(tt)


if __name__ == '__main__':
    read_from_excel()




