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

    def get_case_list(self):
        case_list = []
        if self.get_run_mode() == '0':
            print self.get_run_mode()
            case_list = self.casecfg.get('case_list', 'run_list')
        elif self.get_run_mode() == '1':
            print self.get_run_mode()
            case_list = self.casecfg.get('case_list', 'case_all')
        return case_list

    def get_run_mode(self):
        return self.casecfg.get('run_mode', 'run_mode')