# -*-coding=utf-8 -*-
"""包含功能：插入本地数据库测试用例，拉取数据库测试结果写入excel"""
from dbManual import DBManual
import json,chardet
from handleExcel import HandleExcel
import requests,logging,sys
from config import runconfig
from config import CaseMode


db = DBManual()
cxe = db.connect_casedb() # 获取cur
#cxe = db.connect_remotedb()
#sql = """insert into user_case (case_no,args,url) values (%s,%s,%s)"""
sql = """ select case_no,response,result,test_time from login_case """
'''params = [
    (1,'{"userid":6299163298503852033}','/login/:uid'),
    (2,'{"account":1878294350,"password":"888888"}','/user'),
    (3,'','/user'),
    (4,'{"userName":"cha","email":"sillyapplemi@126.com","sex":0,"birthday":"1990-09-11","emotionStatus":"","personalProfile":""}','/user'),
    (5,'{"flowPlaySettings":0,"commentBoardPrivacySettings":0,"pushSystemNoticeSettings":0,"pushLikeNoticeSettings":0,"pushCommentBoardNoticeSettings":0}','/user/setting'),
    (6,'{"uid":6299163298503852033}','/user/:uid/following?page=1&size=10&sort=default'),
    (7,'{"uid":6299163298503852033}','/user/:uid/follower?page=1&size=11&sort=default')
     ]'''
#cxe.executemany(sql,params)
m=cxe.execute(sql)
data = cxe.fetchmany(m)
#print data
#d = data[0]
#d = list(data)
#print type(d)
db.closeDB(cxe)
result=[]
for i in range(0,10):
    dic={}
    dic['case_no'] = data[i][0]
    d = data[i][1]
    #print type(d)
    print d
    print d.decode('utf-8').encode('gbk')
    dic['response'] = d
    dic['result'] = data[i][2]
    dic['time'] = data[i][3]
    result.append(dic)

#print result
c = CaseMode.CaseConfig()
files = c.get_case_file()
handle = HandleExcel(files)
handle.write_result(files, 'login', result, c.get_result_file())



