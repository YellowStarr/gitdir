# -*-coding=utf-8 -*-
"""包含功能：插入本地数据库测试用例，拉取数据库测试结果写入excel"""
from dbManual import DBManual
from handleExcel import HandleExcel
from config import CaseMode
import time,os
import json,MySQLdb

class tool:

    def __init__(self):
        self.db = DBManual()
        self.cxe = self.db.connect_casedb()  # 获取cur
        path = os.getcwd()
        self.logpth = os.path.join(path, 'log')
        if not os.path.exists(self.logpth):
            os.mkdir(self.logpth)

    def get_login_header(self, api, deviceId, param):
        """返回包含heipaToken 的 header"""
        header = api.get_header(deviceId=deviceId)
        if "phoneNumber" in param.keys():
            res = api.mobile_login(param, header)
        elif "thirdAuthToken" in param.keys():
            res = api.third_login(param['thirdPlatformType'], param, header)
        temp = res.json()
        h = api.get_header(deviceId=deviceId, accessToken=temp['data']['token']['accessToken'])
        return h

    def error_handle(self, cur, case_no, response, t, sql, errorCode=0, *param):
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                assert data["errorCode"] == errorCode, u"错误信息: %s" % data['message']
                try:
                    cur.execute(sql, (d, "pass", t, case_no))
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
            except AssertionError:
                self.mylog(case_no, 'header：', response.headers)
                self.mylog(case_no, 'request url:', response.url)
                if param:
                    self.mylog(case_no, 'request json:', param)
                self.mylog(case_no, 'response data:', d)
                cur.execute(sql, (d, "fail", t, case_no))
        except TypeError:
            data = unicode(response.text, 'utf-8')
            cur.execute(self.sql, (data, "fail", t, case_no))

    def insertCase(self, tablename, params):
        """
        批量插入用例case
        :param tablename: 表名
        :param params: 用例case，必须是数组类
        :return:
        """
        sql = "insert into "+tablename+" (case_no,args,url) values (%s,%s,%s)"
        self.cxe.executemany(sql, params)

    def updateCase(self, sql):
        """
        更新用例case
        """
        # sql = "update "+tablename+" (case_no,args,url) values (%s,%s,%s)"
        self.cxe.execute(sql)

    def insert(self, sql, params):
      
        # sql = "update "+tablename+" (case_no,args,url) values (%s,%s,%s)"
        self.cxe.executemany(sql,params)
        
    def select_result(self, tablename):
        """
        获取测试结果
        :param tablename: 表名
        :return: 返回data
        """
        sql = "select case_no,response,result,test_time from "+ tablename
        n = self.cxe.execute(sql)
        data = self.cxe.fetchmany(n)
        return data

    def trans_list(self, data):
        """
        将获取的结果转换为list，供writeExcel使用
        :param data:
        :return:
        """
        result = []
        for i in range(0, len(data)):
            dic = {}
            dic['case_no'] = data[i][0]
            d = data[i][1]
            # print d
            # print d.decode('utf-8').encode('gbk')
            dic['response'] = d
            dic['result'] = data[i][2]
            dic['time'] = data[i][3]
            result.append(dic)
        return result

    def write_to_excel(self, result):    #将结果写到excel中
        c = CaseMode.CaseConfig()
        files = c.get_case_file()
        handle = HandleExcel(files)
        handle.write_result(files, result, c.get_result_file())

    def cls(self):    #
        self.db.closeDB(self.cxe)

    def mylog(self, func, *args):
        logname = os.path.join(self.logpth, 'log.txt')
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f = open(logname, 'a+')

        if len(args) >1 :
            print "[ %s excuting %s ] %s %s" % (t, func, args[0], args[1])
            f.write("[%s excuting %s] %s %s " % (t, func, args[0], args[1]) + '\n')
        else:
            print "[ %s excuting %s ] %s" % (t, func, args)
            f.write("[%s excuting %s] %s" % (t, func, args )+ '\n')
        f.close()

#print result
if __name__ == "__main__":
    '''r = {}
    t = tool()
    #t.insertCase('user_case', params)
    register_data = t.select_result('register_case')
    register_result = t.trans_list(register_data)
    login_data = t.select_result('login_case')
    login_result = t.trans_list(login_data)
    r['register'] = register_result
    r['login'] = login_result
    user_data = t.select_result("user_case")
    user_result = t.trans_list(user_data)
    r['user'] = user_result
    t.write_to_excel(r)
    t.cls()'''

    '''sql = """insert into data_record (args,url,type) values (%s,%s,%s)"""
    params = [
        # ('),
    ]
    # ('data_record', params)
    t.cls()'''

   



