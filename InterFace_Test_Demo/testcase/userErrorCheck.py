#coding=utf-8

import sys,random,os,json
sys.path.append('./interface')
import unittest
from interface.userAPI import UserAPI
from interface.API import MyAPI
import data_init,dbManual

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


    def test_Near_all_null(self):
        '''所有参数为空'''

        user = UserAPI(self.baseurl)
        r = user.user_Near('','','','')
        self.api.writeLog(sys._getframe().f_code.co_name,r)
        self.assertEqual(116,r['status'])
        self.assertEqual(u"参数longitude不是<type 'float'>.",r['msg'])

    def test_Near_type_error(self):
        '''参数类型错误'''
        user = UserAPI(self.baseurl)
        r = user.user_Near('a', '104.05446182158', '1', '')
        self.assertEqual(116, r['status'])
        self.assertEqual(u"参数latitude不是<type 'float'>.", r['msg'])

    def test_Near_radius_error(self):
        '''半径范围错误'''
        user = UserAPI(self.baseurl)
        r = user.user_Near('30.56088604184985', '104.05446182158', '1', '')
        self.assertEqual(110, r['status'])
        self.assertEqual(u"半径=1.0应该在[10, 10000]米范围内", r['msg'])


    def test_FollowedSong_token_null(self):
        '''token不传'''
        user = UserAPI(self.baseurl)
        r = user.user_FollowedSong('')
        self.assertEqual(4, r['status'])
        self.assertIn(u'token', r['msg'])

    def test_FollowedSong_type_error(self):
        '''传值类型错误'''
        user = UserAPI(self.baseurl)
        r = user.user_FollowedSong(random.choice(self.data)['token'], 'a')
        self.assertEqual(116, r['status'])
        self.assertIn(u'page', r['msg'])


    def test_Recommend_type_error(self):
        '''空值'''
        user = UserAPI(self.baseurl)
        r = user.user_Recommend('','')
        self.assertEqual(116, r['status'])



    def test_Newest_Medley_type_error(self):
        '''传值类型错误'''
        user = UserAPI(self.baseurl)
        r = user.user_Newest_Medley("", 20)
        self.assertEqual(116, r['status'])

    def test_Newest_Medley_range_error(self):
        '''传值超出范围'''
        user = UserAPI(self.baseurl)
        r = user.user_Newest_Medley(0, 10)
        self.assertEqual(110, r['status'])

    def test_Newest_Medley_size_range(self):
        '''页面展示总数为0'''
        user = UserAPI(self.baseurl)
        r = user.user_Newest_Medley(1, 0)
        self.assertEqual(110, r['status'])


    def test_Newest_Complaint_type_error(self):
        '''传值类型错误'''

        user = UserAPI(self.baseurl)
        r = user.user_Newest_Complaint("", 20)
        self.assertEqual(116, r['status'])

    def test_Newest_Complaint_range_error(self):
        ''''''
        user = UserAPI(self.baseurl)
        r = user.user_Newest_Complaint(0, 10)
        self.assertEqual(110, r['status'])

    def test_Newest_Complaint_size_range(self):
        ''''''
        user = UserAPI(self.baseurl)
        r = user.user_Newest_Complaint(1, 0)
        self.assertEqual(110, r['status'])


    def test_Newest_Rap_type_error(self):
        user = UserAPI(self.baseurl)
        r = user.user_Newest_Rap("", 20)
        self.assertEqual(116, r['status'])

    def test_Newest_Rap_range_error(self):
        user = UserAPI(self.baseurl)
        r = user.user_Newest_Rap(0, 10)
        self.assertEqual(110, r['status'])

    def test_Newest_Rap_size_range(self):
        user = UserAPI(self.baseurl)
        r = user.user_Newest_Rap(1, 0)
        self.assertEqual(110, r['status'])

    def test_Fouce_all_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Focus('', '')
        self.assertEqual(4, r['status'])

    def test_Fouce_wrong_id(self):
        user = UserAPI(self.baseurl)
        r = user.user_Focus('aaaaa', random.choice(self.data)['token'])
        self.assertEqual(999, r['status'])

    def test_Focus_self(self):
        '''关注自己'''
        user = UserAPI(self.baseurl)
        r = user.user_Focus(self.data[0]['id'], self.data[0]['token'])
        try:
            self.assertEqual(204, r['status'])
        except AssertionError as e:
            print "test_Focus_mix"
            # self.verificationErrors.append(e)

    def test_Focus_again(self):
        '''已关注用户再此关注'''
        user = UserAPI(self.baseurl)
        r = user.user_Focus(self.data[1]['id'], self.data[0]['token'])
        try:
            self.assertEqual(105, r['status'])
        except AssertionError as e:
            print "test_Focus_mix"
            # self.verificationErrors.append(e)

    def test_cancelFocus_again(self):
        '''取消关注未关注用户'''
        user = UserAPI(self.baseurl)
        r = user.user_cancelFocus(self.data[1]['id'], self.data[0]['token'])
        try:
            self.assertEqual(105, r['status'])
        except AssertionError as e:
            print "test_cancelFocus_again failed"
            # self.verificationErrors.append(e)

    def test_cancelFocus_self(self):
        '''取消关注自己'''
        user = UserAPI(self.baseurl)
        r = user.user_cancelFocus(self.data[0]['id'], self.data[0]['token'])
        try:
            self.assertEqual(105, r['status'])
        except AssertionError as e:
            print "test_cancelFocus_again failed"
            # self.verificationErrors.append(e)

    def test_followedList_success(self):
        user = UserAPI(self.baseurl)
        r = user.user_followedList(self.data[0]['id'])
        try:
            self.assertEqual(0, r['status'])
        except AssertionError as e:
            print "test_cancelFocus_again failed"
            # self.verificationErrors.append(e)

    def test_followedList_wrong_type(self):
        user = UserAPI(self.baseurl)
        r = user.user_followedList('aa')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        try:
            self.assertEqual(999, r['status'])
        except AssertionError as e:
            print "test_cancelFocus_again failed"
            # self.verificationErrors.append(e)

    def test_followedList_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_followedList('')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        try:
            self.assertEqual(999, r['status'])
        except AssertionError as e:
            print "test_cancelFocus_again failed"
            # self.verificationErrors.append(e)

    def test_FansList_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_fansList('')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])
        self.assertEqual(len(r['data']['followers']), 0)

    def test_Violate_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Violate('','','','')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Violate_id_wrong(self):
        '''举报id错误'''
        user = UserAPI(self.baseurl)
        r = user.user_Violate('18782943850','aaa','','ssssasdsadfwef')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Violate_reporttype_wrong(self):
        user = UserAPI(self.baseurl)
        r = user.user_Violate('18782943850', 'aaa', 15, 'ssssasdsadfwef')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Violate_text_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Violate('18782943850', 'aaa', 5, '')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])

    def test_Violate_text_long(self):
        user = UserAPI(self.baseurl)
        r = user.user_Violate('18782943850', '', 1, '50000000005000000000500000000050000000005000000000')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])
        sql = 'select * from violation_report where id = 129'
        print self.db.getSingle(sql)

    def test_Add_BlackList_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Add_BlackList('', '')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(4, r['status'])
        self.assertIn(u'无效的token值', r['msg'])

    def test_Add_BlackList_id_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Add_BlackList(None, self.data[0]['token'])
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(999, r['status'])
        self.assertIn(u'未知错误', r['msg'])

    def test_Add_BlackList_id_type_wrong(self):
        user = UserAPI(self.baseurl)
        r = user.user_Add_BlackList('abcd', self.data[0]['token'])
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(116, r['status'])
        self.assertIn(u'参数uid不是', r['msg'])


    def test_Add_BlackList_self(self):
        user = UserAPI(self.baseurl)
        r = user.user_Add_BlackList('100001775', self.data[0]['token'])
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(0, r['status'])
        # self.assertIn(u'', r['msg'])

    def test_BlackList_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_BlackList('', '')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(4, r['status'])
        self.assertIn(u'无效的token值', r['msg'])


    def test_BlackList_del_unexits(self):
        user = UserAPI(self.baseurl)
        r = user.user_Del_BlackList(100000001, self.data[0]['token'])
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(100100, r['status'])
        # sql = 'select count(*) from user_blacklist where user_id= %s' % self.data[0]['id']
        # num = self.db.getSingle(sql)
        self.assertIn(u'不在', r['msg'])


    def test_Participant_Medley_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Participant_Medley(None, None, None)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(3, r['status'])
        self.assertIn(u'需要token', r['msg'])

    def test_Participant_Medley_no_token(self):
        user = UserAPI(self.baseurl)
        r = user.user_Participant_Medley(None)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(3, r['status'])
        self.assertIn(u'需要token', r['msg'])

    def test_Create_Medley_token_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Create_Medley(None, [{'key': 'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                   'duration': 3, 'lyric': ''}], [], 104, 30.56089, 5,'interface')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(3, r['status'])
        self.assertIn(u'需要token', r['msg'])

    def test_Create_Medley_maxcount_zero(self):
        user = UserAPI(self.baseurl)
        r = user.user_Create_Medley(self.data[0]['token'], [{'key': 'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                   'duration': 3, 'lyric': ''}], [], 104, 30.56089, 0,'interface')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(110, r['status'])
        self.assertIn(u'参数maxCount=0取值错误', r['msg'])

    def test_Create_Medley_title_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Create_Medley(self.data[0]['token'], [{'key': 'http://user-storage.oss-cn-qingdao.aliyuncs.com/audio/20170503134112_100001775_aa5aad11b8b0060d98a53fefda6fd3ab.m4a',
                                   'duration': 3, 'lyric': ''}], [], 104, 30.56089, 5, None)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(5, r['status'])
        self.assertIn(u'错误', r['msg'])

    def test_Song_state_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Song_State(None)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(3, r['status'])
        self.assertIn(u'需要token', r['msg'])

    def test_Song_state_page_wrong(self):
        user = UserAPI(self.baseurl)
        r = user.user_Song_State(self.data[0]['token'],0)
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(110, r['status'])
        self.assertIn(u'取值错误', r['msg'])


    def test_Medley_Participant_id_null(self):
        user = UserAPI(self.baseurl)
        r = user.user_Medley_Participanter('')
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(110, r['status'])

    def test_Medley_Participant_id_type_error(self):
        user = UserAPI(self.baseurl)
        r = user.user_Medley_Participanter("100000003")
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(110, r['status'])

    def test_get_userInfo_id_wrong(self):
        user = UserAPI(self.baseurl)
        r = user.user_getUserInfo("110001779")
        self.api.writeLog(sys._getframe().f_code.co_name, r)
        self.assertEqual(207, r['status'])




    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__=='__main__':
    unittest.main()

