#coding=utf-8

import requests

class NewAPIv1_2:
    def __init__(self, url):
        self.baseurl = url

    def homepage(self):
        url = self.baseurl+'/api/v1.2/homepage'
        r = requests.get(url)
        # response = r.json()
        return r

    def banner(self, start):
        url = self.baseurl+'/api/v1.2/banner?start='+start
        r = requests.get(url)
        return r

    def medley_other(self, uid):
        u"""获取他人的串烧"""
        url = self.baseurl+'/api/1.2/users/'+uid+'/medleys'
        r = requests.get(url)
        # response = r.json()
        return r

    def medley_my(self, token, page=1, size=10):
        u"""获取我的串烧"""
        url = self.baseurl+'/api/v1.2/user/medleys'
        headers = {
            "token": token,
            "Host": self.baseurl,
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params, headers=headers)
        # response = r.json()
        return r

    def complaint_other(self, uid, page=1, size=10):
        url = self.baseurl+'/api/1.2/users/'+uid+'/raps'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # response = r.json()
        return r

    def complaint_my(self, token, status=100, page=1, size=10):
        url = self.baseurl+'/api/v1.2/user/raps'
        headers = {
            "token": token,
            "Host": self.baseurl,
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        params = {'page': page, 'size': size, 'status': status}
        r = requests.get(url, params=params, headers=headers)
        # response = r.json()
        return r

    def solo_other(self, uid, page=1, size=10):
        url = self.baseurl + '/api/1.2/users/' + uid + '/solos'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # response = r.json()
        return r

    def solo_my(self, token, status=100, page=1, size=10):
        url = self.baseurl + '/api/1.2/users/solos'
        headers = {
            "token": token,
            "Host": self.baseurl,
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        params = {'page': page, 'size': size, 'status': status}
        r = requests.get(url, params=params, headers=headers)
        # response = r.json()
        return r

    def client_info(self, action):
        """actions		array<object>
                actionTime		string
                actionType		string
                message		string
                subActionType"""
        url = self.baseurl + '/api/v1.2/statis/action'
        r = requests.post(url, json=action)
        # response = r.json()
        return r

    def client_type(self, info):
        """channelName		string
           clientType		string
           clientVersion		string
           machineID		string
           message		string
           originChannel    string
        """
        url = self.baseurl + 'api/v1.2/statis/channel'
        r = requests.post(url, json=info)
        # response = r.json()
        return r

    def other_info(self, token, uid):
        url = self.baseurl + '/api/v1.2/users/'+uid
        headers = {
            "token": token,
            "Host": self.baseurl,
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        # params = {'page': page, 'size': size, 'status': status}
        r = requests.get(url, headers=headers)
        # response = r.json()
        return r

    def my_info(self, token):
        url = self.baseurl + '/api/v1.2/user'
        headers = {
            "token": token,
            "Host": self.baseurl,
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        # params = {'page': page, 'size': size, 'status': status}
        r = requests.get(url, headers=headers)
        # response = r.json()
        return r
