#coding=utf-8
__author__ = 'qiuwj'
__date__ = '2017-07-10'

import handleExcel
import requests,logging,sys
from config import runconfig
from config import CaseMode
import time,json


class run_case:
    # failcount = 0

    def __init__(self, casefilename):
        self.failList = []
        self.result = []
        self.excel = handleExcel.HandleExcel(casefilename)
        self.testcase = casefilename
        self.baseurl= runconfig.RunConfig().get_base_url()
        self.token = self.get_token()

    def headers_token(self, flag):    #flag为标识是否需要token
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
        return self.result


c = CaseMode.CaseConfig()
file = c.get_case_file()
r = run_case(file)
s = r.handl_single_interface('login')
handle = handleExcel.HandleExcel(file)
handle.write_result(file, 'login', s, c.get_result_file())






