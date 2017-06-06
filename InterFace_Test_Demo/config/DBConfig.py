#coding = utf-8
from ConfigParser import ConfigParser
import os

class DBConfig:
    def __init__(self):
        path = os.getcwd()
        file = os.path.join(path, 'config')
        filename = os.path.join(file, 'dbconfig.conf')
        httpcfg = ConfigParser()
        httpcfg.read(filename)
        self.host = httpcfg.get('db', 'HOST')
        self.port = httpcfg.get('db', 'PORT')
        self.user = httpcfg.get('db', 'USER')
        self.pwd = httpcfg.get('db', 'PASSWD')
        self.db = httpcfg.get('db', 'DB')

    def get_db(self):
        db = {'host':self.host,
              'port':self.port,
              'user':self.user,
              'pwd':self.pwd,
              'db':self.db
              }
        return db