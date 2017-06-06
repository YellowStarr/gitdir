#coding=utf-8

import sys,random
sys.path.append('./interface')
import unittest
from interface.shareAPI import ShareAPI
from interface.API import MyAPI
import data_init,dbManual
from config.runconfig import RunConfig

class ShareTest(unittest.TestCase):
    def setUp(self):
        cfg = RunConfig()
        self.baseurl = cfg.get_base_url()
        self.s = data_init.testData(self.baseurl)
        self.d = self.s.getUserData
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        self.user = ShareAPI(self.baseurl)


    def test_ShareList(self):
        token = self.d[0]['token']
        id = self.d[0]['id']
        response = self.user.share_ShareList(token, id)
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                                'api: %s\nstatus_code: %s\ntext: %s' % (response.url, response.status_code, response.text))

    """def test_ShareList_token_null(self):
        # token = self.d.login_dat[0]['token']
        id = self.d.login_data[0]['id']
        response = self.user.share_ShareList(None, id)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])

    def test_ShareList_id_wrong(self):
        token = self.d.login_data[0]['token']
        # id = self.d.login_data[0]['id']
        response = self.user.share_ShareList(None, 'adfasdf')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])"""

    def test_Share_Inner(self):
        sidList = self.s.getSongIds
        sid = random.choice(sidList)
        token = self.d[0]['token']
        share_reason = 'share reason'
        response = self.user.share_Share_Inner(token, sid, share_reason)
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

    """def test_Share_Inner_sid_wrong(self):
        # sidList = self.d.getSongIds
        # sid = random.choice(sidList)
        token = self.d.login_data[0]['token']
        response = self.user.share_Share_Inner(token, '101111111')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(104, r['status'])"""
