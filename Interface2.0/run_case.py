#coding=utf-8
__author__ = 'qiuwj'
__date__ = '2017-07-10'

import handleExcel
# import requests,logging,sys
from config import runconfig
# from config import CaseMode
# import time,json
from testcase import *


class run_case:
    # failcount = 0

    def __init__(self, casefilename):
        self.failList = []
        self.result = []
        self.excel = handleExcel.HandleExcel(casefilename)
        self.testcase = casefilename
        self.baseurl= runconfig.RunConfig().get_base_url()
        # self.token = self.get_token()

    '''def headers_token(self, flag):    #flag为标识是否需要token
        if flag == 1 or flag == "1":
            headers = {
                "token": self.token,
                "Host": self.baseurl,
                "Accept": "*/*",
                "Accept-Language": "zh-Hans-CN;q=1",
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/json; charset=UTF-8",
                "Connection": "keep-alive",
                "HeipaAppMessage": "deviceId=bf7c30df-68b1-4f16-b009-7e94fd128cd0;clientVersion=2.0;platform=iOS"
            }
        else:
            headers = {
                "Host": self.baseurl,
                # "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
                "Accept": "*/*",
                "Accept-Language": "zh-Hans-CN;q=1",
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/json; charset=UTF-8",
                "Connection": "keep-alive",
                "HeipaAppMessage": "deviceId=bf7c30df-68b1-4f16-b009-8e94fd128cd0;clientVersion=2.0;platform=iOS"
            }
        return headers

    def handl_single_interface(self, sheetname):    # 执行无依赖关系接口的函数
        sheetresult = []
        case_list = self.excel.read_testcase(sheetname)    # 根据传入的sheet名来获取用例
        if len(case_list) > 0:
            for i in range(len(case_list)):
                result_dic = {}
                case_no = case_list[i]['case_no']
                url = self.baseurl+case_list[i]['url']
                args = case_list[i]['args']
                method = case_list[i]['method']
                # expErrorCode = case_list[i]['expdata']
                expcod = case_list[i]['expcode']
                headers = self.headers_token(case_list[i]['token'])
                print headers
                # expdata = case_list[i]['expdata']    # 暂时先不获取expdata，根据实际用例来看，expdata可能需要去数据库抓取数据。单独处理
                if method == 'post':
                    param = eval(args)
                    r = requests.post(url, json=param, headers=headers)

                elif method == 'get':
                    if args != '':
                        param = args
                        r = requests.get(url, params=param, headers=headers)
                    else:
                        print url
                        r = requests.get(url)
                time.sleep(1)   #等待1s获取响应
                print r
                try:
                    d = r.json()
                    errorCode = d['errorCode']
                    data = json.dumps(d, ensure_ascii=False)   # json编码，解决乱码问题
                    print '------------------------------------------------------------------'
                except:
                    print "request does not return a json data"
                    d = r.text
                    data = unicode(d, 'utf-8')
                # data = r.url
                print data
                result_dic['case_no'] = case_no    # 用例编号
                result_dic['rcode'] = r.status_code    # 响应码
                #
                result_dic['rdata'] = data

                # print chardet.detect(result_dic['rdata'])#   #响应数据
                if r.status_code != expcod:    #如果返回码或响应数据与预期不符，则将结果记录为fail    or data != expdata
                    result_dic['result'] = 'fail'
                    # self.failcount = self.failcount+1
                    self.failList.append(result_dic)
                else:
                    result_dic['result'] = 'pass'
                sheetresult.append(result_dic)
                self.result.append(result_dic)
            return sheetresult

    def get_token(self):    #获取token
        url = self.baseurl+'/login'
        print url
        postdata = {
            'phoneNumber': "18782943850",
            "password": "888888",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": "100001"
        }
        r = requests.post(url, json=postdata, headers=self.headers_token(0))
        if r.status_code == 200:
            data = r.json()
            print data
            token = data['data']['token']['accessToken']
            return token
        else:
            logging.error(u'登陆失败')
            sys.exit()

    def handle_relative_interfaces(self, sheetname):    # 处理有关联关系的接口，暂未想好如何实现
        pass

    def get_faillist(self):    #获取失败的case的数组
        return self.failList

    def get_reuslt(self):    #获取失败的case的数组
        return self.result'''


