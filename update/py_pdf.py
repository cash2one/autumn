#encoding=utf-8
import pyPdf


def getPDFContent(path, page):
    content = ""
    # 读入文件
    pdf = pyPdf.PdfFileReader(file(path, "rb"))
    # 循环所有页
    for i in range(1, pdf.getNumPages() + 1):
        if i == page:
            # 提取文本
            print pdf.getPage(19).getContents()
            content += pdf.getPage(i).extractText() + "\n"
    # 处理空格
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    print i
    return content

path = 'D:/temp/pdf_html/data/a.pdf'
print getPDFContent(path, 19).encode("ascii", "ignore")


