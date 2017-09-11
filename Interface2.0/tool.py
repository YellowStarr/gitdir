# -*-coding:utf-8 -*-
"""包含功能：插入本地数据库测试用例，拉取数据库测试结果写入excel"""
from dbManual import DBManual
from handleExcel import HandleExcel
from config import CaseMode
import time,os
import json,MySQLdb,base64

class tool:

    def __init__(self):
        self.db = DBManual()
        self.cxe = self.db.connect_casedb()  # 获取cur
        path = os.getcwd()
        self.logpth = os.path.join(path, 'log')
        if not os.path.exists(self.logpth):
            os.mkdir(self.logpth)
        self.uid = ''
        self.h = ''

    def get_login_header(self, api, deviceId, param):
        """返回包含heipaToken 的 header"""
        header = api.get_header(deviceId=deviceId)

        if "phoneNumber" in param.keys():
            params = param
            pwd = params['password']
            encode = base64.b64encode(pwd)
            params['password'] = encode
            res = api.mobile_login(params, header)
        elif "thirdAuthToken" in param.keys():
            res = api.third_login(param['thirdPlatformType'], param, header)
        temp = res.json()
        self.uid = temp['data']['user']['userId']
        self.h = api.get_header(deviceId=deviceId, accessToken=temp['data']['token']['accessToken'])

    @property
    def get_login_id(self):
        return self.uid

    @property
    def get_header(self):
        return self.h

    def error_handle(self, cur, case_no, response, test_time, sql, errorCode=0, *param):
        ps = ''
        if param:
            for i in xrange(len(param)):

                if isinstance(param[i], dict) or isinstance(param[i], list):
                    p = str(param[i])
                    ps = ps + p
                else:
                    ps = ps + param[i]
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False)
                self.mylog(case_no, 'header：', response.headers)
                self.mylog(case_no, 'request url:', response.url)
                self.mylog(case_no, 'request json:', ps)
                self.mylog(case_no, 'response data:', d)
                assert data["errorCode"] == errorCode, u"错误信息: %s" % data['message']
                try:
                    cur.execute(sql, (ps, d[:4999], "pass", test_time, case_no))
                    print type(d)
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
                    cur.execute(sql, (ps, d[:1000], "pass", test_time, case_no))
            except AssertionError:
                cur.execute(sql, (ps, d[:1000], "fail", test_time, case_no))
        except TypeError:
            data = response.text
            cur.execute(sql, (ps, data[:1000], "fail", test_time, case_no))

    def insertCase(self, tablename, params):
        """
        批量插入用例case
        :param tablename: 表名
        :param params: 用例case，必须是数组类
        :return:
        """
        sql = "insert into "+tablename+" (case_no,args,url) values (%s,%s,%s)"
        self.cxe.executemany(sql, params)

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

    def write_to_excel(self, result):    # 将结果写到excel中
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

        if len(args) > 1:
            print "[ %s excuting case_no: %s ] %s %s" % (t, func, args[0], args[1])
            f.write("[%s excuting case_no: %s] %s %s " % (t, func, args[0], args[1]) + '\n')
        else:
            print "[ %s excuting case_no: %s ] %s" % (t, func, args)
            f.write("[%s excuting case_no: %s] %s" % (t, func, args) + '\n')
        f.write('\n')
        f.close()

    def list_dict_keys(self, dic, keyl):
        """
        将传入的字典中的键转为数组保存
        :param dic:   dict
        :param keyl: list
        :return: list
        """
        if "errorCode" in dic.keys():
            del dic['errorCode']
        if "message" in dic.keys():
            del dic['message']
        for i in dic.keys():
            keyl.append(i)
            if isinstance(dic[i], dict):
                self.list_dict_keys(dic[i], keyl)
            elif isinstance(dic[i], list):
                if len(dic[i]) > 0:
                    inner = dic[i][0]
                else:
                    continue
                if isinstance(inner, dict) or isinstance(inner, list):
                    if len(inner) > 0:
                        self.list_dict_keys(inner, keyl)
                else:
                    continue
        return keyl

    def cmpkeys(self, case_no, response_list, expect_list):
        """
        比较响应数据与期望数据键是否一致。若一致，返回False
        :param response_list:
        :param expect_list:
        :return:
        """
        minus1 = list(set(response_list).difference(set(expect_list)))
        minus2 = list(set(expect_list).difference(set(response_list)))
        diffrence = list(set(minus1).union(minus2))
        if len(minus1) != 0 or len(minus2) != 0:
            self.mylog(case_no, u"response_list: ", response_list)
            self.mylog(case_no, u"expect_list: ", expect_list)
            self.mylog(case_no, u"response_list 与 expect_list 的差异为: ", diffrence)
            return diffrence
        return False


if __name__ == "__main__":
    t = tool()
    r = {}

    index_data = t.select_result('shown_case')
    index_result = t.trans_list(index_data)
    # login_data = t.select_result('login_case')
    # login_result = t.trans_list(login_data)
    r['index'] = index_result
    # r['login'] = login_result
    # user_data = t.select_result("user_case")
    # user_result = t.trans_list(user_data)
    # r['user'] = user_result
    t.write_to_excel(r)
    t.cls()
    # 读取excel中用例内容，将用例写入数据库
    '''h = HandleExcel('casedir\\testcase.xls')
    l = h.read_testcase('index')
    param = []
    sql = """insert into shown_case (case_no, desciption, args, url) values (%s,%s,%s,%s)"""
    for i in range(len(l)):
        param.append((l[i]['CASE_NO'], l[i]['CASE_TITLE'], l[i]['REQUEST'], l[i]['URL']))

    t.insert(sql, param)
    t.cls()'''

   



