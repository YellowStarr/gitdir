# -*-coding:utf-8 -*-

from API2 import API2
import time
from dbManual import DBManual
from tool import tool
import random
from errorCodeConst import errorCodeConst

class user_interactive_case():
    def __init__(self):
        self.api = API2()
        self.casedb = DBManual()
        self.sql = """update user_interactive_case set args=%s,response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t = tool()
        self.deviceid = "34e7a55f-8fb9-4511-b1b7-55d6148fa9bb"
        self.login_param = {
            "phoneNumber": "18782943850",
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, self.login_param)
        self.ecode = errorCodeConst()

    def test_01_collect(self, cid):
        id = cid

        cur = self.casedb.connect_casedb()
        cur.execute('select args from user_interactive_case where id = %s', id)
        result = cur.fetchone()
        kw = eval(result[0])[0]

        header = self.t.get_header
        sql = """update user_interactive_case set args=%s,response=%s,result=%s,test_time=%s WHERE id = %s"""
        response = self.api.op_collect('put', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, id, response, t, sql, 0, kw)
        self.casedb.closeDB(cur)

    '''def test_02_collect_attach(self):
        case_no = 2
        cur = self.casedb.connect_casedb()
        cur.execute('select args from user_interactive_case where id = %s', id)
        result = cur.fetchone()
        kw = eval(result[0])[0]

        header = self.t.get_header
        sql = """update user_interactive_case set args=%s,response=%s,result=%s,test_time=%s WHERE id = %s"""
        response = self.api.op_collect('put', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, sql, 0, kw)
        self.casedb.closeDB(cur)'''

    def test_04_collect_self(self):
        case_no = 4

        header = self.t.get_header
        userid = self.t.get_login_id    # 获取userid
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where public_status = 1 and user_id=%s", userid)    # 获取自己的非串烧作品id
        result = remote_cur.fetchmany(n)
        arg = random.choice(result)    # 随机抽取一个作品id
        self.casedb.closeDB(remote_cur)

        cur = self.casedb.connect_casedb()
        kw = {'userid': str(userid), 'opusid': str(arg[0])}
        response = self.api.op_collect('put', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.CAN_NOT_COLLECT_SELF, kw)
        self.casedb.closeDB(cur)

    def test_05_collect_unlogin(self):
        case_no = 5
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id,user_id from song_basic where creative_type != 4 and public_status = 1")
        result = remote_cur.fetchmany(n)
        arg = random.choice(result)
        self.casedb.closeDB(remote_cur)

        cur = self.casedb.connect_casedb()
        header = self.api.get_header()
        kw = {'userid': str(arg[1]), 'opusid': str(arg[0])}
        response = self.api.op_collect('put', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)
        self.casedb.closeDB(cur)

    def test_06_collect_opus_unexist(self):
        case_no = 6

        cur = self.casedb.connect_casedb()
        # cur.execute("select args")
        header = self.t.get_header

        kw = {'userid': '6298101404421974110', 'opusid': '6301606723438247951'}
        response = self.api.op_collect('put', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.RECORD_UNEXIST, kw)
        self.casedb.closeDB(cur)

    def test_07_collect_duplicate(self):
        case_no = 7

        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        kw = {'opusid': '6302790102099689473', 'userid': '6298120536261519455'}
        response = self.api.op_collect('put', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ALREADY_COLLECTED, kw)
        self.casedb.closeDB(cur)

    def test_08_collect_delete_unlogin(self):
        case_no = 8

        cur = self.casedb.connect_casedb()
        header = self.api.get_header()
        kw = {'userid': '6298101404421974110', 'opusid': '6301606723438247952'}
        response = self.api.op_collect('delete', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)
        self.casedb.closeDB(cur)

    def test_10_collect_delete_no_attach(self):
        case_no = 10

        header = self.t.get_header
        uid = self.t.get_login_id
        sql = """select opus_id from opus_collect where user_id = %s  """
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute(sql, uid)
        result = remote_cur.fetchmany(n)
        arg = random.choice(result)
        self.casedb.closeDB(remote_cur)

        cur = self.casedb.connect_casedb()
        kw = {'userid': str(uid), 'opusid': str(arg[0])}
        response = self.api.op_collect('delete', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)
        self.casedb.closeDB(cur)

    def test_12_collect_delete_uncollect(self):
        case_no = 12

        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        kw = {'userid': '6298101404421974110', 'opusid': '6301606723438247952'}
        response = self.api.op_collect('delete', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.RECORD_UNEXIST, kw)
        self.casedb.closeDB(cur)

    def test_13_collect_list(self):
        case_no = 13

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        # kw = {'userid': '6298101404421974110', 'opusid': '6301606723438247952'}
        response = self.api.op_collect('get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, )
        self.casedb.closeDB(cur)

    def test_14_collect_list_with_param(self):
        case_no = 14

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": [
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
                        "status": 0,
                        "tags": [""],
                        "genre": "",
                        "collectTime": "",
                        "isDeleted": 0
                    }
                ]
            }
        }

        header = self.t.get_header
        cur = self.casedb.connect_casedb()

        param = {'page':1,"size":20,"sort":"default"}
        response = self.api.op_collect('get', header, kwargs=param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_15_collect_list_unlogin(self):
        case_no = 15

        header = self.api.get_header()
        cur = self.casedb.connect_casedb()
        # kw = {'userid': '6298101404421974110', 'opusid': '6301606723438247952'}
        response = self.api.op_collect('get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST)
        self.casedb.closeDB(cur)

    def test_16_collect_list_arg_type_error(self):
        case_no = 16

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        kw = {'page': 'a', "size": 20, "sort": "default"}
        response = self.api.op_collect('get', header, kwargs=kw)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.UNKNOWN_ERROR, kw)
        self.casedb.closeDB(cur)

    def test_17_praise_opuse_without_attach(self):
        case_no = 17

        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id,user_id from song_basic where public_status = 1 and creative_type != 4")
        result = remote_cur.fetchmany(n)
        arg = random.choice(result)
        self.casedb.closeDB(remote_cur)

        header = self.t.get_header
        cur = self.casedb.connect_casedb()
        kw = {'userid': arg[1], "opusid": arg[0]}
        response = self.api.op_praise('opus', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, kw)
        self.casedb.closeDB(cur)

    def test_19_praise_opuse_duplicate(self):
        case_no = 19

        header = self.t.get_header
        userid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select opus_id from opus_thumbs_up where user_id = %s", userid)
        result = remote_cur.fetchmany(n)
        arg = random.choice(result)
        opusid = arg[0]
        remote_cur.execute("select user_id from song_basic where id = %s", opusid)
        creatorid = remote_cur.fetchone()
        self.casedb.closeDB(remote_cur)

        cur = self.casedb.connect_casedb()
        kw = {'userid': creatorid[0], "opusid": opusid}
        response = self.api.op_praise('opus', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ALREADY_PRAISED, kw)
        self.casedb.closeDB(cur)

    def test_20_praise_unlogin(self):
        case_no = 20

        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id,user_id from song_basic where public_status = 1")
        result = remote_cur.fetchmany(n)
        arg = random.choice(result)
        self.casedb.closeDB(remote_cur)

        header = self.api.get_header()
        cur = self.casedb.connect_casedb()
        kw = {'userid': arg[1], "opusid": arg[0]}
        response = self.api.op_praise('opus', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ACCESS_TOKEN_LOST, kw)
        self.casedb.closeDB(cur)

    def test_21_praise_unexist(self):
        case_no = 21

        cur = self.casedb.connect_casedb()
        # cur.execute("select args")
        header = self.t.get_header

        kw = {'userid': '6298101404421974110', 'opusid': '6301606723438247951'}
        response = self.api.op_praise('opus', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.RECORD_UNEXIST, kw)
        self.casedb.closeDB(cur)

    def test_22_praise_unexist_user(self):
        case_no = 22

        cur = self.casedb.connect_casedb()
        # cur.execute("select args")
        header = self.t.get_header

        kw = {'userid': '6298101404421974111', 'opusid': '6301606723438247952'}
        response = self.api.op_praise('opus', header, kwargs=kw)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.USER_INVALID, kw)
        self.casedb.closeDB(cur)

    def test_23_create_virtual(self):
        case_no = 23

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": {
                    "type": "song",
                    "creativeType": "singer",
                    "songId": 0,
                    "songName": "",
                    "createTime": "",
                    "status": 0,
                    "genre": "",
                    "author": {
                        "userId": 0,
                        "userName": "",
                        "avatar": ""
                    }
                }
            }
        }

        param = {
            "songName": "七星鲁王宫",
            "genre": "rap",
            "lyric": "五十年前长沙土夫子，天真无邪，王胖子，闷油瓶，没关系",
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": "测试伴奏1",
                "type": "测试伴奏分类1"
            },
            "singer": {
                "male": {
                    "id": 1,
                }
            },
            "pos": {
                "longitude": 41.0,
                "latitude": 108.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('virtual', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_24_create_virtual_without_singer(self):
        case_no = 24
        param = {
            "songName": "秦岭神树",
            "genre": "rap",
            "lyric": "老痒，五十年前长沙土夫子，天真无邪，王胖子，闷油瓶，没关系",
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": "测试伴奏1",
                "type": "测试伴奏分类1"
            },
            "pos": {
                "longitude": 41.0,
                "latitude": 108.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('virtual', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_25_create_virtual_without_songname(self):
        case_no = 25
        param = {
            "songName": "",
            "genre": "rap",
            "lyric": "五十年前长沙土夫子，天真无邪，王胖子，闷油瓶，没关系",
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": "测试伴奏1",
                "type": "测试伴奏分类1"
            },
            "singer": {
                "male": {
                    "id": 1,
                }
            },
            "pos": {
                "longitude": 41.0,
                "latitude": 108.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('virtual', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_26_create_virtual_lyric_length_overflow(self):
        case_no = 26
        param = {
            "songName": "七星鲁王宫",
            "genre": "rap",
            "lyric": """海森是一个二流演员，他的经纪人辛诺给他介绍了一份工作，原来是大富翁费德诺聘请他去给父亲老费德诺去演场戏。老费德诺病重住院了，费德诺先生本该在医院里陪着他，但费德诺先生很忙，根本挤不出那么多的时间。但他又怕这事传出去会败坏自己的形象，这时他就想到了和自己长得很像的海森。
