#coding=utf-8
import sys
sys.path.append('./interface')
import unittest,requests
from interface.LoginAPI import LoginAPI
from interface.API import MyAPI

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.baseurl = 'http://139.129.208.77:8080'
        self.user = LoginAPI(self.baseurl)
        self.api = MyAPI()
        self.result=""

    def tearDown(self):
        print self.result

    def test_login_success(self):
        u"""登陆成功测试"""
        print "-----------------------------------running test_login_success----------------------------------------- "
        response = self.user.login_Login('18782943850', 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ==')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 0)
        print r['data']['user']['id']

    def test_login_password_wrong(self):
        u'''密码错误测试'''
        print "-----------------------------------running test_login_password_wrong----------------------------------------- "
        response = self.user.login_Login('18782943850', 'A1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ==')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 97)

    def test_login_arguements_wrong(self):
        u'''参数错误'''
        print "-----------------------------------running test_login_arguements_wrong----------------------------------------- "

        url = self.baseurl + '/api/user/login'
        postdata = {}
        response = requests.post(url, json=postdata)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 2)

    def test_login_phone_user_not_exist(self):
        u'''参数错误'''
        print "-----------------------------------running test_login_arguements_wrong----------------------------------------- "

        url = self.baseurl + '/api/user/login'
        postdata = {"terminal": 2, 'arg1': 1, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ==',
                    'phone': '187829438dd'}
        response = requests.post(url, json=postdata)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 98)
        # print response
        """def test_register_success(self):
                print "-----------------------------------running test_register_phone_exists----------------------------------------- "
                lg = LoginAPI(self.baseurl)
                register = lg.register_Register("qiuwjqq", "18782943850", "8888", "1111")
                print register['msg']
                self.assertEqual(register['status'], 111)"""

    def test_register_phone_exists(self):
        u"""手机已注册"""
        print "-----------------------------------running test_register_phone_exists----------------------------------------- "
        response = self.user.register_msgCode('18109053700')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 111)

    def test_login_Update_andriod(self):
        response = self.user.login_Update('andriod')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 0)
        print r

    def test_login_Update_ios(self):
        response = self.user.login_Update('ios')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 0)
        print r

    def test_login_ThirdParty_QQ(self):
        response = self.user.login_ThirdParty('UID_E5471C281EF0A4C785B31A0A58A55342', 'sin', '', '')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 0)
        print r

    def test_login_ThirdParty_QQ_token_wrong(self):
        response = self.user.login_ThirdParty('', 'sin', 2, 0)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 4)
        print r

    def test_forgetpwd_msgCode_no_pbone(self):
        response = self.user.forgetpwd_msgCode()
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 103)
        print r

    def test_forgetpwd_msgCode(self):
        response = self.user.forgetpwd_msgCode('18782943850')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(r['status'], 0)
        print r

if __name__ == '__main__':
        unittest.main()

