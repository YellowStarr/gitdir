#coding=utf-8
__author__ = 'QiuWenjing'


import requests
from interface.API import MyAPI
class MapAPI:
    def __init__(self,url):
        self.baseurl=url
        self.api = MyAPI()

    def map_Near(self, latitude, longitude, radius, token):
        headers = {
            "token": token,
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/near/'
        params = {'latitude': latitude, 'longitude': longitude, 'radius': radius}
        r = requests.get(url, params=params, headers=headers)
        # response = r.json()
        return r