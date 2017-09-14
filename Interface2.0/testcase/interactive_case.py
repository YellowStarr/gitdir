# -*-coding:utf-8 -*-

from API2 import API2
import time
from dbManual import DBManual
from tool import tool
import random
from errorCodeConst import errorCodeConst

class interactive_case():
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

    # 取数据库中args
    @staticmethod
    def select_args(cursor, case_no):
        _get_arg = 'select args from interactive_case where case_no = %s'
        cursor.execute(_get_arg, case_no)
        arg = cursor.fetchone()
        if arg[0] == '':
            return {}
        return eval(arg[0])

    def test_01_song_comment(self):
        case_no = 1
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id, user_id from song_basic where creative_status=5 and public_status=1")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw = {}
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "commentId": 0,
                "commentCount": 0,
                "commentTime": ""
            }
        }

        kw['opusid'] = opus[0]
        kw['userid'] = opus[1]
        kw['param'] = {
            'content': u'发布歌曲评论正向验证'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'post', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_02_song_comment_with_pic(self):
        case_no = 2
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id, user_id from song_basic where creative_status=5 and public_status=1")
        result = remote_cur.fetchone()
        kw = {}
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "commentId": 0,
                "commentCount": 0,
                "commentTime": ""
            }
        }

        kw['opusid'] = result[0]
        kw['userid'] = result[1]
        kw['param'] = {
            # 'content': u'发布歌曲评论正向验证'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'post', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_03_song_comment_blacklist(self):
        case_no = 3
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id from song_basic where creative_status=5 and public_status=1 "
                           "and user_id = 6299163298503852033")
        result = remote_cur.fetchone()
        kw = {}

        kw['opusid'] = result[0]
        kw['userid'] = '6299163298503852033'
        kw['param'] = {
            'content': u'拉黑用户不可评论歌曲'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        # 用户param ={{"phoneNumber": "18782943852","password":"888888","platform":"iOS",
        # "clientVersion":"2.0","machineId":100001}
        uid ='6302709656942805004'
        blackuser_login = {"phoneNumber": "18782943852",
                           "password": "1234567",
                           "platform": "iOS",
                           "clientVersion": "2.0",
                           "machineId": 100001}
        self.api.op_blacklist('put', header, uid)    # 拉黑A

        self.t.get_login_header(self.api, self.deviceid, blackuser_login)    # A登录
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.op_comment('song', 'post', header, kwargs=kw)   # A评论B
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.AUTH_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_04_song_comment_unlogin(self):
        case_no = 4
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id, user_id from song_basic where creative_status=5 and public_status=1")
        result = remote_cur.fetchone()
        kw = {}

        kw['opusid'] = result[0]
        kw['userid'] = result[1]
        kw['param'] = {
            'content': u'拉黑用户不可评论歌曲'
        }
        self.casedb.closeDB(remote_cur)

        cur = self.casedb.connect_casedb()
        header = self.api.get_header()
        response = self.api.op_comment('song', 'post', header, kwargs=kw)   # A评论B
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)
        self.casedb.closeDB(cur)

    def test_05_song_comment_null(self):
        case_no = 5
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id, user_id from song_basic where creative_status=5 and public_status=1")
        result = remote_cur.fetchone()
        kw = {}

        kw['opusid'] = result[0]
        kw['userid'] = result[1]
        kw['param'] = {
            'content': ''
        }
        self.casedb.closeDB(remote_cur)

        cur = self.casedb.connect_casedb()
        header = self.api.get_header()
        response = self.api.op_comment('song', 'post', header, kwargs=kw)   # A评论B
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, kw)
        self.casedb.closeDB(cur)

    def test_06_song_comment_overflow(self):
        case_no = 6
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id, user_id from song_basic where creative_status=5 and public_status=1")
        result = remote_cur.fetchone()
        kw = {}

        kw['opusid'] = result[0]
        kw['userid'] = result[1]
        kw['param'] = {
            'content': '发评论，content超过140字1234567890abcdefghij1234567890abcdefghij1234567890abcdefghij1234567890abcdefghij1234567890abcdefghij1234567890abcdefghij1234567890abcdefghij1'
        }
        self.casedb.closeDB(remote_cur)

        cur = self.casedb.connect_casedb()
        header = self.api.get_header()
        response = self.api.op_comment('song', 'post', header, kwargs=kw)   # A评论B
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARG_LENGTH_ERROR, kw)
        self.casedb.closeDB(cur)

    def test_07_song_comment_opusid_unexist(self):
        case_no = 7
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select user_id from song_basic where creative_status=5 and public_status=1")
        result = remote_cur.fetchone()
        kw = {}

        kw['opusid'] = '1111111111266'
        kw['userid'] = result[0]
        kw['param'] = {
            'content': u'发布歌曲评论，歌曲id不存在'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'post', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_08_read_song_comments(self):
        case_no = 8
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id, user_id from song_basic where creative_status=5 and public_status=1")
        result = remote_cur.fetchone()
        kw = {}
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
                        "isLiked": 0
                    }
                ]
            }
        }

        kw['opusid'] = result[0]
        kw['userid'] = result[1]
        # kw['param'] = {
        #     'content': u'发布歌曲评论，歌曲id不存在'
        # }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_09_read_song_page(self):
        case_no = 9
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id, user_id from song_basic where creative_status=5 and public_status=1")
        result = remote_cur.fetchone()
        kw = {}
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
                        "isLiked": 0
                    }
                ]
            }
        }

        kw['opusid'] = result[0]
        kw['userid'] = result[1]
        kw['param'] = {
            'page': 2
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_10_blacklist_reply(self):
        case_no = 10
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id from song_basic where creative_status=5 and public_status=1 "
                           "and user_id = 6299163298503852033")
        result = remote_cur.fetchone()
        kw = {}
        kw['opusid'] = result[0]
        kw['userid'] = '6299163298503852033'

        remote_cur.execute("select opus_comment_id from opus_comment where delete_status = 0  and opus_id = %s", result[0])
        comment_id_tuple = remote_cur.fetchone()
        kw['commentid'] = comment_id_tuple[0]
        kw['param'] = {
            'content': u'拉黑用户不可回复评论歌曲'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        uid = '6302709656942805004'
        blackuser_login = {"phoneNumber": "18782943852",
                           "password": "1234567",
                           "platform": "iOS",
                           "clientVersion": "2.0",
                           "machineId": 100001}
        self.api.op_blacklist('put', header, uid)  # 拉黑A

        self.t.get_login_header(self.api, self.deviceid, blackuser_login)  # A登录
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.op_comment('comment', 'post', header, kwargs=kw)  # A评论B
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.AUTH_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_42_unblacklist_reply(self):
        case_no = 42
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id from song_basic where creative_status=5 and public_status=1 "
                           "and user_id = 6299163298503852033")
        result = remote_cur.fetchone()
        kw = {}
        kw['opusid'] = result[0]
        kw['userid'] = '6299163298503852033'

        remote_cur.execute("select opus_comment_id from opus_comment where delete_status = 0  and opus_id = %s", result[0])
        comment_id_tuple = remote_cur.fetchone()
        kw['commentid'] = comment_id_tuple[0]
        kw['param'] = {
            'content': u'解除拉黑，用户可回复评论歌曲'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        uid = '6302709656942805004'
        blackuser_login = {"phoneNumber": "18782943852",
                           "password": "1234567",
                           "platform": "iOS",
                           "clientVersion": "2.0",
                           "machineId": 100001}
        self.api.op_blacklist('delete', header, uid)  # 拉黑A

        self.t.get_login_header(self.api, self.deviceid, blackuser_login)  # A登录
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.op_comment('comment', 'post', header, kwargs=kw)  # A评论B
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_43_unblacklist_comment(self):
        case_no = 43
        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id from song_basic where creative_status=5 and public_status=1 "
                           "and user_id = 6299163298503852033")
        result = remote_cur.fetchone()
        kw = {}
        kw['opusid'] = result[0]
        kw['userid'] = '6299163298503852033'
        kw['param'] = {
            'content': u'解除拉黑，用户可回复评论歌曲'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        uid = '6302709656942805004'
        blackuser_login = {"phoneNumber": "18782943852",
                           "password": "1234567",
                           "platform": "iOS",
                           "clientVersion": "2.0",
                           "machineId": 100001}
        self.api.op_blacklist('delete', header, uid)  #

        self.t.get_login_header(self.api, self.deviceid, blackuser_login)  # A登录
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.op_comment('comment', 'post', header, kwargs=kw)  # A评论B
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_11_delete_comment_self(self):
        case_no = 11
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "commentCount": 0
            }
        }

        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select opus_id, id from opus_comment where delete_status = 0 and user_id= %s", uid)
        result = remote_cur.fetchone()
        kw = {}
        kw['opusid'] = result[0]
        kw['commentid'] = result[1]
        remote_cur.execute("select user_id from song_basic where id = %s", result[0])
        owner_id = remote_cur.fetchone()
        kw['userid'] = owner_id[0]
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'delete', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_12_delete_comment_others(self):
        case_no = 12
        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select opus_id, id from opus_comment where delete_status = 0 and user_id != %s", uid)
        result = remote_cur.fetchone()
        kw = {}
        kw['opusid'] = result[0]
        kw['commentid'] = result[1]
        remote_cur.execute("select user_id from song_basic where id = %s", result[0])
        owner_id = remote_cur.fetchone()
        kw['userid'] = owner_id[0]
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'delete', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.AUTH_ERROR, kw)
        self.casedb.closeDB(cur)

    def test_13_composer_delete_comment(self):
        case_no = 13
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "commentCount": 0
            }
        }

        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s", uid)
        res = remote_cur.fetchmany(n)
        # shuffle_r = random.shuffle(list(res))
        kw = {}
        flag = 0
        while (flag < len(res)):
            result = res[flag]
            num = remote_cur.execute("select id, user_id from opus_comment where delete_status = 0 and opus_id= %s", result[0])
            # result = random.choice(res)
            if num > 1:
                comment = remote_cur.fetchone()
                kw['opusid'] = result[0]
                kw['userid'] = comment[1]
                kw['commentid'] = comment[0]
                break
            flag = flag + 1
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'delete', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_14_composer_delete_comment_unexist(self):
        case_no = 14
        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select id from song_basic where user_id = %s", uid)
        result = remote_cur.fetchone()
        kw = {}
        kw['opusid'] = result[0]
        kw['userid'] = uid
        # remote_cur.execute("select id from opus_comment where delete_status = 0 and opus_id= %s", result[0])
        # owner_id = remote_cur.fetchone()
        kw['commentid'] = '635699998989855895'
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'delete', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.RECORD_UNEXIST, kw)

        self.casedb.closeDB(cur)

    def test_15_song_comment_reply(self):
        case_no = 15
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "commentId": "",
                "commentTime": ""
            }
        }
        #
        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id, opus_id, user_id from opus_comment where delete_status=0 GROUP BY (opus_comment_id)")
        result = remote_cur.fetchmany(n)
        a = random.choice(result)
        kw['commentid'] = a[0]
        kw['opusid'] = a[1]
        kw['userid'] = a[2]

        kw['param'] = {
            'content': u'发布歌曲评论回复正向验证'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('comment', 'post', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_16_song_comment_reply_pic(self):
        case_no = 16

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, opus_id, user_id from opus_comment where delete_status=0 GROUP BY (opus_comment_id)")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['opusid'] = opus[1]
        kw['userid'] = opus[2]

        kw['commentid'] = opus[0]

        kw['param'] = {
            'content': u'发布歌曲评论回复正向验证,http://ddfefe/pic'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('comment', 'post', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_18_read_replys(self):
        case_no = 18
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "comment": [
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
            }
        }

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select opus_id, opus_comment_id, user_id from opus_comment where delete_status=0 and reply_comment_id !=''")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['opusid'] = opus[0]
        kw['commentid'] = opus[1]
        kw['userid'] = opus[2]
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('comment', 'get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_20_delete_comment_has_children(self):
        case_no = 20
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "commentCount": 0
            }
        }

        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        remote_cur.execute("select opus_id, opus_comment_id from opus_comment where delete_status = 0 \
                           and reply_comment_id != '' and user_id= %s", uid)
        result = remote_cur.fetchone()
        kw = {}
        kw['opusid'] = result[0]
        kw['commentid'] = result[1]
        kw['userid'] = uid
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'delete', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    '''def test_21_read_comment_page(self):
        case_no =21

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, opus_id, user_id from opus_comment where delete_status=0 GROUP BY (opus_comment_id)")
        result = remote_cur.fetchmany(n)
        for i in xrange(len(result)):
            a = result[i]
            remote_cur.execute("select count(*) from opus_comment where opus_comment_id= %s", a[0])
            count = remote_cur.fetchone()
            if count[0] > 10:
                kw['commentid'] = a[0]
                kw['opusid'] = a[1]
                kw['userid'] = a[2]
                break
        kw['param'] = {
            'page': 1,
            'size': 10
        }
        remote_cur.execute("select user_id from song_basic where id = %s", kw['opusid'])
        userid = remote_cur.fetchone()
        kw['userid'] = userid[0]
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('song', 'get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_22_read_comment_page_turn(self):
        case_no =22

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, opus_id from opus_comment where delete_status=0 GROUP BY (opus_comment_id)")
        result = remote_cur.fetchmany(n)
        for i in xrange(len(result)):
            a = result[i]
            remote_cur.execute("select count(*) from opus_comment where opus_comment_id= %s", a[0])
            count = remote_cur.fetchone()
            if count[0] > 10:
                kw['commentid'] = a[0]
                kw['opusid'] = a[1]
                break
        kw['param'] = {
            'page': 1,
            'size': 10
        }
        remote_cur.execute("select user_id from song_basic where id = %s", kw['opusid'])
        userid = remote_cur.fetchone()
        kw['userid'] = userid[0]
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('comment', 'get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        kw['param'] = {
            'page': 2,
            'size': 10
        }
        response = self.api.op_comment('comment', 'get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)
        self.casedb.closeDB(cur)'''

    def test_23_song_comment_praise(self):
        case_no = 23
        kw = {}
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "likeCount": 0
            }
        }

        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id, opus_id, user_id from opus_comment where delete_status=0 GROUP BY (opus_comment_id)")
        result = remote_cur.fetchmany(n)
        a = random.choice(result)
        kw['commentid'] = a[0]
        kw['opusid'] = a[1]
        kw['userid'] = a[2]

        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_praise('comment', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_24_song_comment_praise_again(self):
        case_no = 24
        kw = {}
        uid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select comment_id, opus_id from opus_comment_like where user_id= %s", uid)
        result = remote_cur.fetchmany(n)
        a = random.choice(result)
        kw['commentid'] = a[0]
        kw['opusid'] = a[1]

        remote_cur.execute("select user_id from song_basic where id = %s", kw['opusid'])
        userid = remote_cur.fetchone()
        kw['userid'] = userid[0]

        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.op_praise('comment', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ALREADY_PRAISED, kw)

        self.casedb.closeDB(cur)

    def test_26_read_reply_page(self):
        case_no =26

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, opus_id, user_id from opus_comment where delete_status=0 GROUP BY (opus_comment_id)")
        result = remote_cur.fetchmany(n)
        for i in xrange(len(result)):
            a = result[i]
            remote_cur.execute("select count(*) from opus_comment where opus_comment_id= %s", a[0])
            count = remote_cur.fetchone()
            if count[0] > 10:
                kw['commentid'] = a[0]
                kw['opusid'] = a[1]
                kw['userid'] = a[2]
                break
        kw['param'] = {
            'page': 1,
            'size': 10
        }

        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('comment', 'get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_28_read_reply_page_turn(self):
        case_no =28

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, opus_id, user_id from opus_comment where delete_status=0 GROUP BY (opus_comment_id)")
        result = remote_cur.fetchmany(n)
        for i in xrange(len(result)):
            a = result[i]
            remote_cur.execute("select count(*) from opus_comment where opus_comment_id= %s", a[0])
            count = remote_cur.fetchone()
            if count[0] > 10:
                kw['commentid'] = a[0]
                kw['opusid'] = a[1]
                kw['userid'] = a[2]
                break
        kw['param'] = {
            'page': 1,
            'size': 10,
            'sort': 'hot'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_comment('comment', 'get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        kw['param'] = {
            'page': 2,
            'size': 10,
            'sort': 'hot'
        }
        response = self.api.op_comment('comment', 'get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)
        self.casedb.closeDB(cur)

    def test_29_list_self_unpublish_opus(self):
        case_no = 29
        # remote_cur = self.casedb.connect_remotedb()
        # remote_cur.execute("select from song_basic where creative_status=5 and public_status=1")
        # result = remote_cur.fetchone()
        kw = {}
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": [
                    {
                        "type": "song",
                        "songId": 0,
                        "genre": "",
                        "creativeType": "",
                        "createTime": "",
                        "creativeStatus": "",
                        "songName": "",
                        "author": {
                            "userId": 0,
                            "userName": "",
                            "avatar": ""
                        }
                    }
                ]
            }
        }
        param = {
            'page': 1
        }
        # self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_opus(1, header, 0, param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_30_list_self_publish_opus(self):
        case_no = 30
        # remote_cur = self.casedb.connect_remotedb()
        # remote_cur.execute("select from song_basic where creative_status=5 and public_status=1")
        # result = remote_cur.fetchone()
        kw = {}
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": [{
                    "type": "song",
                    "genre": "",
                    "creativeType": "",
                    "createTime": "",
                    "creativeStatus": "",
                    "rankingTag": [""],
                    "songId": 0,
                    "songName": "",
                    "image": "",
                    "description": "",
                    "songUrl": "",
                    "songDuration": 0,
                    "listenCount": 0,
                    "collectCount": 0,
                    "commentCount": 0,
                    "shareCount": 0,
                    "likeCount": 0,
                    "author": {
                        "userId": 0,
                        "userName": "",
                        "avatar": ""
                    },
                    "publishTime": "",
                    "maxParticipantCount": 0,
                    "currParticipantCount": 0
                }]
            }
        }
        param = {
            'page': 1,
            'size': 5
        }
        # self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_opus(1, header, 1, param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_31_listen_without_attach(self):
        case_no = 31
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "listenCount": 0
            }
        }

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, user_id from song_basic where creative_status=5 and public_status=1 and delete_status = 0")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            'listenDuration': 5
        }
        remote_cur.execute("select listen_count from song_attach where id = %s", opus[0])
        listen_count = remote_cur.fetchone()  # 获取原始
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.listen(header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        r = response.json()
        assert listen_count[0]+1 == r['data']['listenCount'], "The origin listen_count is:%s" % listen_count[0]
        self.casedb.closeDB(cur)

    def test_32_listen_without_attach_uncount(self):
        case_no = 32

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, user_id from song_basic where creative_status=5 and public_status=1 and delete_status = 0")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            'listenDuration': 4
        }
        remote_cur.execute("select listen_count from song_attach where id = %s", opus[0])
        listen_count = remote_cur.fetchone()    # 获取原始
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.listen(header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code

        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        r = response.json()
        assert listen_count[0] == r['data']['listenCount'], "'listen' data count wrong"
        self.casedb.closeDB(cur)

    def test_33_listen_format_error(self):
        case_no = 33

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, user_id from song_basic where creative_status=5 and public_status=1 and delete_status = 0")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            'listenDuration': 10.9
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.listen(header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_34_listen_opus_id_unexist(self):
        case_no = 34

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, user_id from song_basic where creative_status=5 and public_status=1 and delete_status = 0")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['userid'] = opus[1]
        kw['opusid'] = 623369899989845

        kw['param'] = {
            'listenDuration': 10
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.listen(header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.RECORD_UNEXIST, kw)

        self.casedb.closeDB(cur)

    def test_35_listen_opus_unlogin(self):
        case_no = 35

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, user_id from song_basic where creative_status=5 and public_status=1 and delete_status = 0")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            'listenDuration': 10
        }
        self.casedb.closeDB(remote_cur)

        header = self.api.get_header()
        cur = self.casedb.connect_casedb()
        response = self.api.listen(header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)

        self.casedb.closeDB(cur)

    def test_36_join_medley(self):
        case_no = 36

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "participant": {
                    "id": 0,
                    "order": 0,
                    "time": ""
                }
            }
        }
        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id from song_basic where creative_type = 4 and delete_status = 0 AND public_status = 1\
             and curr_participant_count < max_participant_count")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        # kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            "audio": {
                "url": "http://eeeeee",
                "duration": 10,
                "lyric": ""
            }
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_medley('post', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_37_join_medley_again(self):
        case_no = 37

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id from song_basic where creative_type = 4 and delete_status = 0 AND public_status = 1\
             and curr_participant_count < max_participant_count")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        # kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            "audio": {
                "url": "http://eeeeee",
                "duration": 10,
                "lyric": ""
            }
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        self.api.op_medley('post', header, kwargs=kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code

        kw['param'] = {
            "audio": {
                "url": "http://eeeeee",
                "duration": 26,
                "lyric": "look what you made me do"
            }
        }
        response = self.api.op_medley('post', header, kwargs=kw)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        self.casedb.closeDB(cur)

    def test_38_join_medley_full(self):
        case_no = 38

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id from song_basic where creative_type = 4 and delete_status = 0 AND public_status = 1\
             and curr_participant_count = max_participant_count")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        # kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            "audio": {
                "url": "http://eeeeee",
                "duration": 10,
                "lyric": ""
            }
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_medley('post', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.STATE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_39_join_medley_deleted(self):
        case_no = 39

        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id from song_basic where creative_type = 4 and delete_status = 1")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        # kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            "audio": {
                "url": "http://eeeeee",
                "duration": 10,
                "lyric": ""
            }
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_medley('post', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.STATE_ERROR, kw)

        self.casedb.closeDB(cur)

    def test_40_get_participantors(self):
        case_no = 40

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "participant": [
                    {
                        "author": {
                            "userId": 0,
                            "userName": "",
                            "avatar": "",
                        },
                        "isOwnner": 0,  # 是否是串烧的作者, 1代表是, 0代表不是
                        "createTime": "",
                        "audio": {
                            "url": "",
                            "duration": "",
                            "lyric": ""
                        },
                        "id": 0
                    }
                ],
                "currParticipantCount": 0,
                "maxParticipantCount": 0
            }
        }
        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id from song_basic where creative_type = 4 and delete_status = 0 AND public_status = 1")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        # kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        # kw['param'] = {
        #     "audio": {
        #         "url": "http://eeeeee",
        #         "duration": 10,
        #         "lyric": ""
        #     }
        # }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_medley('get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_41_get_participantors_unique(self):
        case_no = 41

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "participant": [
                    {
                        "author": {
                            "userId": 0,
                            "userName": "",
                            "avatar": "",
                        },
                        "isOwnner": 0,  # 是否是串烧的作者, 1代表是, 0代表不是
                        "createTime": "",
                        "audio": {
                            "url": "",
                            "duration": "",
                            "lyric": ""
                        },
                        "id": 0
                    }
                ],
                "currParticipantCount": 0,
                "maxParticipantCount": 0
            }
        }
        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id from song_basic where creative_type = 4 and delete_status = 0 AND public_status = 1 \
             and curr_participant_count>1")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        # kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            "unique": 1
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        response = self.api.op_medley('get', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_44_publish(self):
        case_no = 44

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "publishTime": ""
            }
        }
        param = {
            "description": u"发布作品描述信息",
            "image": "https://image.baidu.com",
            "songName": "发布作品",
            "lyric": u"东夏国，高丽，元朝"
        }

        header = self.t.get_header
        userid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s and delete_status=0 and creative_status= 5 and public_status=0", userid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        self.casedb.closeDB(remote_cur)

        response = self.api.opus_publish(opus[0], param, header)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_45_publish_desc_null(self):
        case_no = 45
        param = {
            "description": "",
            "image": "https://image.baidu.com",
            "songName": "发布作品",
            "lyric": u"东夏国，高丽，元朝"
        }

        header = self.t.get_header
        userid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s and delete_status=0 and creative_status= 5 and public_status=0", userid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        self.casedb.closeDB(remote_cur)

        response = self.api.opus_publish(opus[0], param, header)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)

        self.casedb.closeDB(cur)

    def test_46_publish_image_null(self):
        case_no = 46
        param = {
            "description": u"发布作品描述信息",
            "image": "",
            "songName": "发布作品",
            "lyric": u"东夏国，高丽，元朝"
        }

        header = self.t.get_header
        userid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s and delete_status=0 and creative_status= 5 and public_status=0", userid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        self.casedb.closeDB(remote_cur)

        response = self.api.opus_publish(opus[0], param, header)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_47_publish_songName_null(self):
        case_no = 47
        param = {
            "description": u"发布作品描述信息",
            "image": "https://image.baidu.com",
            "songName": "",
            "lyric": u"东夏国，高丽，元朝"
        }

        header = self.t.get_header
        userid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s and delete_status=0 and creative_status= 5 and public_status=0", userid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        self.casedb.closeDB(remote_cur)

        response = self.api.opus_publish(opus[0], param, header)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_48_publish_already_published(self):
        case_no = 48
        param = {
            "description": u"发布已发布作品描述信息",
            "image": "https://image.baidu.com",
            "songName": "发布作品",
            "lyric": u"东夏国，高丽，元朝"
        }

        header = self.t.get_header
        userid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s and delete_status=0 and creative_status= 5 and public_status = 1", userid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        self.casedb.closeDB(remote_cur)

        response = self.api.opus_publish(opus[0], param, header)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.STATE_ERROR, param)
        self.casedb.closeDB(cur)

    def test_49_delete_published_opus(self):
        case_no = 49

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "deleteTime": ""
            }
        }

        header = self.t.get_header
        userid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s and delete_status=0 and creative_status= 5 and public_status=1", userid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        self.casedb.closeDB(remote_cur)

        response = self.api.delete_opus(header, opus[0])

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_50_delete_unpublish_opus(self):
        case_no = 50
        header = self.t.get_header
        userid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s and delete_status=0 and public_status=0", userid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        self.casedb.closeDB(remote_cur)

        response = self.api.delete_opus(header, opus[0])

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)
        self.casedb.closeDB(cur)

    def test_51_publish_delete(self):
        case_no = 51

        param = {
            "description": u"发布作品描述信息",
            "image": "https://image.baidu.com",
            "songName": "发布作品",
            "lyric": u"东夏国，高丽，元朝"
        }
        header = self.t.get_header
        userid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s and delete_status=1", userid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        self.casedb.closeDB(remote_cur)

        response = self.api.opus_publish(opus[0], param, header)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.STATE_ERROR, param)

        self.casedb.closeDB(cur)

    def test_52_get_oss_image(self):
        case_no = 52
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "file": [
                    {
                        "type": "image",
                        "md5": "",
                        "name": "",
                        "extension": "",
                        "signedUrl": ""
                    }
                ]
            }
        }
        param = {
            "file": [
                {
                    "type": "image",
                    "md5": "sdfwfasdfwefasdfwef",
                    "name": "image1",
                    "extension": "jpg"
                }
            ]
        }
        header = self.t.get_header
        response = self.api.get_oss_url(header, param)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_53_get_oss_audio(self):
        case_no = 53
        param = {
            "file": [
                {
                    "type": "audio",
                    "md5": "sdfwfasdfwefasdfwef",
                    "name": "audio",
                    "extension": "mp3"
                }
            ]
        }
        header = self.t.get_header
        response = self.api.get_oss_url(header, param)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_54_get_oss_audio_md5_null(self):
        case_no = 54
        param = {
            "file": [
                {
                    "type": "audio",
                    "md5": "",
                    "name": "audio",
                    "extension": "mp3"
                }
            ]
        }
        header = self.t.get_header
        response = self.api.get_oss_url(header, param)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_55_get_oss_audio_name_null(self):
        case_no = 55
        param = {
            "file": [
                {
                    "type": "audio",
                    "md5": "sdfwfasdfwefasdfwef",
                    "name": "",
                    "extension": "mp3"
                }
            ]
        }
        header = self.t.get_header
        response = self.api.get_oss_url(header, param)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_56_get_oss_audio_name_null(self):
        case_no = 56
        param = {
            "file": [
                {
                    "type": "audio",
                    "md5": "sdfwfasdfwefasdfwef",
                    "name": "audio",
                    "extension": ""
                }
            ]
        }
        header = self.t.get_header
        response = self.api.get_oss_url(header, param)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_57_give_mark(self):
        case_no = 57
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "score": 0
            }
        }

        self.t.get_login_header(self.api, self.deviceid, self.login_param2)
        header = self.t.get_header
        uid = self.t.get_login_id
        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        # 获取作品id 作者id
        opusids = remote_cur.execute("select opus_id from opus_score where user_id=%s", uid)
        score_list = remote_cur.fetchmany(opusids)    # 获取当前登陆用户id已评分的作品id列表
        n = remote_cur.execute(
            "select id, user_id from song_basic where creative_status=5 and public_status=1 and delete_status = 0")
        result = remote_cur.fetchmany(n)
        # 将已评分过得作品剔除
        for i in score_list:
            if i in result[0]:
                a = result[0].index(i)
                result[0].pop(a)
        opus = random.choice(result)

        kw['userid'] = opus[1]
        kw['opusid'] = opus[0]
        kw['param'] = {
            'score': 5
        }
        self.casedb.closeDB(remote_cur)

        response = self.api.opus_score(header, kw)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)
        self.casedb.closeDB(cur)

    def test_58_give_mark_again(self):
        case_no = 58

        uid = self.t.get_login_id
        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, user_id from song_basic where creative_status=5 and public_status=1 and delete_status = 0 and user_id != %s", uid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            'score': 9.6
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        self.api.opus_score(header, kw)
        response = self.api.opus_score(header, kw)

        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.AUTH_ERROR, kw)
        self.casedb.closeDB(cur)

    def test_59_give_mark_score_negative(self):
        case_no = 59

        uid = self.t.get_login_id
        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, user_id from song_basic where creative_status=5 and public_status=1 and delete_status = 0 and user_id != %s", uid)
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        kw['param'] = {
            'score': -5
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        response = self.api.opus_score(header, kw)
        cur = self.casedb.connect_casedb()
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, kw)
        self.casedb.closeDB(cur)

    def test_25_song_detail(self):
        case_no = 25

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)
        self.casedb.closeDB(cur)

        rm = self.casedb.connect_remotedb()
        sql = """SELECT count(*) FROM opus_comment WHERE opus_id=%s"""
        rm.execute(sql, kw['opusid'])
        comments_tuple = rm.fetchone()
        self.casedb.closeDB(rm)

        r = response.json()
        if comments_tuple[0] != r['data']['opus']['commentCount']:
            print "commentCount not equal"

    def test_60_song_detail(self):
        case_no = 60

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)
        self.casedb.closeDB(cur)

        rm = self.casedb.connect_remotedb()
        sql = """SELECT create_time, public_time FROM song_basic WHERE id=%s"""
        rm.execute(sql, kw['opusid'])
        time_tuple = rm.fetchone()
        self.casedb.closeDB(rm)

        r = response.json()
        if time_tuple[0] != r['data']['opus']['createTime'] and time_tuple[1] != r['data']['opus']['publishTime']:
            print "time not equal"
            print "create time is %s , publish time is %s" % (time_tuple[0], time_tuple[1])

    def test_61_song_detail(self):
        case_no = 61

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)

        rm = self.casedb.connect_remotedb()
        sql = """SELECT is_talent_share FROM opus_share WHERE opus_id=%s"""
        rm.execute(sql, kw['opusid'])
        is_talent_tuple = rm.fetchmany()
        self.casedb.closeDB(rm)
        istalent = 0
        r = response.json()
        for i in range(len(is_talent_tuple[0])):
            if is_talent_tuple[0][i] == 1:
                istalent = 1
                break
        cur = self.casedb.connect_casedb()
        sql = """update interactive_case set result=%s WHERE case_no = %s """
        self.t.data_error(cur, case_no, istalent, r['data']['opus']['isTalentShare'], sql)

        self.casedb.closeDB(cur)

    def test_62_song_detail(self):
        case_no = 62

        header = self.t.get_header
        uid = self.t.get_login_id
        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)
        self.casedb.closeDB(cur)

        rm = self.casedb.connect_remotedb()
        sql = """SELECT count(*) FROM opus_thumbs_up WHERE opus_id=%s and user_id=%s"""
        rm.execute(sql, (kw['opusid'], uid))
        liked_tuple = rm.fetchone()
        self.casedb.closeDB(rm)

        r = response.json()
        if liked_tuple[0] != r['data']['opus']['isLiked']:
            print "isLiked share not equal"

    def test_63_song_detail(self):
        case_no = 63

        header = self.t.get_header
        uid = self.t.get_login_id
        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)
        self.casedb.closeDB(cur)

        rm = self.casedb.connect_remotedb()
        sql = """SELECT count(*) FROM opus_collect WHERE opus_id=%s and user_id=%s"""
        rm.execute(sql, (kw['opusid'], uid))
        collected_tuple = rm.fetchone()
        self.casedb.closeDB(rm)

        r = response.json()
        if collected_tuple[0] != r['data']['opus']['isLiked']:
            print "isLiked share not equal"

    def test_65_song_detail(self):
        case_no = 65

        header = self.t.get_header
        uid = self.t.get_login_id
        cur = self.casedb.connect_casedb()
        kw = self.select_args(cur, case_no)
        response = self.api.get_song_detail(0, header, kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)
        self.casedb.closeDB(cur)

        rm = self.casedb.connect_remotedb()
        sql = """SELECT listen_count, collect_count, share_count, thumbs_up_count FROM song_attach WHERE id=%s"""
        rm.execute(sql, kw['opusid'])
        countz_tuple = rm.fetchone()
        self.casedb.closeDB(rm)

        r = response.json()
        if countz_tuple[0] != r['data']['opus']['listenCount'] and countz_tuple[1] != r['data']['opus']['collectCount'] \
                and countz_tuple[2] != r['data']['opus']['shareCount'] and countz_tuple[3] != r['data']['opus']['likeCount']:
            print countz_tuple[0]
