#coding=utf-8
import sys
sys.path.append('./interface')
import unittest,requests
from interface.LoginAPI import LoginAPI
from data_init import testData
from interface.API import MyAPI
from classifyCode import ClassifyCode

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.baseurl = 'http://test.rapself.com:9091'
        self.user = LoginAPI(self.baseurl)
        login = testData()
        self.udata = login.getUserData[0]
        self.api = MyAPI()
        self.result = ""
        self.classifycode = ClassifyCode()
    def tearDown(self):
        print self.result

    def test_login_success(self):
        u"""登陆成功测试"""
        print "-----------------------------------running test_login_success----------------------------------------- "
        response = self.user.login_Login(self.udata['phoneNumber'], self.udata['password'])
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(r['status'], 0, 'wrong')
            print r['data']['user']['id']
        except:
            print 'status code:%s' % response.status_code
            # self.classifycode.comparecode(response)
            # self.classifycode.classify_err_by_code()
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_login_password_wrong(self):
        u"""密码错误测试"""
        print "-----------------------------------running test_login_password_wrong----------------------------------------- "
        response = self.user.login_Login('18782943850', 'A1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ==')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 97)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            # self.classifycode.comparecode(response)
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_login_arguements_wrong(self):
        u"""参数错误"""
        print "-----------------------------------running test_login_arguements_wrong----------------------------------------- "

        url = self.baseurl + '/api/user/login'
        postdata = {}
        response = requests.post(url, json=postdata)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 2)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_login_phone_user_not_exist(self):
        u"""参数错误"""
        print "-----------------------------------running test_login_arguements_wrong----------------------------------------- "

        url = self.baseurl + '/api/user/login'
        postdata = {"terminal": 2, 'arg1': 1, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ==',
                    'phone': '187829438dd'}
        response = requests.post(url, json=postdata)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 98)
            # print response
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_register_phone_exists(self):
        u"""手机已注册"""
        print "-----------------------------------running test_register_phone_exists----------------------------------------- "
        response = self.user.register_msgCode('18109053700')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 111)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_login_Update_andriod(self):
        response = self.user.login_Update('andriod')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 0)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_login_Update_ios(self):
        response = self.user.login_Update('ios')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 0)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_login_ThirdParty_QQ(self):
        response = self.user.login_ThirdParty('UID_E5471C281EF0A4C785B31A0A58A55342', 'sin', '', '')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 0)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_login_ThirdParty_QQ_token_wrong(self):
        response = self.user.login_ThirdParty('', 'sin', 2, 0)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 4)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_forgetpwd_msgCode_no_pbone(self):
        response = self.user.forgetpwd_msgCode()
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 103)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_forgetpwd_msgCode(self):
        response = self.user.forgetpwd_msgCode('18782943850')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 0)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_register(self):
        response = self.user.register_Register('qiuwj', 15350556639, '888888', '0000')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(r['status'], 0)
        except:
            print 'status code:%s' % response.status_code
            # self.api.writeLog(sys._getframe().f_code.co_name,
            #                   'api: %s\nstatus_code: %s' % (response.url, response.status_code))
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

if __name__ == '__main__':
        unittest.main()

