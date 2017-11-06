#coding=utf-8
__author__ = 'qiuwj'
__date__ = '2017-07-10'

import handleExcel
from config import runconfig
# from config import CaseMode
# import time,json
from testcase import *
import os, time
from API2 import API2


class run_case:
    def __init__(self):
        self.failList = []
        self.result = []
        self.logpth = os.path.join(os.getcwd(), 'log')

    def mylog(self, func):
        logname = os.path.join(self.logpth, 'machineId.txt')
        # nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f = open(logname, 'a+')
            # print "[ %s excuting case_no: %s ] %s" % (nowtime, func, args)
        for i in func:
            f.write('%s,"%s"\n' % (func[i], i))
        # f.write('\n')
        f.close()

    '''def handl_single_interface(self, sheetname):    # 执行无依赖关系接口的函数
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
            return sheetresult'''

if __name__ == '__main__':

    # bs = business_check.business_check()
    # bs.dayranking_status_and_publish_time_check()
    '''api = API2()
    s = run_case()
    dic = {}
    for mid in range(20000001, 20015001):
        param = {"machineId": mid, "password": "", "platform": "iOS", "clientVersion": "2.0"}
        response = api.device_register(param)
        r = response.json()
        dic[mid] = r['data']['deviceId']
    s.mylog(dic)'''

    # r = register_case.register_case()
    # r.test_register_device()
    # r.test_mobile_register()

    # uc = user_case.user_case()
    # uc.test_02_my_info()
    # uc.test_04_modify_my_info()
    # uc.test_02_my_info()
    # uc.test_binding_list()
    # uc.test_delete_binding()
    # uc.test_binding_list()
    # uc.test_01_user_info()
    # uc.test_13_unfocus()

    # uc.test_12_fans_list()
    # uc.test_09_focus()
    # uc.test_12_fans_list()
    # uc.test_11_focus_again()
    # uc.test_15_blacklist()
    # uc.test_16_blacklist_again()
    # uc.test_18_unblacklist()
    # uc.test_23_banding_phone()
    # uc.test_24_banding_phone_again()
    # uc.test_25_banding_weibo()
    # uc.test_26_banding_qq_again()
    '''uc.test_18_unblacklist()

    uc.test_03_my_info_unlogin()

    uc.test_05_modify_setting()
    uc.test_06_modify_setting_wrong_value()
    uc.test_08_get_setting()
    uc.test_10_focus_list()
    uc.test_12_fans_list()

    uc.test_14_unfocus_unknown()
    uc.test_15_blacklist()
    uc.test_17_blacklist_list()
    uc.test_18_unblacklist()
    uc.test_19_banding_phone()
    uc.test_20_already_banding_phone()
    uc.test_21_banding_phone_wrong_format()
    uc.test_22_banding_phone_longer()
    uc.test_27_banding_weibo_again()
    uc.test_28_user_info_unlogin()
    uc.test_29_modify_my_info()
    uc.test_30_modify_sex_2()
    uc.test_31_modify_settings_unlogin()
    uc.test_32_focus_self()
    uc.test_33_focus_list_unlogin()
    uc.test_34_blacklist_unexist()
    uc.test_35_blacklist_self()'''

    # sc = shown_case.shown_case(1)
    '''sc.test_23_scout()
    sc.test_24_musician()
    sc.test_02_recommend_page()
    sc.test_13_newest()
    sc.test_23_scout()
    sc.test_33_voilate()
    sc.test_4_search_user()
    sc.test_5_search_user_partial()
    sc.test_6_search_opus()
    sc.test_7_hot_search_opus_english()
    sc.test_41_search_user()
    sc.test_56_search_user_english_partial()
    sc.test_57_hot_search_opus_english_partial()
    sc.test_38_feedback()
    sc.test_39_feedback_contact()
    sc.test_40_feedback_content_null()
    sc.test_42_opus_detail_comment()
    sc.test_51_opus_detail_comment()
    sc.test_58_recommend_page()
    sc.test_60_recommend_page()
    sc.test_34_voilate_type_wrong()
    sc.test_35_voilate_text_null()
    sc.test_36_voilate_id_wrong()
    sc.test_37_voilate_violateType_null()
    sc.test_52_voilate_song()
    sc.test_53_voilate_comment()
    sc.test_01_recommend()
    sc.test_recomend_unlogin()
    sc.test_8_hot_page()

    sc.test_58_recommend_page()
    sc.test_59_recommend_page()
    # print type(sc.test_59_recommend_page)
    sc.test_61_recommend_page()
    sc.test_9_hot_page()
    sc.test_10_hot_page()
    sc.test_11_hot_page()
    sc.test_12_hot_page()
    sc.test_13_newest()
    sc.test_14_newest()
    sc.test_15_newest()
    sc.test_16_newest()
    sc.test_17_newest()
    sc.test_18_rank()
    sc.test_19_rank()
    sc.test_20_rank()
    sc.test_21_rank()
    sc.test_22_rank()

    sc.test_24_musician()
    sc.test_25_musician()
    sc.test_26_musician()
    sc.test_27_musician()
    sc.test_28_musician()
    sc.test_29_musician()
    # sc.test_30_musician()
    sc.test_31_musician()
    sc.test_32_musician()
    sc.test_42_opus_detail_comment()
    sc.test_50_opus_detail_comment()

    sc.test_46_opus_detail_comment()'''


    uic = user_interactive_case.user_interactive_case()
    # uic.test_10_collect_delete_no_attach()
    uic.test_30_create_free_nomix()
    '''uic.test_29_create_virtual_singer_zero()
    uic.test_04_collect_self()
    uic.test_23_create_virtual()
    uic.test_65_share()
    uic.test_32_create_free_songduration_type_wrong()
    uic.test_35_create_free_lyric_null()
    uic.test_34_create_free_accomtype_unexist()
    uic.test_33_create_free_accomid_unexist()'''
    # uic.test_01_collect(1)
    # uic.test_10_collect_delete_no_attach()
    # uic.test_01_collect(1)
    # uic.test_10_collect_delete_no_attach()
    # uic.test_01_collect(1)
    # uic.test_10_collect_delete_no_attach()
    '''uic.test_05_collect_unlogin()
    uic.test_06_collect_opus_unexist()
    uic.test_07_collect_duplicate()
    uic.test_08_collect_delete_unlogin()
    uic.test_10_collect_delete_no_attach()
    uic.test_12_collect_delete_uncollect()
    uic.test_13_collect_list()
    uic.test_14_collect_list_with_param()
    uic.test_15_collect_list_unlogin()
    uic.test_16_collect_list_arg_type_error()
    uic.test_17_praise_opuse_without_attach()
    uic.test_19_praise_opuse_duplicate()
    uic.test_20_praise_unlogin()
    uic.test_21_praise_unexist()
    uic.test_22_praise_unexist_user()
    uic.test_24_create_virtual_without_singer()
    uic.test_25_create_virtual_without_songname()
    uic.test_26_create_virtual_lyric_length_overflow()
    uic.test_27_create_virtual_without_comurl()
    uic.test_28_create_virtual_lyric_english()
    uic.test_31_create_free_mix()

    uic.test_36_create_intel()
    uic.test_37_create_intel_songduration_negtive()
    uic.test_38_create_intel_latitude_over()
    uic.test_39_create_medley()
    uic.test_40_create_medley_max_zero()
    uic.test_41_create_medley_description_null()
    uic.test_42_modify_song_info()
    uic.test_43_modify_published_song_info()
    uic.test_44_modify_info_null()
    uic.test_45_modify_songname_overflow()
    uic.test_46_share_link()
    uic.test_47_share_link_unpublished_opusid()
    uic.test_49_share()
    uic.test_51_share()
    uic.test_54_share_list()'''
    # uic.test_57_share_delete()

    # uic.test_66_share()

    # ic = interactive_case.interactive_case(1)
    # ic.test_15_song_comment_reply()
    # ic.test_18_read_replys()
    # ic.test_30_list_self_publish_opus()
    # ic.test_29_list_self_unpublish_opus()
    # ic.test_49_delete_published_opus()
    # ic.test_60_song_detail()
    # ic.test_57_give_mark()
    # ic.test_61_song_detail()
    ''''# ic.test_48_publish_already_published()
    # ic.test_20_delete_comment_has_children()

    # ic.test_54_get_oss_audio_md5_null()
    # ic.test_55_get_oss_audio_name_null()
    # ic.test_56_get_oss_audio_name_null()
    # ic.test_33_listen_format_error()
    # ic.test_01_song_comment()
    # ic.test_05_song_comment_null()
    # ic.test_06_song_comment_overflow()
    # ic.test_07_song_comment_opusid_unexist()
    # ic.test_02_song_comment_with_pic()
    ic.test_03_song_comment_blacklist()
    ic.test_04_song_comment_unlogin()
    ic.test_08_read_song_comments()
    ic.test_09_read_song_page()
    ic.test_10_blacklist_reply()
    ic.test_11_delete_comment_self()
    ic.test_12_delete_comment_others()
    ic.test_13_composer_delete_comment()
    ic.test_14_composer_delete_comment_unexist()
    ic.test_15_song_comment_reply()
    ic.test_16_song_comment_reply_pic()
    ic.test_18_read_replys()
    ic.test_23_song_comment_praise()
    ic.test_24_song_comment_praise_again()
    ic.test_25_song_detail()
    ic.test_26_read_reply_page()
    ic.test_28_read_reply_page_turn()
    ic.test_29_list_self_unpublish_opus()
    ic.test_30_list_self_publish_opus()
    ic.test_31_listen_without_attach()
    ic.test_32_listen_without_attach_uncount()
    ic.test_34_listen_opus_id_unexist()
    ic.test_35_listen_opus_unlogin()
    ic.test_36_join_medley()
    ic.test_37_join_medley_again()
    ic.test_38_join_medley_full()
    ic.test_39_join_medley_deleted()
    ic.test_40_get_participantors()
    ic.test_41_get_participantors_unique()
    ic.test_42_unblacklist_reply()
    ic.test_43_unblacklist_comment()
    ic.test_44_publish()
    ic.test_45_publish_desc_null()
    ic.test_46_publish_image_null()
    ic.test_47_publish_songName_null()
    ic.test_49_delete_published_opus()
    ic.test_50_delete_unpublish_opus()
    ic.test_51_publish_delete()
    ic.test_52_get_oss_image()
    ic.test_53_get_oss_audio()
    ic.test_57_give_mark()
    ic.test_58_give_mark_again()
    ic.test_59_give_mark_score_negative()

    ic.test_62_song_detail()
    ic.test_63_song_detail()
    ic.test_65_song_detail()'''

    # nc = notice_case.notice_case(1)
    # nc.test_03_flag_notice()
    # nc.test_03_flag_notice()
    # nc.test_03_flag_notice()
    '''nc.test_01_unread_message_count()
    nc.test_02_unread_message_count()

    nc.test_04_flag_notice()
    nc.test_05_flag_notice()
    nc.test_06_flag_notice()
    nc.test_07_flag_like()
    nc.test_08_flag_like()
    nc.test_09_flag_like()
    nc.test_10_flag_like()
    nc.test_11_flag_comment()
    nc.test_12_flag_comment()
    nc.test_13_flag_comment()
    nc.test_14_flag_comment()
    nc.test_15_flag_share()
    nc.test_16_flag_share()
    nc.test_17_flag_share()
    nc.test_18_flag_share()'''
    # nc.test_19_clear_notice()
    '''nc.test_20_clear_comment()
    nc.test_21_clear_like()
    nc.test_22_clear_share()
    nc.test_23_read_notice()
    nc.test_24_read_notice()
    nc.test_25_read_notice()
    nc.test_26_read_notice()
    nc.test_27_read_notice()
    nc.test_28_read_notice()
    nc.test_29_read_notice()
    nc.test_30_read_notice()
    nc.test_31_read_like()
    nc.test_32_read_comment()
    nc.test_33_read_share()
    nc.test_34_unread_r()
    nc.test_35_unread_comment()
    nc.test_36_unread_like()
    nc.test_37_unread_share()'''

    # c = other_case.other_Case()
    # c.test_18_scout_list()
    # c.test_17_scout_list()
    '''c.test_01_ranking_friend()
    c.test_02_ranking_friend()
    c.test_03_ranking_friend()
    c.test_04_ranking_friend()
    c.test_05_ranking_friend()
    c.test_06_ranking_friend()
    c.test_07_ranking_friend()
    c.test_08_ranking_friend()
    c.test_09_ranking_fans()
    c.test_10_ranking_fans()
    c.test_11_ranking_fans()
    c.test_12_ranking_fans()
    c.test_13_ranking_fans()
    c.test_14_ranking_fans()
    c.test_15_ranking_fans()
    c.test_16_ranking_fans()

    c.test_18_scout_list()
    c.test_19_scout_list()
    c.test_20_scout_list()
    c.test_21_scout_list()
    c.test_22_scout_list()
    c.test_23_scout_list()
    c.test_24_scout_list()'''