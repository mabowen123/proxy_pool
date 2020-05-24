from random import randint
from fake_useragent import UserAgent
import time
import requests
import hashlib
import json
from r import r
import threading


class base:
    _instance = None
    _first = False

    def __init__(self):
        if self._first == False:
            self.proxy = r().get("ip*")
            self.ua = UserAgent(verify_ssl=False)
            self._first = True

    def __new__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def random_proxy(self):
        proxy_len = len(self.proxy)
        if proxy_len == 0:
            return {}
        ip = self.proxy[randint(0, proxy_len - 1)]
        return {
            'http': ip,
            'https': ip
        }

    @property
    def random_headers(self):
        return {
            'User-Agent': self.ua.random
        }

    def sleep(self, double_int=0):
        second = randint(1, 10)
        if double_int > 0:
            second = second * double_int

        time.sleep(second)

    def get(self, url):
        try:
            print("{}请求开始".format(url))
            response = requests.get(url, headers=self.random_headers, proxies=self.random_proxy, timeout=10)
            if response.status_code == 200:
                self.sleep()
                return response.text
            else:
                self.sleep(randint(10, 60))
                return False
        except Exception as e:
            print("{}请求错误,{}".format(url, e))
            return False

    def ip_set(self, ip, prefix='http'):
        print(threading.current_thread().getName(), '开始')
        prefix = prefix.lower()
        url = '{}://whois.pconline.com.cn/ipJson.jsp?json=true'.format(prefix)
        try:
            response = requests.get(url, headers=self.random_headers, proxies={
                prefix: ip
            }, timeout=10)
            if response.status_code == 200 and json.loads(response.text)['regionCode'] == '0':
                key = "ip:{}:{}".format(prefix, hashlib.md5(ip.encode(encoding='UTF-8')).hexdigest())
                r().set(key, ip)
                self.proxy.append(ip)
        except Exception as e:
            print("{}请求错误,{}".format(url, e))
            pass
