#coding=utf-8

import sys
sys.path.append('./interface')
import unittest
from interface.indexAPI import IndexAPI
from interface.API import MyAPI
import data_init, dbManual, requests

class IndexErrorTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://test.rapself.com:8080'  # java
        # self.baseurl = 'http://139.129.208.77:9091'
        self.d = data_init.testData(self.baseurl)
        self.data = self.d.getUserData
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        self.user = IndexAPI(self.baseurl)

    def test_Recommend_type_error(self):
        response = self.user.index_Recommend('', '')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])

    def test_Recommend_arg_error(self):
        response = self.user.index_Recommend(0, 10)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Song_State_token_error(self):
        # token = self.d.login_data[0]['token']
        response = self.user.index_Song_State('sdfsdfsdfewsf', 1, 20)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(4, r['status'])

    def test_Song_State_token_null(self):
        # token = self.d.login_data[0]['token']
        response = self.user.index_Song_State(None, 1, 20)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])

    def test_Hot_Rap_range_error(self):
        response = self.user.index_Hot_Music('raps', size=-1)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])


    def test_Rank_range_error(self):
        response = self.user.index_Rank(0)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Rank_range_error2(self):
        response = self.user.index_Rank(1, 0)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Rank_type_error(self):
        response = self.user.index_Rank('')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])

    def test_Song_state_null(self):
        response = self.user.index_Song_State(None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])
        self.assertIn(u'需要token', r['msg'])

    def test_Song_state_page_wrong(self):
        response = self.user.index_Song_State(self.data[0]['token'], 0)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])
        self.assertIn(u'取值错误', r['msg'])

    """def test_Homepage(self):
        url = self.baseurl + '/api/homepage'
        r = requests.get(url, params={'a': 1})
        response = r.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response)
        self.assertEqual(107, response['status']) """