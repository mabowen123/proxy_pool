from request import base
import threading
import json


class api:
    def __init__(self):
        self.page = 1
        self.params = [
            {"app_id": 243367, "sign": "cd86a92468a94ea3a28421f291876d51"},
            {"app_id": 243246, "sign": "da16d98a4db94f7d886a0e2d536142cb"},
        ]

    def run(self, url):
        print(threading.current_thread().getName(), "启动")
        key = 1
        count = 1
        while count <= self.page:
            html = base().get("{}?showapi_appid={}&showapi_sign={}&page={}".format(url, self.params[key]['app_id'],
                                                                                   self.params[key]['sign'], count))
            count += 1
            if html == False:
                continue

            json_str = json.loads(html)
            body = json_str['showapi_res_body']
            self.page = body['pagebean']['allPages']
            if json_str['showapi_res_code'] == 0 and body['ret_code'] == 0:
                for item in body['pagebean']['contentlist']:
                    thread = threading.Thread(target=base().ip_set, args=["{}:{}".format(item['ip'], item['port']), ])
                    thread.name = '线程apiIP查询:{}:{}'.format(item['ip'], item['port'])
                    thread.start()
