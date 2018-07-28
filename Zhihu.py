#!/usr/bin/env python3

from urllib import request
from bs4 import BeautifulSoup
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


class ZhiHu:
    def __init__(self):
        self.url = 'http://daily.zhihu.com'

    def daily(self):
        page = request.urlopen(self.url)
        soup = BeautifulSoup(page, 'html.parser')
        ret = soup.findAll(attrs={'class': ['box']})
        head = '''<html><head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"><body>'''
        end = '''</body></head></html>'''
        for item in ret:
            if item.a:
                body = '''<h3><a href='%s'>%s</a></h3><br> ''' % (self.url + item.a.get('href'), item.text)
                head += body
        head += end
        send_email(head, 'Zhihu Daily ')


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(str, subj):
    from_addr = '420501980@qq.com'
    password = 'slglsojbvkyabjig'
    to_addr = ['doraemoner@msn.cn']
    smtp_server = 'smtp.qq.com'

    msg = MIMEText(str, 'html', 'utf-8')
    msg['From'] = _format_addr('Pythoner <%s>' % from_addr)
    msg['To'] = _format_addr('管理员 <%s>' % to_addr)
    msg['Subject'] = Header(subj + time.strftime('%F'), 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


if __name__ == '__main__':
    z = ZhiHu()
    z.daily()
