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
    register_data = t.select_result('register_case')
    register_result = t.trans_list(register_data)
    login_data = t.select_result('login_case')
    login_result = t.trans_list(login_data)
    r['register'] = register_result
    r['login'] = login_result
    t.write_to_excel(r)
    t.cls()

    '''params = [
        (12,'{"userid":6299163298503852033}','/login/:uid'),
        (2,'{"account":1878294350,"password":"888888"}','/user'),
        (3,'','/user'),
        (4,'{"userName":"cha","email":"sillyapplemi@126.com","sex":0,"birthday":"1990-09-11","emotionStatus":"","personalProfile":""}','/user'),
        (5,'{"flowPlaySettings":0,"commentBoardPrivacySettings":0,"pushSystemNoticeSettings":0,"pushLikeNoticeSettings":0,"pushCommentBoardNoticeSettings":0}','/user/setting'),
        (6,'{"uid":6299163298503852033}','/user/:uid/following?page=1&size=10&sort=default'),
        (7,'{"uid":6299163298503852033}','/user/:uid/follower?page=1&size=11&sort=default')]'''

   



