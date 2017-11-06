# -*-coding:utf-8 -*-

from API2 import API2
import time
from dbManual import DBManual
from tool import tool
import random
from errorCodeConst import errorCodeConst
from config import runconfig


class notice_case:
    def __init__(self, islocal=0):
        self.api = API2(islocal)
        self.casedb = DBManual()
        self.sql = """update notice_case set args=%s,response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t = tool()
        self.login_param, self.deviceid = runconfig.RunConfig().get_login(islocal)

        self.login_param2 = {
            "phoneNumber": "18782943852",
            "password": "1234567",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, self.login_param)
        self.ecode = errorCodeConst()

    # 取数据库中args
    @staticmethod
    def select_args(cursor, case_no):
        _get_arg = 'select args from notice_case where case_no = %s'
        cursor.execute(_get_arg, case_no)
        arg = cursor.fetchone()
        if arg[0] == '':
            return {}
        return eval(arg[0])

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

    def test_02_unread_message_count(self):
        case_no = 2

        header = self.api.get_header()

        cur = self.casedb.connect_casedb()
        response = self.api.get_unread('unread', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST)

        self.casedb.closeDB(cur)

    def test_03_flag_notice(self):
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
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_04_flag_notice(self):
        case_no = 4

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('r', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        self.casedb.closeDB(cur)

    def test_05_flag_notice(self):
        case_no = 5

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_06_flag_notice(self):
        case_no = 6

        header = self.api.get_header()

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)

        self.casedb.closeDB(cur)

    def test_07_flag_like(self):
        case_no = 7
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "lastReadAt": "2017-07-27 14:49:00"
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('like', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_08_flag_like(self):
        case_no = 8

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_notice('like', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        self.casedb.closeDB(cur)

    def test_09_flag_like(self):
        case_no = 9

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('like', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_10_flag_like(self):
        case_no = 10

        header = self.api.get_header()

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('like', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)

        self.casedb.closeDB(cur)

    def test_11_flag_comment(self):
        case_no = 11
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "lastReadAt": "2017-07-27 14:49:00"
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('comment', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_12_flag_comment(self):
        case_no = 12

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        # kw = self.select_args(cur, case_no)
        response = self.api.op_notice('comment', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        self.casedb.closeDB(cur)

    def test_13_flag_comment(self):
        case_no = 13

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('comment', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_14_flag_comment(self):
        case_no = 14

        header = self.api.get_header()

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('comment', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)

        self.casedb.closeDB(cur)

    def test_15_flag_share(self):
        case_no = 15
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "lastReadAt": "2017-07-27 14:49:00"
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('share', 'put', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_16_flag_share(self):
        case_no = 16

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        # kw = self.select_args(cur, case_no)
        response = self.api.op_notice('share', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        self.casedb.closeDB(cur)

    def test_17_flag_share(self):
        case_no = 17

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('share', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_18_flag_share(self):
        case_no = 18

        header = self.api.get_header()

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('share', 'put', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)

        self.casedb.closeDB(cur)

    def test_19_clear_notice(self):
        case_no = 19
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

    def test_20_clear_comment(self):
        case_no = 20
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "updateTime": ""
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

    def test_21_clear_like(self):
        case_no = 21
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "updateTime": ""
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

    def test_22_clear_share(self):
        case_no = 22
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "updateTime": ""
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

    def test_23_read_notice(self):
        case_no = 23
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "udpateTime": ""
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'get', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_24_read_notice(self):
        case_no = 24

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'get', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, kw)

        self.casedb.closeDB(cur)

    def test_25_read_notice(self):
        case_no = 25

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_26_read_notice(self):
        case_no = 26

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, kw)

        self.casedb.closeDB(cur)

    def test_27_read_notice(self):
        case_no = 27

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_28_read_notice(self):
        case_no = 28

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_29_read_notice(self):
        case_no = 29

        header = self.api.get_header()

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)

        self.casedb.closeDB(cur)

    def test_30_read_notice(self):
        case_no = 30

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_notice('r', 'get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_TYPE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_32_read_comment(self):
        case_no = 32
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

    def test_31_read_like(self):
        case_no = 31
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

    def test_33_read_share(self):
        case_no = 33
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

    def test_34_unread_r(self):
        case_no = 34
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

    def test_35_unread_comment(self):
        case_no = 35
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

    def test_36_unread_like(self):
        case_no = 36
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

    def test_37_unread_share(self):
        case_no = 37
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