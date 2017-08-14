# -*-coding=utf-8 -*-
"""
注册部分测试用例，对应testcase中register.测试每个用例的响应结果会写到数据库中register_case表中对应的case_no中的response中
1. 长度错误，错误码未定义
"""
    
from API2 import API2
import unittest, time
import MySQLdb
import json,logging
from dbManual import DBManual

class register_case(unittest.TestCase):
    def setUp(self):
        self.api = API2()
        self.casedb = DBManual()

    ''''def test_register_device(self):    # 设备注册正向验证
        case_no = 1
        cur = self.casedb.connect_casedb()
        param = {"machineId": "10000003", "password": "", "platform": "iOS", "clientVersion": "2.0"}
        response = self.api.device_register(param)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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

    def test_register_device_same_machineid(self):    # 同一个machineId再次注册
        case_no = 2
        cur = self.casedb.connect_casedb()
        param = {"machineId": "10000003", "password": "", "platform": "iOS", "clientVersion": "2.0"}
        response = self.api.device_register(param)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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

    def test_register_device_machineid_null(self):    # machineId为空，不能注册成功
        case_no = 3
        cur = self.casedb.connect_casedb()
        param = {"machineId": "", "password": "", "platform": "iOS", "clientVersion": "2.0"}
        response = self.api.device_register(param)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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

    def test_register_device_lack_args(self):    # 设备注册缺少参数
        case_no = 4
        cur = self.casedb.connect_casedb()
        param = {"machineId": ""}
        response = self.api.device_register(param)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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

    def test_register_device_platform_wrong(self):    #设备注册 platform取值错误
        case_no = 5
        cur = self.casedb.connect_casedb()
        param = {"machineId": "10000004", "password": "", "platform": "iOOS", "clientVersion": "2.0"}
        #insql = """insert into register_case (case_no,args,url) values (3,%s,%s)"""
        response = self.api.device_register(param)
       # cur.execute(in_sql,(param,response.url))
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100103, u"错误信息: %s" % data['message'])
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

    def test_register_weixin(self):    # 微信住注册，注册需要使用deviceID。machineID与deviceID必须一致
        case_no = 6
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 2"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        param = {"thirdAuthToken": "weixintoken3", "thirdAccoutName": "weixinq",
                 "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
                 "thirdPlatformType": "weixin", "platform": "iOS", "clientVersion": "2.0"}
        response = self.api.third_register('weixin', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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

    def test_register_weibo(self):
        case_no = 7
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 1"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        param = {"thirdAuthToken": "weibotoken3", "thirdAccoutName": "weibo3",
                 "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
                 "thirdPlatformType": "weibo", "platform": "iOS", "clientVersion": "2.0"}
        response = self.api.third_register('weibo', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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

    def test_register_qq(self):
        case_no = 8
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 1"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        param = {"thirdAuthToken": "addmachienId", "thirdAccoutName": "qq3",
                 "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
                 "thirdPlatformType": "qq", "platform": "iOS", "clientVersion": "2.0", "machineId": 10000003}
        response = self.api.third_register('qq', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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

    def test_register_weixin_duplicate(self):
        case_no = 9
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 2"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        param = {"thirdAuthToken": "weixintoken3", "thirdAccoutName": "weixinq",
                 "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
                 "thirdPlatformType": "weixin", "platform": "iOS", "clientVersion": "2.0"}
        response = self.api.third_register('weixin', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100401, u"错误信息: %s" % data['message'])
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

    def test_register_weibo_duplicate(self):
        case_no = 10
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 1"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        param = {"thirdAuthToken": "weibotoken3", "thirdAccoutName": "weibo3",
                 "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
                 "thirdPlatformType": "weibo", "platform": "iOS", "clientVersion": "2.0"}
        response = self.api.third_register('weibo', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100401, u"错误信息: %s" % data['message'])
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

    def test_register_qq_duplicate(self):
        case_no = 11
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 1"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        param = {"thirdAuthToken": "qqtoken3", "thirdAccoutName": "qq3",
                 "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
                 "thirdPlatformType": "qq", "platform": "iOS", "clientVersion": "2.0"}
        response = self.api.third_register('qq', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100401, u"错误信息: %s" % data['message'])
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

    def test_register_weixin_platform_null(self):
        case_no = 12
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 1"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        param = {"thirdAuthToken": "weixintoken3", "thirdAccoutName": "weixinq",
                 "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
                 "thirdPlatformType": "weixin", "platform": "", "clientVersion": "2.0"}
        response = self.api.third_register('weixin', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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

    def test_register_qq_more_args(self):    # 多了参数不做控制
        case_no = 13
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 1"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        param = {"thirdAuthToken": "addmachienId_1", "thirdAccoutName": "qq_1",
                 "avatarUrl": "http://imgsrc.baidu.com/imgad/pic/item/267f9e2f07082838b5168c32b299a9014c08f1f9.jpg",
                 "thirdPlatformType": "qq", "platform": "iOS", "clientVersion": "2.0", "machineId": 10000003}
        response = self.api.third_register('qq', param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()

            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100101, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')

            cur.execute(sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)

    def test_mobile_register(self):    # 先发送注册短信验证码，再注册手机
        sms_id = 19    # 用例中短信接口的id
        phone_id =20   # 手机接口的id
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 1"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        sms_param = {"phoneNumber": 18782943852}
        phone_param = {"phoneNumber": "18782943852", "password": "888888", "platform": "iOS", "clientVersion":"2.0",
                       "registerSmsCode": "0000", "registerSmsId": ""}
        response = self.api.mobile_sms(sms_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE id = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, sms_id))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, sms_id))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, sms_id))

        registerSmsId = data['data']['registerSmsId']
        phone_param['registerSmsId'] = registerSmsId
        response = self.api.mobile_register(phone_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, phone_id))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, phone_id))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, phone_id))
        self.casedb.closeDB(cur)

    def test_mobile_register_verify_code(self):  #
        case_no = 18
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 2"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        sms_param = {"phoneNumber": "18782943854"}
        response = self.api.mobile_sms(sms_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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
                print data['message']
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_mobile_register_wrong_number(self):  # 手机格式错误
        case_no = 15  # 用例中短信接口的id
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 1"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        sms_param = {"phoneNumber": "187829438dd"}
        response = self.api.mobile_sms(sms_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100102, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_mobile_register_wrong_veryfy_code(self):  # 验证码错误
        case_no = 16  # 手机接口的id case_no:16
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 1"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        sms_param = {"phoneNumber": "18782943853"}
        phone_param = {"phoneNumber": "18782943853", "password": "888888", "platform": "iOS",
                       "clientVersion": "2.0", "registerSmsCode": "0001", "registerSmsId": ""}
        response = self.api.mobile_sms(sms_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])


        registerSmsId = data['data']['registerSmsId']
        phone_param['registerSmsId'] = registerSmsId
        response = self.api.mobile_register(phone_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100103, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_mobile_register_wrong_smsid(self):  # smsmid错误
        case_no = 17
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 2"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        sms_param = {"phoneNumber": "18782943854"}
        phone_param = {"phoneNumber": "18782943854", "password": "888888", "platform": "iOS", "clientVersion":"2.0",
                       "registerSmsCode":"0000", "registerSmsId": "4F2D6B7CFEFA6D2C-1-15DDEE42868-200000028"}
        response = self.api.mobile_sms(sms_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        # t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.assertEqual(data["errorCode"], 0, u"错误信息: %s" % data['message'])

        response = self.api.mobile_register(phone_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100103, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)'''

    def test_mobile_register_phone_length_shorter(self):  #
        case_no = 19
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 2"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        sms_param = {"phoneNumber":"1878294381"}
        response = self.api.mobile_sms(sms_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100108, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_mobile_register_password_length_shorter(self):  #
        case_no = 20
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 2"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        sms_param = {"phoneNumber":"18782943855"}
        response = self.api.mobile_sms(sms_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        sms_data = response.json()
        # t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        phone_param = {"phoneNumber": "18782943855", "password": "88888", "platform": "iOS", "clientVersion": "2.0",
                       "registerSmsCode": "0000", "registerSmsId": ""}
        registerSmsId = sms_data['data']['registerSmsId']
        phone_param['registerSmsId'] = registerSmsId
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        response = self.api.mobile_register(phone_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100108, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_mobile_register_password_length_longer(self):  #
        case_no = 21
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 2"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        sms_param = {"phoneNumber":"18782943856"}
        response = self.api.mobile_sms(sms_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        # t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        phone_param = {"phoneNumber":"18782943856","password":"88888888888888888","platform":"iOS",
                       "clientVersion":"2.0","registerSmsCode":"0000","registerSmsId":""}
        registerSmsId = response['data']['registerSmsId']
        phone_param['registerSmsId'] = registerSmsId
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        response = self.api.mobile_register(phone_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100108, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)

    def test_mobile_register_password_length(self):  #
        case_no = 22
        cur = self.casedb.connect_casedb()
        s = "select response from register_case where case_no = 2"
        cur.execute(s)
        dr = cur.fetchone()
        device = eval(dr[0])
        device_id = device['data']['deviceId']
        header = self.api.get_header(deviceId=device_id)
        sms_param = {"phoneNumber":"18782943857"}
        response = self.api.mobile_sms(sms_param, header)
        sms_data = response.json()
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)

        phone_param = {"phoneNumber":"18782943857","password":"88888888+./88888","platform":"iOS",
                       "clientVersion":"2.0","registerSmsCode":"0000","registerSmsId":""}
        registerSmsId = sms_data['data']['registerSmsId']
        phone_param['registerSmsId'] = registerSmsId
        sql = """update register_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        response = self.api.mobile_register(phone_param, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 100108, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                print data['message']
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(sql, (data, "fail", t, case_no))
        self.casedb.closeDB(cur)
if __name__ == "__main__":
    unittest.main()

