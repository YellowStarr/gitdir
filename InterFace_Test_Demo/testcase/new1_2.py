#coding=utf-8

import sys
sys.path.append('./interface')
import unittest
from interface.newAPIv1_2 import NewAPIv1_2
from interface.API import MyAPI
import data_init,dbManual

class newAPITest(unittest.TestCase):
    def setUp(self):
        # self.baseurl = 'http://test.rapself.com:9091'
        self.baseurl = 'http://test.rapself.com:8080'
        self.d = data_init.testData(self.baseurl)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.user = NewAPIv1_2(self.baseurl)
        # self.err=[]

    def test_banner(self):
        response = self.user.banner('0')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (0,
                              response.url, response.status_code, response.text))

    def test_homepage(self):
        response = self.user.homepage()
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (0, response.url, response.status_code, response.text))

    def test_usermedley(self):
        uid = '100001773'
        response = self.user.medley_other(uid)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (uid, response.url, response.status_code, response.text))

    def test_usercomplaint(self):
        uid = '100001773'
        response = self.user.complaint_other(uid)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (uid, response.url, response.status_code, response.text))

    def test_usersolo(self):
        uid = '100001773'
        response = self.user.solo_other(uid)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (uid, response.url, response.status_code, response.text))

    def test_mymedley(self):
        token = self.d.getUserData[0]['token']
        response = self.user.medley_my(token)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (token, response.url, response.status_code, response.text))

    def test_mycomplaint(self):
        token = self.d.getUserData[0]['token']
        response = self.user.complaint_my(token)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (token, response.url, response.status_code, response.text))

    def test_mysolo(self):
        token = self.d.getUserData[0]['token']
        response = self.user.solo_my(token)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (token, response.url, response.status_code, response.text))

    def test_myinfo(self):
        token = self.d.getUserData[0]['token']
        response = self.user.my_info(token)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (token, response.url, response.status_code, response.text))