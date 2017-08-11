# -*-coding=utf-8 -*-
"""
登陆部分测试用例，对应testcase中login。测试每个用例的响应结果会写到数据库中login_case表中对应的case_no中的response中
"""

from API2 import API2
import unittest, time
import MySQLdb
import json, logging
from dbManual import DBManual


class login_case(unittest.TestCase):
    def setUp(self):
        self.api = API2()
        self.casedb = DBManual()

    def test_01_login_mobile(self):
        case_no = 1
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"phoneNumber": "18782943850", "password": "888888", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.mobile_login(param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')

            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_02_mobile_login_phone_wrong(self):
        case_no = 2
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {'phoneNumber': "18300000000", "password": "888888", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.mobile_login(param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100402, u"错误信息: %s" % data['message'])

                try:
                    sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
                cur.execute(sql, (data, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            logging.info("返回值非json: %s")
            sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_03_mobile_login_pwd_wrong(self):
        case_no = 3
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {'phoneNumber': "18782943850", "password": "123456", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.mobile_login(param, header)
        # http 响应码
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            # errorCode错误码
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100404, u"错误信息: %s" % data['message'])

                try:
                    sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            logging.info("返回值非json: %s")
            sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_04_mobile_login_lack_args(self):
        case_no = 4
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {'phoneNumber': "18782943850", "password": "888888"}
        response = self.api.mobile_login(param, header)
        # http 响应码
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            # errorCode错误码
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100105, u"错误信息: %s" % data['message'])

                try:
                    sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            logging.info("返回值非json: %s")
            sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_05_mobile_login_type_wrong(self):
        case_no = 5
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {'phoneNumber': 18782943850, "password": "888888", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.mobile_login(param, header)
        # http 响应码
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            # errorCode错误码
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100102, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            logging.info("返回值非json: %s")
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_06_login_weixin(self):
        case_no = 6
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken": "weixintoken", "thirdPlatformType": "weixin", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        response = self.api.third_login('weixin', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_07_login_weixin_token_wrong(self):
        case_no = 7
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"weixintoke","thirdPlatformType":"weixin","platform":"iOS",
                 "clientVersion":"2.0","machineId":100001}
        response = self.api.third_login('weixin', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100402, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_08_login_weixin_lack_args(self):
        case_no = 8
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"weixintoke","thirdPlatformType":"weixin","machineId":100001}
        response = self.api.third_login('weixin', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100105, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            logging.info("返回值非json: %s")
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_09_login_qq(self):
        case_no = 9
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"qqtoken","thirdPlatformType":"qq","platform":"iOS","clientVersion":"2.0","machineId":100001}
        response = self.api.third_login('qq', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])
                try:

                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_10_login_qq_token_wrong(self):
        case_no = 10
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"qqtoke","thirdPlatformType":"qq","platform":"iOS",
                 "clientVersion":"2.0","machineId":100001}
        response = self.api.third_login('qq', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100402, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_11_login_qq_lack_args(self):
        case_no = 11
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken": "qqtoken","platform":"iOS","clientVersion":"2.0","machineId":100001}
        response = self.api.third_login('qq', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100105, u"错误信息: %s" % data['message'])
                try:

                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_12_login_weibo(self):
        case_no = 12
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"weibotoken","thirdPlatformType":"weibo","platform":"iOS",
                 "clientVersion":"2.0","machineId": 100001}
        response = self.api.third_login('weibo', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_13_login_weibo_token_wrong(self):
        case_no = 13
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"weibotokn","thirdPlatformType":"qq","platform":"iOS",
                 "clientVersion":"2.0","machineId":100001}
        response = self.api.third_login('weibo', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100402, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_14_login_weibo_lack_args(self):
        case_no = 14
        cur = self.casedb.connect_casedb()
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken":"weibotokn","thirdPlatformType":"weibo"}
        response = self.api.third_login('weibo', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100105, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')

            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_15_device_login(self):
        case_no = 15
        cur = self.casedb.connect_casedb()
        # header = self.api.get_header({"deviceId": "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"})
        param = {"deviceId":"34e7a55f-8fb9-4511-b1b7-55d6148fa9bb","password":"","platform":"iOS",
                 "clientVersion": "2.0"}
        response = self.api.device_login(param)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_16_device_login_lack_args(self):
        case_no = 16
        cur = self.casedb.connect_casedb()
        # header = self.api.get_header({"deviceId": "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"})
        param = {"deviceId": "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"}
        response = self.api.device_login(param)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100105, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')

            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    # 刷新token接口，需要去拿已登陆的用户的token。去本地数据库取response。前置条件为case_no 1 6 9 12 result=pass
    def test_17_refresh_token(self):
        case_no = 17
        param = {"refreshToken": "", "accessToken": "", "platform": "iOS", "clientVersion": "2.0", "machineId": 100001}
        select_sql = """select response from login_case where case_no = 1 """
        #数据库取数据
        cur = self.casedb.connect_casedb()
        cur.execute(select_sql)
        re = cur.fetchone()
        res = eval(re[0])    # str数据转为dict
        tokendic = res['data']['token']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb", accessToken=tokendic['accessToken'])
        param["refreshToken"] = tokendic['refreshToken']
        param['accessToken'] = tokendic['accessToken']

        response = self.api.refresh_token(param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])

                try:

                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            # data = unicode(response.text, 'utf-8')
            print "wrong"
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
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
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100208, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')

            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
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
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100208, u"错误信息: %s" % data['message'])

                try:

                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')

            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_20_modify_pwd(self):
        case_no = 20
        headerdic = {}
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
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            logging.info("返回值非json: %s")
            sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_21_logout(self):
        case_no = 21
        select_sql = """select response from login_case where case_no = 1 """
        # 数据库取数据
        cur = self.casedb.connect_casedb()
        cur.execute(select_sql)
        re = cur.fetchone()
        res = eval(re[0])  # str数据转为dict
        tokendic = res['data']['token']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb", accessToken=tokendic['accessToken'])
        param = {"platform": "iOS", "machineId": 100001}
        response = self.api.login_out(param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])

                try:

                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            # logging.info("返回值非json: %s")
            # sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
            cur.execute(sql, (data, "fail", t, case_no))

        self.casedb.closeDB(cur)

    def test_22_logout_lack_args(self):
        case_no = 22

        select_sql = """select response from login_case where case_no = 6 """
        # 数据库取数据
        cur = self.casedb.connect_casedb()
        cur.execute(select_sql)
        re = cur.fetchone()
        res = eval(re[0])  # str数据转为dict
        tokendic = res['data']['token']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb",accessToken=tokendic['accessToken'])
        param = {"platform": "iOS"}
        response = self.api.login_out(param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100207, u"错误信息: %s" % data['message'])

                try:

                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')

            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_23_logout_machineid_wrong(self):
        case_no = 23
        select_sql = """select response from login_case where case_no = 12 """
        # 数据库取数据
        cur = self.casedb.connect_casedb()
        cur.execute(select_sql)
        re = cur.fetchone()

        res = eval(re[0])  # str数据转为dict
        tokendic = res['data']['token']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb", accessToken=tokendic['accessToken'])
        param = {"platform": "iOS", "machineId":1000100}
        response = self.api.login_out(param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100207, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')

            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_24_logout_unlogin(self):
        case_no = 24
        cur = self.casedb.connect_casedb()
        header = self.api.get_header()
        param = {"platform": "iOS", "machineId": 100001}
        response = self.api.login_out(param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update login_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100207, u"错误信息: %s" % data['message'])

                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')

            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

if __name__ == "__main__":
    unittest.main()








