# -*-coding=utf-8 -*-
"""
登陆部分测试用例，对应testcase中login。测试每个用例的响应结果会写到数据库中login_case表中对应的case_no中的response中
"""

from API2 import API2
import unittest, time
import MySQLdb
import json, logging
from dbManual import DBManual


class user_case(unittest.TestCase):
    def setUp(self):
        self.api = API2()
        self.casedb = DBManual()
        self.sql = """update user_case set response=%s,result=%s,test_time=%s WHERE case_no = %s"""

    def test_01_user_info(self):    # 获取用户信息
       # print "[%s testing :%s]" % (time.strftime("%Y-%m-%d %H:%M:%S"), 'test_01_user_info')
        case_no = 1
        cur = self.casedb.connect_casedb()
        select_sql = """select args from user_case where case_no =%s"""
        cur.execute(select_sql, case_no)
        pa = cur.fetchone()
        param = eval(pa[0])
        userid = param['userid']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb")
        param = {"thirdAuthToken": "weiboton", "thirdPlatformType": "weibo", "platform": "iOS",
                 "clientVersion": "2.0", "machineId": 100001}
        wblg = self.api.third_login('weibo', param, header)
        temp = wblg.json()
        temp = json.dumps(temp, ensure_ascii=False)

        token = temp['data']['token']['accessToken']
        header = self.api.get_header(deviceId="34e7a55f-8fb9-4511-b1b7-55d6148fa9bb", accessToken=token)
        response = self.api.get_user_info(userid, header)
        self.assertEqual(response.status_code, 200, u"http响应错误，错误码 %s" % response.status_code)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.assertEqual(data["errorCode"], 1, u"错误信息: %s" % data['message'])
                try:
                    cur.execute(self.sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                cur.execute(self.sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(self.sql, (data, "fail", t, case_no))
        # cur.close()
        self.casedb.closeDB(cur)







if __name__ == "__main__":
    unittest.main()








