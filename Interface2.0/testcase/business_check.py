# -*-coding:utf-8 -*-

from API2 import API2
import time, datetime
from dbManual import DBManual
from tool import tool
import random, json
from errorCodeConst import errorCodeConst
from config import runconfig


class business_check:

    def __init__(self, islocal=0):
        self.api = API2(islocal)
        self.casedb = DBManual()
        # self.sql = """update shown_case set args=%s,response=%s,result=%s,test_time=%s WHERE case_no = %s"""
        self.t = tool()
        self.login_param, self.deviceid = runconfig.RunConfig().get_login(islocal)

        self.login_param2 = {
            "phoneNumber": "18782943852",
            "password": "1234567",
            "platform": "iOS",
            "clientVersion": "2.0",
            "machineId": 100001
        }
        self.t.get_login_header(self.api, self.deviceid, self.login_param)
        self.ecode = errorCodeConst()

    def release_page_length_check(self):    # 检查每页是否20个
        header = self.t.get_header
        isPass = False
        # cur = self.casedb.connect_casedb()
        param = {'page': 1}
        response = self.api.shown_page('newest', header, param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        _data = response.json()    # json 数据
        opus_list = _data['data']['page'][0]['data']
        opus_size = len(opus_list)
        today = datetime.datetime.today()
        for i in xrange(0, opus_size):
            str_time = opus_list[i]['createTime']
            format_time = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            delta = today - format_time
            delta_days = delta.days
            if delta_days > 7:
                print "%s & %s & %s" % (opus_list[i]['songId'], opus_list[i]['createTime'], delta_days)

    def release_status_and_publish_time_check(self):    # 检查新鲜页面发布时间是否符合需求，发布时间在7日内
        header = self.t.get_header
        # isPass = False
        # cur = self.casedb.connect_casedb()
        param = {'page': 2}
        response = self.api.shown_page('newest', header, param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        _data = response.json()  # json 数据
        opus_list = _data['data']['page'][0]['data']
        opus_size = len(opus_list)
        today = datetime.datetime.today()
        for i in xrange(0, opus_size):
            str_time = opus_list[i]['createTime']
            format_time = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            delta = today - format_time
            delta_days = delta.days
            if delta_days > 7:
                print "%s & %s & %s" % (opus_list[i]['songId'], opus_list[i]['createTime'], delta_days)

    def dayranking_status_and_publish_time_check(self):    # 检查新鲜页面发布时间是否符合需求，发布时间在7日内
        header = self.t.get_header
        # isPass = False
        # cur = self.casedb.connect_casedb()
        param = {'page': 1, 'size': 40}
        response = self.api.shown_page('dayranking', header, param)
        assert response.status_code == 200, u"http响应错误，错误码 %s" % response.status_code
        _data = response.json()  # json 数据
        opus_list = _data['data']['opus']
        opus_size = len(opus_list)
        today = datetime.datetime.today()
        for i in xrange(0, opus_size):
            str_time = opus_list[i]['createTime']
            format_time = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            delta = today - format_time
            delta_days = delta.days
            print delta_days
            if delta_days > 7:
                print "%s & %s & %s" % (opus_list[i]['songId'], opus_list[i]['createTime'], delta_days)