#coding=utf-8

import requests

class LoginAPI:
    def __init__(self,url):
        self.baseurl=url

    def forgetpwd_modifyPwd(self,phoneNumber='',password='',code=''):
        u''' 忘记密码页面修改密码接口
            Method:post

            @param string phoneNumber:
            @param string password:
            @param string code:验证码
            @return: status:0 成功,1 旧密码错误 99 数据错误
        '''
        url = self.baseurl+'/api/forgetPass'
        postdata = {'phoneNumber':phoneNumber, 'password': password,
                    "code": code}
        r = requests.post(url, json=postdata)
        # print r.text
        # self.assertEqual(200, r.status_code)
        # r = r.json()

        return r

    def forgetpwd_msgCode(self, phoneNumber=''):
        u''' 忘记密码页面短信验证码接口
            Method:get
            Request：
            @param string phoneNumber:
            @return:
                data:{identifyCode},status,msg
        '''
        url = self.baseurl+'/api/getCodeForNewPass'
        param = {'phoneNumber': phoneNumber}
        r = requests.get(url, params=param)
        # print r.text
        # self.assertEqual(200, r.status_code)
        # r = r.json()
        return r


    def register_msgCode(self, phoneNumber=''):
        u''' 注册页面短信验证码接口
            Method:get
            Request：
            @param string phoneNumber:
            @return:
                data:{identifyCode},status：0 成功 1 失败,msg
        '''
        url = self.baseurl+'/api/getIdentifyingCode'
        param = {'phoneNumber': phoneNumber}
        r = requests.get(url, params=param)
        # print r.text
        # self.assertEqual(200, r.status_code)
        # r = r.json()
        return r

    def register_Register(self, username='', phoneNumber='', password='', code=''):
        u''' 注册接口
            Method:post
            @param string username:
            @param string phoneNumber:
            @param string password:
            @param string code:验证码
            @return:
                msg,status:111 手机号已注册,100 用户创建失败 999 未知错误,data{userId}
        '''
        url = self.baseurl+'/api/register'
        postdata = {'username': username, 'password': password, 'code': code, 'phoneNumber': phoneNumber}
        r = requests.post(url, json=postdata)
        # r = r.json()
        return r

    def login_Login(self, phoneNumber='', password=''):
        u''' 登陆接口
            Method:post
            @param  phoneNumber:string
            @param string password:加密字符串
            @return:
                data{token,user:{id,phone,username,email}},msg,status:1 用户名或密码错误,0 成功 99 数据错误,
        '''
        url = self.baseurl+'/api/user/login'

        postdata = {"terminal": 2, 'password': password, 'phone': phoneNumber}
        r = requests.post(url, json=postdata)
        # r = r.json()
        return r

    def login_Update(self, type):
        u''' 软件版本更新
            Method:get
                @return:
                data{version:{ext,version,url,upgradeContent,platform,minimumSupportVersion,force:0，1 强制更新}},msg,status:0 成功
        '''
        url = self.baseurl + '/api/clientVersion/' + type
        #url = self.baseurl + '/api/clientVersion/'
        r = requests.get(url)
        # r = r.json()
        return r

    def login_InitConfig(self,accessId='ios'):
        u'''获取初始化
            Method:get
            @return:
                data{config:{ossAccessKeySecret,ossBucketName,ossAccessKeyId,andriod:{},ossEndPoint,ios:{}}},msg,status:0 成功
        '''
        params={'accessId':accessId}
        url = self.baseurl + '/api/config'
        r = requests.get(url,params=params)
        print r.text
        # r = r.json()
        return r

    def login_ThirdParty(self, token, username, sex, thirdPartyType):
        url = self.baseurl+'/api/thirdPartyLogin'
        params = {'userName': username, 'sex': sex, 'thirdPartyType': thirdPartyType, 'token': token}
        r = requests.post(url, json=params)
        # r = r.json()
        return r

