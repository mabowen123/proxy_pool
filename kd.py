import threading
from _datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime
from request import base


class kd:
    def __init__(self):
        self.page = 100

    def run(self, url):
        count = 1
        while count <= self.page:
            html = base().get("{}{}".format(url, count))
            count += 1
            if html == False:
                continue
            bs = BeautifulSoup(html, 'lxml')
            table = bs.find(name="table", attrs={"class": "table table-bordered table-striped"}).find('tbody').find_all(
                'tr')
            for item in table:
                td = item.find_all('td')
                ip = td[0].string
                port = td[1].string
                key = td[3].string
                time = datetime.strptime(td[6].string, '%Y-%m-%d %H:%M:%S')
                now = datetime.now()
                if (now - time).days > 3:
                    continue
                thread = threading.Thread(target=base().ip_set, args=["{}:{}".format(ip, port), key, ])
                thread.name = '线程IP查询:{}:{}'.format(ip, port)
                thread.start()
