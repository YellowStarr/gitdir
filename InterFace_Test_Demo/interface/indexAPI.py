#coding=utf-8
__author__ = 'QiuWenjing'

import requests
from interface.API import MyAPI
class IndexAPI:
    def __init__(self,url):
        self.baseurl=url
        self.api = MyAPI()

    def index_Recommend(self, page=1, size=10):
        u'''官方推荐'''
        url = self.baseurl + '/api/song/recommend'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Recommend', r.text)
        
        return r

    def index_Song_State(self, token, page=1, size=10):
        u'''该Url包括(4:合成失败,6:合成中)两个状态的歌曲'''
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
        url = self.baseurl + '/api/user/song/status'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params, headers=headers)
        # self.api.writeLog('user_Song_State', r.text)
        
        return r

    def index_Hot_Music(self,type,size=10,page=1):
        u'''获取热门歌曲信息
        :type raps|medleys|complaints|battles
        @return
        {data:{song:[{fanCount,maxCount,createTime,personTimes,userId,portrait,commentCount,
            songName,id,image,currCount,lyric,listenCount,praiseCount,status,userName,shareCount,
            collectCount,description}],msg,status}
        '''
        url = self.baseurl + '/api/hot/' + type
        param = {'size': size, 'page': page}
        r = requests.get(url, params=param)
        
        return r

    def index_Rank(self,page=1,size=50):
        u'''排行榜
            @:return data:{[songs:{category,collectCount,commentCount,createTime,description...}]}
        '''
        url = self.baseurl + '/api/song/ranking'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        
        return r

    def index_Homepage(self):
        url = self.baseurl + '/api/homepage'
        r = requests.get(url)
        
        return r