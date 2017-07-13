#coding=utf-8
__author__ = 'qiuwj'
__date__ = '2017-07-10'

import handleExcel
import requests,logging,sys
from config import runconfig
from config import CaseMode

class run_case:
    # failcount = 0
    def __init__(self, casefilename):
        self.failList = []
        self.result = []
        self.excel = handleExcel.HandleExcel(casefilename)
        self.testcase = casefilename
        self.baseurl= runconfig.RunConfig().get_base_url()

    def handl_single_interface(self, sheetname):    #执行无依赖关系接口的函数
        sheetresult = []
        token = self.get_token()
        headers = {
            "token": token,
            "Host": self.baseurl,
            "User-Agent": "HeiPa/1.0.1 (iPhone; iOS 9.3.5; Scale/2.00)",
            "Accept": "*/*",
            "Accept-Language": "zh-Hans-CN;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        case_list = self.excel.read_testcase(sheetname)
        if len(case_list) > 0:
            for i in range(len(case_list)):
                result_dic = {}
                case_no = case_list[i]['case_no']
                url = self.baseurl+case_list[i]['url']
                args = case_list[i]['args']
                method = case_list[i]['method']
                expcod = case_list[i]['expcode']
                expdata = case_list[i]['expdata']
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
                data = r.json()
                # data = r.url

                result_dic['case_no'] = case_no
                result_dic['rcode'] = r.status_code
                result_dic['rdata'] = data
                if r.status_code != expcod or data != expdata:
                    result_dic['result'] = 'fail'
                    # self.failcount = self.failcount+1
                    self.failList.append(result_dic)
                else:
                    result_dic['result'] = 'pass'
                sheetresult.append(result_dic)
                self.result.append(result_dic)
            return sheetresult

    def get_token(self):
        url = self.baseurl.join('/api/user/login')
        postdata = {"terminal": 2, 'password': '888888', 'phone': '18782943850'}
        r = requests.post(url, json=postdata)
        if r.status_code == 200:
            data = r.json()
            token = data['data']['token']
            return token
        else:
            logging.error(u'登陆失败')
            sys.exit()

    def handle_relative_interfaces(self,sheetname):
        pass

    def get_faillist(self):    #获取失败的case的数组
        return self.failList

    def get_reuslt(self):    #获取失败的case的数组
        return self.result


print '____________________________________'
c = CaseMode.CaseConfig()
file = c.get_case_file()
r = run_case(file)
s = r.handl_single_interface('login')
handle = handleExcel.HandleExcel(file)
handle.write_result(file, 'login', s, c.get_result_file())






