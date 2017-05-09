import time,sys
# sys.path.append('./interface')
sys.path.append('testcase')
import HTMLTestRunner
import unittest
from testcase import loginTests,userinfoTest,userErrorCheck,coreTest,accompany

# test_dir='./testcase'
# discover=unittest.defaultTestLoader.discover(test_dir,pattern='*_test.py')

if __name__=="__main__":
    print "---------------------------------------start-----------------------------------------"
    caseNames = [
        # login_test.Login_Test,
        # subject_test.Subject_Test,
        # loginTests.GetLoginTest,
        # userinfoTest.userinfoTest,
        # userErrorCheck.userErrorCheck,
        coreTest.coreTest,
        # accompany.Accompany,

    ]

    testunit = unittest.TestSuite()
    for i in range(0, len(caseNames)):
        testunit.addTest(unittest.makeSuite(caseNames[i]))

    nowtime = time.strftime("%Y-%m-%d@%H_%M_%S", time.localtime(time.time()))
    filename = 'report\\' + nowtime + "reporter.html"
    fp = file(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='testcase-logintest', description='desc')

    runner.run(testunit)