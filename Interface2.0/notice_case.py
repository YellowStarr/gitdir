# -*-coding:utf-8 -*-

from API2 import API2
import time
from dbManual import DBManual
from tool import tool
import random
from errorCodeConst import errorCodeConst

class shown_case():
    def __init__(self):
        self.api = API2()
        self.casedb = DBManual()
        self.sql = """update interactive_case set args=%s,response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t = tool()
        self.deviceid = "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"
        login_param = {
            "phoneNumber": "18782943850",
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }

        self.login_param2 = {
            "phoneNumber": "18782943852",
            "password": "1234567",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, login_param)
        self.ecode = errorCodeConst()

    def test_01_unread_message_count(self):
        case_no = 1
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "unreadCount": {
                    "like": 0,
                    "r": 0,
                    "comment": 0,
                    "share": 0
                }
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.get_unread('unread', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_02_flag_notice(self):
        case_no = 2
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "lastReadAt": "2017-07-27 14:49:00"
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('r', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_03_flag_like(self):
        case_no = 3
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "lastReadAt": "2017-07-27 14:49:00"
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('like', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_04_flag_comment(self):
        case_no = 4
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "lastReadAt": "2017-07-27 14:49:00"
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('comment', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_05_flag_share(self):
        case_no = 5
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "lastReadAt": "2017-07-27 14:49:00"
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('share', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_06_clear_notice(self):
        case_no = 6
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "udpateTime": ""
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('r', 'delete', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_07_clear_comment(self):
        case_no = 7
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "udpateTime": ""
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('comment', 'delete', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_08_clear_like(self):
        case_no = 8
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "udpateTime": ""
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('like', 'delete', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_09_clear_share(self):
        case_no = 9
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "udpateTime": ""
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('share', 'delete', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_10_read_notice(self):
        case_no = 10
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "udpateTime": ""
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('r', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_12_read_comment(self):
        case_no = 12
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "userNotice": [
                    {
                        "content": "",
                        "createTime": "",
                        "noticeId": 0,
                        "unread": 1
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('comment', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_11_read_like(self):
        case_no = 11
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "userNotice": [
                    {
                        "content": "",
                        "createTime": "",
                        "noticeId": 0,
                        "unread": 1
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('like', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_13_read_share(self):
        case_no = 13
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "userNotice": [
                    {
                        "content": "",
                        "createTime": "",
                        "noticeId": 0,
                        "unread": 1
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('share', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_14_unread_r(self):
        case_no = 1
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "unreadCount": 0
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.get_unread('r', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_15_unread_comment(self):
        case_no = 15
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "unreadCount": 0
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.get_unread('comment', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_16_unread_like(self):
        case_no = 16
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "unreadCount": 0
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.get_unread('like', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_17_unread_share(self):
        case_no = 17
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "unreadCount": 0
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.get_unread('share', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)