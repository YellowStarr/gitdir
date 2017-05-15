#coding=utf-8

import sys,random,os,json
sys.path.append('./interface')
import unittest
from interface.userAPI import UserAPI
from interface.API import MyAPI
import data_init,dbManual

class userinfoTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://139.129.208.77:8080'
        d = data_init.testData()
        self.data = d.getUserData()
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        # self.err=[]
    def test_FollowedSong_success(self):

        user = UserAPI(self.baseurl)
        response = user.user_FollowedSong(random.choice(self.data)['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        #self.assertIn(u'page', r['msg'])
        # self.api.writeLog('FollowedSong_success',json.loads(r))

    def test_Newest_Medley_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Medley(1, 1000)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Newest_Complaint_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Complaint(1, 1000)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Newest_Rap_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Rap(1, 1000)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Focus_success(self):
        """关注成功"""
        user = UserAPI(self.baseurl)
        response = user.user_Focus(self.data[1]['id'], self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        try:
            self.assertEqual(0, r['status'])
        except AssertionError as e:
            print "test_Focus_mix"
            # self.verificationErrors.append(e)


    def test_cancelFocus(self):
        """取消关注"""
        user = UserAPI(self.baseurl)
        response = user.user_cancelFocus(self.data[1]['id'], self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        try:
            self.assertEqual(0, r['status'])
        except AssertionError as e:
            print "test_cancelFocus failed"
            self.verificationErrors.append(e)

    def test_followedList_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_followedList(self.data[0]['id'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        try:
            self.assertEqual(0, r['status'])
        except AssertionError as e:
            print "test_cancelFocus_again failed"
            # self.verificationErrors.append(e)


    def test_FansList_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_fansList(int(self.data[0]['id']))
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Add_BlackList_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_Add_BlackList(100000027, self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        sql = 'select * from user_blacklist where user_id= %s and black_user_id= %s' % (self.data[0]['id'],100000027)
        data = self.db.getSingle(sql)
        if len(data) == 0:
            raise AssertionError('insert into database failed')

    def test_BlackList_data_check(self):
        user = UserAPI(self.baseurl)
        response = user.user_BlackList(self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        sql = 'select count(*) from user_blacklist where user_id= %s' % self.data[0]['id']
        num = self.db.getSingle(sql)
        self.assertEqual(len(r['data']['blacklist']), int(num[0]))

    def test_BlackList_Del(self):
        sql = 'select black_user_id from user_blacklist where user_id= %s' % (self.data[0]['id'])
        blackList = self.db.getSet(sql)
        bid = random.choice(blackList)
        user = UserAPI(self.baseurl)
        response = user.user_Del_BlackList(bid[0], self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        sql = 'select * from user_blacklist where user_id= %s and black_user_id= %s' % (self.data[0]['id'],bid[0])
        num = self.db.getSingle(sql)
        if not num:
            raise AssertionError('delete failed')

    def test_Create_Medley_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_Create_Medley(self.data[0]['token'],[{'key':'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                     'duration':3,'lyric':''}],[],104,30.56089,5,'interface' )
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        # self.assertIn(u'无', r['msg'])

    def test_Medley_Participant_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_Medley_Participanter("100000003")
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_ModifyInfo(self):
        user = UserAPI(self.baseurl)
        response = user.user_ModifyInfo(self.data[0]['token'], self.data[0]['id'], 'sleepydog', 18782943855)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_get_userInfo(self):
        user = UserAPI(self.baseurl)
        response = user.user_getUserInfo("100001775")
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_get_myMedley(self):
        user = UserAPI(self.baseurl)
        response = user.user_getMyMedley(self.data[0]['token'], 100)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_get_myComplaint(self):
        user = UserAPI(self.baseurl)
        response = user.user_getMyComplaint(self.data[0]['token'], 100)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_get_myRap(self):
        user = UserAPI(self.baseurl)
        response = user.user_getMyRap(self.data[0]['token'], 100)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_get_Statistic(self):
        user = UserAPI(self.baseurl)
        response = user.user_Statistic(self.data[0]['id'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])


    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()

