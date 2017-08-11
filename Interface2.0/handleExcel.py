#coding=utf-8
__author__='qiuwj'
__date__='2017-07-10'

from xlutils.copy import copy

import xlrd,xlwt
import os,sys
import logging,time

class HandleExcel:
    def __init__(self,testcase):
        self.filepath = os.path.join(os.getcwd(), testcase)
        print self.filepath
        if not os.path.exists(self.filepath):
            logging.error(u'测试用例不存在，请检查用例路径')
            sys.exit()
        self.testcase = xlrd.open_workbook(self.filepath)
        self.sheets = self.testcase.sheet_names()    #获取sheets数组

    def read_by_sheetname(self,wbook,sheetname):    #按sheet名获取数据
        if sheetname not in self.sheets:
            logging.error(u'sheet不存在，请检查sheet名')
            sys.exit()
        else:
            table = wbook.sheet_by_name(sheetname)
            print type(wbook)
            return table

    def read_testcase(self,sheetname):    #获取每行测试用例,返回用例数组
        table = self.read_by_sheetname(self.testcase,sheetname)
        rows = table.nrows
        print '%s 有 %s 条测试用例' % (sheetname, rows-1)
        # cols = table.ncols
        testcase_list = []
        for row in range(1, rows):
            case = {}
            print 'reading testcase %s' % table.cell_value(row,0)
            case['case_no'] = table.cell_value(row, 0)
            case['token'] = table.cell_value(row, 2)
            case['url'] = table.cell_value(row, 3)
            case['method'] = table.cell_value(row, 4)
            case['args'] = table.cell_value(row, 5)
            case['expcode'] = table.cell_value(row, 6)
            case['expdata'] = table.cell_value(row, 7)
            testcase_list.append(case)
        return testcase_list

    def write_result(self, workbook, sheetname, result, resultfile):    #将测试结果写入excel，传入测试用例文件，测试结果数组，及保存文件名
        """

        :param workbook: excel名
        :param sheetname: sheet名
        :param result: 结果数组 result=[{"case_no","response","result","time"}]
        :param resultfile: 保存的excel名
        :return:
        """
        testfile = xlrd.open_workbook(workbook)
        copyfile = copy(testfile)
        table = copyfile.get_sheet(sheetname)
        if not isinstance(result, list):
            logging.error(u'result 请传入数组')
            sys.exit()
        else:
            for i in range(0, len(result)):
                # row = result[i]['case_no'].split('-')[1]
                row = result[i]['case_no']
                # table.write(int(row), 8, result[i]['rcode'])
                table.write(int(row), 9, result[i]['response'])
                table.write(int(row), 11, str(result[i]['time']))
                if result[i]['result'] == 'fail':    #如果测试结果为fail 则该单元格标红
                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = 2
                    style = xlwt.XFStyle()
                    style.pattern = pattern
                    table.write(int(row), 10, 'fail', style)
                else:
                    table.write(int(row), 10, 'pass')
            print "[%s saving xls name :%s]" % (time.strftime("%Y-%m-%d %H:%M:%S"), resultfile)
            copyfile.save(resultfile)