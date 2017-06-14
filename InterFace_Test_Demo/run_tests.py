#coding:utf-8
import os,sys
# sys.path.append('./interface')
sys.path.append('testcase')
import HTMLTestRunner
import unittest
from testcase import *
from config.CaseMode import CaseConfig
import logging
import mail

if __name__ == "__main__":
    print "---------------------------------------start-----------------------------------------"
    case = CaseConfig()
    caseNames = eval(case.get_case_list())
    # 运行时，先判断Log文件夹中是否已存在log.txt文件，若存在，删除
    path = os.getcwd()
    logpth = os.path.join(path, 'log')
    if not os.path.exists(logpth):
        os.mkdir(logpth)
        print logpth
    logname = os.path.join(logpth, 'log.txt')
    if os.path.exists(logname):
        os.remove(logname)

    testunit = unittest.TestSuite()
    for i in range(0, len(caseNames)):
        testunit.addTest(unittest.makeSuite(caseNames[i]))
    # nowtime = time.strftime("%Y-%m-%d@%H_%M_%S", time.localtime(time.time()))
    reportpath = os.path.join(path, 'report')
    if not os.path.exists(reportpath):
        os.mkdir(reportpath)
    filename = os.path.join(reportpath, 'reporter.html')
    fp = file(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='testcase-logintest', description='嘿啪app接口测试')

    runner.run(testunit)

    # m = mail.SendMail()
    # m.send()


