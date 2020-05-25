import threading
from xc import xc
from request import base
from api import api
from kd import kd


class main:
    def __init__(self):
        base()
        self.thread_pool = []
        self.urls = {
            "kd_intr": "https://www.kuaidaili.com/free/intr/",
            "kd_inha": "https://www.kuaidaili.com/free/inha/",
            'xc_http': 'http://www.xicidaili.com/wt/',
            'xc_https': 'http://www.xicidaili.com/wn/',
            'route_showapi': "http://route.showapi.com/22-1"
        }
        self.functions = {
            'xc': xc(),
            'route': api(),
            'kd': kd()
        }

    def run(self):
        for key, url in self.urls.items():
            fc = self.functions[key.split('_')[0]]
            thread = threading.Thread(target=fc.run, args=(url,))
            thread.name = "线程" + key
            self.thread_pool.append(thread)

        for thread in self.thread_pool:
            thread.start()

        for thread in self.thread_pool:
            thread.join()


if __name__ == "__main__":
    main = main()
    main.run()
