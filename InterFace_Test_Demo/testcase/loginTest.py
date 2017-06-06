#coding=utf-8
import sys
sys.path.append('./interface')
import unittest,requests
from interface.LoginAPI import LoginAPI
from data_init import testData
from interface.API import MyAPI
from config.runconfig import RunConfig

class LoginTest(unittest.TestCase):

    def setUp(self):
        cfg = RunConfig()
        self.baseurl = cfg.get_base_url()
        self.user = LoginAPI(self.baseurl)
        login = testData(self.baseurl)
        self.udata = login.getUserData[0]
        self.api = MyAPI()
        self.result = ""
        # self.classifycode = ClassifyCode()
    def tearDown(self):
        print self.result

    def test_login_success(self):
        u"""登陆成功测试"""
        print "-----------------------------------running test_login_success----------------------------------------- "
        response = self.user.login_Login(self.udata['phoneNumber'], self.udata['password'])
        args = {"terminal": 2, 'password': self.udata['password'], 'phone': self.udata['phoneNumber']}
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(r['status'], 0, 'wrong')
            print r['data']['user']['id']
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args: %s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                              response.url, response.status_code, response.text))

    '''def test_login_password_wrong(self):
        u"""密码错误测试"""
        print "-----------------------------------running test_login_password_wrong----------------------------------------- "
        response = self.user.login_Login('18782943850', 'A1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ==')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(r['status'], 97)
        except:
            print 'status code:%s' % response.status_code
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
            self.assertEqual(r['status'], 98)
        except:
            print 'status code:%s' % response.status_code
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

            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))'''

    def test_login_Update_andriod(self):
        response = self.user.login_Update('andriod')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(r['status'], 0)
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % 'andriod'
            print u'响应内容: %s\n' % response.text
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

            self.assertEqual(r['status'], 0)
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % 'ios'
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    def test_login_ThirdParty_QQ(self):
        args = {'userName':  'sin', 'sex':  '1', 'thirdPartyType': '2', 'token': 'UID_E5471C281EF0A4C785B31A0A58A55342'}
        response = self.user.login_ThirdParty(args)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()

            self.assertEqual(r['status'], 0)
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n'% args
            print u'响应内容: %s\n'% response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))

    '''def test_login_ThirdParty_QQ_token_wrong(self):
        response = self.user.login_ThirdParty('', 'sin', 2, 0)
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(r['status'], 4)
        except:
            print 'status code:%s' % response.status_code

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
            self.assertEqual(r['status'], 103)
        except:
            print 'status code:%s' % response.status_code
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
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'api: %s\nstatus_code: %s\ntext: %s' % (
                              response.url, response.status_code, response.text))'''

    def test_forgetpwd(self):
        """忘记密码"""
        args = {'phoneNumber': '18782943850', 'password': '21218cca77804d2ba1922c33e0151105',
                    "code": '0000'}
        response = self.user.forgetpwd_msgCode('18782943850')
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            try:
                r = self.user.forgetpwd_modifyPwd(args)
                self.assertEqual(200, r.status_code)
            except:
                print 'url: %s\n' % r.url
                print u'状态码: %s' % r.status_code
                print u'传递的参数是: %s\n' % args
                print u'响应内容: %s\n' % r.text
        except:
            print 'url: %s\n' % response.url
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % args['phoneNumber']
            print u'响应内容: %s\n' % response.text

    '''def test_register(self):
        response = self.user.register_Register('qiuwj', '15350556639', '888888', '0000')
        args = {'username': 'qiuwj', 'password': '888888', 'code': '0000', 'phoneNumber': '15350556639'}
        try:
            self.assertEqual(200, response.status_code, 'status code:%s' % response.status_code)
            r = response.json()
            self.assertEqual(r['status'], 0)
        except:
            print u'状态码: %s' % response.status_code
            print u'传递的参数是: %s\n' % args
            print u'响应内容: %s\n' % response.text
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                              'args:%s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                              response.url, response.status_code, response.text))'''

if __name__ == '__main__':
        unittest.main()
