#coding=utf-8
__author__ = 'QiuWenjing'

import requests
from interface.API import MyAPI
class ShareAPI:
    def __init__(self,url):
        self.baseurl=url
        self.api = MyAPI()

    def share_ShareList(self, token, userid, page=1, size=10):
        u'''关注的人的作品接口
            Method:get
            @return:
                data{songs:[{category,collectCount,commentCount,createTime,description,
                fanCount,id,images,isPublic,listenCount,loginUserName,lyric,portrait,
                praiseCount,shareHtmlUrl,shareReason,songDuration,songName,songUrl,userId,
                userName},]},msg,status
        '''
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
        url = self.baseurl + '/api/user/shareList'
        params = {'userId': userid, 'page': page, 'size': size}
        r = requests.get(url, params=params, headers=headers)
        # response = r.json()
        return r

    def share_Share_Inner(self, token, sid):
        u'''站内分享
            Method:get
            @return:
                data{count},msg,status
        '''
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
        url = self.baseurl + '/api/user/share'
        params = {'id':sid}
        r = requests.post(url,json=params,headers=headers)
        # response = r.json()
        return r

    """def share_Share_Outter(self, token, id, cate):
        u'''站外分享
            Method:get
            @return:
                data{count},msg,status
        '''
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
        url = self.baseurl + 'api/user/share/html'
        params = {'id':id,'cate':cate}
        r = requests.get(url,json=params,headers=headers)
        response = r.json()
        return response"""