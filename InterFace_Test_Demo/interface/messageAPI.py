#coding=utf-8
__author__ = 'QiuWenjing'

import requests
from interface.API import MyAPI
class MessageAPI:
    def __init__(self,url):
        self.baseurl=url
        self.api = MyAPI()

    def message_Unread(self, token):
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
            "Host": self.baseurl,
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/noticeunreadcount'
        r = requests.get(url, headers=headers)
        # response = r.json()
        return r

    def message_History(self, token, type, page=1, size=10):
        u'''关注的人的作品接口
        type = sys|notice
            Method:get
            @return:
                data{msgs},msg,status
        '''
        headers = {
            "token": token,
            "Host": self.baseurl,
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/sysmsghistory/'+type
        params = {'page': page, 'size': size}
        r = requests.post(url, json=params, headers=headers)
        # response = r.json()
        return r