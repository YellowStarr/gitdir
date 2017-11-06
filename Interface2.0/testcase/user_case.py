# -*-coding=utf-8 -*-
"""
登陆部分测试用例，对应testcase中login。测试每个用例的响应结果会写到数据库中login_case表中对应的case_no中的response中
"""
from API2 import API2
import unittest, time
from dbManual import DBManual
from tool import tool
from errorCodeConst import errorCodeConst
from config import runconfig
import base64


class user_case:
    def __init__(self, islocal=0):
        self.api = API2(islocal)
        self.casedb = DBManual(islocal)
        self.sql = """update user_case set args=%s, response= %s,result= %s,test_time= %s WHERE case_no = %s"""
        self.t = tool()
        # self.deviceid = "c37c6b3c-10cc-411d-abfe-200135522e6d"
        self.login_param, self.deviceid = runconfig.RunConfig().get_login(islocal)
        self.t.get_login_header(self.api, self.deviceid, self.login_param)
        self.ecode = errorCodeConst()

    def test_01_user_info(self):    # 获取用户信息
        case_no = 1
        cur = self.casedb.connect_casedb()

        header = self.t.get_header
        uid = self.t.get_login_id
        response = self.api.get_user_info(uid, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)
        self.casedb.closeDB(cur)

    def test_28_user_info_unlogin(self):
        case_no = 28
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        response = self.api.get_user_info('6301346050607153160', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST)
        self.casedb.closeDB(cur)

    def test_02_my_info(self):    # 获取用户信息
        case_no = 2
        cur = self.casedb.connect_casedb()

        header = self.t.get_header
        response = self.api.get_my_info(header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql)
        self.casedb.closeDB(cur)

    def test_03_my_info_unlogin(self):    # 获取用户信息
        case_no = 3
        cur = self.casedb.connect_casedb()

        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        response = self.api.get_my_info(header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100201)
        self.casedb.closeDB(cur)

    def test_04_modify_my_info(self):
        case_no = 4
        cur = self.casedb.connect_casedb()

        header = self.t.get_header
        param = {
            "userName": "yaokun",
            "avatar": "", "email":
            "qiuwenjing@tuyabeat.com",
            "sex": 1,
            "birthday": "1990-09-16",
            "emotionStatus": 2,
            "personalProfile": "",
            "backgroundImageUrl": "http://www.baidu.com"
        }
        response = self.api.modify_my_info(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_05_modify_setting(self):
        case_no = 5
        cur = self.casedb.connect_casedb()

        header = self.t.get_header

        param = {"commentBoardPrivacySettings": 1, "pushLikeNoticeSettings": 1}

        response = self.api.op_settings('patch', header, params=param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_06_modify_setting_wrong_value(self):    # 获取用户信息
        case_no = 6
        cur = self.casedb.connect_casedb()

        header = self.t.get_header

        param = {"commentBoardPrivacySettings": 2, "pushSystemNoticeSettings": 0}
        response = self.api.op_settings('patch', header, params=param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100103, param)
        self.casedb.closeDB(cur)

    '''def test_07_modify_setting_NaN(self):    #
        case_no = 7
        cur = self.casedb.connect_casedb()

        header = self.t.get_header

        param = {"commentBoardPrivacySettings": "a"}
        response = self.api.op_settings('patch', header, params=param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql)
        self.casedb.closeDB(cur)'''

    def test_08_get_setting(self):    # 获取用户信息
        case_no = 8
        cur = self.casedb.connect_casedb()

        header = self.t.get_header
        response = self.api.op_settings('get', header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)
        self.casedb.closeDB(cur)

    def test_09_focus(self):    # 关注用户
        case_no = 9
        cur = self.casedb.connect_casedb()
        uid = '6311841386878468166'

        header = self.t.get_header

        response = self.api.op_focus('put', uid, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, uid)
        self.casedb.closeDB(cur)

    def test_10_focus_list(self):    # 关注用户列表
        case_no = 10
        cur = self.casedb.connect_casedb()
        uid = '6302709656942805004'

        header = self.t.get_header

        response = self.api.op_focus('get', uid, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, uid)
        # cur.close()
        self.casedb.closeDB(cur)

    def test_11_focus_again(self):
        """
        重复关注用户
        :return:
        """
        case_no = 11
        cur = self.casedb.connect_casedb()
        uid = '6302709656942805004'

        header = self.t.get_header

        response = self.api.op_focus('put', uid, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql)
        self.casedb.closeDB(cur)

    def test_12_fans_list(self):    # 粉丝列表
        case_no = 12
        cur = self.casedb.connect_casedb()
        uid = self.t.get_login_id

        header = self.t.get_header

        response = self.api.get_fans_list(uid, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql)
        self.casedb.closeDB(cur)

    def test_13_unfocus(self):    # 取消关注
        case_no = 13
        cur = self.casedb.connect_casedb()
        uid = '6302709656942805004'

        header = self.t.get_header

        response = self.api.op_focus('delete', uid, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql)
        self.casedb.closeDB(cur)

    def test_14_unfocus_unknown(self):
        """
        取消关注未关注用户
        :return:
        """
        case_no = 14
        cur = self.casedb.connect_casedb()
        uid = '6301346047952158727'

        header = self.t.get_header

        response = self.api.op_focus('delete', uid, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql)
        # cur.close()
        self.casedb.closeDB(cur)

    def test_15_blacklist(self):
        case_no = 15
        cur = self.casedb.connect_casedb()
        uid = '6298101404421974110'

        header = self.t.get_header

        response = self.api.op_blacklist('put', header, uid)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, uid)
        # cur.close()
        self.casedb.closeDB(cur)

    def test_16_blacklist_again(self):
        case_no = 16
        cur = self.casedb.connect_casedb()
        uid = '6298101404421974110'

        header = self.t.get_header

        response = self.api.op_blacklist('put', header, uid)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ALREADY_IN_BLACKLIST, uid)
        self.casedb.closeDB(cur)

    def test_17_blacklist_list(self):
        case_no = 17
        cur = self.casedb.connect_casedb()
        # uid = '6301346050607153160'

        header = self.t.get_header

        response = self.api.op_blacklist('get', header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql)
        # cur.close()
        self.casedb.closeDB(cur)

    def test_18_unblacklist(self):
        """
        取消加黑
        :return:
        """
        case_no = 18
        cur = self.casedb.connect_casedb()
        uid = '6298101404421974110'

        header = self.t.get_header

        response = self.api.op_blacklist('delete', header, uid)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql)
        # cur.close()
        self.casedb.closeDB(cur)

    def test_19_banding_phone(self):
        case_no = 19
        cur = self.casedb.connect_casedb()
        third_param = {
            "thirdAuthToken": "weixintoken3",
            "thirdPlatformType": "weixin",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        header = self.t.get_login_header(self.api, self.deviceid, third_param)

        response = self.api.bind_phone_sms({"phoneNumber": "13036582900"}, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 0, {"phoneNumber": "13036582900"})
        self.casedb.closeDB(cur)

    def test_20_already_banding_phone(self):
        case_no = 20
        cur = self.casedb.connect_casedb()
        third_param = {
            "thirdAuthToken": "weixintoken3",
            "thirdPlatformType": "weixin",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        header = self.t.get_login_header(self.api, self.deviceid, third_param)

        response = self.api.bind_phone_sms({"phoneNumber": "18782943850"}, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 100401, third_param)
        self.casedb.closeDB(cur)

    def test_27_banding_weibo_again(self):
        """
        18782943857再次绑定微博平台的另一账号
        :return:
        """
        case_no = 27
        cur = self.casedb.connect_casedb()
        phone_param = {
            'phoneNumber': "18782943857",
            "password": "88888888+./88888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        header = self.t.get_login_header(self.api, self.deviceid, phone_param)

        param = {
            "thirdAuthToken": "banding27",
            "thirdAccountName": "machineid wrong",
            "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
            "thirdPlatformType": "weibo",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }

        response = self.api.bind_third('weibo', param, header)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 100407, param)
        self.casedb.closeDB(cur)

    def test_29_modify_my_info(self):
        case_no = 29
        cur = self.casedb.connect_casedb()

        header = self.t.get_header
        param = {"userName": "qiuwjPhone"}
        response = self.api.modify_my_info(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_34_blacklist_unexist(self):
        """
        加黑不存在的用户
        :return:
        """
        case_no = 34
        cur = self.casedb.connect_casedb()
        uid = '6301346050607153161'

        header = self.t.get_header

        response = self.api.op_blacklist('put', header, uid)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100408, uid)
        # cur.close()
        self.casedb.closeDB(cur)

    def test_21_banding_phone_wrong_format(self):
        case_no = 21
        cur = self.casedb.connect_casedb()
        third_param = {
            "thirdAuthToken": "weixintoken3",
            "thirdPlatformType": "weixin",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        header = self.t.get_login_header(self.api, self.deviceid, third_param)

        response = self.api.bind_phone_sms({"phoneNumber": "1303658oe90"}, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 100103, third_param)
        self.casedb.closeDB(cur)

    def test_22_banding_phone_longer(self):
        case_no = 22
        cur = self.casedb.connect_casedb()
        third_param = {"thirdAuthToken": "weixintoken3", "thirdPlatformType": "weixin", "platform": "iOS",
                       "clientVersion": "2.0",
                       "machineId": 100001}
        header = self.t.get_login_header(self.api, self.deviceid, third_param)

        response = self.api.bind_phone_sms({"phoneNumber":"1303658291011"}, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 100103, third_param)
        self.casedb.closeDB(cur)

    def test_23_banding_phone(self, phoneNumber):
        case_no = 23
        cur = self.casedb.connect_casedb()
        # 第三方登陆账号
        third_param = {
            "thirdAuthToken": "weixintoken",
            "thirdPlatformType": "weixin",
            "platform": "iOS",
            "machineId": 100001
        }

        self.t.get_login_header(self.api, self.deviceid, third_param)
        header = self.t.get_header

        re = self.api.bind_phone_sms({"phoneNumber": phoneNumber}, header=header)
        assert re.status_code == 200, u"http响应错误，错误码 %s" % re.status_code
        data = re.json()

        param = {
            "phoneNumber": phoneNumber,
            "password": base64.b64encode("888888"),
            "platform": "iOS",
            "clientVersion": "2.0",
            "bindingPhoneNumberSmsCode": "0000",
            "bindingPhoneNumberSmsId": data['data']['bindingPhoneNumberSmsId']
        }

        response = self.api.bind_phone(param, header)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_24_banding_phone_again(self, phoneNumber):
        case_no = 24
        cur = self.casedb.connect_casedb()
        third_param = {
            "thirdAuthToken": "weixintoken",
            "thirdPlatformType": "weixin",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, third_param)
        header = self.t.get_header

        re = self.api.bind_phone_sms({"phoneNumber": phoneNumber}, header=header)
        assert re.status_code == 200, u"http响应错误，错误码 %s" % re.status_code
        data = re.json()

        param = {
            "phoneNumber": phoneNumber,
            "password": base64.b64encode("888888"),
            "platform": "iOS",
            "clientVersion": "2.0",
            "bindingPhoneNumberSmsCode": "0000",
            "bindingPhoneNumberSmsId": data['data']['bindingPhoneNumberSmsId']

        }

        response = self.api.bind_phone(param, header)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 100406, param)
        self.casedb.closeDB(cur)

    def test_25_banding_weibo(self):
        case_no = 25
        cur = self.casedb.connect_casedb()
        phone_param = {
            'phoneNumber': "13000000000",
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, phone_param)
        header = self.t.get_header

        param = {
            "thirdAuthToken": "banding3858",
            "thirdAccountName": "weibo3858",
            "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
            "thirdPlatformType": "weibo",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        response = self.api.bind_third('weibo', param, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_26_banding_qq_again(self):
        """
        18782943857再次绑定qq
        :return:
        """
        case_no = 26
        cur = self.casedb.connect_casedb()
        phone_param = {
            'phoneNumber': "13000000000",
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, phone_param)
        header = self.t.get_header

        param = {
            "thirdAuthToken": "weibotoken4",
            "thirdAccountName": "weibo4",
            "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
            "thirdPlatformType": "qq",
            "clientVersion": "2.0",
            "machineId": 100001
        }

        response = self.api.bind_third('qq', param, header)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 100401, param)
        self.casedb.closeDB(cur)

    def test_30_modify_sex_2(self):
        case_no = 30
        cur = self.casedb.connect_casedb()

        header = self.t.get_header
        param = {"sex": 3}
        response = self.api.modify_my_info(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100103, param)
        self.casedb.closeDB(cur)

    def test_31_modify_settings_unlogin(self):
        case_no = 31
        cur = self.casedb.connect_casedb()

        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"commentBoardPrivacySettings": 1, "pushLikeNoticeSettings": 1}
        response = self.api.op_settings('patch', header, params=param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100201, param)
        self.casedb.closeDB(cur)

    def test_32_focus_self(self):
        """
        关注自己
        :return:
        """
        case_no = 32
        cur = self.casedb.connect_casedb()

        header = self.t.get_header

        response = self.api.op_focus('put', '6299163298503852033', header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 200604)
        self.casedb.closeDB(cur)

    def test_33_focus_list_unlogin(self):  # 关注用户列表
        case_no = 33
        cur = self.casedb.connect_casedb()
        uid = '6302709656942805004'

        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")

        response = self.api.op_focus('get', uid, header=header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100201)
        self.casedb.closeDB(cur)

    def test_35_blacklist_self(self):
        case_no = 35
        cur = self.casedb.connect_casedb()
        uid = self.t.get_login_id

        header = self.t.get_header

        response = self.api.op_blacklist('put', header, uid)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 200605, uid)
        # cur.close()
        self.casedb.closeDB(cur)

    def test_binding_list(self):
        third_param = {
            "thirdAuthToken": "weibotoken4",
            "thirdPlatformType": "qq",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, third_param)
        header = self.t.get_header
        r = self.api.bind_list(header)
        print r.json()

    def test_delete_binding(self):
        third_param = {
            "thirdAuthToken": "weibotoken4",
            "thirdPlatformType": "qq",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, third_param)
        header = self.t.get_header
        r = self.api.delete_bind('qq', header)
        print r.text.decode('utf-8')
