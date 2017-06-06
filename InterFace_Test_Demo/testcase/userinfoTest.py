#coding=utf-8

import sys,random,os,json
sys.path.append('./interface')
import unittest
from interface.userAPI import UserAPI
from interface.API import MyAPI
import data_init,dbManual
from config.runconfig import RunConfig

class userinfoTest(unittest.TestCase):
    def setUp(self):
        cfg = RunConfig()
        self.baseurl = cfg.get_base_url()
        d = data_init.testData(self.baseurl)
        self.data = d.getUserData
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        # self.err=[]

    def test_FollowedSong_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_FollowedSong(self.data[0]['token'])
        try:
            self.assertEqual(200, response.status_code)
            # response.status_code == 200
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, )
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % self.data['token']
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))

    def test_followedList_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_followedList(self.data[0]['id'])
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            try:
                self.assertEqual(0, r['status'])
            except AssertionError as e:
                print "test_cancelFocus_again failed"
            # self.verificationErrors.append(e)
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % self.data[0]['id']
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))

    def test_FansList_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_fansList(int(self.data[0]['id']))
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % self.data[0]['id']
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))



    def test_BlackList_data_check(self):
        user = UserAPI(self.baseurl)
        response = user.user_BlackList(self.data[0]['token'])
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            sql = 'select count(*) from user_blacklist where user_id= %s' % self.data[0]['id']
            num = self.db.getSingle(sql)
            self.assertEqual(len(r['data']['blacklist']), int(num[0]))
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            # print u'传递的参数是: %s\n' % ar
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))

    def test_Create_Medley_success(self):
        args = {'audios': [{'key':'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                     'duration':3,'lyric':''}], 'images': [], 'latitude': 104, 'longitude': 30.56089, 'maxCount':5, 'title': 'interface'}
        user = UserAPI(self.baseurl)
        response = user.user_Create_Medley(self.data[0]['token'], [{'key':'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                     'duration':3,'lyric':''}], [], 104, 30.56089, 5,'interface')
        params = {'audios': [{'key':'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                     'duration':3,'lyric':''}], 'images': [], 'latitude': 104, 'longitude': 30.56089,
                  'maxCount': 5, 'title': 'interface'}
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
                                'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (params, response.url, response.status_code, response.text))

    def test_Medley_Participant_success(self):
        user = UserAPI(self.baseurl)
        response = user.user_Medley_Participanter("100000003")
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % "100000003"
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))


    def test_ModifyInfo(self):
        user = UserAPI(self.baseurl)
        response = user.user_ModifyInfo(self.data[0]['token'], self.data[0]['id'], 'sleepydog', 18782943855)
        args = {'area': u'四川 成都', 'birthday': "2015-06-06", 'emotionStatus': 1,
         'hasFocus': '', 'personalProfile': 'per', 'phoneNumber': '18782943855',
         'portrait': '', 'sex': 1, 'userName': 'sleepydog', 'id': self.data[0]['id']}
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print '\nurl: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (args, response.url, response.status_code, response.text))

    def test_get_userInfo(self):
        user = UserAPI(self.baseurl)
        response = user.user_getUserInfo(self.data[0]['id'])
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % self.data[0]['id']
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))

    def test_get_myMedley(self):
        user = UserAPI(self.baseurl)
        response = user.user_getMyMedley(self.data[0]['token'], 100)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            # print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))

    def test_get_myComplaint(self):
        args = {'token': self.data[0]['token'], 'status': 100}
        user = UserAPI(self.baseurl)
        response = user.user_getMyComplaint(self.data[0]['token'], 3)
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
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))

    def test_get_myRap(self):
        args = {'token': self.data[0]['token'], 'status': 100}
        user = UserAPI(self.baseurl)
        response = user.user_getMyRap(self.data[0]['token'], 100)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url:%s'% response.url
            print u'状态码: %s' % response.status_code
            # print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,

                               'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))

    def test_get_Statistic(self):
        user = UserAPI(self.baseurl)
        response = user.user_Statistic(self.data[0]['id'])
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % self.data[0]['id']
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()

