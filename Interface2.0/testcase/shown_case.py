# -*-coding:utf-8 -*-

from API2 import API2
import time
from dbManual import DBManual
from tool import tool
import random, json
from errorCodeConst import errorCodeConst

class shown_case():
    def __init__(self):
        self.api = API2()
        self.casedb = DBManual()
        self.sql = """update shown_case set args=%s,response=%s,result=%s,test_time=%s WHERE case_no = %s"""
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

    # 取数据库中args
    @staticmethod
    def select_args(cursor, case_no):
        _get_arg = 'select args from shown_case where case_no = %s'
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

    def test_01_recommend(self):
        case_no = 1

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "page": [
                    {
                        "type": "banner",
                        "data": [
                            {
                                "type": "xxx",
                                "image": "",
                                "url": "",
                                "bannerId": 0,
                                "name": "",
                                "createTime": "",
                                "updateTime": ""
                            }
                        ]
                    },
                    {
                        "type": "opus",
                        "data": [
                            {
                                "author": {
                                    "userId": 0,
                                    "userName": "",
                                    "avatar": ""
                                },
                                "type": "song",
                                "creativeType": "",
                                "songId": 0,
                                "songName": "",
                                "description": "",
                                "image": "",
                                "songUrl": "",
                                "songDuration": 0,
                                "listenCount": 0,
                                "collectCount": 0,
                                "commentCount": 0,
                                "shareCount": 0,
                                "likeCount": 0,
                                "createTime": "",
                                "recommendTime": "",
                                "recommendTags": [""],
                                "tags": [""],
                                "genre": ""  # 作品流派
                            }
                        ],
                        next: ""
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('recommend', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_02_recommend_page(self):
        case_no = 2

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        args = self.select_args(cur, case_no)
        response = self.api.shown_page('recommend', header, args)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, args)

        self.casedb.closeDB(cur)

    def test_03_recommend_no_next(self):
        case_no = 3

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('recommend', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_4_search_user(self):
        case_no = 4

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.search('user', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_5_search_user_partial(self):
        case_no = 5

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.search('user', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_6_search_opus(self):
        case_no = 6

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.search('opus', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_7_hot_search_opus_english(self):
        case_no = 7

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.search('opus', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_8_hot_page(self):
        case_no = 8
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "page": [
                    {
                        "type": "opus",
                        "data": [
                            {
                                "author": {
                                    "userId": 0,
                                    "userName": "",
                                    "avatar": ""
                                },
                                "type": "song",
                                "creativeType": "",
                                "songId": 0,
                                "songName": "",
                                "description": "",
                                "image": "",
                                "songUrl": "",
                                "songDuration": 0,
                                "listenCount": 0,
                                "collectCount": 0,
                                "commentCount": 0,
                                "shareCount": 0,
                                "likeCount": 0,
                                "createTime": "",
                                "recommendTime": "",
                                "recommendTags": [""],
                                "tags": [""],
                                "genre": "",
                                "comment": [{
                                    "commentText": "",
                                    "commentTime": "",
                                    "author": {
                                        "userId": 0,
                                        "userName": "",
                                        "avatar": ""
                                    },
                                    "likeCount": 0
                                }]
                            }
                        ]
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('hot', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_9_hot_page(self):
        case_no = 9

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('hot', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_10_hot_page(self):
        case_no = 10

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('hot', header, kw)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_11_hot_page(self):
        case_no = 11

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('hot', header, kw)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_12_hot_page(self):
        case_no = 12

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('hot', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_13_newest(self):
        case_no = 13
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "page": [
                    {
                        "type": "opus",
                        "data": [
                            {
                                "author": {
                                    "userId": 0,
                                    "userName": "",
                                    "avatar": ""
                                },
                                "type": "song",
                                "creativeType": "",
                                "songId": 0,
                                "songName": "",
                                "description": "",
                                "image": "",
                                "songUrl": "",
                                "songDuration": 0,
                                "listenCount": 0,
                                "collectCount": 0,
                                "commentCount": 0,
                                "shareCount": 0,
                                "likeCount": 0,
                                "createTime": "",
                                "recommendTime": "",
                                "recommendTags": [""],
                                "tags": [""],
                                "genre": "",
                                "comment": [{
                                    "commentText": "",
                                    "commentTime": "",
                                    "author": {
                                        "userId": 0,
                                        "userName": "",
                                        "avatar": ""
                                    },
                                    "likeCount": 0
                                }]
                            }
                        ]
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('newest', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_14_newest(self):
        case_no = 14

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('newest', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_15_newest(self):
        case_no = 15

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('newest', header, kw)
        # assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_16_newest(self):
        case_no = 16

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('newest', header, kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_17_newest(self):
        case_no = 17

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('newest', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_18_rank(self):
        case_no = 18
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "page": [
                    {
                        "type": "rankingDay",
                        "data": [
                            {
                                "author": {
                                    "userId": 0,
                                    "userName": "",
                                    "avatar": ""
                                },
                                "type": "song",
                                "creativeType": "",
                                "songId": 0,
                                "songName": "",
                                "description": "",
                                "image": "",
                                "songUrl": "",
                                "songDuration": 0,
                                "listenCount": 0,
                                "collectCount": 0,
                                "commentCount": 0,
                                "shareCount": 0,
                                "likeCount": 0,
                                "createTime": "",
                                "recommendTime": "",
                                "recommendTags": [""],
                                "tags": [""],
                                "genre": "",
                                "ranking": 0
                            }
                        ]
                    },
                    {
                        "type": "rankingWeek",
                        "data": [
                            {
                                "author": {
                                    "userId": 0,
                                    "userName": "",
                                    "avatar": ""
                                },
                                "type": "song",
                                "creativeType": "",
                                "songId": 0,
                                "songName": "",
                                "description": "",
                                "image": "",
                                "songUrl": "",
                                "songDuration": 0,
                                "listenCount": 0,
                                "collectCount": 0,
                                "commentCount": 0,
                                "shareCount": 0,
                                "likeCount": 0,
                                "createTime": "",
                                "recommendTime": "",
                                "recommendTags": [""],
                                "tags": [""],
                                "genre": "",
                                "ranking": 0
                            }
                        ]
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('ranking', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_19_rank(self):
        case_no = 19

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('ranking', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_20_rank(self):
        case_no = 20

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('ranking', header, kw)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_21_rank(self):
        case_no = 21

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('ranking', header, kw)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_22_rank(self):
        case_no = 22

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('ranking', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_23_musician(self):
        case_no = 23
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "user": [
                    {
                        "userId": 0,
                        "userName": "",
                        "avatar": "",
                        "ranking": 0,
                        "score": 0,
                        "gradeText": "",
                        "followerCount": 0,
                        "opusCount": "",
                        "scoutCount": 0,
                        "isFollowed": 0
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_24_musician(self):
        case_no = 24

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_25_musician(self):
        case_no = 25

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_26_musician(self):
        case_no = 26

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_27_musician(self):
        case_no = 27

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_28_musician(self):
        case_no = 28

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_29_musician(self):
        case_no = 29

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_30_musician(self):
        case_no = 30

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_31_musician(self):
        case_no = 31

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_32_musician(self):
        case_no = 32

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.shown_page('musician', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    '''def test_12_scout(self):
        case_no = 12
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "user": [
                    {
                        "userId": 0,
                        "userName": "",
                        "avatar": "",
                        "ranking": 0,
                        "score": 0,
                        "followerCount": 0,
                        "opusCount": "",
                        "scoutCount": 0,
                        "isFollowed": 0
                    }
                ]
            }
        }

        kw = {}
        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.shown_page('scout', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)'''

    def test_33_voilate(self):
        case_no = 33
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "sequence": ""
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_34_voilate_type_wrong(self):
        case_no = 34

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARG_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_35_voilate_text_null(self):
        case_no = 35

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, kw)

        self.casedb.closeDB(cur)

    def test_36_voilate_id_wrong(self):
        case_no = 36
        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.RECORD_UNEXIST, kw)

        self.casedb.closeDB(cur)

    def test_37_voilate_violateType_null(self):
        case_no = 37

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, kw)

        self.casedb.closeDB(cur)

    def test_38_feedback(self):
        case_no = 38
        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(1, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_39_feedback_contact(self):
        case_no = 39

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(1, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_40_feedback_content_null(self):
        case_no = 40
        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(1, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, kw)

        self.casedb.closeDB(cur)

    def test_41_search_user(self):
        case_no = 41

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "user": [
                    {
                        "userId": 0,
                        "userName": "",
                        "avatar": "",
                        "level": "",
                        "opusCount": 0
                    }
                ]
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.search('user', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_43_opus_detail_comment(self):
        case_no = 43

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        print kw
        response = self.api.get_song_detail(1, header, kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_44_opus_detail_comment(self):
        case_no = 44

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(1, header, kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_45_opus_detail_comment(self):
        case_no = 45

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(1, header, kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_46_opus_detail_comment(self):
        case_no = 46

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(1, header, kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_47_opus_detail_comment(self):
        case_no = 47

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(1, header, kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

        remote_cur = self.casedb.connect_remotedb()
        sql = """SELECT count(*) FROM opus_comment WHERE opus_id=%s AND id = opus_comment_id"""
        remote_cur.execute(sql, kw['opusid'])
        comments_tuple = remote_cur.fetchone()


    def test_48_opus_detail_comment(self):
        case_no = 48

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(1, header, kw)
        # assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_49_opus_detail_comment(self):
        case_no = 49

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(1, header, kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_50_opus_detail_comment(self):
        case_no = 50

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(1, header, kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_51_opus_detail_comment(self):
        case_no = 51

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(1, header, kw)
        # assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_52_voilate_song(self):
        case_no = 52
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "sequence": ""
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_53_voilate_comment(self):
        case_no = 53
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "sequence": ""
            }
        }

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.violate_feedback(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_55_hot_word(self):
        case_no = 55

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "keyword": [
                    {
                        "text": ""
                    }
                ]
            }
        }
        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.search('hot', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_42_opus_detail_comment(self):
        case_no = 42

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "comment": [
                {
                "commentId": 0,
                "createTime": "",
                "likeCount": 0,
                "replyCount": 0,
                "author": {
                    "userId": 0,
                    "userName": "",
                    "avatar": ""
                },
                "content": "",
                "status": 0,
                "isLiked": 0,                   # 是否已点赞,
                "reply": [
                    {
                        "commentId": 0,
                        "createTime": "",
                        "likeCount": 0,
                        "author": {
                            "userId": 0,
                            "userName": "",
                            "avatar": ""
                        },
                        "content": "",
                        "status": 0,
                        "isLiked": 0,
                        "replyTo": {
                            "author": {
                                "userId": 0,
                                "userName": "",
                                "avatar": ""
                            },
                            "commentId": 0,
                            "commentTime": "",
                            "content": "",
                            "likeCount": 0,
                            "status": 0
                        }
                    }
                ]
            }]
        }
        }
        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(1, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_57_hot_search_opus_english_partial(self):
        case_no = 57

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.search('opus', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_56_search_user_english_partial(self):
        case_no = 56

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.search('user', header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

'''if __name__ == "__main__":
    s = shown_case()
    # s.test_recomend_unlogin()
    # s.test_01_recommend()
    # s.test_02_recommend_page()
    # s.test_03_recommend_no_next()
    # s.test_4_search_user()
    # s.test_5_search_user_partial()
    # s.test_6_search_opus()
    # s.test_7_hot_search_opus_english()
    # s.test_8_hot_page()
    # s.test_9_hot_page()
    # s.test_10_hot_page()
    # s.test_11_hot_page()
    # s.test_12_hot_page()
    # s.test_13_newest()
    # s.test_14_newest()
    # s.test_15_newest()
    # s.test_16_newest()
    # s.test_17_newest()
    # s.test_18_rank()
    # s.test_19_rank()
    # s.test_20_rank()
    # s.test_21_rank()
    # s.test_22_rank()
    s.test_23_musician()
    # s.test_24_musician()
    # s.test_25_musician()
    # s.test_26_musician()
    # s.test_27_musician()
    # s.test_28_musician()
    # s.test_29_musician()
    # s.test_30_musician()
    # s.test_31_musician()
    # s.test_32_musician()
    # s.test_33_voilate()
    # s.test_34_voilate_type_wrong()
    # s.test_35_voilate_text_null()
    # s.test_36_voilate_id_wrong()
    # s.test_37_voilate_violateType_null()
    # s.test_38_feedback()
    # s.test_39_feedback_contact()
    # s.test_40_feedback_content_null()
    # s.test_41_search_user()
    # s.test_42_opus_detail_comment()
    # s.test_43_opus_detail_comment()
    # s.test_44_opus_detail_comment()
    # s.test_45_opus_detail_comment()
    # s.test_46_opus_detail_comment()
    # s.test_47_opus_detail_comment()
    # s.test_48_opus_detail_comment()
    # s.test_49_opus_detail_comment()
    # s.test_50_opus_detail_comment()
    # s.test_51_opus_detail_comment()
    # s.test_52_voilate_song()
    # s.test_53_voilate_comment()
    # s.test_55_hot_word()
    # s.test_56_search_user_english_partial()
    # s.test_57_hot_search_opus_english_partial()'''
