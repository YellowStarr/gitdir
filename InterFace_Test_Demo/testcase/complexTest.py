#coding=utf-8

import sys,random
sys.path.append('./interface')
import unittest
from interface.CoreAPI import CoreAPI
from interface.userAPI import UserAPI
from interface.indexAPI import IndexAPI
from interface.API import MyAPI
import data_init,dbManual

class ComplextTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://test.rapself.com:8080'  # java
        # self.baseurl = 'http://139.129.208.77:9091'
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

    def test_check_Rank_num(self):   # 检查返回的歌曲是否是30首
        rank = IndexAPI(self.baseurl)
        response = rank.index_Rank(1, 40)
        r = response.json()
        self.api.writeLog('ranking json', response.text)
        # self.assertEqual(30, len(r['data']['songs']))

    '''def test_check_Rank_score(self):   # 检查返回的歌曲排行是否是按照计算规则排序
        rank = IndexAPI(self.baseurl)
        response = rank.index_Rank(1, 10)
        # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        r = response.json()
        err = 0
        # self.assertEqual(30, len(r['data']['songs']))
        for i in range(len(r['data']['songs'])):
            score = r['data']['songs'][i]['score']
            praise = r['data']['songs'][i]['praiseCount']
            listen = r['data']['songs'][i]['listenCount']
            # repo = r['data']['songs'][i]['repost']
            collect = r['data']['songs'][i]['collectCount']
            s = self.api.hotWork(listen, praise, 0.0, collect)
            if abs(score - s) > 1.0:
                print "rank %s: socre is %s, compute result is %s, song id is %s" % (i+1, score, s, r['data']['songs'][i]['id'])
                err += 1
        self.assertEqual(0, err)'''

    def test_Comment(self):     # 评论
        sid = random.choice(self.sidList)
        response = self.user.core_Comment_V1(sid)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name+'%s' % sid, response.text)

        count = len(r['data']['comments'])
        content = u'这是接口评论'
        self.user.core_songComment(self.data[0]['token'], sid, content)
        newresponse = self.user.core_Comment_V1(sid)
        self.api.writeLog(sys._getframe().f_code.co_name + 'after', newresponse.text)
        newr = newresponse.json()
        newcount = len(newr['data']['comments'])
        self.assertEqual(newcount, count+1)

    def test_delComment(self):     # 删除评论
        err = 0
        sid = random.choice(self.sidList)
        self.user.core_Comment_V1(sid)
        content = u'这是要删除的接口评论'
        response = self.user.core_songComment(self.data[0]['token'], sid, content)
        r = response.json()
        cid = r['data']['id']      # 获取评论id

        self.user.core_Del_Comment(self.data[0]['token'], cid)
        newr = self.user.core_Comment_V1(sid)
        newres = newr.json()
        for i in range(len(newres['data']['comments'])):
            if cid == newres['data']['comments'][i]['id']:
                err = 1
        self.assertEqual(0, err)

    def test_Add_BlackList_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_Add_BlackList('100000001', self.data[0]['token'])
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            sql = 'select * from user_blacklist where user_id= %s and black_user_id= %s' % (self.data[0]['id'], 100000001)
            data = self.db.getSingle(sql)
            if len(data) == 0:
                raise AssertionError('insert into database failed')
            user.user_Del_BlackList('100000001', self.data[0]['token'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))


    '''def test_BlackList_Del(self):
        sql = 'select black_user_id from user_blacklist where user_id= %s' % (self.data[0]['id'])
        blackList = self.db.getSet(sql)
        bid = random.choice(blackList)
        user = UserAPI(self.baseurl)
        response = user.user_Del_BlackList(bid[0], self.data[0]['token'])
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            sql = 'select * from user_blacklist where user_id= %s and black_user_id= %s' % (self.data[0]['id'], bid[0])
            num = self.db.getSingle(sql)
            # if not num:
                # raise AssertionError('delete failed')
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))'''




