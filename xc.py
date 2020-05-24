import threading
from bs4 import BeautifulSoup
from datetime import datetime
import re
from request import base


class xc:
    def __init__(self):
        self.page = 100

    def run(self, url):
        print(threading.current_thread().getName(), "启动")
        count = 1
        while count <= self.page:
            html = base().get("{}{}".format(url, count))
            count += 1
            if html == False:
                continue
            bs = BeautifulSoup(html, 'lxml')
            ip = bs.findAll(name="tr", attrs={"class": re.compile("(odd)|()")})
            for item in ip:
                td = item.find_all('td')
                ip = td[1].string
                port = td[2].string
                key = td[5].string
                time = datetime.strptime('20' + td[9].string + ':00', '%Y-%m-%d %H:%M:%S')
                now = datetime.now()
                if (now - time).days > 3:
                    continue
                thread = threading.Thread(target=base().ip_set, args=["{}:{}".format(ip, port), key, ])
                thread.name = '线程IP查询:{}:{}'.format(ip, port)
                thread.start()
