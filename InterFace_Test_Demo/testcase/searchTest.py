#coding=utf-8

import sys
sys.path.append('./interface')
import unittest
from interface.searchAPI import SearchAPI
from interface.API import MyAPI
import data_init,dbManual

class SearchTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://139.129.208.77:8080'
        self.d = data_init.testData()
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        self.user = SearchAPI(self.baseurl)

    def test_search_Song_CN(self):
        keyword = u'木头人'
        sql = 'SELECT COUNT(*) FROM song_basic_info where song_name LIKE "%' + keyword.encode('utf-8') + '%" and song_status=1'
        num = self.db.excuteSQL(sql)
        print num
        response = self.user.search_Song(keyword)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        self.assertEqual(num, len(r['data']['songs']))
    def test_search_Song_EN(self):
        keyword = u'oo'
        sql = 'SELECT COUNT(*) FROM song_basic_info where song_name LIKE "%' + keyword + '%"and song_status=1'
        num = self.db.excuteSQL(sql)
        print num
        response = self.user.search_Song(keyword)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        self.assertEqual(num, len(r['data']['songs']))

    def test_search_Song_DIG(self):
        keyword = u'11'
        sql = 'SELECT COUNT(*) FROM song_basic_info where song_name LIKE "%' + keyword + '%" and song_status=1'
        num = self.db.excuteSQL(sql)
        print num
        response = self.user.search_Song(keyword)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        self.assertEqual(num, len(r['data']['songs']))
    def test_search_User_CN(self):
        keyword = u'罗亮'
        sql = 'SELECT COUNT(*) FROM user_profile_basic where user_name LIKE "%' + keyword.encode('utf-8') + '%"'
        num = self.db.excuteSQL(sql)
        print num
        response = self.user.search_User(keyword)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        self.assertEqual(num, len(r['data']['users']))

    def test_search_User_EN(self):
        keyword = u'sleepyhead'
        sql = 'SELECT COUNT(*) FROM user_profile_basic where user_name LIKE "%' + keyword + '%"'
        num = self.db.excuteSQL(sql)
        print num
        response = self.user.search_User(keyword)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        self.assertEqual(num, len(r['data']['users']))

    def test_search_Hot(self):
        response = self.user.search_Hot()
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])