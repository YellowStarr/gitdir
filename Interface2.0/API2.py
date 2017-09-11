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

    def get_fans_list(self, uid, header, **params):
        url = self.get_baseurl + "/user/%s/follower" % uid
        if 'param' in params.keys():
            r = requests.get(url, params=params['param'], headers=header)
        else:
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

    def op_collect(self, method, header, **kwargs):
        """
        收藏接口，包括收藏，收藏列表，取消收藏
        get时，args传page,size,sort
        put 或delete,则传递userId,opusId,有attach时还有attach
        :param method: [put|get|delete]
        :param header:
        :param kwargs:{'userid', 'opusid'}
        :return:
        """
        if kwargs:
            kwargs = kwargs['kwargs']
        if method in ['put', 'delete']:
            userid = kwargs['userid']
            opusid = kwargs['opusid']
            if 'attach' in kwargs.keys():
                attach = kwargs['attach']
                if method == 'put':
                    url = self.get_baseurl + "/user/collect/%s/%s" % (userid, opusid)
                    r = requests.put(url, json={"attach": attach}, headers=header)
                else:
                    url = self.get_baseurl + '/user/collect/%s/%s' % (userid, opusid)
                    r = requests.delete(url,params=attach, headers=header)
            else:
                url = self.get_baseurl + "/user/collect/%s/%s" % (userid, opusid)
                if method == 'put':
                    r = requests.put(url, headers=header)
                else:
                    r = requests.delete(url, headers=header)
        elif method == 'get':
            url = self.get_baseurl + '/user/collect'
            if kwargs:
                r = requests.get(url, params=kwargs, headers=header)
            else:
                r = requests.get(url, headers=header)
        else:
            raise ValueError("Method must be [PUT,DELETE,GET]")
        return r

    def op_praise(self, typo, header, **kwargs):
        """
        点赞接口，包括作品点赞，评论点赞
        :param typo: [opus|comment]
        :param header:
        :param kwargs:点赞作品{'userid','opusid'};点赞评论{'userid','opusid'，'commentid'}
        :return:
        """
        if kwargs:
            kwargs = kwargs['kwargs']
        if typo == 'opus':
            url = self.get_baseurl + '/user/like/%s/%s' % \
                                     (kwargs['userid'], kwargs['opusid'])
            if 'attach' in kwargs.keys():
                r = requests.put(url, json={'attach': kwargs['attach']}, headers=header)
            else:
                r = requests.put(url, headers=header)
        elif typo == 'comment':
            url = self.get_baseurl + '/comment/like/%s/opus/song/%s/%s' % \
                                         (kwargs['userid'], kwargs['opusid'], kwargs['commentid'])
            r = requests.put(url, headers=header)
        else:
            raise ValueError("Method must be [PUT,DELETE,GET]")
        return r

    # 创作接口，包括虚拟歌手，自由说唱，智能说唱，串烧
    def create_virtual_singer(self, typo, data, header):
        """
        创作虚拟歌手作品，自由说唱，智能说唱,串烧
        :param typo: virtual|free|intelligent|medley
        :param data:{}
        :param header:
        :return:
        """
        if typo == 'virtual':
            url = self.get_baseurl + '/opus/song/singer'
        elif typo == 'free':
            url = self.get_baseurl + '/opus/song/free'
        elif typo == 'intelligent':
            url = self.get_baseurl + '/opus/song/intel'
        elif typo == 'medley':
            url = self.get_baseurl + '/opus/song/medley'
        else:
            raise ValueError("Typo value wrong, must in [virtual,free,intelligent,medley]")
        r = requests.post(url, json=data, headers=header)
        return r

    def modify_opus_info(self, songid, data, header):
        """
        修改歌曲信息
        :param songid:
        :param data:
        :param header:
        :return:
        """
        url = self.get_baseurl + '/opus/song/%s' % songid
        r = requests.patch(url, json=data, headers=header)
        return r

    def op_share(self, method, header, **kwargs):
        """
        分享操作相关，分享，取消分享，分享列表
        :param method: put\delete\get
        :param data:
        :param header:
        :param kwargs:
        :return:
        """
        if kwargs:
            kwargs = kwargs['kwargs']
        if method == 'put':
            url = self.get_baseurl + '/user/share/%s/%s' % (kwargs['userid'], kwargs['opusid'])
            r = requests.put(url, json=kwargs['param'], headers=header)
        elif method == 'delete':
            url = self.get_baseurl + '/user/share/%s' % (kwargs['shareid'])
            if 'attach' in kwargs.keys():
                url = self.get_baseurl + '/user/share'
                r = requests.delete(url, params=kwargs['param'], headers=header)
            else:
                r = requests.delete(url, headers=header)
        elif method == 'get':
            url = self.get_baseurl + '/user/share'
            if kwargs:
                r = requests.get(url, params=kwargs, headers=header)
            else:
                r = requests.get(url, headers=header)
        else:
            raise ValueError("Method must be [PUT,DELETE,GET]")
        return r

    def get_version(self, platform, header):
        url ='http://139.224.68.41:8080/api/update/version/%s' % platform
        r = requests.get(url, headers=header)
        return r

    def get_share_link(self, opusid, header):
        url = self.get_baseurl + '/user/share/%s/share_link' % opusid
        r = requests.get(url, headers=header)
        return r

    # 发布作品
    def opus_publish(self, opusid, data, header):

        url = self.get_baseurl + '/opus/song/%s/publish' % opusid
        r = requests.patch(url, json=data, headers=header)
        return r

    def op_comment(self, typo, method, header, **kwargs):
        """
        歌曲详情页面评论及子评论相关操作
        :param typo:  song|comment 代表歌曲评论和子评论
        :param method: post|get|delete
        :param header:
        :param kwargs:
        :return:
        """
        if kwargs:
            kwargs = kwargs['kwargs']
        if typo == 'song':
            if method == 'post':
                url = self.get_baseurl + '/comment/%s/opus/song/%s' % (kwargs['userid'], kwargs['opusid'])
                r = requests.post(url, json=kwargs['param'], headers=header)
            elif method == 'delete':
                url = self.get_baseurl + '/comment/%s/opus/song/%s/%s' % (kwargs['userid'], kwargs['opusid'], kwargs['commentid'])
                r = requests.delete(url, headers=header)
            elif method == 'get':
                url = self.get_baseurl + '/comment/%s/opus/song/%s' % (kwargs['userid'], kwargs['opusid'])
                if 'param' in kwargs.keys():
                    r = requests.get(url, params=kwargs['param'], headers=header)
                else:
                    r = requests.get(url, headers=header)
            else:
                raise ValueError("Method must be [PUT,DELETE,GET]")
        elif typo == 'comment':
            if method == 'post':
                url = self.get_baseurl + '/comment/%s/opus/song/%s/%s' % (kwargs['userid'], kwargs['opusid'], kwargs['commentid'])
                r = requests.post(url, json=kwargs['param'], headers=header)
            elif method == 'delete':
                url = self.get_baseurl + '/comment/%s/opus/song/%s/%s' % (kwargs['userid'], kwargs['opusid'], kwargs['commentid'])
                r = requests.delete(url, headers=header)
            elif method == 'get':
                url = self.get_baseurl + '/comment/%s/opus/song/%s/%s' % (kwargs['userid'], kwargs['opusid'], kwargs['commentid'])
                if 'param' in kwargs.keys():
                    r = requests.get(url, params=kwargs['param'], headers=header)
                else:
                    r = requests.get(url, headers=header)
            else:
                raise ValueError("Method must be [PUT,DELETE,GET]")
        return r

    # 查看别人已发布作品，查看自己发布及未发布作品
    def op_opus(self, myself, header, ispublish=1, param={}):
        """
        :param myself: 0,1
        :param ispublish:  取值为0，1
        :param header:
        :param param:
        :return:
        """
        url_list = ['/user/opus/unpublished', '/user/opus/published']
        if myself == 1:
            url = self.get_baseurl + url_list[ispublish]
            if param:
                r = requests.get(url, params=param, headers=header)
            else:
                r = requests.get(url, headers=header)
        elif myself == 0:
            url = self.get_baseurl + '/user/%s/opus/published' % param['userid']
            if 'param' in param.keys():
                r = requests.get(url, params=param['param'], headers=header)
            else:
                r = requests.get(url, headers=header)
        return r

    def listen(self, header, **kwargs):
        if kwargs:
            kwargs = kwargs['kwargs']
        url = self.get_baseurl + '/user/listen/%s/%s' % (kwargs['userid'], kwargs['opusid'])
        r = requests.put(url, json=kwargs['param'], headers=header)
        return r

    # 加入串烧，查看串烧参与者，撤销加入串烧
    def op_medley(self, method, header, **kwargs):
        try:
            kwargs = kwargs['kwargs']
        except ValueError:
            print kwargs
        url = self.get_baseurl + '/opus/song/%s/participant' % kwargs['opusid']
        if method == 'post':
            r = requests.post(url, json=kwargs['param'], headers=header)
        elif method == 'get':    # 查看串烧参与者
            if 'param' in kwargs.keys():
                r = requests.get(url, params=kwargs['param'], headers=header)
            else:
                r = requests.get(url, headers=header)
        elif method == 'delete':
            url = self.get_baseurl + '/opus/song/%s/participant/%s' % (kwargs['opusid'],kwargs['participantid'])
            r = requests.delete(url, headers=header)
        return r

    # 删除作品
    def delete_opus(self, header, sid):
        url = self.get_baseurl + '/opus/song/%s' % sid
        r = requests.delete(url, headers=header)
        return r

    def get_oss_url(self, header, param):
        url = self.get_baseurl + '/oss/presign'
        r = requests.post(url, json=param, headers=header)
        return r

    def opus_score(self, header, param):

        url = self.get_baseurl + '/user/score/%s/%s' % (param['userid'], param['opusid'])
        r = requests.put(url, json=param['param'], headers=header)
        return r

    def shown_page(self, key, header, param):
        """
        展示页面接口。推荐recommend，热门hot，最新newest，榜单ranking，音乐人musician，星探scout
        :param key:
        :param header:
        :param param:
        :return:
        """
        urldict = {
            'recommend': '/page/recommend',
            'hot': '/page/popular',
            'newest': '/page/release',
            'ranking': '/page/ranking',
            'musician': '/ranking/user/musician',
            'scout': '/ranking/user/scout'
        }

        url = self.get_baseurl + urldict[key]
        r = requests.get(url, params=param, headers=header)
        return r

    # 反馈及举报
    def violate_feedback(self, key, header, param):
        """
        key取值为0,1.0为举报，1为反馈
        :param key:
        :param header:
        :param param:
        :return:
        """
        url_list = ['/violate', '/feedback']
        url = self.get_baseurl + url_list[key]
        r = requests.post(url, json=param, headers=header)
        return r

    def get_song_detail(self, flag, header, param):
        """歌曲详情页面评论列表"""
        if flag == 0:
            url = self.get_baseurl + '/page/opus/song/%s' % param['opusid']
        elif flag == 1:
            url = self.get_baseurl + '/page/comment/%s/opus/song/%s' % (param['userid'], param['opusid'])
        if 'param' in param.keys():
            r = requests.get(url, params=param['param'], headers=header)
        else:
            r = requests.get(url, headers=header)
        return r

    def search(self, key, header, param):
        url_dict = {
            'user': '/search/user',
            'opus': '/search/opus/song',
            'hot': '/search/keyword'
        }
        url = self.get_baseurl + url_dict[key]
        if param:
            r = requests.get(url, params=param, headers=header)
        else:
            r = requests.get(url, headers=header)
        return r

    # 操作消息接口
    def op_notice(self, key, method, header, param={}):
        """
        通知查看、清空、已读操作
        :param key: r系统通知,like点赞，share转发，comment评论
        :param header:
        :param param:
        :return:
        """
        url_dict = {
            'r': '/notice/r',
            'like': '/notice/like',
            'share': '/notice/share',
            'comment': '/notice/comment',
        }
        url = self.get_baseurl + url_dict[key]
        if method == 'get':    # 查看通知
            if 'param' in param.keys():
                r = requests.get(url, params=param, headers=header)
            else:
                r = requests.get(url, headers=header)
        elif method == 'put':    # 标记通知为已读
            if 'lastReadAt' in param.keys():
                r = requests.put(url, json=param, headers=header)
            else:
                r = requests.put(url, headers=header)
        elif method == 'delete':    # 清空通知列表
                r = requests.delete(url, headers=header)
        else:
            raise ValueError("METHOD ERROR! MUST BE GET or PUT or DELETE")
        return r

    def get_unread(self, key, header):
        """
        获取未读通知
        :param key: unread未读消息，r系统通知,like点赞，share转发，comment评论
        :param header:
        :param param:
        :return:
        """
        url_dict = {
            'unread': '/notice/unread_count',
            'r': '/notice/r/unread_count',
            'like': '/notice/like/unread_count',
            'share': '/notice/share/unread_count',
            'comment': '/notice/comment/unread_count',
        }
        url = self.get_baseurl + url_dict[key]
        r = requests.get(url, headers=header)
        return r

    # def song_popularity(self):
    #
    #     popularity = share * 3 + collect * 2 + listen * 3 + praise + comment * 2
    #     return popularity
























