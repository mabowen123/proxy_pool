from datetime import datetime
import threading
from xc import xc
from request import base
from api import api


class main:
    # cd86a92468a94ea3a28421f291876d51 243367
    # da16d98a4db94f7d886a0e2d536142cb 243246
    def __init__(self):
        base()
        self.thread_pool = []
        self.urls = {
            # 'xc_http': 'http://www.xicidaili.com/wt/',
            # 'xc_https': 'http://www.xicidaili.com/wn/',
            'route_showapi': "http://route.showapi.com/22-1?showapi_appid={}&showapi_sign={}".format(
                '243367',
                'cd86a92468a94ea3a28421f291876d51'
            )
        }
        self.functions = {
            'xc': xc(),
            'route': api()
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
