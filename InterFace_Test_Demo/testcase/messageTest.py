#coding=utf-8

import sys
sys.path.append('./interface')
import unittest
from interface.messageAPI import MessageAPI
from interface.API import MyAPI
import data_init,dbManual

class MessageTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://test.rapself.com:8080'  # java
        # self.baseurl = 'http://139.129.208.77:9091'
        d = data_init.testData(self.baseurl)
        self.d = d.getUserData
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        self.user = MessageAPI(self.baseurl)

    def test_message_Unread(self):
        token = self.d[0]['token']
        response = self.user.message_Unread(token)
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
    """def test_message_Unread_token_null(self):
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
        self.assertEqual(4, r['status'])"""

    def test_message_History_sys(self):
        token = self.d[0]['token']
        response = self.user.message_History(token, 'sys')
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

    def test_message_History_notice(self):
        token = self.d[0]['token']
        response = self.user.message_History(token, 'notice')
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

    """def test_message_History_notice_token_null(self):
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
        self.assertEqual(4, r['status'])"""