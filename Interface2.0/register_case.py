# -*-coding=utf-8 -*-
"""测试数据的管理是个问题，应该存放在本地数据库，还是将数据写到excel？
另外需要保存的数据是 deviceId machineId userId 第三方登陆token 用户名。手机号，密码
测试阶段，验证码是0000.需要写数据库处理代码，去数据库拿数据对比，还是用unittest测试套件。要加email
用。先存本地数据库.返回数据还需要验证，json格式。期望值保存在数据库以json格式。还要考虑数据库设计"""

"""
注册部分测试用例，对应testcase中register.测试每个用例的响应结果会写到数据库中register_case表中对应的case_no中的response中
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

    def test_register_device(self):
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

    def test_register_device_same_machineid(self):
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

    def test_register_device_machineid_null(self):
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

    def test_register_device_lack_args(self):    # 设备注册machineId为空
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

    def test_register_device_platform_wrong(self):
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

    def test_register_weixin(self):
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

if __name__ == "__main__":
    unittest.main()

