#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class SmtpSender(object):
    """
    The class just `smtp` protocol, login user, then send mail to receives.
    `MIMEImage`: Show mail body image, not attach.this use `MIMEMultipart`
    `MIMEText`: Use in mail body character or mail attach. also use `MIMEMultipart`
    """

    def __init__(self, _user, _pwd, _receivers, _host='localhost', _port=25, timeout=60.0, subtype='mixed'):
        self.__user_name = _user
        self.__password = _pwd
        self.__port = _port
        self.__smtp_server = None
        self.__timeout = timeout
        self.__msg = MIMEMultipart(subtype)
        self.__host = _host if _host != 'localhost' else 'smtp.' + _user[_user.find('@') + 1:]
        self.__receivers = _receivers if not isinstance(_receivers, list) else ', '.join(_receivers)

    def add_head(self, subject):
        self.__msg['To'] = Header(self.__receivers, 'utf-8')  # "self.__msg['To'] = self.__receivers" is ok
        self.__msg['From'] = Header(self.__user_name, 'utf-8')
        self.__msg['Subject'] = Header('Subject: ' + subject, 'utf-8')

    def add_attach(self, body, files):
        _files = [] if files is None else files
        files_list = [_files] if _files and isinstance(_files, basestring) else _files

        # 构造附件
        for filename in files_list:  # could fit multi files.
            with open(filename, 'rb') as fd:
                att = MIMEText(fd.read(), 'base64', 'utf-8')
                att["Content-Type"] = "application/octet-stream"
                att["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(filename)
                self.__msg.attach(att)
        content = MIMEText(body, 'plain', 'utf-8')  # show mail text
        self.__msg.attach(content)

    def send_mail(self, subject='attach file', body='', files=None,
                  mail_options=None, rcpt_options=None):
        mail_options = [] if mail_options is None else mail_options
        rcpt_options = [] if rcpt_options is None else rcpt_options

        try:
            self.__smtp_server = smtplib.SMTP(timeout=self.__timeout)
            self.__smtp_server.connect(self.__host, self.__port)
            self.__smtp_server.login(self.__user_name, self.__password)
            self.add_head(subject)
            self.add_attach(body, files)
            self.__smtp_server.sendmail(self.__user_name, self.__receivers, self.__msg.as_string(),
                                        mail_options, rcpt_options)
        except smtplib.SMTPException as e:
            print "Error: unable to send email", e
        else:
            print "Successfully sent email"
        finally:
            if self.__smtp_server is not None:
                self.__smtp_server.quit()
                self.__smtp_server = None


if __name__ == '__main__':
    # '脚本之家'上有一些实例，可做参考
    user, password = 'xutaoding@163.com', '5869654tao'
    receivers = 'xutao.ding@chinascopefinancial.com'  # ['xutaoding@aliyun.com', 'xutaoding_lm@sina.cn']
    mail_body = '您将会收到四个附件：图片，文本，excel和压缩包。'
    attach_files = ['d:/temp/31887.jpg', 'd:/temp/1416461873.32.txt', 'd:/temp/Expense Statement.xls',
                    'd:/temp/XlsxWriter.tar.gz']

    smtp = SmtpSender(user, password, receivers)
    smtp.send_mail('attach soup python', mail_body, attach_files)
    pass



