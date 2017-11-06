# coding = utf-8
from ConfigParser import ConfigParser
import os

class DBConfig:
    def __init__(self):
        path = os.getcwd()
        file = os.path.join(path, 'config')
        filename = os.path.join(file, 'dbconfig.conf')
        self.httpcfg = ConfigParser()
        self.httpcfg.read(filename)

    def get_casedb(self):
        host = self.httpcfg.get('casedb', 'HOST')
        port = self.httpcfg.get('casedb', 'PORT')
        user = self.httpcfg.get('casedb', 'USER')
        pwd = self.httpcfg.get('casedb', 'PASSWD')
        db = self.httpcfg.get('casedb', 'DB')
        db = {'host': host,
              'port': port,
              'user': user,
              'pwd': pwd,
              'db': db
              }
        return db

    def get_remotedb(self, islocal=0):
        if islocal == 0:
            host = self.httpcfg.get('remoutdb', 'HOST')
            port = self.httpcfg.get('remoutdb', 'PORT')
            user = self.httpcfg.get('remoutdb', 'USER')
            pwd = self.httpcfg.get('remoutdb', 'PASSWD')
            db = self.httpcfg.get('remoutdb', 'DB')
        elif islocal == 1:
            host = self.httpcfg.get('jmeterdb', 'HOST')
            port = self.httpcfg.get('jmeterdb', 'PORT')
            user = self.httpcfg.get('jmeterdb', 'USER')
            pwd = self.httpcfg.get('jmeterdb', 'PASSWD')
            db = self.httpcfg.get('jmeterdb', 'DB')
        db = {'host': host,
              'port': port,
              'user': user,
              'pwd': pwd,
              'db': db
              }
        return db
