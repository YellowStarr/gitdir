#coding=utf-8

import sys,random,os,json
sys.path.append('./interface')
import unittest
from interface.CoreAPI import CoreAPI
from interface.indexAPI import IndexAPI
from interface.API import MyAPI
import data_init,dbManual

class ComplextTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://test.rapself.com:9091'
        self.d = data_init.testData()
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
        self.assertEqual(30, len(r['data']['songs']))

    def test_check_Rank_score(self):   # 检查返回的歌曲排行是否是按照计算规则排序
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
        self.assertEqual(0, err)

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
            if cid == newres['data']['comments']['id']:
                err = 1
        self.assertEqual(0, err)







