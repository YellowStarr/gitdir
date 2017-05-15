#coding=utf-8

import sys
sys.path.append('./interface')
import unittest
from interface.indexAPI import IndexAPI
from interface.API import MyAPI
import data_init,dbManual

class IndexTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://139.129.208.77:8080'
        self.d = data_init.testData()
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        self.user = IndexAPI(self.baseurl)

    def test_Recommend(self):
        response = self.user.index_Recommend(1, 20)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Song_State(self):
        token = self.d.login_data[0]['token']
        response = self.user.index_Song_State(token, 1, 20)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Hot_Rap(self):
        response = self.user.index_Hot_Music('raps')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Hot_Complaint(self):
        response = self.user.index_Hot_Music('complaints')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Hot_Medley(self):
        response = self.user.index_Hot_Music('medleys')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Rank(self):
        response = self.user.index_Rank()
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_Homepage(self):
        response = self.user.index_Homepage()
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])