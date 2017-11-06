# -*-coding:utf-8 -*-

from API2 import API2
import time
from dbManual import DBManual
from tool import tool
import json
from errorCodeConst import errorCodeConst
from config import runconfig


class other_Case:

    def __init__(self, islocal=0):
        self.api = API2(islocal)
        self.casedb = DBManual()
        self.sql = """update other_case set args=%s,response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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
        _get_arg = 'select args from other_case where case_no = %s'
        cursor.execute(_get_arg, case_no)
        arg = cursor.fetchone()
        if arg[0] == '':
            return {}
        return eval(arg[0])

    def test_recomend_unlogin(self):
        kw = {}

        header = self.api.get_header()

        # cur = self.casedb.connect_casedb()
        response = self.api.shown_page('recommend', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            assert self.ecode.ACCESS_TOKEN_LOST == response.json()['errorCode']
        except AssertionError:
            print json.dumps(response.json(), ensure_ascii=False)

        # self.casedb.closeDB(cur)

    def test_01_ranking_friend(self):
        case_no = 1

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "friend": [
                    {
                        "userId": 0,
                        "userName": "",
                        "level": "",
                        "ranking": 0,
                        "avatar": ""
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('friend', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_02_ranking_friend(self):
        case_no = 2

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('friend', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, args)

        self.casedb.closeDB(cur)

    def test_03_ranking_friend(self):
        case_no = 3

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('friend', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, args)

        self.casedb.closeDB(cur)

    def test_04_ranking_friend(self):
        case_no = 4

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('friend', header, args)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, args)

        self.casedb.closeDB(cur)

    def test_05_ranking_friend(self):
        case_no = 5

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('friend', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, args)

        self.casedb.closeDB(cur)

    def test_06_ranking_friend(self):
        case_no = 6

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('friend', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, args)

        self.casedb.closeDB(cur)

    def test_07_ranking_friend(self):
        case_no = 7

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('friend', header, args)
        if response.status_code == 500:
            print u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, args)

        self.casedb.closeDB(cur)

    def test_08_ranking_friend(self):
        case_no = 8

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('friend', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, args)

        self.casedb.closeDB(cur)

    def test_09_ranking_fans(self):
        case_no = 9

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "friend": [
                    {
                        "userId": 0,
                        "userName": "",
                        "level": "",
                        "ranking": 0,
                        "avatar": ""
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('fans', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_10_ranking_fans(self):
        case_no = 10

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('fans', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, args)

        self.casedb.closeDB(cur)

    def test_11_ranking_fans(self):
        case_no = 11

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('fans', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, args)

        self.casedb.closeDB(cur)

    def test_12_ranking_fans(self):
        case_no = 12

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('fans', header, args)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, args)

        self.casedb.closeDB(cur)

    def test_13_ranking_fans(self):
        case_no = 13

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('fans', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, args)

        self.casedb.closeDB(cur)

    def test_14_ranking_fans(self):
        case_no = 14

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('fans', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, args)

        self.casedb.closeDB(cur)

    def test_15_ranking_fans(self):
        case_no = 15

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('fans', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, args)

        self.casedb.closeDB(cur)

    def test_16_ranking_fans(self):
        case_no = 16

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.ranking_friend_fans('fans', header, args)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, args)

        self.casedb.closeDB(cur)

    def test_17_scout_list(self):
        case_no = 17

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "user": [
                    {
                        "userId": 0,
                        "userName": "",
                        "avatar": ""
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.scout_list(header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_18_scout_list(self):
        case_no = 18

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.scout_list(header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_19_scout_list(self):
        case_no = 19

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.scout_list(header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, kw)

        self.casedb.closeDB(cur)

    def test_20_scout_list(self):
        case_no = 20

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.scout_list(header, kw)
        if response.status_code == 500:
            print u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_TYPE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_21_scout_list(self):
        case_no = 21

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.scout_list(header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_22_scout_list(self):
        case_no = 22

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.scout_list(header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_23_scout_list(self):
        case_no = 23

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.scout_list(header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_24_scout_list(self):
        case_no = 24

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.scout_list(header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_25_cancel_join_medley(self):
        case_no = 25

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "deleteTime": "",
                "currParticipantCount": 0,
                "maxParticipantCount": 0
            }
        }
        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_medley('delete', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_26_cancel_join_medley(self):
        case_no = 26

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_medley('delete', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.AUTH_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_27_cancel_join_medley(self):
        case_no = 27

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.op_medley('delete', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.AUTH_ERROR, kw)

        self.casedb.closeDB(cur)

