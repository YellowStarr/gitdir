#coding = utf-8
from ConfigParser import ConfigParser
import os

class CaseConfig:
    def __init__(self):
        path = os.getcwd()
        file = os.path.join(path, 'config')
        filename = os.path.join(file, 'case_list.conf')
        self.casecfg = ConfigParser()
        self.casecfg.read(filename)
        # self.casecfg.get('run_mode', 'run_mode')

    def get_case_file(self):
        # case_file = []
        casefile = self.casecfg.get('case_list', 'casefile')
        return casefile

    def get_result_file(self):
        return self.casecfg.get('case_list', 'resultfile')

    def get_excel_config(self):
        excel_Dict = {
            'CASE_NO': int(self.casecfg.get('excel_config', 'CASE_NO')),
            'INTERFACE': int(self.casecfg.get('excel_config', 'INTERFACE_NAME')),
            'CASE_TITLE': int(self.casecfg.get('excel_config', 'CASE_TITLE')),
            'URL': int(self.casecfg.get('excel_config', 'URL')),
            'METHOD': int(self.casecfg.get('excel_config', 'METHOD')),
            'FORESETTING': int(self.casecfg.get('excel_config', 'FORESETTING')),
            'REQUEST': int(self.casecfg.get('excel_config', 'REQUEST')),
            'ACTUAL_RESPONSE': int(self.casecfg.get('excel_config', 'ACTUAL_RESPONSE')),
            'TEST_RESULT': int(self.casecfg.get('excel_config', 'TEST_RESULT')),
            'EXPECTED_RESPONSE': int(self.casecfg.get('excel_config', 'EXPECTED_RESPONSE')),
            'TEST_DATETIME': int(self.casecfg.get('excel_config', 'TEST_DATETIME'))
        }
        return excel_Dict
