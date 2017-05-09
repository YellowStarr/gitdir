#coding=utf-8
__author__ = 'QiuWenjing'


import requests
from interface.API import MyAPI
class UserAPI:
    def __init__(self,url):
        self.baseurl=url
        self.api = MyAPI()

    def user_Near(self,latitude,longitude,radius,token):
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

        response = r.json()
        return response

    def user_FollowedSong(self,token,page=1,size=10):
        u'''关注的人的作品接口
            Method:get
            @return:
                data{advertisement:[{des,url,name,id,image,ios},]},msg,status
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
        url = self.baseurl + '/api/user/followed/song'
        params = {'page': page, 'size': size}
        r = requests.get(url,params=params,headers=headers)
        # self.api.writeLog('user_FollowedSong', r.text)
        response = r.json()
        return response

    def user_Recommend(self, page=1, size=10):
        u'''官方推荐'''
        url = self.baseurl + '/api/song/recommend'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Recommend', r.text)
        response = r.json()
        return response

    def user_Newest_Medley(self, page=1, size=10):
        u'''最新串烧'''
        url = self.baseurl + '/api/song/medley/newest'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Newest_Medley', r.text)
        response = r.json()
        return response

    def user_Newest_Complaint(self, page=1, size=10):
        u'''最新吐槽'''
        url = self.baseurl + '/api/song/complaint/newest'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Newest_Complaint', r.text)
        response = r.json()
        return response

    def user_Newest_Rap(self, page=1, size=10):
        u'''最新串烧'''
        url = self.baseurl + '/api/song/rap/newest'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Newest_Rap', r.text)
        response = r.json()
        return response

    def user_Focus(self,id,token):
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
        url = self.baseurl + '/api/user/focus'
        params = {'id': id}
        r = requests.post(url, json=params, headers=headers)
        # self.api.writeLog('user_Focus', r.text)
        response = r.json()
        return response

    def user_cancelFocus(self,id,token):
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
        url = self.baseurl + '/api/user/cancelFocus'
        params = {'id': id}
        r = requests.post(url, json=params, headers=headers)
        # self.api.writeLog('user_cancelFocus', r.text)
        response = r.json()
        return response

    def user_followedList(self, id):
        u'''关注列表'''

        url = self.baseurl + '/api/user/followed'
        params = {'id': id}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_followedList', r.text)
        response = r.json()
        return response

    def user_fansList(self, id):
        u'''粉丝列表'''
        # headers = {
        #     "token": token,
        #     "Host": "139.129.208.77:8080",
        #     "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
        #     "Accept": "*/*",
        #     "Accept-Language": "zh-Hans-CN;q=1",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Content-Type": "application/json;charset=UTF-8",
        #     "Connection": "keep-alive"
        # }
        url = self.baseurl + '/api/user/follower'
        params = {'id': id}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_fansList', r.text)
        response = r.json()
        return response

    def user_Violate(self,contact,reportid,reporttype,text):
        '''举报
        @param reportid: number 被举报人id
        @param reporttype: number
        @param text: string
        '''
        url = self.baseurl + '/api/violate'
        params = {'contact': contact, 'reportId': reportid, 'reportType': reporttype, 'text': text}
        r = requests.post(url, json=params)
        # self.api.writeLog('user_Violate', r.text)
        response = r.json()
        return response

    def user_Add_BlackList(self, id, token):
        u'''加入黑名单'''
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
        url = self.baseurl + '/api/user/blacklist'
        params = {'uid': id}
        r = requests.post(url, json=params, headers=headers)
        # self.api.writeLog('user_Add_BlackList', r.text)
        response = r.json()
        return response

    def user_Del_BlackList(self, id, token):
        u'''移出黑名单'''
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
        url = self.baseurl + '/api/user/blacklist/delete'
        params = {'uid': id}
        r = requests.post(url, json=params, headers=headers)
        # self.api.writeLog('user_Del_BlackList', r.text)
        response = r.json()
        return response

    def user_BlackList(self, page, token):
        u'''黑名单'''
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
        url = self.baseurl + '/api/user/blacklist'
        params = {'page': page}
        r = requests.get(url, params=params, headers=headers)
        # self.api.writeLog('user_BlackList', r.text)
        response = r.json()
        return response

    def user_Participant_Medley(self, token, page=1, size=10):
        u'''我加入的串烧'''
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
        url = self.baseurl + '/api/user/join/medley/underWay'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params, headers=headers)
        # self.api.writeLog('user_Participant_Medley', r.text)
        response = r.json()
        return response

    def user_Create_Medley(self, token, audios, images, latitude, longitude, maxcount, title):
        u'''我加入的串烧'''
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
        url = self.baseurl + '/api/audio/createMedley'
        params = {'audios': audios, 'images': images, 'latitude':latitude, 'longitude':longitude, 'maxCount':maxcount, 'title':title}
        r = requests.post(url, json=params, headers=headers)
        # self.api.writeLog('user_Create_Medley', r.text)
        response = r.json()
        return response

    def user_Song_State(self, token, page=1, size=10):
        u'''该Url包括(4:合成失败,6:合成中)两个状态的歌曲'''
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
        url = self.baseurl + '/api/user/song/status'
        params = {'page': page, 'size': size}
        r = requests.get(url, params=params, headers=headers)
        # self.api.writeLog('user_Song_State', r.text)
        response = r.json()
        return response

    def user_Medley_Participanter(self, songId):
        u'''串烧参与者'''

        url = self.baseurl + '/api/medleys/participants/all'
        params = {'songId': songId}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Medley_Participanter', r.text)
        response = r.json()
        return response

    def user_Medley_Participanter_Once(self, songId):
        u'''串烧参与者去重'''

        url = self.baseurl + '/api/medleys/participants'
        params = {'songId': songId}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Medley_Participanter_Once', r.text)
        response = r.json()
        return response

    def user_ModifyInfo(self, area, birthday, emotionStatus, hasFocus, id, personalProfile,
                        phoneNumber, portrait, sex, userName, token):
        u'''修改用户信息'''
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
        url = self.baseurl + '/api/modifyUserInfo'
        params = {'area': area,'birthday': birthday,'emotionStatus': emotionStatus,
                  'hasFocus': hasFocus,'personalProfile': personalProfile,'phoneNumber': phoneNumber,
                  'portrait': portrait,'sex': sex,'userName': userName,'id':id}
        r = requests.post(url, json=params, headers=headers)
        # self.api.writeLog('user_ModifyInfo', r.text)
        response = r.json()
        return response

    def user_getUserInfo(self, id):
        u'''获取用户信息'''

        url = self.baseurl + '/api/getUserInfo'
        params = {'id':id}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_getUserInfo', r.text)
        response = r.json()
        return response

    def user_getMyMedley(self, token,status,page=1,size=10):
        u'''我的串烧'''
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
        url = self.baseurl + '/api/user/medleys'
        params = {'status':status,'page':page,'size':size}
        r = requests.get(url, params=params, headers=headers)
        # self.api.writeLog('user_getMyMedley', r.text)
        response = r.json()
        return response

    def user_getMyComplaint(self, token,status,page=1,size=10):
        u'''获取吐槽作品'''
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
        url = self.baseurl + '/api/user/complaints'
        params = {'status':status,'page':page,'size':size}
        r = requests.get(url, params=params, headers=headers)
        # self.api.writeLog('user_getMyComplaint', r.text)
        response = r.json()
        return response

    def user_getMyRap(self, token, status, page=1, size=10):
        u'''获取我的独白'''
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
        url = self.baseurl + '/api/user/raps'
        params = {'status': status, 'page': page, 'size': size}
        r = requests.get(url, params=params, headers=headers)
        # self.api.writeLog('user_getMyRap', r.text)
        response = r.json()
        return response

    def user_Statistic(self, id):
        u'''获取用户扩展信息'''
        url = self.baseurl + '/api/user/statistic'
        params = {'id': id}
        r = requests.get(url, params=params)
        # self.api.writeLog('user_Statistic', r.text)
        response = r.json()
        return response