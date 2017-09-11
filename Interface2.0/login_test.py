# -*-coding=utf-8 -*-
"""
登陆部分测试用例，对应testcase中login。测试每个用例的响应结果会写到数据库中login_case表中对应的case_no中的response中
待解决日志问题
"""

from API2 import API2
import unittest, time
import MySQLdb
import json, sys
from dbManual import DBManual
from tool import tool
import base64

class login_case():
    def __init__(self):
        self.api = API2()
        self.casedb = DBManual()
        self.t = tool()
        self.login_param = {
            "phoneNumber": "18782943850",
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.deviceId = "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"
        self.t.get_login_header(self.api, self.deviceId, self.login_param)
        self.sql = """update login_case set args=%s, response=%s,result=%s,test_time=%s WHERE case_no = %s"""

    def test_01_login_mobile(self):
        case_no = 1
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")

        response = self.api.mobile_login(self.login_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 0, self.login_param)
        self.casedb.closeDB(cur)

    def test_02_mobile_login_phone_wrong(self):
        case_no = 2
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {'phoneNumber': "18300000000", "password": "888888", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.mobile_login(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100402, param)
        self.casedb.closeDB(cur)

    def test_03_mobile_login_pwd_wrong(self):
        case_no = 3
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {'phoneNumber': "18782943850", "password": "123456", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.mobile_login(param, header)
        # http 响应码
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100404, param)
        self.casedb.closeDB(cur)

    def test_04_mobile_login_lack_args(self):
        case_no = 4
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {'phoneNumber': "18782943850", "password": "888888"}
        response = self.api.mobile_login(param, header)
        # http 响应码
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100105, param)
        self.casedb.closeDB(cur)

    def test_05_mobile_login_type_wrong(self):
        case_no = 5
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {'phoneNumber': 18782943850, "password": "888888", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.mobile_login(param, header)
        # http 响应码
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100102, param)
        self.casedb.closeDB(cur)

    def test_06_login_weixin(self):
        case_no = 6
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken": "weixin_token2", "thirdPlatformType": "weixin", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.third_login('weixin', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_07_login_weixin_token_wrong(self):
        case_no = 7
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"weixintoke","thirdPlatformType":"weixin","platform":"iOS",
                 "clientVersion":"2.0","machineId":100001}
        response = self.api.third_login('weixin', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100402, param)
        self.casedb.closeDB(cur)

    def test_08_login_weixin_lack_args(self):
        case_no = 8
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"weixintoke","thirdPlatformType":"weixin","machineId":100001}
        response = self.api.third_login('weixin', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100105, param)
        self.casedb.closeDB(cur)

    def test_09_login_qq(self):
        case_no = 9
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"qqtoken","thirdPlatformType":"qq","platform":"iOS","clientVersion":"2.0","machineId":100001}
        response = self.api.third_login('qq', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_10_login_qq_token_wrong(self):
        case_no = 10
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken": "qqtoke", "thirdPlatformType": "qq", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.third_login('qq', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100402, param)
        self.casedb.closeDB(cur)

    def test_11_login_qq_lack_args(self):
        case_no = 11
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken": "qqtoken","platform":"iOS","clientVersion":"2.0"}
        response = self.api.third_login('qq', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100105, param)
        self.casedb.closeDB(cur)

    def test_12_login_weibo(self):
        case_no = 12
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken": "weibotoken", "thirdPlatformType": "weibo", "platform": "iOS",
                 "clientVersion": "2.0","machineId": 100001}
        response = self.api.third_login('weibo', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_13_login_weibo_token_wrong(self):
        case_no = 13
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"weibotokn","thirdPlatformType":"qq","platform":"iOS",
                 "clientVersion":"2.0","machineId":100001}
        response = self.api.third_login('weibo', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100402, param)
        self.casedb.closeDB(cur)

    def test_14_login_weibo_lack_args(self):
        case_no = 14
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"weibotokn","thirdPlatformType":"weibo"}
        response = self.api.third_login('weibo', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100105, param)
        self.casedb.closeDB(cur)

    def test_15_device_login(self):
        case_no = 15
        cur = self.casedb.connect_casedb()
        # header = self.api.get_header({"deviceId": "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"})
        param = {"deviceId": "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb", "password": "", "platform": "iOS",
                 "clientVersion": "2.0"}
        response = self.api.device_login(param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_16_device_login_lack_args(self):
        case_no = 16
        cur = self.casedb.connect_casedb()
        # header = self.api.get_header({"deviceId": "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"})
        param = {"deviceId": "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"}
        response = self.api.device_login(param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100105, param)
        self.casedb.closeDB(cur)

    # 刷新token接口，需要去拿已登陆的用户的token。去本地数据库取response。前置条件为case_no 1 6 9 12 result=pass
    def test_17_refresh_token(self):
        case_no = 17

        # qq登陆
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken": "qqtoken", "thirdPlatformType": "qq", "platform": "iOS", "clientVersion": "2.0",
                 "machineId": 100001}
        response = self.api.third_login('qq', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        res = response.json()
        # 从返回json中获取token
        tokendic = res['data']['token']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb", accessToken=tokendic['accessToken'])
        param["refreshToken"] = tokendic['refreshToken']
        param['accessToken'] = tokendic['accessToken']

        response = self.api.refresh_token(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100404, param)
        self.casedb.closeDB(cur)

    def test_18_refresh_token_wrong(self):
        case_no = 18

        param = {"refreshToken": "", "accessToken": "", "platform": "iOS", "clientVersion": "2.0", "machineId": 100001}
        select_sql = """select response from login_case where case_no = 1 """
        #数据库取数据
        cur = self.casedb.connect_casedb()
        cur.execute(select_sql)
        re = cur.fetchone()
        res = eval(re[0])    # str数据转为dict
        tokendic = res['data']['token']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb",accessToken=tokendic['accessToken'])

        param["refreshToken"] = "dddddddddddddddddddddddddddd"
        param['accessToken'] = tokendic['accessToken']

        response = self.api.refresh_token(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100208, param)
        self.casedb.closeDB(cur)

    def test_19_access_token_wrong(self):
        case_no = 19
        param = {"refreshToken": "", "accessToken": "", "platform": "iOS", "clientVersion": "2.0", "machineId": 100001}
        select_sql = """select response from login_case where case_no = 1 """
        #数据库取数据
        cur = self.casedb.connect_casedb()
        cur.execute(select_sql)
        re = cur.fetchone()
        res = eval(re[0])    # str数据转为dict
        tokendic = res['data']['token']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb",accessToken=tokendic['accessToken'])

        param["refreshToken"] = tokendic['refreshToken']
        param['accessToken'] = "ddddddddddddddddddddddddddddddddddddddddd"

        response = self.api.refresh_token(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100208, param)
        self.casedb.closeDB(cur)

    def test_20_modify_pwd(self):
        case_no = 20

        select_sql = """select response from login_case where case_no = 1 """
        # 数据库取数据
        cur = self.casedb.connect_casedb()
        cur.execute(select_sql)
        re = cur.fetchone()
        res = eval(re[0])  # str数据转为dict
        tokendic = res['data']['token']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb", accessToken=tokendic['accessToken'])
        param = {"phoneNumber": "18782943850"}
        response = self.api.password_back_sms(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_21_logout(self):
        case_no = 21
        select_sql = """select response from login_case where case_no = 12 """
        # 数据库取数据
        cur = self.casedb.connect_casedb()
        header = self.t.get_login_header(self.api, self.deviceId, self.login_param)
        param = {"platform": "iOS", "machineId": 100001}
        response = self.api.login_out(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        self.casedb.closeDB(cur)

    def test_22_logout_lack_args(self):
        """
        退出登陆，缺少参数
        """
        case_no = 22
        # 数据库取数据
        cur = self.casedb.connect_casedb()

        header = self.t.get_header
        param = {"platform": "iOS"}
        response = self.api.login_out(param, header)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.t.error_handle(cur, case_no, response, t, self.sql, 100105, param)
        self.casedb.closeDB(cur)

    def test_23_logout_machineid_wrong(self):
        case_no = 23
        cur = self.casedb.connect_casedb()
        header = self.t.get_header

        param = {"platform": "iOS", "machineId": 1000100}
        response = self.api.login_out(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100209, param)
        self.casedb.closeDB(cur)

    def test_24_logout_unlogin(self):
        case_no = 24
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cur = self.casedb.connect_casedb()
        header = self.api.get_header()
        param = {"platform": "iOS", "machineId": 100001}
        print "[%s excuting case %s ] params: %s" % (t, 'test_24_logout_unlogin', param)
        response = self.api.login_out(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 100201, param)

        self.casedb.closeDB(cur)

    def test_25_login_machineId_not_match_deviceid(self):
        case_no = 25

        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"phoneNumber": "18782943852", "password": "888888", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 10001222}

        response = self.api.mobile_login(param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t.error_handle(cur, case_no, response, t, sql, 100410, param)
        self.casedb.closeDB(cur)

    def test_26_password_back_phone_has_letter(self):
        case_no = 26

        param = {
            "phoneNumber": "18782943852",
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_login_header(self.api, self.deviceId, param)

        response = self.api.password_back_sms({"phoneNumber":"18782943oz0"},header)

        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t.error_handle(cur, case_no, response, t, sql, 100401, {"phoneNumber":"18782943oz0"})
        self.casedb.closeDB(cur)

    def test_27_password_back_phone_length_longer(self):
        case_no = 27

        param = {
            "phoneNumber": "18782943852",
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_login_header(self.api, self.deviceId, param)

        response = self.api.password_back_sms({"phoneNumber": "1878294385200"},header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t.error_handle(cur, case_no, response, t, sql, 100401, {"phoneNumber": "1878294385200"})
        self.casedb.closeDB(cur)

    def test_28_password_back_phone(self):   # 密码修改成功后，查看是否是登陆状态
        case_no = 28

        param = {
            "phoneNumber": "18782943852",
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_login_header(self.api, self.deviceId, param)

        res = self.api.password_back_sms({"phoneNumber": "18782943852"}, header)
        assert res.status_code == 200, u"http响应错误，错误码 %s" % res.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        pwd = base64.b64encode("1234567")
        data = res.json()
        pwd_param = {
            "phoneNumber": "18782943852",
            "password": pwd,
            "platform": "iOS",
            "clientVersion": "2.0",
            "retrievalPasswordSmsCode": "0000",
            "retrievalPasswordSmsCode": "0000",
            "retrievalPasswordSmsId": ""
        }
        pwd_param['retrievalPasswordSmsId'] = data['data']['retrievalPasswordSmsId']
        response = self.api.password_back(pwd_param, header)
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t.error_handle(cur, case_no, response, t, sql, 0, pwd_param)
        self.casedb.closeDB(cur)

    def test_29_third_modify_pwd_with_no_banding(self):
        case_no = 29

        param = {
            "thirdAuthToken": "qqtoken",
            "thirdPlatformType": "qq",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": "100001"
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header()

        response = self.api.password_back_sms({"phoneNumber": "18782943700"}, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t.error_handle(cur, case_no, response, t, sql, 100401, {"phoneNumber": "18782943700"})
        self.casedb.closeDB(cur)

if __name__ == "__main__":
    # unittest.main()
    test = login_case()
    test.test_23_logout_machineid_wrong()
    test.test_22_logout_lack_args()
    # test.test_06_login_weixin()








