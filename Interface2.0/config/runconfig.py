#coding = utf-8
from ConfigParser import ConfigParser
import os

class RunConfig:
    def __init__(self):
        path = os.getcwd()
        file = os.path.join(path, 'config')
        filename = os.path.join(file, 'httpconfig.conf')
        httpcfg = ConfigParser()
        httpcfg.read(filename)
        self.url = httpcfg.get('baseurl', 'url')

    def get_base_url(self):
        return self.url

    # def get_db(self):
        # return self.db
