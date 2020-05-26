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
            self.lock = threading.Lock()

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
            'User-Agent': self.ua.random,
            'Connection': 'close'
        }

    def sleep(self, double_int=0):
        second = randint(1, 10)
        if double_int > 0:
            second = second * double_int

        time.sleep(second)

    def get(self, url, use_proxy=True):
        try:
            print("{}请求开始".format(url))
            proxy = {}
            if use_proxy:
                proxy = self.random_proxy
            response = requests.get(url, headers=self.random_headers, proxies=proxy, verify=False, timeout=(60, 120))
            if response.status_code == 200:
                self.sleep()
                return response.text
            else:
                if use_proxy:
                    self.proxy.remove(proxy['http'])
                self.sleep(randint(10, 60))
                return False
        except Exception as e:
            self.sleep(randint(10, 60))
            return False

    def ip_set(self, ip, prefix='http'):
        print(threading.current_thread().getName(), '开始')
        prefix = prefix.lower()
        url = '{}://whois.pconline.com.cn/ipJson.jsp?json=true'.format(prefix)
        retries = 0
        max_retries = 3
        self.lock.acquire()
        while retries < max_retries:
            try:
                requests.Session().keep_alive = False
                response = requests.get(url, headers=self.random_headers, proxies={
                    prefix: ip
                }, verify=False, timeout=60)
                if response.status_code == 200 and json.loads(response.text)['regionCode'] == '0':
                    key = "ip:{}:{}".format(prefix, hashlib.md5(ip.encode(encoding='UTF-8')).hexdigest())
                    r().set(key, ip)
                    self.proxy.append(ip)
                    break
            except Exception as e:
                retries += 1
                self.sleep()
                if retries == max_retries:
                    print("ip查询请求{}次错误,{}".format(retries, e))

        self.lock.release()
