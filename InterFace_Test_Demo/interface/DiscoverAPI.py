#coding=utf-8

import requests

class DiscoverAPI:
    def __init__(self,url):
        self.baseurl=url

    def discover_ADs(self):
        u'''发现广告接口
            Method:get
            @return:
                data{advertisement:[{des,url,name,id,image,ios},]},msg,status
        '''
        url = self.baseurl + '/api/findAd'
        r = requests.get(url)
        # r = r.json()
        return r

    def discover_Latest(self):
        u'''发现-最新
            Method:get
            @return:
                data
                {discover:
                    [
                        {
                            data:
                                [
                                    {
                                        description,userId,portrait,id,userName,commentCount,createTime,songUrl,
                                        praiseCount,songDuration,listenCount,shareCount,songName,status,image,images
                                    }
                                ],
                            type:solo,medley,complaint
                        }
                    ]
                },msg,status
        '''
        url = self.baseurl + '/api/discover'
        r = requests.get(url)
        # print r.text
        # r = r.json()
        return r

    def discover_Followed(self):
        u"""关注列表
        @Method:get
        @return:
            data:{songs:[
                hasCollect,images,songName,collectCount,songUrl,userName,praiseCount,fanCount,hasPraise,portrait,
                listenCount,id,shareHtmlUrl,description,isPublic,creatTime,songDuration,commentCount,userId,category
                ]},msg,status
        """
        url = self.baseurl+"/api/user/followed/song"
        r = requests.get(url, {'size': 10, 'page': 1})
        # r = r.json()
        return r

    def discover_Activity(self):
        u"""活动
        @Method:get
        @return:
            data:{activitys:[{
                homePageUrl,particiWay,name,posterImagUrl,endTime,activityType,
                creatTime,description,startTime,activityId,state}
                ]},msg,status
        """
        url = self.baseurl+"/api/activitys"
        r = requests.get(url)
        # r = r.json()
        return r

    def discover_Join_Activity(self, songId, actId):
        u"""加入活动
        @Method:post
        @post:{songId,activityId}
        @return:
            data:{notice},msg,status
        """
        url = self.baseurl+"/api/activitys"
        r = requests.post(url,json={'songId':songId,'activityId':actId})
        # r = r.json()
        return r

    def discover_Activity_Detail_T30(self, actId):
        """
        @Method:get
        @params:page,size,activityId
        @return:
            data:{songs:[
                images,songName,collectCount,songUrl,userName,praiseCount,fanCount,portrait,
                listenCount,id,shareHtmlUrl,description,creatTime,songDuration,commentCount,category,lyric
                ]},msg,status
        """
        url = self.baseurl+"/api/activity/song/hot"
        params = {'size': 10, 'page': 1, 'activityId': actId}
        r = requests.get(url, params=params)
        # r = r.json()
        return r

    def discover_Activity_Song(self, actId):
        u"""发现-活动-获取用户参加该活动的歌曲和排名
        @param actId:
        @return:
            data:{songs:[
                images,songName,collectCount,songUrl,userName,praiseCount,fanCount,portrait,
                listenCount,id,shareHtmlUrl,description,creatTime,songDuration,commentCount,category,lyric
                ]},msg,status,rank
        """
        url = self.baseurl + "/api/activity/user/song"
        params = {'activityId': actId}
        r = requests.get(url, params=params)
        # r = r.json()
        return r

    def discover_Activity_New30(self,actId):
        u"""发现-活动-获取最新参加活动的歌曲
        @param actId:
        @return:
            data:{songs:[
                images,songName,collectCount,songUrl,userName,praiseCount,fanCount,portrait,
                listenCount,id,shareHtmlUrl,description,creatTime,songDuration,commentCount,category,lyric
                ]},msg,status,rank
        """
        url = self.baseurl + "/api/activity/song"
        params = {'size':10,'page':1,'activityId':actId}
        r = requests.get(url, params=params)
        # r = r.json()
        return r

    def user_Newest_Medley(self, page=1, size=10):
        u'''最新串烧'''
        url = self.baseurl + '/api/song/medley/newest'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Newest_Medley', r.text)

        return r

    def user_Newest_Complaint(self, page=1, size=10):
        u'''最新吐槽'''
        url = self.baseurl + '/api/song/complaint/newest'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Newest_Complaint', r.text)
        #
        return r

    def user_Newest_Rap(self, page=1, size=10):
        u'''最新串烧'''
        url = self.baseurl + '/api/song/rap/newest'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Newest_Rap', r.text)

        return r
    # def discover_New_Complaint(self):
