# -*-coding:utf-8 -*-

from API2 import API2
from dbManual import DBManual
from tool import tool
import random
import json
from errorCodeConst import errorCodeConst
import base64

class mix_case():
    def __init__(self):
        self.api = API2()
        self.casedb = DBManual()
        # self.sql = """update user_interactive_case set args=%s,response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t = tool()
        self.deviceid = "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"

        self.ecode = errorCodeConst()
        self.pwd = base64.b64encode("888888")

    def register(self, phonenumber):
        header = self.api.get_header(deviceId=self.deviceid)
        sms_param = {"phoneNumber": phonenumber}
        phone_param = {
            "phoneNumber": phonenumber,
            "password": self.pwd,
            "platform": "iOS",
            "clientVersion": "2.0",
            "registerSmsCode": "0000",
            "registerSmsId": ""
        }

        response = self.api.mobile_sms(sms_param, header)
        data = response.json()
        registerSmsId = data['data']['registerSmsId']
        phone_param['registerSmsId'] = registerSmsId
        response = self.api.mobile_register(phone_param, header)
        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.t.mylog('register', 'header：', response.headers)
        self.t.mylog('register', 'request url:', response.url)
        self.t.mylog('register', 'request json:', phonenumber)
        self.t.mylog('register', 'response data:', d)

    def login(self, phonenumber):
        param = {
            "phoneNumber": phonenumber,
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, param)

    def listen(self):
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

        header = self.t.get_header
        # cur = self.casedb.connect_casedb()
        response = self.api.listen(header, kwargs=kw)
        # assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        # t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.t.mylog('listen', 'header：', response.headers)
        self.t.mylog('listen', 'request url:', response.url)
        self.t.mylog('listen', 'request json:', kw)
        self.t.mylog('listen', 'response data:', d)

    def share(self):
        header = self.t.get_header

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id, user_id from song_basic where creative_status = 5 and public_status = 1"""
        n = remote_cur.execute(sql)
        result = remote_cur.fetchmany(n)
        song_tuple = random.choice(result)
        songid = song_tuple[0]
        userid = song_tuple[1]
        self.casedb.closeDB(remote_cur)

        p = {
            "param": {"content": u"站内分享", "app": 1},
            "userid": str(userid),
            "opusid": str(songid)
        }

        response = self.api.op_share('put', header, kwargs=p)
        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.t.mylog('share', 'header：', response.headers)
        self.t.mylog('share', 'request url:', response.url)
        self.t.mylog('share', 'request json:', p)
        self.t.mylog('share', 'response data:', d)

    def comment(self):
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id, user_id from song_basic where creative_status=5 and public_status=1")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw = {}
        kw['opusid'] = opus[0]
        kw['userid'] = opus[1]
        kw['param'] = {
            'content': u'发布歌曲评论正向验证'
        }
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        response = self.api.op_comment('song', 'post', header, kwargs=kw)
        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.t.mylog('comment', 'header：', response.headers)
        self.t.mylog('comment', 'request url:', response.url)
        self.t.mylog('comment', 'request json:', kw)
        self.t.mylog('comment', 'response data:', d)

    def focus(self):
        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from user_profile_basic """
        n = remote_cur.execute(sql)
        result = remote_cur.fetchmany(n)
        song_tuple = random.choice(result)
        userid = song_tuple[0]
        self.casedb.closeDB(remote_cur)
        # cur = self.casedb.connect_casedb()
        # uid = '6301346050607153160'

        header = self.t.get_header

        response = self.api.op_focus('put', userid, header=header)
        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.t.mylog('focus', 'header：', response.headers)
        self.t.mylog('focus', 'request url:', response.url)
        self.t.mylog('focus', 'request json:', userid)
        self.t.mylog('focus', 'response data:', d)

    def comment_praise(self):
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, opus_id, user_id from opus_comment where delete_status=0 GROUP BY (opus_comment_id)")
        result = remote_cur.fetchmany(n)
        a = random.choice(result)
        kw = {}
        kw['commentid'] = a[0]
        kw['opusid'] = a[1]
        kw['userid'] = a[2]

        self.casedb.closeDB(remote_cur)

        header = self.t.get_header

        # cur = self.casedb.connect_casedb()
        response = self.api.op_praise('comment', header, kwargs=kw)
        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.t.mylog('comment_praise', 'header：', response.headers)
        self.t.mylog('comment_praise', 'request url:', response.url)
        self.t.mylog('comment_praise', 'request json:', kw)
        self.t.mylog('comment_praise', 'response data:', d)

    def prais(self):
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id,user_id from song_basic where public_status = 1 and creative_type != 4")
        result = remote_cur.fetchmany(n)
        arg = random.choice(result)
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        # cur = self.casedb.connect_casedb()
        kw = {'userid': arg[1], "opusid": arg[0]}
        response = self.api.op_praise('opus', header, kwargs=kw)
        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.t.mylog('prais', 'header：', response.headers)
        self.t.mylog('prais', 'request url:', response.url)
        self.t.mylog('prais', 'request json:', kw)
        self.t.mylog('prais', 'response data:', d)

    def collect(self):
        kw = {}
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(
            "select id, user_id from song_basic where creative_status=5 and public_status=1 and delete_status = 0")
        result = remote_cur.fetchmany(n)
        opus = random.choice(result)
        kw['userid'] = opus[1]
        kw['opusid'] = opus[0]

        header = self.t.get_header
        # sql = """update user_interactive_case set args=%s,response=%s,result=%s,test_time=%s WHERE id = %s"""
        response = self.api.op_collect('put', header, kwargs=kw)
        data = response.json()
        d = json.dumps(data, ensure_ascii=False)
        self.t.mylog('collect', 'header：', response.headers)
        self.t.mylog('collect', 'request url:', response.url)
        self.t.mylog('collect', 'request json:', kw)
        self.t.mylog('collect', 'response data:', d)

if __name__ == "__main__":
    phone_list = [13000000000, 13000000001, 13000000002, 13000000003, 13000000004, 13000000005, 13000000006, 13000000007,
                  13000000008, 13000000009, 13000000010, 13000000011, 13000000012, 13000000013, 13000000014, 13000000015,
                  13000000016, 13000000017, 13000000018, 13000000019, 13000000020]
    # t = tool()
    r = mix_case()
    for i in range(len(phone_list)):
        r.login(phone_list[i])
        r.listen()
        r.share()
        r.comment()
        r.focus()
        r.comment_praise()
        r.prais()
        r.collect()
        # t.get_header
        # r.register(phone_list[i])