　　海森想了想，就同意了。海森是个演员，很会抓各种人物的行为特点和声音特点，经过两天的练习，已学得惟妙惟肖，就连费德诺先生本人也分辨不出来。再戴上根据费德诺先生的面貌特制的橡皮面具，简直就是费德诺先生再生了。他就和费德诺先生签下了合同，正式演出了。
　　尽管如此，海森还是演得小心翼翼。第一次走进病房时，他给老费德诺送上一束鲜花后，就老老实实地坐到床边。老费德诺先生看到他到来，已是很高兴了，就开始絮絮叨叨地说起了他童年的趣事。海森不敢搭腔，只是在一边不时地应和一句，或是笑笑。但即使这样，老费德诺先生也已经很满足了，脸上一直带着幸福的微笑。两个小时的时间过得很快，海森看时间一到，就站起身来。老费德诺一把拉住了他的胳膊，乞怜地望着他，“再陪我一会儿吧，我知道你很忙，但我真的想跟你再说说话呀。10分钟，只需要你10分钟。好吗？”海森看到老人眼睛里那份热切的期待和隐隐的凄楚，不忍拒绝，就又坐到床前，听他诉说着。老费德诺先生又说了10分钟，这才和他依依不舍地告别，并热切地要求他明天准时赶过来。海森点了点头，这才走出了老人的病房。
　　经纪人辛诺递给他一张支票，海森高兴地收起了支票，却觉得眼前猛地闪过一阵炫目的光，两个人慌忙闭上眼睛。过了片刻，两个人睁开眼睛，却见眼前站着一个年轻人，声称是《太阳快报》的记者，听闻费德诺先生放弃了很多生意，每天都赶到医院来陪伴父亲，很是感动，特地来采访的。
　　海森不愧是一个演员，很快就酝酿出了情绪，来了一个现场表演。他诉说了自己对父亲的爱，诉说了父亲对自己的好，说到动情处，还流下了两滴眼泪，感动得记者眼圈儿都红了，又不失时机地给他拍了一张大特写。
　　第二天一早，海森还没睡醒，就接到了费德诺给他打来的电话。费德诺先生异常兴奋，说《太阳快报》登出了那篇专访，非常精彩，感动了很多人。一大早，就有很多人打电话对他表示敬意，还有几个合作伙伴要尽快跟他签订供货合同。他要提高付给海森的酬金，还要把合同期延长。
　　海森继续如约赶到医院，慢慢地他不仅听老费德诺先生说话，还给他讲了几个笑话。老费德诺笑得前仰后合，一张脸乐开了花，一再要他讲下去。海森发挥着他的表演才能，把那些看上去平淡无奇的笑话讲得绘声绘色，喜得老费德诺像个孩子一样兴奋地笑着。不知不觉间，竟已过了半个多小时，海森想到和费德诺先生还有约，忙着匆匆告别了。
　　这天下午，海森又像往常一样，赶到医院。老费德诺的情绪很不好，他说已经感觉到了死亡的逼近。海森也发觉他脸色很不好，去找主治医生询问病情。主治医生这才告诉他，老费德诺的情况确实不大妙，这主要是因为他们刚从他的血液化验中发现了一种病毒变异。这种病毒原本是在药物的控制范围内的，不会致命，但变异后就变得非常疯狂，到现在为止还没有药物可以抑制它，它会要了老费德诺的命。
　　海森给费德诺先生打了电话，通报了老费德诺的病情，然后恳求他抽出一些时间到医院去陪陪老费德诺，这可是他生命的最后几天了。费德诺连连推辞，“我没有时间，真的没有时间，还希望你能多陪陪他，我可以支付给你更多的钱。”海森生气了，“费德诺先生，在你的眼里只有钱吗？他是你的父亲，他现在需要你。”费德诺也生气了，“不用你来教训我，我知道该怎么做。请你按照合同做，不然……”他话里的意思很明白。海森将面临巨额合同赔款。
　　海森给气病了。辛诺把他送到医院。医生对他进行了全面的检查。脸色变得凝重起来。海森开上了玩笑""",
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": "测试伴奏1",
                "type": "测试伴奏分类1"
            },
            "singer": {
                "female": {
                    "id": 1,
                }
            },
            "pos": {
                "longitude": 41.0,
                "latitude": 108.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('virtual', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARG_LENGTH_ERROR)
        self.casedb.closeDB(cur)

    def test_27_create_virtual_without_comurl(self):
        case_no = 27
        param = {
            "songName": u"秦岭神树",
            "genre": "rap",
            "lyric": u"老痒，五十年前长沙土夫子，天真无邪，王胖子，闷油瓶，没关系",
            "accom": {
                "id": 1,
                "url": "",
                "name": u"测试伴奏1",
                "type": u"测试伴奏分类1"
            },
            "pos": {
                "longitude": 41.0,
                "latitude": 108.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('virtual', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_28_create_virtual_lyric_english(self):
        case_no = 28
        param = {
            "songName": u"云顶天宫",
            "genre": "rap",
            "lyric": u"五十年前长沙土夫子，life is struggle，王胖子，闷油瓶",
            "accom": {
                "id": 1,
                "url": "http://xxxx",
                "name": u"测试伴奏1",
                "type": u"测试伴奏分类1"
            },
            "singer": {
                "male": {
                    "id": 1,
                }
            },
            "pos": {
                "longitude": 41.0,
                "latitude": 108.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('virtual', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, param)
        self.casedb.closeDB(cur)

    def publish(self):
        param = {
            "description": u"发布作品描述信息",
            "image": "https://image.baidu.com",
            "songName": "gta5",
            "lyric": u"东夏国，高丽，元朝"
        }

        header = self.t.get_header
        userid = self.t.get_login_id
        remote_cur = self.casedb.connect_remotedb()
        n = remote_cur.execute("select id from song_basic where user_id = %s and creative_status= 5", userid)
        result = remote_cur.fetchmany(n)
        arg = random.choice(result)
        self.casedb.closeDB(remote_cur)

        response = self.api.opus_publish(arg[0], param, header)
        print arg[0]
        print response.text

    def test_29_create_virtual_singer_zero(self):
        case_no = 29
        param = {
            "songName": u"云顶天宫",
            "genre": "rap",
            "lyric": u"五十年前长沙土夫子，life is struggle，王胖子，闷油瓶",
            "accom": {
                "id": 1,
                "url": "http://xxxx",
                "name": u"测试伴奏1",
                "type": u"测试伴奏分类1"
            },
            "singer": {
                "male": {
                    "id": 0,
                },
                "female": {
                    "id": 1,
                }
            },
            "pos": {
                "longitude": 41.0,
                "latitude": 108.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('virtual', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, param)
        self.casedb.closeDB(cur)

    def test_30_create_free_nomix(self):
        case_no = 30

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": {
                    "type": "song",
                    "creativeType": "free",
                    "songId": 0,
                    "songName": "",
                    "createTime": "",
                    "genre": "",
                    "author": {
                        "userId": 0,
                        "userName": "",
                        "avatar": ""
                    }
                }
            }
        }

        param = {
            "songName": "自由说唱",
            "genre": "rap",
            "lyric": "吱吱吱，呦呦呦",
            "songUrl": "http://free.song.com",
            "songDuration": 30,
            "isNeedMix": 0,
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": u"测试伴奏1",
                "type": u"测试伴奏分类1"
            },
            "pos": {
            "longitude": 150.0,
            "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('free', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_31_create_free_mix(self):
        case_no = 31

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": {
                    "type": "song",
                    "creativeType": "free",
                    "songId": 0,
                    "songName": "",
                    "createTime": "",
                    "genre": "",
                    "author": {
                        "userId": 0,
                        "userName": "",
                        "avatar": ""
                    }
                }
            }
        }

        param = {
            "songName": "自由说唱",
            "genre": "rap",
            "lyric": "吱吱吱，呦呦呦",
            "songUrl": "http://free.song.com",
            "songDuration": 30,
            "isNeedMix": 1,
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": u"测试伴奏1",
                "type": u"测试伴奏分类1"
            },
            "pos": {
            "longitude": 150.0,
            "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('free', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_32_create_free_songduration_type_wrong(self):
        case_no = 32
        param = {
            "songName": "自由说唱",
            "genre": "rap",
            "lyric": "吱吱吱，呦呦呦",
            "songUrl": "http://free.song.com",
            "songDuration": 'a',
            "isNeedMix": 0,
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": u"测试伴奏1",
                "type": u"测试伴奏分类1"
            },
            "pos": {
            "longitude": 150.0,
            "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('free', param, header)
        assert response.status_code == 500, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    '''def test_33_create_free_accomid_unexist(self):
        case_no = 33
        param = {
            "songName": "自由说唱",
            "genre": "rap",
            "lyric": "吱吱吱，呦呦呦",
            "songUrl": "http://free.song.com",
            "songDuration": 30,
            "isNeedMix": 0,
            "accom": {
                "id": 0,
                "url": "http://xxx",
                "name": u"测试伴奏1",
                "type": u"测试伴奏分类1"
            },
            "pos": {
            "longitude": 150.0,
            "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('free', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, param)
        self.casedb.closeDB(cur)

    def test_34_create_free_accomtype_unexist(self):
        case_no = 34
        param = {
            "songName": "自由说唱",
            "genre": "rap",
            "lyric": "吱吱吱，呦呦呦",
            "songUrl": "http://free.song.com",
            "songDuration": 30,
            "isNeedMix": 0,
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": u"测试伴奏1",
                "type": u"测试伴奏分类2"
            },
            "pos": {
                "longitude": 150.0,
                "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('free', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, param)
        self.casedb.closeDB(cur)'''

    def test_35_create_free_lyric_null(self):
        case_no = 35
        param = {
            "songName": "自由说唱",
            "genre": "rap",
            "lyric": "",
            "songUrl": "http://free.song.com",
            "songDuration": 30,
            "isNeedMix": 0,
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": u"测试伴奏1",
                "type": u"测试伴奏分类1"
            },
            "pos": {
                "longitude": 150.0,
                "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('free', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_36_create_intel(self):
        case_no = 36

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": {
                    "type": "song",
                    "creativeType": "intel",
                    "songId": 0,
                    "songName": "",
                    "createTime": "",
                    "genre": "",
                    "author": {
                        "userId": 0,
                        "userName": "",
                        "avatar": ""
                    }
                }
            }
        }

        param = {
            "songName": "智能说唱",
            "genre": "rap",
            "lyric": "you don't know about me,but I'm feeling 22",
            "songUrl": "http://taylor.22.com",
            "songDuration": 60,
            "accom": {
            "id": 1,
            "url": "http://accom.url.com",
            "name": "测试伴奏1",
            "type": "测试伴奏类型1"
            },
            "pos": {
                "longitude": 0.0,
                "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('intelligent', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_37_create_intel_songduration_negtive(self):
        case_no = 37
        param = {
            "songName": "智能说唱",
            "genre": "rap",
            "lyric": "you don't know about me,but I'm feeling 22",
            "songUrl": "http://taylor.22.com",
            "songDuration": -60,
            "accom": {
            "id": 1,
            "url": "http://accom.url.com",
            "name": "测试伴奏1",
            "type": "测试伴奏类型1"
            },
            "pos": {
                "longitude": 0.0,
                "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('intelligent', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, param)
        self.casedb.closeDB(cur)

    def test_38_create_intel_latitude_over(self):
        case_no = 38
        param = {
            "songName": u"智能说唱",
            "genre": "rap",
            "lyric": "you don't know about me,but I'm feeling 22",
            "songUrl": "http://taylor.22.com",
            "songDuration": 60,
            "accom": {
            "id": 1,
            "url": "http://accom.url.com",
            "name": u"测试伴奏1",
            "type": u"测试伴奏类型1"
            },
            "pos": {
                "longitude": 0.0,
                "latitude": 20.012010101010
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('intelligent', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

    def test_39_create_medley(self):
        case_no = 39

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": {
                    "type": "song",
                    "creativeType": "medley",
                    "songId": 0,
                    "songName": "",
                    "createTime": "",
                    "genre": "",
                    "author": {
                        "userId": 0,
                        "userName": "",
                        "avatar": ""
                    }
                }
            }
        }

        param = {
            "songName": "串烧",
            "genre": "rap",
            "lyric": "阿士大夫撒大",
            "songUrl": "http://dddd.com",
            "songDuration":20,
            "description": "描述上岛咖啡计算机发送到",
            "image": "http://www.xinlang.com",
            "maxParticipantCount": 5,
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": "测试伴奏1",
                "type": "测试伴奏类型1"
            },
            "pos": {
                "longitude": 0.0,
                "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('medley', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_40_create_medley_max_zero(self):
        case_no = 40
        param = {
            "songName": "串烧",
            "genre": "rap",
            "lyric": "阿士大夫撒大",
            "songUrl": "http://dddd.com",
            "songDuration":20,
            "description": "描述上岛咖啡计算机发送到",
            "image": "http://www.xinlang.com",
            "maxParticipantCount": 0,
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": "测试伴奏1",
                "type": "测试伴奏类型1"
            },
            "pos": {
                "longitude": 0.0,
                "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('medley', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_VALUE_ERROR, param)
        self.casedb.closeDB(cur)

    def test_41_create_medley_description_null(self):
        case_no = 41
        param = {
            "songName": "串烧",
            "genre": "rap",
            "lyric": "阿士大夫撒大",
            "songUrl": "http://dddd.com",
            "songDuration": 20,
            "description": "",
            "image": "http://www.xinlang.com",
            "maxParticipantCount": 5,
            "accom": {
                "id": 1,
                "url": "http://xxx",
                "name": "测试伴奏1",
                "type": "测试伴奏类型1"
            },
            "pos": {
                "longitude": 0.0,
                "latitude": 0.0
            }
        }
        cur = self.casedb.connect_casedb()
        header = self.t.get_header
        response = self.api.create_virtual_singer('medley', param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_42_modify_song_info(self):
        case_no = 42
        header = self.t.get_header
        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from song_basic where user_id = %s and creative_status = 5 and public_status = 0"""
        n = remote_cur.execute(sql, uid)
        result = remote_cur.fetchmany(n)
        songid_tuple = random.choice(result)
        songid = songid_tuple[0]
        self.casedb.closeDB(remote_cur)
        reslist = []
        explist = []
        expect_data = {
            "data": {
                "opus": {
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
                    "tags": [""],
                    "genre": "",
                    "author": {
                        "userId": 0,
                        "userName": "",
                        "avatar": ""
                    }
                }
            }
        }

        param = {
            "songName": "修改歌曲信息",
            "description": "修改歌曲信息描述",
            "image": "http://image.change.com",
            "lyric": "歌词修改内容"
        }
        cur = self.casedb.connect_casedb()
        response = self.api.modify_opus_info(songid, param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)
        self.casedb.closeDB(cur)

        re = self.t.list_dict_keys(response.json(), reslist)
        exp = self.t.list_dict_keys(expect_data, explist)
        self.t.cmpkeys(re, exp)

    def test_43_modify_published_song_info(self):
        case_no = 43
        header = self.t.get_header
        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from song_basic where user_id = %s and creative_status = 5 and public_status = 1"""
        n = remote_cur.execute(sql, uid)
        result = remote_cur.fetchmany(n)
        songid_tuple = random.choice(result)
        songid = songid_tuple[0]
        self.casedb.closeDB(remote_cur)

        param = {
            "songName": "修改歌曲信息",
            "description": "修改歌曲信息描述",
            "image": "http://image.change.com",
            "lyric": "歌词修改内容"
        }
        cur = self.casedb.connect_casedb()
        response = self.api.modify_opus_info(songid, param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.STATE_ERROR, param)
        self.casedb.closeDB(cur)

    def test_44_modify_info_null(self):
        case_no = 44
        header = self.t.get_header
        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from song_basic where user_id = %s and creative_status = 5 and public_status = 0"""
        n = remote_cur.execute(sql, uid)
        result = remote_cur.fetchmany(n)
        songid_tuple = random.choice(result)
        songid = songid_tuple[0]
        self.casedb.closeDB(remote_cur)

        param = {
            "songName": "",
            "description": "",
            "image": "",
            "lyric": ""
        }
        cur = self.casedb.connect_casedb()
        response = self.api.modify_opus_info(songid, param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARGS_NULL, param)
        self.casedb.closeDB(cur)

    def test_45_modify_songname_overflow(self):
        case_no = 45
        header = self.t.get_header
        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from song_basic where user_id = %s and creative_status = 5 and public_status = 0"""
        n = remote_cur.execute(sql, uid)
        result = remote_cur.fetchmany(n)
        songid_tuple = random.choice(result)
        songid = songid_tuple[0]
        self.casedb.closeDB(remote_cur)

        param = {
            "songName": u"修改歌曲名信息超过十个字符"
        }
        cur = self.casedb.connect_casedb()
        response = self.api.modify_opus_info(songid, param, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.ARG_LENGTH_ERROR, param)
        self.casedb.closeDB(cur)

    def test_46_share_link(self):
        case_no = 46
        header = self.t.get_header

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "link": [
                    {
                        "type": "weibo",
                        "url": ""
                    },
                    {
                        "type": "qq",
                        "url": ""
                    },
                    {
                        "type": "weixin",
                        "url": ""
                    }
                ]
            }
        }

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from song_basic where creative_status = 5 and public_status = 1"""
        n = remote_cur.execute(sql)
        result = remote_cur.fetchmany(n)
        songid_tuple = random.choice(result)
        songid = songid_tuple[0]
        self.casedb.closeDB(remote_cur)

        cur = self.casedb.connect_casedb()
        response = self.api.get_share_link(songid, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, songid)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_47_share_link_unpublished_opusid(self):
        case_no = 47
        header = self.t.get_header

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from song_basic where creative_status = 0 and public_status = 0"""
        n = remote_cur.execute(sql)
        result = remote_cur.fetchmany(n)
        songid_tuple = random.choice(result)
        songid = songid_tuple[0]
        self.casedb.closeDB(remote_cur)

        cur = self.casedb.connect_casedb()
        response = self.api.get_share_link(songid, header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.STATE_ERROR, songid)
        self.casedb.closeDB(cur)

    def test_48_share_inner(self):
        case_no = 48
        header = self.t.get_header

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id, user_id from song_basic where creative_status = 5 and public_status = 1"""
        n = remote_cur.execute(sql)
        result = remote_cur.fetchmany(n)
        song_tuple = random.choice(result)
        songid = song_tuple[0]
        userid = song_tuple[1]
        self.casedb.closeDB(remote_cur)

        p ={
            "param": {"content": u"站内分享", "app": 1},
            "userid": str(userid),
            "opusid": str(songid)
        }

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('put', header, kwargs=p)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # self.t.error_handle(cur, case_no, response, t, self.sql, 0, p)
        self.casedb.closeDB(cur)

    def test_49_share_outter(self):
        case_no = 49
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
            "param": {"content": u"站外分享", "app": 0, "outside": [{"type": "weixin", "url": "http://xxxxxxxxxxx"}]},
            "userid": str(userid),
            "opusid": str(songid)
        }

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('put', header, kwargs=p)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, p)
        self.casedb.closeDB(cur)

    def test_50_share_inner_attach(self):
        case_no = 50
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
            "param": {"attach": "eyJzaGFyZUlkIjo2MzA2MzY5MzQ2MzA2MzEwMTQ2LCJzaGFyZU1hcmtlcklkIjo2Mjk5MTYzMjk4NTAzODUyMDMzfQ==", "content": "站内分享带attach", "app": 0, "outside": [{"type": "weixin", "url": "http://xxxxxxxxxxx"}]},
            "userid": '6302790102099689473',
            "opusid": '6298120536261519455'
        }

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('put', header, kwargs=p)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, p)
        self.casedb.closeDB(cur)

    def test_51_share_outter_attach(self):
        case_no = 51
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
            "param": {"attach": "xxx", "content": u"站外分享", "app": 0, "outside": [{"type": "weixin", "url": "http://xxxxxxxxxxx"}]},
            "userid": str(userid),
            "opusid": str(songid)
        }

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('put', header, kwargs=p)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, p)
        self.casedb.closeDB(cur)

    def test_52_share_inner_content_null(self):
        case_no = 52
        header = self.t.get_header
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "shareCount": 0
            }
        }

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id, user_id from song_basic where creative_status = 5 and public_status = 1"""
        n = remote_cur.execute(sql)
        result = remote_cur.fetchmany(n)
        song_tuple = random.choice(result)
        songid = song_tuple[0]
        userid = song_tuple[1]
        self.casedb.closeDB(remote_cur)

        p = {
            "param": {"content": "", "app": 1},
            "userid": str(userid),
            "opusid": str(songid)
        }

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('put', header, kwargs=p)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, p)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_53_share_outter_content_null(self):
        case_no = 53
        header = self.t.get_header

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "shareCount": 0
            }
        }

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id, user_id from song_basic where creative_status = 5 and public_status = 1"""
        n = remote_cur.execute(sql)
        result = remote_cur.fetchmany(n)
        song_tuple = random.choice(result)
        songid = song_tuple[0]
        userid = song_tuple[1]
        self.casedb.closeDB(remote_cur)

        p = {
            "param": {"content":"","app": 0, "outside": [{"type": "weixin", "url": "http://xxxxxxxxxxx"}]},
            "userid": str(userid),
            "opusid": str(songid)
        }

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('put', header, kwargs=p)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, p)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_54_share_list(self):
        case_no = 54
        header = self.t.get_header

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": [
                    {
                        "target": {
                            "author": {
                                "userId": 0,
                                "userName": "",
                                "avatar": "",
                                "level": ""
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
                            "status": 0,
                            "tags": [""],
                            "genre": "",
                            "isDeleted": 0
                        },
                        "shareTime": "",
                        "share": {
                            "shareId": 0,
                            "content": "",
                            "app": 0,
                            "outside": [
                                {
                                    "type": "",
                                    "url": ""
                                }
                            ]
                        },
                        "isTalentShare": 0
                    }]
            }
        }

        p = {
            "page": 1,
            "size": 10,
            "sort": "default"
        }

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('get', header, kwargs=p)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, p)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_55_share_list_default(self):
        case_no = 55
        header = self.t.get_header

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "opus": [
                    {
                    "target": {
                        "author": {
                            "userId": 0,
                            "userName": "",
                            "avatar": "",
                            "level": ""
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
                    "status": 0,
                    "tags": [""],
                    "genre": "",
                    "isDeleted": 0
                },
                "shareTime": "",
                "share": {
                    "shareId": 0,
                    "content": "",
                    "app": 0,
                    "outside": [
                        {
                            "type": "",
                            "url": ""
                        }
                    ]
                },
                "isTalentShare": 0
                }]
            }
        }

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('get', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_56_share_list_sort_hot(self):
        case_no = 56
        header = self.t.get_header

        p = {
            "page": 1,
            "size": 10,
            "sort": "hot"
        }

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('get', header, kwargs=p)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, p)
        self.casedb.closeDB(cur)

    def test_57_share_delete(self):
        case_no = 57
        header = self.t.get_header
        uid = self.t.get_login_id

        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "shareCount": 0
            }
        }

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from opus_share where user_id = %s """
        n = remote_cur.execute(sql, uid)
        if not n:
            self.casedb.closeDB(remote_cur)
            raise ValueError("no share record")
        result = remote_cur.fetchmany(n)
        self.casedb.closeDB(remote_cur)
        share = random.choice(result)
        shareid = share[0]
        param = {"shareid": shareid}
        cur = self.casedb.connect_casedb()
        response = self.api.op_share('delete', header, kwargs=param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, param)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    '''def test_58_share_delete_attach(self):
        case_no = 58
        header = self.t.get_header
        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from opus_share where user_id = %s """
        n = remote_cur.execute(sql, uid)
        if not n:
            self.casedb.closeDB(remote_cur)
            raise ValueError("no share record")
        result = remote_cur.fetchmany(n)
        self.casedb.closeDB(remote_cur)
        share = random.choice(result)
        shareid = share[0]

        param = {"attach":""}
        cur = self.casedb.connect_casedb()
        response = self.api.op_share('delete', header, kwargs=param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, shareid)
        self.casedb.closeDB(cur)

    def test_59_share_delete_nonpass_attach(self):
        case_no = 59
        header = self.t.get_header
        uid = self.t.get_login_id

        remote_cur = self.casedb.connect_remotedb()
        sql = """select id from opus_share where user_id = %s """
        n = remote_cur.execute(sql, uid)
        if not n:
            self.casedb.closeDB(remote_cur)
            raise ValueError("no share record")
        result = remote_cur.fetchmany(n)
        share = random.choice(result)
        shareid = share[0]

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('delete', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0, shareid)
        self.casedb.closeDB(cur)'''

    def test_60_share_delete_unexist(self):
        case_no = 60
        header = self.t.get_header

        param = {"shareid": '6306369355483447301'}

        cur = self.casedb.connect_casedb()
        response = self.api.op_share('delete', header, kwargs=param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.RECORD_UNEXIST, param)
        self.casedb.closeDB(cur)

    def test_61_get_version_ios(self):
        case_no = 61
        header = self.t.get_header
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "version": {
                    "version": "",
                    "upgradeContent": "",
                    "url": "",
                    "force": 0,
                    "platform": "",
                    "ext": "",
                    "minimumSupportVersion": ""
                }
            }
        }

        cur = self.casedb.connect_casedb()
        response = self.api.get_version('iOS', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_62_get_version_andriod(self):
        case_no = 62
        header = self.t.get_header
        r_list = []
        e_list = []
        expect_data = {
            "data": {
                "version": {
                    "version": "",
                    "upgradeContent": "",
                    "url": "",
                    "force": 0,
                    "platform": "",
                    "ext": "",
                    "minimumSupportVersion": ""
                }
            }
        }

        cur = self.casedb.connect_casedb()
        response = self.api.get_version('Android', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        res = self.t.list_dict_keys(response.json(), r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys(case_no, res, exp)

        self.casedb.closeDB(cur)

    def test_63_get_version_platform_error(self):
        case_no = 63
        header = self.t.get_header

        cur = self.casedb.connect_casedb()
        response = self.api.get_version('sybian', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, self.ecode.API_INVALID)
        self.casedb.closeDB(cur)

    def test_64_get_version_ios_unlogin(self):
        case_no = 64
        header = self.api.get_header()

        cur = self.casedb.connect_casedb()
        response = self.api.get_version('iOS', header)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.t.error_handle(cur, case_no, response, t, self.sql, 0)
        self.casedb.closeDB(cur)

if __name__ == "__main__":
    case = user_interactive_case()
    case.test_01_collect(1)
    # case.test_05_collect_unlogin()
    # case.test_06_collect_opus_unexist()
    # case.test_07_collect_duplicate()
    # case.test_08_collect_delete_unlogin()
    # case.test_10_collect_delete_no_attach()
    # case.test_12_collect_delete_uncollect()
    # case.test_13_collect_list()
    # case.test_14_collect_list_with_param()
    # case.test_15_collect_list_unlogin()
    # case.test_16_collect_list_arg_type_error()
    # case.test_17_praise_opuse_without_attach()
    # case.test_19_praise_opuse_duplicate()
    # case.test_20_praise_unlogin()
    # case.test_21_praise_unexist()
    # case.test_22_praise_unexist_user()
    # case.test_23_create_virtual()
    # case.test_24_create_virtual_without_singer()
    # case.test_25_create_virtual_without_songname()
    # case.test_26_create_virtual_lyric_length_overflow()
    # case.test_27_create_virtual_without_comurl()
    # case.test_28_create_virtual_lyric_english()
    # case.test_04_collect_self()
    # case.publish()
    # case.test_29_create_virtual_singer_zero()
    # case.test_30_create_free_nomix()
    # case.test_31_create_free_mix()
    # case.test_32_create_free_songduration_type_wrong()

    # case.test_35_create_free_lyric_null()
    # case.test_36_create_intel()
    # case.test_37_create_intel_songduration_negtive()
    # case.test_38_create_intel_latitude_over()
    # case.test_39_create_medley()
    # case.test_40_create_medley_max_zero()
    # case.test_41_create_medley_description_null()
    # case.test_42_modify_song_info()
    # case.test_43_modify_published_song_info()
    # case.test_44_modify_info_null()
    # case.test_45_modify_songname_overflow()
    # case.test_46_share_link()
    # case.test_47_share_link_unpublished_opusid()
    case.test_48_share_inner()
    # case.test_49_share_outter()
    # case.test_50_share_inner_attach()
    # case.test_52_share_inner_content_null()
    # case.test_53_share_outter_content_null()
    # case.test_54_share_list()
    # case.test_55_share_list_default()
    # case.test_56_share_list_sort_hot()
    # case.test_57_share_delete()
    # case.test_60_share_delete_unexist()
    # case.test_61_get_version_ios()
    # case.test_62_get_version_andriod()
    # case.test_63_get_version_platform_error()



