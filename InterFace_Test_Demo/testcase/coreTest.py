#coding=utf-8

import sys,random,time
sys.path.append('./interface')
import unittest
from interface.CoreAPI import CoreAPI
from interface.API import MyAPI
import data_init, dbManual
from config.runconfig import RunConfig
class coreTest(unittest.TestCase):
    def setUp(self):
        cfg = RunConfig()
        self.baseurl = cfg.get_base_url()
        self.d = data_init.testData(self.baseurl)
        self.data = self.d.getUserData
        self.sidList = self.d.getSongIds
        self.auList = self.d.getAudios()
        self.cidList = self.d.getComments()
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        self.user = CoreAPI(self.baseurl)
        # self.err=[]

    def test_Compose_rap(self):
        audio = random.choice(self.auList)
        print audio
        response = self.user.core_Compose(self.data[0]['token'], 'rap', u'qiuwj post', [{"key":audio[1],
                              "lyric": audio[4], "duration": audio[2]}],
                                          [], 104, 30.508, [audio[4]], 100001775)

        args = {'title': u'接口post', 'audios': [{"key": audio[1], "lyric": audio[4], "duration": audio[2]}], 'images': [], 'latitude': 104, 'longitude': 30.508,
                'lyric': [audio[4]], 'description': '', 'userId': 100001775, 'isPublic': 1}
        print audio[2]
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                              response.url, response.status_code, response.text))


    def test_Compose_complaint(self):
        audio = random.choice(self.auList)
        print audio
        response = self.user.core_Compose(self.data[0]['token'], 'complaint', u'接口post',[{"key": audio[1], "lyric": "", "duration": audio[2]}], [], 104, 30.508, [audio[4]], 100001775)
        args = {'title': u'接口post', 'audios': [{"key": audio[1], "lyric": "", "duration": audio[2]}], 'images': [], 'latitude': 104, 'longitude': 30.508,
                'lyric': [audio[4]], 'description': '', 'userId': 100001775, 'isPublic': 1}
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                              response.url, response.status_code, response.text))


    def test_RecommendLyric(self):
        response = self.user.core_RecommendLyrics(100)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            num = self.db.getALL('solo_recommend_lyric')
            self.assertEqual(len(num), len(r['data']['lyrics']))
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            # print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_Listen(self):
        id = random.choice(self.sidList)
        print id
        sql = 'SELECT listen_count FROM song_basic_info WHERE id=%s' % id
        init_count =self.db.getSingle(sql)
        response = self.user.core_Listen(id, self.data[0]['token'])
        args = id
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            sec_count = self.db.getSingle(sql)
            self.assertEqual(init_count[0]+1, sec_count[0])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            # print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                              response.url, response.status_code, response.text))

    def test_Comment_V1(self):
        """获取评论，按热门"""
        response = self.user.core_Comment_V1('100000933')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % '100000933'
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_Comment_V1_Time(self):
        """获取评论，按时间"""
        response = self.user.core_Comment_V1('100000933', sort='hot')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % '100000933'
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_Comment_Praise(self):
        """评论点赞"""
        response = self.user.core_Comment_Praise(self.data[0]['token'], 888, 1)
        args = {'token':self.data[0]['token'], 'id': 888, 'idType': 1}
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % '888'
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                              response.url, response.status_code, response.text))

    def test_Comment_cancelPraise(self):
        response = self.user.core_Comment_CancelPraise(self.data[0]['token'], 888, 1)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % '888'
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_SongDetail_V1(self):
        songid = random.choice(self.sidList)
        response = self.user.core_SongDetail_V1(songid)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % songid
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_Song_Praise(self):
        id = random.choice(self.sidList)
        print
        sql = 'SELECT user_id FROM song_praise_info WHERE song_id = %s' % id
        uids = self.db.getSet(sql)
        print uids
        uidList = []
        if len(uids) > 0:
            for i in range(len(uids)):
                uidList.append(uids[i][0])
            response = self.user.core_Praise(self.data[0]['token'], id)
            try:
                self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
                r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
                if self.data[0]['id'] not in uidList:
                    self.assertEqual(0, r['status'])
                else:
                    self.assertEqual(105, r['status'])
            except:
                print 'url: %s\n' % response.url
                print u'状态码: %s' % response.status_code
                print u'传递的参数是: %s\n' % id
                print u'响应内容: %s\n' % response.text
                raise
            finally:
                self.api.writeLog(sys._getframe().f_code.co_name,
                                  'api: %s\nstatus_code: %s\ntext: %s' % (
                                      response.url, response.status_code, response.text))
        else:
            response = self.user.core_Praise(self.data[0]['token'], id)
            try:
                self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
                r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
                self.assertEqual(0, r['status'])
            except:
                print 'url: %s\n' % response.url
                print u'状态码: %s' % response.status_code
                print u'传递的参数是: %s\n' % id
                print u'响应内容: %s\n' % response.text
                raise
            finally:
                self.api.writeLog(sys._getframe().f_code.co_name,
                                  'api: %s\nstatus_code: %s\ntext: %s' % (
                                      response.url, response.status_code, response.text))

    def test_Song_cancelPraise(self):
        sql = 'SELECT song_id FROM song_praise_info WHERE user_id = 100001775'
        sids = self.db.getSet(sql)
        print sids
        sidList = []
        try:
            if len(sids)>0:
                for i in range(len(sids)):
                     sidList.append(int(sids[i][0]))
                id = random.choice(sidList)
                sql = 'SELECT count(*) FROM song_praise_info WHERE song_id = %s' % id
                print id
                count = self.db.getSingle(sql)
                response = self.user.core_cancelPraise(self.data[0]['token'], id)
                self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
                r = response.json()
                # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
                if count > 0:
                    self.assertEqual(0, r['status'])
                else:
                    self.assertEqual(999, r['status'])
            else:
                self.api.writeLog(sys._getframe().f_code.co_name, 'has no sid')
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % id
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_Collect(self):
        uid = self.data[0]['id']
        sid = random.choice(self.sidList)
        sql = 'SELECT user_id FROM song_collect_info WHERE song_id = %s' % sid
        uids = self.db.getSet(sql)
        response = self.user.core_Collect(self.data[0]['token'], sid)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            if len(uids) == 0:
                self.assertEqual(0, r['status'])
            else:
                uidList = []
                for i in range(len(uids)):
                    uidList.append(int(uids[i][0]))
                if uid in uidList:
                    self.assertEqual(105, r['status'])
                else:
                    self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % sid
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_cancelCollect(self):
        uid = self.data[0]['id']
        sql = 'SELECT song_id FROM song_collect_info WHERE user_id = %s' % uid
        sids = self.db.getSet(sql)
        sidList = []
        try:
            if len(sids) > 0:
                for i in range(len(sids)):
                     sidList.append(int(sids[i][0]))
                id = random.choice(sidList)
                sql = 'SELECT count(*) FROM song_collect_info WHERE song_id = %s' % id
                print id
                count = self.db.getSingle(sql)
                response = self.user.core_cancelCollect(self.data[0]['token'], id)
                self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
                r = response.json()
                self.api.writeLog(sys._getframe().f_code.co_name, response.text)
                if count > 0:
                    self.assertEqual(0, r['status'])
                else:
                    self.assertEqual(999, r['status'])
            else:
                self.api.writeLog(sys._getframe().f_code.co_name, 'user_id %s has no collection' % uid)
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % id
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_Mycollect(self):
        token = self.data[0]['token']
        uid = self.data[0]['id']
        response = self.user.core_MyCollection(token)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            sql = 'SELECT count(*) from song_collect_info c,song_basic_info b where c.user_id = %s and c.song_id=b.id ' % uid
            collect = self.db.getSet(sql)
            print collect
            self.assertEqual(int(collect[0][0]), len(r['data']['songs']))
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            # print u'传递的参数是: %s\n' % songid
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))


    def test_Get_New_subComment(self):

        # token = self.data[0]['token']
        response = self.user.core_Get_SubComment(912, sort='new')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % '912'
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_Get_Hot_subComment(self):
        # token = self.data[0]['token']
        response = self.user.core_Get_SubComment(912)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % '912'
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_subComment(self):
        """发布子评论"""
        sql = 'SELECT * FROM sub_comment WHERE status=1 AND  song_comment_id=912'
        commentset = self.db.getSet(sql)
        # print commentset
        comm = random.choice(commentset)
        print comm
        token = self.data[0]['token']
        response = self.user.core_Post_SubComment(token, '912', str(comm[0]), u'图片', str(comm[2]), comm[3], [])

        args = {'toCommentId': str(comm[0]), 'songCommentId': 912, 'content': u'图片', 'toUserId': str(comm[2]),
                 'toUserName': comm[3], 'commentAsset': []}
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
        # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                                  response.url, response.status_code, response.text))

    '''def test_Del_subComment(self):
        token = self.data[0]['token']
        response = self.user.core_Del_SubComment(token, 240)
        r = response.json()
        # r = self.user.core_Del_Comment(token, 240)
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    '''

    def test_Del_Music(self):
        """删除我的歌曲"""
        user_id = self.data[0]['id']
        token = self.data[0]['token']
        sql = 'SELECT * FROM song_basic_info WHERE user_id = %s AND song_status = 1 AND audio_type=%s' % (user_id, 2)
        songSet = self.db.getSet(sql)
        ran_song = random.choice(songSet)
        sid = ran_song[0]
        print sid
        response = self.user.core_Del_Music(token, 'raps', sid)
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % sid
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args:%s\napi: %s\nstatus_code: %s\ntext: %s' % (sid,
                                  response.url, response.status_code, response.text))

    def test_Join_Medley(self):
        token = self.data[0]['token']
        audioSet = self.d.getMedleyAudio()    # 从数据库中抓取一组音频
        medleySet = self.d.getUndoneMedley()   # 从数据库主抓取一组待加入的串烧
        ran_audio = random.choice(audioSet)    # 随机选择一首音频
        ran_medley = random.choice(medleySet)    # 随机获取一首待加入的串烧
        mid = ran_medley[1]
        print ran_audio
        participanter = ran_medley[5]
        print 'audio id is %s and medley id is %s'%(ran_audio[0], mid)
        audio = [{'key': ran_audio[1], 'duration': ran_audio[2], 'lyric': ran_audio[4]}]
        response = self.user.core_JoinMedley(token, audio, mid)
        args = {'audios': audio, 'songId': mid}
        try:
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            sql = 'SELECT curr_participant_count FROM medley_song_info WHERE song_id =%s ' % mid
            ran_medley = self.db.getSingle(sql)
            cur_participanter = ran_medley[0]
            self.assertEqual(participanter+1, cur_participanter)
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % mid
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args:%s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                                  response.url, response.status_code, response.text))

    '''def test_songComment(self):    # 评论歌曲，主评论
        token = self.data[0]['token']
        sid = random.choice(self.sidList)    # 随机获取歌曲id
        print sid
        cr = self.user.core_Comment_V1(sid)
        try:
            self.assertEqual(200, cr.status_code)
            comments = cr.json()
            comNum = len(comments['data']['comments'])
            content = 'comment'
        except:
            print 'get comments failed, status code wrong. code:%s' % cr.status_code
            raise
        response = self.user.core_songComment(token, sid, content)
        args = {'id': sid, 'content': content, 'resource': []}
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            cur_response = self.user.core_Comment_V1(sid)
            cur_comments = cur_response.json()
            cur_comNum = len(cur_comments['data']['comments'])
            self.assertEqual(comNum+1, cur_comNum)
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                                  response.url, response.status_code, response.text))'''

    '''def test_Del_songComment(self):
        token = self.data[0]['token']
        uid = self.data[0]['id']
        sql = 'SELECT id FROM song_comment_info WHERE user_id=%s AND  status = 0' % uid
        commentSet = self.db.getSet(sql)
        cid = random.choice(commentSet)[0]                #随机获取评论id
        response = self.user.core_Del_Comment(token, cid)
        try:
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            cur_sql = 'SELECT status FROM song_comment_info WHERE id=%s ' % uid
            time.sleep(2)
            comment_status = self.db.excuteSQL(cur_sql)
            self.assertEqual(0, comment_status)
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: songcommentid: %s\napi: %s\nstatus_code: %s\ntext: %s' % (cid,
                                  response.url, response.status_code, response.text))'''

if __name__ == "__main__":
    unittest.main()