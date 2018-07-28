from urllib import request

from bs4 import BeautifulSoup

from scrapy.Zhihu import send_email


class ShenTuCao:
    def __init__(self):
        self.url = 'https://www.zhihu.com'

    def tu_cao(self):
        head = '''<html><head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8"><body>'''
        end = '''</body></head></html>'''
        for pagenum in range(1, 3):  # 从第1页爬到第20页

            strpagenum = str(pagenum)  # 页数的str表示
            print("Getting data for Page " + strpagenum)  # shell里面显示的，表示已爬到多少页
            url = 'http://www.zhihu.com/collection/27109279?page=' + strpagenum  # 网址
            page = request.urlopen(url)  # 打开网页
            soup = BeautifulSoup(page, 'html.parser')  # 用BeautifulSoup解析网页

            # 找到具有class属性为下面两个的所有Tag
            # ALL = soup.findAll(attrs={'class': ['zm-item-title', 'zh-summary summary clearfix']})
            ALL = soup.findAll(attrs={'class': ['zm-item-title', 'zm-item-rich-text expandable js-collapse-body']})

            count = pagenum
            for each in ALL:  # 枚举所有的问题和回答
                if each.name == 'h2':  # 如果Tag为h2类型，说明是问题
                    # print(each.a)  # 问题中还有一个<a..>，所以要each.a.string取出内容
                    if each.a:  # 如果非空，才能写入
                        writable = str(pagenum) + '.' + str(count - pagenum) + ' ' + each.string
                        body = '''<h3>%s</h3> ''' % writable
                        head += body
                        count += 1
                else:  # 如果是回答，同样写入
                    cnt = str(each.text)
                    # t = cnt.replace('\n\n', '')
                    more = each.a.get('href')
                    if cnt:
                        index = cnt.index('\n\n\n')
                        s = cnt[index+3:len(cnt)-22]
                        body = '''<p>%s</p><p><a href='%s'>更多精彩</a></p>''' % (s, self.url + more)
                        head += body

        head += end
        send_email(head, '神吐槽')


if __name__ == '__main__':
    s = ShenTuCao()
    s.tu_cao()