'''if __name__ == "__main__":
    case = interactive_case()

    case.test_01_song_comment()
    # case.test_03_song_comment_blacklist()
    # case.test_43_unblacklist_comment()
    # case.test_08_read_song_comments()
    # case.test_10_blacklist_reply()
    # case.test_42_unblacklist_reply()
    # case.test_15_song_comment_reply()
    # case.test_18_read_replys()
    # case.test_20_delete_comment_has_children()
    # case.test_21_read_reply_page()
    # case.test_22_read_reply_page_turn()
    case.test_23_song_comment_praise()
    # case.test_24_song_comment_praise_again()
    # case.test_29_list_self_unpublish_opus()
    # case.test_30_list_self_publish_opus()
    case.test_31_listen_without_attach()
    # case.test_31_listen_without_attach()
    # case.test_32_listen_without_attach_uncount()
    # case.test_33_listen_format_error()
    # case.test_36_join_medley()
    # case.test_04_song_comment_unlogin()
    # case.test_05_song_comment_null()
    # case.test_06_song_comment_overflow()
    # case.test_07_song_comment_opusid_unexist()
    # case.test_09_read_song_page()
    # case.test_11_delete_comment_self()
    # case.test_12_delete_comment_others()
    # case.test_13_composer_delete_comment()
    # case.test_14_composer_delete_comment_unexist()
    # case.test_15_song_comment_reply()
    # case.test_16_song_comment_reply_pic()
    # case.test_26_read_reply_page()
    # case.test_28_read_reply_page_turn()
    # case.test_34_listen_opus_id_unexist()
    # case.test_35_listen_opus_unlogin()
    # case.test_37_join_medley_again()
    # case.test_38_join_medley_full()
    # case.test_39_join_medley_deleted()
    # case.test_40_get_participantors()
    # case.test_41_get_participantors_unique()
    # case.test_44_publish()
    # case.test_45_publish_desc_null()
    # case.test_46_publish_image_null()
    # case.test_47_publish_songName_null()
    # case.test_48_publish_already_published()
    # case.test_49_delete_published_opus()
    # case.test_50_delete_unpublish_opus()
    # case.test_51_publish_delete()
    # case.test_52_get_oss_image()
    # case.test_53_get_oss_audio()
    # case.test_54_get_oss_audio_md5_null()
    # case.test_55_get_oss_audio_name_null()
    # case.test_56_get_oss_audio_name_null()

    # case.test_57_give_mark()
    # case.test_58_give_mark_again()
    # case.test_59_give_mark_score_negative()
    # case.test_60_give_mark_score_out_of_range()'''


