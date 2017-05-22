#coding:utf-8
import os,sys
# sys.path.append('./interface')
sys.path.append('testcase')
import HTMLTestRunner
import unittest
from testcase import *
import mail
# test_dir='./testcase'
# discover=unittest.defaultTestLoader.discover(test_dir,pattern='*_test.py')

if __name__=="__main__":
    print "---------------------------------------start-----------------------------------------"

    caseNames = [
        loginTest.LoginTest,
        userinfoTest.userinfoTest,
        # userErrorCheck.userErrorCheck,
        coreTest.coreTest,
        # coreErrorTest.coreErrorTest,
        # accompany.Accompany,
        searchTest.SearchTest,
        mapTest.MapTest,
        indexTest.IndexTest,
        shareTest.ShareTest,
        messageTest.MessageTest,
        # indexErrorTest.IndexErrorTest,
        # complexTest.ComplextTest,

    ]
    # 运行时，先判断Log文件夹中是否已存在log.txt文件，若存在，删除
    path = os.getcwd()
    logpth =os.path.join(path, 'log')
    logname = os.path.join(logpth, 'log.txt')
    if os.path.exists(logname):
        os.remove(logname)
        # os.open('log.txt', 'a+')

    testunit = unittest.TestSuite()
    for i in range(0, len(caseNames)):
        testunit.addTest(unittest.makeSuite(caseNames[i]))
    # nowtime = time.strftime("%Y-%m-%d@%H_%M_%S", time.localtime(time.time()))
    reportpath = os.path.join(path, 'report')
    filename = os.path.join(reportpath, 'reporter.html')
    fp = file(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='testcase-logintest', description='desc')

    runner.run(testunit)
    m = mail.SendMail(['1095222570@qq.com', '263697396@qq.com', '358014589@qq.com'])
    m.send()