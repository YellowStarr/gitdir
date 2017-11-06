# -*-coding:utf-8 -*-
# __author__ = "qiuwenjing"
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

    # 比较期望响应码是否等于实际响应码，将pass or fail 写入数据库
    def error_handle(self, cur, case_no, response, test_time, sql, errorCode=0, *param):
        ps = ''
        if param:
            for i in xrange(len(param)):

                if isinstance(param[i], dict) or isinstance(param[i], list):
                    p = str(param[i])
                    ps = ps + p
                else:
                    ps = ps + str(param[i])
        # _data = json.dumps(eval(ps), ensure_ascii=False, indent=1)
        try:
            data = response.json()
            try:
                d = json.dumps(data, ensure_ascii=False, indent=1)
                self.mylog(case_no, 'header：', response.headers)
                self.mylog(case_no, 'request url:', response.url)
                self.mylog(case_no, 'request json:', ps)
                self.mylog(case_no, 'response data: \n', d)
                print "\n"
                assert data["errorCode"] == errorCode, u"错误信息: %s" % data['message']
                try:
                    cur.execute(sql, (ps, d[:4999], "pass", test_time, case_no))
                    # print type(d)
                except MySQLdb.Error, e:
                    print "manual database error:%s" % e
                    cur.execute(sql, (ps, d[:1000], "pass", test_time, case_no))
            except AssertionError:
                cur.execute(sql, (ps, d[:1000], "fail", test_time, case_no))
        except TypeError:
            data = response.text
            cur.execute(sql, (ps, data[:1000], "fail", test_time, case_no))

    def data_error(self, cur, case_no, expectdata, actualdata, sql):
        self.mylog(case_no, 'database data ：%s', expectdata)
        self.mylog(case_no, 'response data：%s', actualdata)
        if expectdata != actualdata:
            cur.execute(sql, ("fail", case_no))

    # 重新定义错误处理函数，包含响应码比较，返回数据比较，日志记录
    # 需要重新写个处理mysql数据库的类函数 1）数据库连接 2）创建数据表 3）插入用例 4）更新用例 5）
    # 重新整理处理Excel的函数 1）读取excel；2）写回excel
    # 日志中包含执行的函数名，用例标题（从excel中读取），尝试将数据格式化 用json.dumps(obj, indent=1)
    def newErrorHandler(self, func_name, status_code, response, test_time, error_code=0, *param):
        """
        思路： 先比较服务器返回的status_code，之后再比较errorCode；
        如果errorCode相等，继续比较响应数据,响应中要比较字段及特定的某些值；如果errorCode不相等，则终止比较，数据库写fail。
        日志要添加function_name， case_title, response_data。打印到控制台的数据，需要格式化
        """
        pass

    def executeSQL(self, sql, params):
        self.cxe.executemany(sql, params)

    def select_result(self, tablename):
        """
        获取测试结果
        :param tablename: 表名
        :return: 返回data
        """
        sql = "select case_no,response,result,test_time from " + tablename
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
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f = open(logname, 'a+')
        if len(args) > 1:
            print "[ %s excuting case_no: %s ] %s %s" % (nowtime, func, args[0], args[1])
            f.write("[%s excuting case_no: %s] %s %s " % (nowtime, func, args[0], args[1]) + '\n')
        else:
            print "[ %s excuting case_no: %s ] %s" % (nowtime, func, args)
            f.write("[%s excuting case_no: %s] %s" % (nowtime, func, args) + '\n')
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
    data_tables = {'register_case': 'register',
                   'login_case': 'login',
                   'user_case': 'user',
                   'user_interactive_case': 'user_interactive',
                   'shown_case': 'shown',
                   'other_case': 'other',
                   'interactive_case': 'interactive',
                   'notice_case': 'notice'}
    for i in data_tables:
        index_data = t.select_result(i)
        index_result = t.trans_list(index_data)
        r[data_tables[i]] = index_result
    t.write_to_excel(r)
    t.cls()
    '''
    h = HandleExcel('casedir\\testcase.xls')
    l = h.read_testcase('user_interactive')
    param = []
    sql = """insert into user_interactive_case (case_no,interface,url,case_title,method,args) VALUES (%s,%s,%s,%s,%s,%s)"""
    for i in range(63, len(l)):
        param.append((l[i]['CASE_NO'], l[i]['INTERFACE'], l[i]['URL'], l[i]['CASE_TITLE'], l[i]['METHOD'], l[i]['REQUEST']))

    t.executeSQL(sql, param)
    t.cls()'''


   



