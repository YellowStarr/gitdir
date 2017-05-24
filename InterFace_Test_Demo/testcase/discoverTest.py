#coding=utf-8

import sys,random,os,json
sys.path.append('./interface')
import unittest
from interface.DiscoverAPI import DiscoverAPI
from interface.API import MyAPI
import data_init,dbManual

class discoverTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://139.129.208.77:9091'
        self.d = data_init.testData()
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


