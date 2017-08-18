# -*-coding=utf-8-*-

import requests
from config import runconfig
import logging


class API2:

    @property
    def get_baseurl(self):
        return runconfig.RunConfig().get_base_url()

    def get_header(self, **kwargs):
        """
        注册时，header中不需要token及heipamessage
        :param args: 可传{accessToken，deviceId}
        :return: header
        """
        header = {
            "Host": self.get_baseurl,
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        if "deviceId" in kwargs.keys():
            deviceId = kwargs['deviceId']
            header["HeipaAppMessage"] = "deviceId=%s;clientVersion=2.0;platform=iOS" % deviceId
            if "accessToken" in kwargs.keys():
                token = kwargs['accessToken']
                header['heipaToken'] = token
        return header

    def device_register(self, params):
        """
        设备注册，返回设备id
        :param params: 传入machineID，password，platform,clientVersion
        :return: r
        """
        header = self.get_header()
        url = self.get_baseurl+"/user/register/device"
        r = requests.post(url, json=params, headers=header)
        return r

    def device_login(self, params):
        """
         设备登陆,需要设备Id
        :param params:
        :return:
        """
        header = self.get_header()
        url = self.get_baseurl+"/login/device"
        r = requests.post(url, json=params, headers=header)
        return r

    def mobile_register(self, params, header):
        """
        手机注册,header中需要带上heipamessage
        :param header:
        :param params:
        :return:
        """
        url = self.get_baseurl+"/user/register/mobile"
        r = requests.post(url, json=params, headers=header)
        return r

    def mobile_sms(self, params, header):
        """
        手机注册获取验证码
        :param params: 手机号
        :param header:
        :return:
        """
        url = self.get_baseurl+"/sms/register/mobile"
        r = requests.get(url, params=params, headers=header)
        return r

    def mobile_login(self, params, header):
        """
        注册时的deviceId和登陆时的deviceId应该一致，否则应该不能登陆
        :param params:
        :param header: 需要带上heipamessage
        :return:
        """
        url = self.get_baseurl+"/login"
        r =requests.post(url, json=params, headers=header)
        return r

    def third_register(self, third, params, header):
        """
        :param third:取值为 weixin weibo qq
        :param params:
        :param header:
        :return:
        """
        url = self.get_baseurl+"/user/register/third/%s" % third
        r = requests.post(url, json=params, headers=header)
        return r

    def third_login(self, third, params, header):
        """
        :param third:  取值为 weixin weibo qq
        :param params:
        :param header:
        :return:
        """
        url = self.get_baseurl + "/login/third/%s" % third
        r = requests.post(url, json=params, headers=header)
        return r

    def bind_third(self, third, params, header):
        """
        绑定第三方账号
        :param params:
        :param header:
        :return:
        """
        url = self.get_baseurl+"/user/account/binding/%s" % third
        r = requests.put(url, json=params, headers=header)
        return r

    def bind_phone(self, params, header):
        """
        绑定手机，需要获取验证码,需先调用bind_phone_sms（）
        :param params:
        :param header:
        :return:
        """
        url = self.get_baseurl+"/user/account/binding/phoneNumber"
        r = requests.put(url, params=params, headers=header)
        return r

    def bind_phone_sms(self, params, header):
        """
        第三方绑定手机，获取验证码
        :param params:
        :param header:
        :return:
        """
        url = self.get_baseurl + "/sms/register/third"
        r = requests.get(url, params=params, headers=header)
        return r

    def password_back_sms(self, params, header):
        """
        找回密码，发送手机验证码
        :param params: phoneNumber
        :param header:
        :return:
        """
        url = self.get_baseurl + "/sms/password/retrieval"
        r = requests.get(url, params=params, headers=header)
        return r

    def password_back(self, params, header):
        """
        找回密码，需要调用password_back_sms（）
        :param params:
        :param header:
        :return:
        """
        url = self.get_baseurl+"/user/password"
        r = requests.patch(url, json=params, headers=header)
        return r
    def login_out(self, params, header):
        """
        退出登录
        """
        url = self.get_baseurl+"/logout"
        r = requests.post(url, json=params, headers=header)
        return r

    def refresh_token(self, params, header):

        url = self.get_baseurl+"/refresh/accessToken"
        r = requests.post(url, json=params, headers=header)
        return r

    def get_user_info(self, uid, header):

        url = self.get_baseurl+"/user/%s" % uid
        r = requests.get(url, headers=header)
        return r

    def get_my_info(self, header):

        url = self.get_baseurl+"/user"
        r = requests.get(url, headers=header)
        return r

    def modify_my_info(self, param, header):

        url = self.get_baseurl+"/user"
        r = requests.patch(url, json=param, headers=header)
        return r

    def op_settings(self, method, header, **params):

        url = self.get_baseurl+"/user/settings"
        if method == 'patch':
            # print params
            r = requests.patch(url, json=params['params'], headers=header)
        elif method == 'get':
            r = requests.get(url, headers=header)
        else:
            raise ValueError('method must be patch or get')
        return r

    def op_focus(self, method, uid, header, **kwargs):
        """
        :param method: [put|get|delete]
        :param uid: 被关注用户id
        :param header:
        :param kwargs: page
        :return:
        """
        if method == 'get':
            if 'page' in kwargs.keys():
                url = self.get_baseurl + \
                      "/user/%s/following?page=%s&size=10&sort=default" % (uid, kwargs['page'])
            else:
                url = self.get_baseurl + \
                      "/user/%s/following?page=1&size=10&sort=default" % (uid)
            r = requests.get(url, headers=header)
        elif method == 'put':
            url = self.get_baseurl + "/user/following/%s" % uid
            r = requests.put(url, headers=header)
        elif method == 'delete':
            url = self.get_baseurl + "/user/following/%s" % uid
            r = requests.delete(url, headers=header)
        else:
            raise ValueError('method must be PUT or GET or DELETE')
        return r

    def get_fans_list(self, uid, header):
        url = self.get_baseurl + "/user/%s/follower?page=1&size=10&sort=default" % uid
        r = requests.get(url, headers=header)
        return r

    def op_blacklist(self, method, header, *uid):
        """
        :param method: [put|get|delete]
        :param uid: 被加黑用户id
        :param header:
        :return:
        """
        if method == 'get':
            url = self.get_baseurl + "/user/blacklist?page=1&size=10"
            r = requests.get(url, headers=header)
        elif method == 'put':
            url = self.get_baseurl + "/user/blacklist/%s" % uid
            r = requests.put(url, headers=header)
        elif method == 'delete':
            url = self.get_baseurl + "/user/blacklist/%s" % uid
            r = requests.delete(url, headers=header)
        else:
            raise ValueError('method must be PUT or GET or DELETE')
        return r






