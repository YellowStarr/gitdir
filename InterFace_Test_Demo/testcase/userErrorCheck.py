#coding=utf-8

import sys, random
sys.path.append('./interface')
import unittest, requests
from interface.userAPI import UserAPI
from interface.API import MyAPI
import data_init, dbManual

class userErrorCheck(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://139.129.208.77:8080'
        d = data_init.testData()
        self.data = d.getUserData()
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        # self.err=[]

    def test_FollowedSong_token_null(self):
        '''token不传'''
        user = UserAPI(self.baseurl)
        response = user.user_FollowedSong(None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])
        # self.assertIn(u'token', r['msg'])

    def test_FollowedSong_token_wrong(self):
        '''token不传'''
        user = UserAPI(self.baseurl)
        response = user.user_FollowedSong('')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(4, r['status'])
        # self.assertIn(u'token', r['msg'])

    def test_FollowedSong_type_error(self):
        '''传值类型错误'''
        user = UserAPI(self.baseurl)
        response = user.user_FollowedSong(random.choice(self.data)['token'], 'a')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])
        self.assertIn(u'page', r['msg'])

    def test_Recommend_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Recommend(None, None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])

    def test_Recommend_range_out(self):
        user = UserAPI(self.baseurl)
        response = user.user_Recommend(0, 10)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Recommend_type_error(self):
        user = UserAPI(self.baseurl)
        response = user.user_Recommend(1, 'a')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])

    def test_Newest_Medley_type_error(self):
        '''传值类型错误'''
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Medley("a", 20)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])

    def test_Newest_Medley_range_error(self):
        '''传值超出范围'''
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Medley(0, 10)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Newest_Medley_size_range(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Medley(1, 0)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Newest_Complaint_type_error(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Complaint("", 20)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])

    def test_Newest_Complaint_range_error(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Complaint(0, 10)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Newest_Complaint_size_range(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Complaint(1, 0)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Newest_Rap_type_error(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Rap("a", 20)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])

    def test_Newest_Rap_range_error(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Rap(0, 10)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Newest_Rap_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Newest_Rap(None, None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Fouce_token_null(self):          #关注
        user = UserAPI(self.baseurl)
        response = user.user_Focus(None, None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(4, r['status'])

    def test_Fouce_wrong_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Focus(None, random.choice(self.data)['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])

    def test_Fouce_wrong_id(self):
        user = UserAPI(self.baseurl)
        response = user.user_Focus('aaaaa', random.choice(self.data)['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])

    def test_Focus_self(self):
        user = UserAPI(self.baseurl)
        response = user.user_Focus(self.data[0]['id'], self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(204, r['status'])

    def test_Focus_again(self):
        '''已关注用户再此关注'''
        user = UserAPI(self.baseurl)
        response = user.user_Focus(self.data[1]['id'], self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(105, r['status'])

    def test_cancelFocus_unfocus(self):
        '''取消关注未关注用户'''
        user = UserAPI(self.baseurl)
        response = user.user_cancelFocus(self.data[1]['id'], self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(105, r['status'])

    def test_cancelFocus_token_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_cancelFocus(self.data[1]['id'], None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(4, r['status'])

    def test_cancelFocus_id_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_cancelFocus(None, self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])

    def test_followedList_wrong_id(self):
        user = UserAPI(self.baseurl)
        response = user.user_followedList('aa')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])

    def test_followedList_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_followedList(None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])

    def test_FansList_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_fansList(None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        # self.assertEqual(len(r['data']['followers']), 0)

    def test_FansList_id_wrong(self):
        user = UserAPI(self.baseurl)
        response = user.user_fansList('a')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(0, r['status'])
        self.assertEqual(len(r['data']['followers']), 0)

    def test_Violate_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Violate(None, None, None, None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])

    def test_Violate_id_wrong(self):
        """举报id错误"""
        user = UserAPI(self.baseurl)
        response = user.user_Violate('18782943850', 'aaa', '', 'ssssasdsadfwef')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])

    def test_Add_BlackList_token_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Add_BlackList('', None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])
        self.assertIn(u'无效的token值', r['msg'])

    def test_Add_BlackList_token_wrong(self):
        user = UserAPI(self.baseurl)
        response = user.user_Add_BlackList('', 'a')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(4, r['status'])
        self.assertIn(u'无效的token值', r['msg'])

    def test_Add_BlackList_id_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Add_BlackList(None, self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])
        self.assertIn(u'未知错误', r['msg'])

    def test_Add_BlackList_id_type_wrong(self):
        user = UserAPI(self.baseurl)
        response = user.user_Add_BlackList('abcd', self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])
        self.assertIn(u'参数uid不是', r['msg'])

    def test_Add_BlackList_again(self):
        user = UserAPI(self.baseurl)
        user.user_Add_BlackList(100000029, self.data[0]['token'])
        response = user.user_Add_BlackList(100000029, self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(100101, r['status'])
        self.assertIn(u'已在黑名单', r['msg'])

    def test_Add_BlackList_self(self):
        user = UserAPI(self.baseurl)
        response = user.user_Add_BlackList(self.data[0]['id'], self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])
        # self.assertIn(u'', r['msg'])

    def test_BlackList_token_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_BlackList(None, '')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])
        self.assertIn(u'需要token', r['msg'])

    def test_BlackList_del_unexsit(self):
        user = UserAPI(self.baseurl)
        response = user.user_Del_BlackList(100000001, self.data[0]['token'])
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(100100, r['status'])
        # sql = 'select count(*) from user_blacklist where user_id= %s' % self.data[0]['id']
        # num = self.db.getSingle(sql)
        self.assertIn(u'不在黑名单', r['msg'])

    def test_Participant_Medley_range_out(self):
        user = UserAPI(self.baseurl)
        response = user.user_Participant_Medley(self.data[0]['token'], 0, None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Participant_Medley_type_error(self):
        user = UserAPI(self.baseurl)
        response = user.user_Participant_Medley(self.data[0]['token'], 'a')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])

    def test_Create_Medley_token_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Create_Medley(None, [
            {'key': 'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
             'duration': 3,
             'lyric': ''}
        ], [], 104, 30.56089, 5,'interface')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])
        self.assertIn(u'需要token', r['msg'])

    def test_Create_Medley_maxcount_zero(self):
        user = UserAPI(self.baseurl)
        response = user.user_Create_Medley(self.data[0]['token'], [{'key': 'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                   'duration': 3, 'lyric': ''}], [], 104, 30.56089, 0,'interface')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])
        self.assertIn(u'参数maxCount=0取值错误', r['msg'])

    def test_Create_Medley_title_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Create_Medley(self.data[0]['token'], [{'key': 'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                   'duration': 3, 'lyric': ''}], [], 104, 30.56089, 5, '')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(5, r['status'])
        self.assertIn(u'错误', r['msg'])

    def test_Create_Medley_lalo_wrong(self):
        user = UserAPI(self.baseurl)
        response = user.user_Create_Medley(self.data[0]['token'], [{'key': 'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                   'duration': 3, 'lyric': ''}], [], -104, -30.56089, 5, '')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(112, r['status'])
        self.assertIn(u'错误', r['msg'])

    def test_Medley_Participant_id_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Medley_Participanter(None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_Medley_Participant_id_type_error(self):
        user = UserAPI(self.baseurl)
        response = user.user_Medley_Participanter("10000002a")
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(110, r['status'])

    def test_get_userInfo_id_wrong(self):
        user = UserAPI(self.baseurl)
        response = user.user_getUserInfo("110001779")
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(98, r['status'])

    def test_ModifyInfo_id_wrong(self):
        user = UserAPI(self.baseurl)
        response = user.user_ModifyInfo(self.data[0]['token'], "110001779",'sleepydog', 187829748888)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])

    def test_ModifyInfo_token_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_ModifyInfo(None, self.data[0]['id'], 'sleepydog', 187829748888)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(3, r['status'])

    def test_ModifyInfo_args_miss(self):
        headers = {
            "token": self.data[0]['token'],
            "Host": "139.129.208.77:8080",
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json;charset=UTF-8",
            "Connection": "keep-alive"
        }
        url = self.baseurl + '/api/modifyUserInfo'
        params = {'userName': 'dd', 'id': 100001775}
        response = requests.post(url, json=params, headers=headers)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(2, r['status'])

    def test_Statistic_id_wrong(self):
        user = UserAPI(self.baseurl)
        response = user.user_Statistic("110001779")
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(98, r['status'])

    def test_Statistic_id_null(self):
        user = UserAPI(self.baseurl)
        response = user.user_Statistic(None)
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(999, r['status'])

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()

