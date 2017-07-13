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