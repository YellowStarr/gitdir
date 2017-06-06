#coding=utf-8
#伴奏接口测试
import requests
import unittest,os
from interface.API import MyAPI
from config.runconfig import RunConfig

class Accompany(unittest.TestCase):
    """this is class doc"""
    def setUp(self):
        self.api = MyAPI()
        cfg = RunConfig()
        self.baseurl = cfg.get_base_url()   #java
        # self.baseurl = 'http://139.129.208.77:9091'
        self.cateIdList = [10000001, 10000002, 10000003, 10000004, 10000005, 10000006, 10000007, 1000000, 10000009]

    def test_accompany_Classify(self):
        """this is method doc"""
        url = self.baseurl + '/api/music/type'
        # param = {'page': 1, 'size': 10}
        r = requests.get(url)
        response = r.json()
        print response['status']
        print len(response['data']['categorys'])

    def test_accompany_Search(self):
        url = self.baseurl + '/api/sort/music'
        for i in range(len(self.cateIdList)):
            print i
            param = {'categoryId': self.cateIdList[i], 'page': 1, 'size': 10}
            r = requests.get(url, params=param)
            response = r.json()
            # self.api.writeLog(sys._getframe().f_code.co_name, response)
            print response['status']
            if len(response['data']['musics']) == 0:
                print '%s has no data'%self.cateIdList[i]
            else:
                accompanys = response['data']['musics']
                for j in range(len(accompanys)):
                    self.assertNotEqual('null', accompanys[j]['musicWavSize'], 'musicsize:%s'%accompanys[j]['musicWavSize'])
                    if 0 == accompanys[j]['useCount']:
                        print 'useCount:%s'%accompanys[j]['useCount']

if __name__ == "__main__":
    unittest.main()