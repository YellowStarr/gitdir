#coding = utf-8
from ConfigParser import ConfigParser
import os

class RunConfig:
    def __init__(self):
        path = os.getcwd()
        file = os.path.join(path, 'config')
        filename = os.path.join(file, 'httpconfig.conf')
        self.httpcfg = ConfigParser()
        self.httpcfg.read(filename)

    def get_base_url(self, islocal=0):
        if islocal == 1:
            title = 'baseurl_local'
        else:
            title = 'baseurl'
        url = self.httpcfg.get(title, 'url')
        return url

    def get_login(self, islocal=0):
        if islocal == 1:
            title = 'login_local'
        else:
            title = 'login'
        phoneNumber = self.httpcfg.get(title, 'phoneNumber')
        password = self.httpcfg.get(title, 'password')
        platform = self.httpcfg.get(title, 'platform')
        clientVersion = self.httpcfg.get(title, 'clientVersion')
        machineId = self.httpcfg.get(title, 'machineId')
        deviceId = self.httpcfg.get(title, 'deviceId')
        login = {
            "phoneNumber": phoneNumber,
            "password": password,
            "platform": platform,
            "clientVersion": clientVersion,
            "machineId": machineId
        }
        return login, deviceId
