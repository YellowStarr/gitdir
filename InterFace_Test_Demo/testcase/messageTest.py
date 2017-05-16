#coding=utf-8

import sys
sys.path.append('./interface')
import unittest
from interface.messageAPI import MessageAPI
from interface.API import MyAPI
import data_init,dbManual

class MessageTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://139.129.208.77:8080'
        self.d = data_init.testData()
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        self.user = MessageAPI(self.baseurl)

    def test_message_Unread(self):
        token = self.d.login_data[0]['token']
        response = self.user.message_Unread(token)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        # self.assertEqual(num, len(r['data']['songs']))

    def test_message_Unread_token_null(self):
        # token = self.d.login_data[0]['token']
        response = self.user.message_Unread(None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])
        # self.assertEqual(num, len(r['data']['songs']))

    def test_message_Unread_token_wrong(self):
        # token = self.d.login_data[0]['token']
        response = self.user.message_Unread('ddd')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(4, r['status'])

    def test_message_History_sys(self):
        token = self.d.login_data[0]['token']
        response = self.user.message_History(token, 'sys')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_message_History_notice(self):
        token = self.d.login_data[0]['token']
        response = self.user.message_History(token, 'notice')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])

    def test_message_History_notice_token_null(self):
        # token = self.d.login_data[0]['token']
        response = self.user.message_History(None, 'notice')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])

    def test_message_History_notice_token_wrong(self):
        # token = self.d.login_data[0]['token']
        response = self.user.message_History('asdfsadf', 'notice')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(4, r['status'])