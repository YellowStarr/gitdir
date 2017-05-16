import time,sys
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
        # loginTests.LoginTest,
        # userinfoTest.userinfoTest,
        # userErrorCheck.userErrorCheck,
        # coreTest.coreTest,
        # coreErrorTest.coreErrorTest,
        # accompany.Accompany,
        # searchTest.SearchTest,
        # mapTest.MapTest,
        # indexTest.IndexTest,
        # shareTest.SearchTest,
        # messageTest.MessageTest,
        indexErrorTest.IndexErrorTest,

    ]

    testunit = unittest.TestSuite()
    for i in range(0, len(caseNames)):
        testunit.addTest(unittest.makeSuite(caseNames[i]))
    # nowtime = time.strftime("%Y-%m-%d@%H_%M_%S", time.localtime(time.time()))
    filename = 'report\\reporter.html'
    fp = file(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='testcase-logintest', description='desc')

    runner.run(testunit)
    m = mail.SendMail()
    m.send()