'''c = CaseMode.CaseConfig()
file = c.get_case_file()
r = run_case(file)
s = r.handl_single_interface('login')
handle = handleExcel.HandleExcel(file)
handle.write_result(file, 'login', s, c.get_result_file())'''
if __name__ == '__main__':
    c = other_case.other_Case()

    sc = shown_case.shown_case()
    sc.test_4_search_user()
    sc.test_5_search_user_partial()
    sc.test_6_search_opus()
    sc.test_7_hot_search_opus_english()
    sc.test_41_search_user()
    sc.test_56_search_user_english_partial()
    sc.test_57_hot_search_opus_english_partial()

    # sc.test_23_musician()
    # sc.test_38_feedback()
    # sc.test_39_feedback_contact()
    # sc.test_40_feedback_content_null()
    # sc.test_37_voilate_violateType_null()
    # sc.test_33_voilate()
    # sc.test_34_voilate_type_wrong()
    # sc.test_35_voilate_text_null()
    # sc.test_36_voilate_id_wrong()
    # sc.test_52_voilate_song()
    # sc.test_53_voilate_comment()
    # sc.test_01_recommend()
    # sc.test_recomend_unlogin()
    # sc.test_8_hot_page()
    # sc.test_42_opus_detail_comment()
    # sc.test_46_opus_detail_comment()
    # sc.test_51_opus_detail_comment()

    # uic = user_interactive_case.user_interactive_case()
    # uic.test_30_create_free_nomix()
    # uic.test_45_modify_songname_overflow()
    # uic.test_23_create_virtual()
    # uic.test_30_create_free_nomix()

    # ic = interactive_case.interactive_case()
    # r = ic.test_36_join_medley()
    # ic.test_52_get_oss_image()
    # ic.test_25_song_detail()
    # ic.test_60_song_detail()
    # ic.test_61_song_detail()
    # ic.test_62_song_detail()
    # ic.test_63_song_detail()
    # ic.test_65_song_detail()
    # ic.test_31_listen_without_attach()
    # ic.test_32_listen_without_attach_uncount()

    # nc = notice_case.notice_case()
    # nc.test_01_unread_message_count()
    # nc.test_02_unread_message_count()
    # nc.test_03_flag_notice()
    # nc.test_04_flag_notice()
    # nc.test_05_flag_notice()
    # nc.test_06_flag_notice()
    # nc.test_07_flag_like()
    # nc.test_08_flag_like()
    # nc.test_09_flag_like()
    # nc.test_10_flag_like()
    # nc.test_11_flag_comment()
    # nc.test_12_flag_comment()
    # nc.test_13_flag_comment()
    # nc.test_14_flag_comment()
    # nc.test_15_flag_share()
    # nc.test_16_flag_share()
    # nc.test_17_flag_share()
    # nc.test_18_flag_share()
    # nc.test_19_clear_notice()
    # nc.test_20_clear_comment()
    # nc.test_21_clear_like()
    # nc.test_22_clear_share()
    # nc.test_23_read_notice()
    # nc.test_24_read_notice()
    # nc.test_25_read_notice()
    # nc.test_26_read_notice()
    # nc.test_27_read_notice()
    # nc.test_28_read_notice()
    # nc.test_29_read_notice()
    # nc.test_30_read_notice()
    # nc.test_31_read_like()
    # nc.test_32_read_comment()
    # nc.test_33_read_share()
    # nc.test_34_unread_r()
    # nc.test_35_unread_comment()
    # nc.test_36_unread_like()
    # nc.test_37_unread_share()

    # c.test_01_ranking_friend()
    # c.test_02_ranking_friend()
    # c.test_03_ranking_friend()
    # c.test_04_ranking_friend()
    # c.test_05_ranking_friend()
    # c.test_06_ranking_friend()
    # c.test_07_ranking_friend()
    # c.test_08_ranking_friend()
    # c.test_09_ranking_fans()
    # c.test_10_ranking_fans()
    # c.test_11_ranking_fans()
    # c.test_12_ranking_fans()
    # c.test_13_ranking_fans()
    # c.test_14_ranking_fans()
    # c.test_15_ranking_fans()
    # c.test_16_ranking_fans()
    # c.test_17_scout_list()
    # c.test_18_scout_list()
    # c.test_19_scout_list()
    # c.test_20_scout_list()
    # c.test_21_scout_list()
    # c.test_22_scout_list()
    # c.test_23_scout_list()
    # c.test_24_scout_list()
    # c.test_25_cancel_join_medley()
    # c.test_26_cancel_join_medley()
    # c.test_27_cancel_join_medley()










