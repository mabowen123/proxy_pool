from request import base
import threading
import json


class api:
    def __init__(self):
        self.page = 10

    def run(self, url):
        print(threading.current_thread().getName(), "启动")
        count = 1
        while count <= self.page:
            html = base().get("{}&page={}".format(url, count))
            count += 1
            if html == False:
                continue

            json_str = json.loads(html)
            body = json_str['showapi_res_body']
            self.page = body['pagebean']['allPages']
            if json_str['showapi_res_code'] == 0 and body['ret_code'] == 0:
                for item in body['pagebean']['contentlist']:
                    thread = threading.Thread(target=base().ip_set, args=["{}:{}".format(item['ip'], item['port']), ])
                    thread.name = '线程IP查询:{}:{}'.format(item['ip'], item['port'])
                    thread.start()
