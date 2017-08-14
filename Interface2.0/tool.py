# -*-coding=utf-8 -*-
"""包含功能：插入本地数据库测试用例，拉取数据库测试结果写入excel"""
from dbManual import DBManual
from handleExcel import HandleExcel
from config import CaseMode

class tool:
    def __init__(self):
        self.db = DBManual()
        self.cxe = self.db.connect_casedb()  # 获取cur

    def insertCase(self, tablename, params):
        """
        批量插入用例case
        :param tablename: 表名
        :param params: 用例case，必须是数组类
        :return:
        """
        sql = "insert into "+tablename+" (case_no,args,url) values (%s,%s,%s)"
        self.cxe.executemany(sql, params)

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


#print result
if __name__ == "__main__":
    r = {}
    t = tool()
    # t.insertCase('user_case', params)
    '''register_data = t.select_result('register_case')
    register_result = t.trans_list(register_data)
    login_data = t.select_result('login_case')
    login_result = t.trans_list(login_data)
    r['register'] = register_result
    r['login'] = login_result
    t.write_to_excel(r)
    t.cls()'''

    params = [
        (19, '{"phoneNumber":"1878294381"}', '/sms/register/mobile'),
        (20, '{"phoneNumber":"18782943855","password":"88888","platform":"iOS","clientVersion":"2.0","registerSmsCode":"0000","registerSmsId":""}', '/sms/register/mobile'),
        (21, '{"phoneNumber":"18782943854","password":"88888888888888888","platform":"iOS","clientVersion":"2.0","registerSmsCode":"0000","registerSmsId":""}', '/sms/register/mobile'),
        (22, '{"phoneNumber":"18782943856","password":"888888888+./88888","platform":"iOS","clientVersion":"2.0","registerSmsCode":"0000","registerSmsId":""}', '/sms/register/mobile'),
    ]
    t.insertCase('register_case', params)
    t.cls()

   



