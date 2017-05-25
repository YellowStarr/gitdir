#coding=utf-8

import sys
sys.path.append('./interface')
import unittest
from interface.indexAPI import IndexAPI
from interface.API import MyAPI
import data_init,dbManual

class IndexTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://test.rapself.com:8080'  # java
        # self.baseurl = 'http://139.129.208.77:9091'
        d = data_init.testData(self.baseurl)
        self.d = d.getUserData
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        self.user = IndexAPI(self.baseurl)

    def test_Recommend(self):
        response = self.user.index_Recommend(1, 20)
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_Song_State(self):
        token = self.d[0]['token']
        response = self.user.index_Song_State(token, 1, 20)
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_Hot_Rap(self):
        response = self.user.index_Hot_Music('raps')
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_Hot_Complaint(self):
        response = self.user.index_Hot_Music('complaints')
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_Hot_Medley(self):
        response = self.user.index_Hot_Music('medleys')
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_Rank(self):
        response = self.user.index_Rank()
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))

    def test_Homepage(self):
        response = self.user.index_Homepage()
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                                  response.url, response.status_code, response.text))