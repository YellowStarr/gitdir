#coding=utf-8
import sys
sys.path.append('./interface')
import unittest,requests
from interface.LoginAPI import LoginAPI
from interface.DiscoverAPI import DiscoverAPI
from interface.API import MyAPI
from interface.CoreAPI import CoreAPI


class GetLoginTest(unittest.TestCase):

        def setUp(self):
                self.baseurl = 'http://139.129.208.77:8080'
                self.result=""


        def tearDown(self):
                print self.result


        def test_RankScore(self):
                print "------------testing test_RankScore------------------ "
                myApi=MyAPI(self.baseurl)
                postNum=myApi.getRepostNum('100000746')
                print postNum

        def test_HotSong(self):
                print "------------testing test_HotSong------------------ "
                myApi=MyAPI(self.baseurl)
                songScore=myApi.hotWork(10,2,0,0)
                print "11%s"%songScore

                songScore = myApi.hotWork(4,1,0,1)
                print u"古诗%s"%songScore

        def test_UserInfo(self):
                u"""测试用户信息接口"""
                print "------------testing test_UserInfo------------------ "
                api = MyAPI(self.baseurl)
                udata=api.getTokenAndId()
                url=self.baseurl+'/api/getUserInfo'
                r2=requests.get(url,params={'id':udata['id']})
                print r2.url
                print r2.text
                headers = {
                        "token": udata['token'],
                        "Host": "139.129.208.77:8080",
                        "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
                        "Accept": "*/*",
                        "Accept-Language": "zh-Hans-CN;q=1",
                        "Accept-Encoding": "gzip, deflate",
                        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                        "Connection": "keep-alive"
                }

                getUserInfo='http://139.129.208.77:8080/api/user/raps'
                r3 = requests.get(getUserInfo,params={'page':1,'size':3,'status':1},headers=headers)
                print r3.url
                print r3.text

        def test_modifyUserInfo(self):
        #修改个人信息 /api/modifyUserInfo
                print "------------testing test_modifyUserInfo------------------ "
                api = MyAPI(self.baseurl)

                udata=api.getTokenAndId()
                headers = {
                        "token": udata['token'],
                        "Host": "139.129.208.77:8080",
                        "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
                        "Accept": "*/*",
                        "Accept-Language":"zh-Hans-CN;q=1",
                        "Accept-Encoding": "gzip, deflate",
                        "Content-Type":"application/json; charset=UTF-8",
                        "Connection":"keep-alive"
                        }
                modifydata={'userName':"sleepyhead","personalProfile":'post data'}
                getUserInfo='http://139.129.208.77:8080/api/modifyUserInfo'
                r = requests.post(url=getUserInfo,json=modifydata,headers=headers)
                print r.text

        def test_login_success(self):
                u"""登陆成功测试"""
                print "-----------------------------------running test_login_success----------------------------------------- "
                lg=LoginAPI(self.baseurl)
                result2 = lg.login_Login('18782943850','G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ==')
                self.assertEqual(result2['status'],0)
                print result2['data']['user']['id']

        def test_login_password_wrong(self):
                u'''密码错误测试'''
                print "-----------------------------------running test_login_password_wrong----------------------------------------- "
                lg=LoginAPI(self.baseurl)
                result=lg.login_Login()
                if result['status'] != 0:
                        print result['msg'].encode('utf-8')
                result2 = lg.login_Login('18782943850','888888')
                self.assertEqual(result2['status'],999)
                # print result2['data']['user']['id']
        def test_register_success(self):
                print "-----------------------------------running test_register_phone_exists----------------------------------------- "
                lg = LoginAPI(self.baseurl)
                register = lg.register_Register("qiuwjqq", "18782943850", "8888", "1111")
                print register['msg']
                self.assertEqual(register['status'], 111)

        def test_register_phone_exists(self):
                u"""手机已注册"""
                print "-----------------------------------running test_register_phone_exists----------------------------------------- "
                lg = LoginAPI(self.baseurl)
                r=lg.register_msgCode('18109053700')
                print r['status']
                register=lg.register_Register("qiuwjqq","18109053700","8888","1111")
                print register['msg']
                self.assertEqual(register['status'],111)

        def test_update(self):
                lg = CoreAPI(self.baseurl)
                result2 = lg.core_Listen('100000770','eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ5MzAwMDM4OSwiaWF0IjoxNDkyOTk2Nzg5fQ.eyJpZCI6MTAwMDAxNzc1fQ.pX0FcCiQq22j2XeZBMttLylHxAJQEU201LmWEWxyh7s')
                # print result2['data']['discover'][0]['data'][0]['shareCount']
        def test_hot_music(self):
                lg = CoreAPI(self.baseurl)
                lg.core_Hot_Music('raps')

        def test_del_music(self):
                lg = CoreAPI(self.baseurl)
                result2 = lg.core_Del_Music('raps',100000770,'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ5MzA5MDgyMCwiaWF0IjoxNDkzMDg3MjIwfQ.eyJpZCI6MTAwMDAxNzc2fQ.D4RuiAN_DZqhSucgRpXKu9hGbwz0YnR5ddX12T6TbfA')
                # print result2['data']['discover'][0]['data'][0]['shareCount']
        def test_get_medley(self):
                lg = CoreAPI(self.baseurl)
                lg.core_getMedley()
if __name__ == '__main__':
        unittest.main()

