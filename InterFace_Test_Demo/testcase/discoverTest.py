#coding=utf-8

import sys,random,os,json
sys.path.append('./interface')
import unittest
from interface.DiscoverAPI import DiscoverAPI
from interface.API import MyAPI
import data_init,dbManual
from config.runconfig import RunConfig

class discoverTest(unittest.TestCase):
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
        self.user = DiscoverAPI(self.baseurl)
        # self.err=[]




    def test_Latest(self):
        response = self.user.discover_Latest()
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Followed(self):
        response = self.user.discover_Followed()
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Newest_Medley_success(self):  # 最新串烧

        response = self.user.user_Newest_Medley(1, 10)
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_Newest_Complaint_success(self):

        response = self.user.user_Newest_Complaint(1, 10)
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
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_Newest_Rap_success(self):
        response = self.user.user_Newest_Rap(1, 10)
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
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))
    """
        def test_ADs(self):
        response = self.user.discover_ADs()
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text
        self.assertEqual(0, r['status'])
    def test_Activity(self):
        response = self.user.discover_Activity()
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text
        self.assertEqual(0, r['status'])

    def test_Join_Activity(self):
        sid =
        actid =
        response = self.user.discover_Join_Activity()
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text
        self.assertEqual(0, r['status'])

    def test_Activity_Detail_T30(self):
        actid =
        response = self.user.discover_Activity_Detail_T30(actid)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text
        self.assertEqual(0, r['status'])

    def test_Activity_Song(self):
        actid =
        response = self.user.discover_Activity_Song(actid)
        self.api.writeLog(sys._getframe().f_code.co_name, response.text
        self.assertEqual(0, r['status'])

    def test_Activity_New30(self):
        actid =
        response = self.user.discover_Activity_New30(actid)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text
        self.assertEqual(0, r['status'])"""


