#coding=utf-8

import sys,random,os,json
sys.path.append('./interface')
import unittest
from interface.CoreAPI import CoreAPI
from interface.API import MyAPI
import data_init,dbManual

class coreTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://139.129.208.77:8080'
        self.d = data_init.testData()
        self.data = self.d.getUserData()
        self.sidList = self.d.getSongIds()
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
        r = self.user.core_Compose(self.data[0]['token'], 'rap', u'接口post',[{"key" :audio[1],
                              "lyric": audio[4],"duration" : audio[2]}],[],104,30.508,[audio[4]],
                              100001775)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Compose_complaint(self):
        audio = random.choice(self.auList)
        print audio
        r = self.user.core_Compose(self.data[0]['token'], 'complaint', u'接口post',[{"key" :audio[1],
                              "lyric": "", "duration": audio[2]}],[], 104, 30.508, [audio[4]], 100001775)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])


    def test_RecommendLyric(self):
        r = self.user.core_RecommendLyrics(100)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])
        num = self.db.getALL('solo_recommend_lyric')
        self.assertEqual(len(num), len(r['data']['lyrics']))

    def test_Listen(self):
        id = random.choice(self.sidList)
        print id
        sql = 'SELECT listen_count FROM song_basic_info WHERE id=%s' % id
        init_count =self.db.getSingle(sql)
        r = self.user.core_Listen(id, self.data[0]['token'])
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])
        sec_count = self.db.getSingle(sql)
        self.assertEqual(init_count[0]+1, sec_count[0])




    def test_Comment_V1(self):
        '''获取评论，按热门'''
        r = self.user.core_Comment_V1(100000933)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Comment_V1_Time(self):
        '''获取评论，按时间'''
        r = self.user.core_Comment_V1(100000933,sort=0)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Comment_Praise(self):
        '''评论点赞'''
        r = self.user.core_Comment_Praise(self.data[0]['token'], 888, 1)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])
        # num = self.db.getALL('solo_recommend_lyric')
        # self.assertEqual(len(num), len(r['data']['lyrics']))

    def test_Comment_cancelPraise(self):
        r = self.user.core_Comment_CancelPraise(self.data[0]['token'], 888, 1)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_SongDetail_V1(self):
        songid = random.choice(self.sidList)
        r = self.user.core_SongDetail_V1(songid)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

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
            r = self.user.core_Praise(self.data[0]['token'], id)
            self.api.writeLog(sys._getframe().f_code.co_name, r)
            if self.data[0]['id'] not in uidList:
                self.assertEqual(0, r['status'])
            else:
                self.assertEqual(105, r['status'])
        else:
            r = self.user.core_Praise(self.data[0]['token'], id)
            self.api.writeLog(sys._getframe().f_code.co_name, r)
            self.assertEqual(0, r['status'])


    def test_Song_cancelPraise(self):
        sql = 'SELECT song_id FROM song_praise_info WHERE user_id = 100001775'
        sids = self.db.getSet(sql)
        print sids
        sidList = []
        if len(sids)>0:
            for i in range(len(sids)):
                 sidList.append(int(sids[i][0]))
            id = random.choice(sidList)
            sql = 'SELECT count(*) FROM song_praise_info WHERE song_id = %s' % id
            print id
            count = self.db.getSingle(sql)
            r = self.user.core_cancelPraise(self.data[0]['token'], id)
            self.api.writeLog(sys._getframe().f_code.co_name, r)
            if count > 0:
                self.assertEqual(0, r['status'])
            else:
                self.assertEqual(999, r['status'])
        else:
            self.api.writeLog(sys._getframe().f_code.co_name, 'has no sid')

    def test_Collect(self):
        uid = self.data[0]['id']
        sid = random.choice(self.sidList)
        sql = 'SELECT user_id FROM song_collect_info WHERE song_id = %s' % sid
        uids = self.db.getSet(sql)
        r = self.user.core_Collect(self.data[0]['token'], sid)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
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

    def test_cancelCollect(self):
        uid = self.data[0]['id']
        sql = 'SELECT song_id FROM song_collect_info WHERE user_id = %s' % uid
        sids = self.db.getSet(sql)
        sidList = []
        if len(sids) > 0:
            for i in range(len(sids)):
                 sidList.append(int(sids[i][0]))
            id = random.choice(sidList)
            sql = 'SELECT count(*) FROM song_collect_info WHERE song_id = %s' % id
            print id
            count = self.db.getSingle(sql)
            r = self.user.core_cancelCollect(self.data[0]['token'], id)
            self.api.writeLog(sys._getframe().f_code.co_name, r)
            if count > 0:
                self.assertEqual(0, r['status'])
            else:
                self.assertEqual(999, r['status'])
        else:
            self.api.writeLog(sys._getframe().f_code.co_name, 'user_id %s has no collection'%uid)

    def test_Mycollect(self):
        token = self.data[0]['token']
        uid = self.data[0]['id']
        r = self.user.core_MyCollection(token)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])
        sql = 'SELECT count(*) from song_collect_info c,song_basic_info b where c.user_id = %s and c.song_id=b.id and b.song_status=1' % uid
        collect = self.db.getSet(sql)
        print collect
        self.assertEqual(int(collect[0][0]), len(r['data']['songs']))

    def test_Rank(self):
        r = self.user.core_Rank()
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Get_New_subComment(self):
        '''获取子评论'''
        # token = self.data[0]['token']
        r = self.user.core_Get_SubComment(912, sort='new')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Get_Hot_subComment(self):
        '''获取子评论'''
        token = self.data[0]['token']
        r = self.user.core_Post_SubComment(token, 906, '', '图片', '', '', [{'resourceType':1, 'url':'http://user-storage.oss-cn-qingdao.aliyuncs.com/img/20170505025853_100001811_88bf6884e7d205dbabd79965393194ca.png'}])
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])
    def test_subComment(self):
        '''发布子评论'''
        token = self.data[0]['token']
        r = self.user.core_Post_SubComment(token, 912, '', '图片', '', '', [{'resourceType':1, 'url':'http://user-storage.oss-cn-qingdao.aliyuncs.com/img/20170505025853_100001811_88bf6884e7d205dbabd79965393194ca.png'}])
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    """def test_Del_subComment(self):
        token = self.data[0]['token']
        r = self.user.core_Del_SubComment(token, 240)
        # r = self.user.core_Del_Comment(token, 240)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])"""

    def test_Get_HotMusic(self):
        r = self.user.core_Hot_Music('raps')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Del_Music(self):
        '''删除我的歌曲'''
        user_id = self.data[0]['id']
        token = self.data[0]['token']
        sql = 'SELECT * FROM song_basic_info WHERE user_id = %s AND song_status = 1 AND audio_type=%s' % (user_id, 2)
        songSet = self.db.getSet(sql)
        ran_song = random.choice(songSet)
        sid = ran_song[0]
        print sid
        r = self.user.core_Del_Music(token, 'raps', sid)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Join_Medley(self):
        token = self.data[0]['token']
        audioSet = self.d.getMedleyAudio()
        medleySet = self.d.getUndoneMedley()
        ran_audio = random.choice(audioSet)
        ran_medley = random.choice(medleySet)
        mid = ran_medley[1]
        print ran_audio
        participanter = ran_medley[5]
        print 'audio id is %s and medley id is %s'%(ran_audio[0],mid)
        audio = [{'key':ran_audio[1], 'duration':ran_audio[2], 'lyric':ran_audio[4]}]
        r = self.user.core_JoinMedley(token, audio, mid)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0,r['status'])
        sql = 'SELECT curr_participant_count FROM medley_song_info WHERE song_id =%s ' % mid
        ran_medley = self.db.getSingle(sql)
        cur_participanter = ran_medley[0]
        self.assertEqual(participanter+1, cur_participanter)

    def test_songComment(self):
        token = self.data[0]['token']
        sid = random.choice(self.sidList)
        print sid
        comments = self.user.core_Comment_V1(sid)
        comNum = len(comments['data']['comments'])
        content='comment'
        r = self.user.core_songComment(token, sid, content)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])
        cur_comments = self.user.core_Comment_V1(sid)
        cur_comNum = len(cur_comments['data']['comments'])
        self.assertEqual(comNum+1, cur_comNum)

    def test_Del_songComment(self):
        token = self.data[0]['token']
        uid = self.data[0]['id']
        sql = 'SELECT id FROM song_comment_info WHERE user_id=%s' % uid
        count_sql = 'SELECT count(*) FROM song_comment_info WHERE user_id=%s' % uid
        commentSet = self.db.getSet(sql)
        commentN = self.db.excuteSQL(count_sql)
        cid = random.choice(commentSet)[0]
        r = self.user.core_Del_Comment(token, cid)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0,r['status'])
        cur_commentN = self.db.excuteSQL(count_sql)
        self.assertEqual(commentN-1, cur_commentN)









if __name__ == "__main__":
    unittest.main()