# -*-coding:utf-8 -*-
# 伴奏接口测试，需要敏捷性，
from API2 import API2
import unittest
import random
import json
from tool import tool
from errorCodeConst import errorCodeConst
from config import runconfig
import requests


class accom_case(unittest.TestCase):

    def setUp(self, islocal=0):
        self.api = API2(islocal)
        self.t = tool()
        self.login_param, self.deviceid = runconfig.RunConfig().get_login(islocal)
        self.t.get_login_header(self.api, self.deviceid, self.login_param)
        self.ecode = errorCodeConst()

    '''def test_01_get_accom(self):
        """ 热门伴奏接口 """
        print "---------------------------executing testing:test_01_get_accom-------------------------------"
        r_list = []
        e_list = []
        expect_data = {
            "accom": [{
                "id": 0,
                "name": "",
                "url": "",
                "duration": 0,
                "size": "",
                "usageCount": 0,
                "bpm": "",
                "isCollected": 0
            }]
        }

        params = {
            'page': 2,
            'size': 10,
            'sort': 'use'
        }
        api = "/accom"
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.get(url, params=params, headers=header)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        res = self.t.list_dict_keys(data, r_list)
        exp = self.t.list_dict_keys(expect_data, e_list)
        self.t.cmpkeys("test_get_accom", res, exp)

    def test_02_get_accom_data(self):
        """ 热门伴奏接口验证数据正确性 """
        print "---------------------------executing testing:test_02_get_accom_data-------------------------------"

        params = {
            'page': 1,
            'size': 10,
            'sort': 'use'
        }
        api = "/accom"
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.get(url, params=params, headers=header)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        print json.dumps(data, ensure_ascii=False, indent=1)
        # self.assertEqual(data['data'][0]['name'], "Just Smile", "伴奏名有误")
        # self.assertEqual()

    def test_03_get_accom_category(self):
        """ 获取伴奏分类信息接口 并检查分类信息数据"""
        category_define = {
            'ec': {'enName': 'East Coast', 'cnName': '东海岸'},
            'wc': {'enName': 'West Coast', 'cnName': '西海岸'},
            'sh': {'enName': 'Southern Hip-Hop', 'cnName': '南部嘻哈'},
            'gr': {'enName': 'Gangsta Rap', 'cnName': '匪帮说唱'},
            'jh': {'enName': 'Jazz Hip Hop', 'cnName': '爵士说唱'},
            'ol': {'enName': 'Old School', 'cnName': '老派说唱'},
            'tr': {'enName': 'Trap', 'cnName': '陷阱说唱'},
            'ah': {'enName': 'Alternative Hip-Hop', 'cnName': '另类说唱'},
            'pr': {'enName': 'Pop Rap', 'cnName': '流行说唱'},
            'dr': {'enName': 'Dance Rap', 'cnName': '舞曲'}
        }
        print "---------------------------executing testing:test_03_get_accom_category-------------------------------"
        api = "/accom/category"
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.get(url, headers=header)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        category_length = len(data['data']['category'])   # 获取分类长度
        assert category_length>0, "返回的数据为空"
        category = data['data']['category']
        random_data = random.choice(category)
        cg = random_data['category']
        if category_define.has_key(cg):
            self.assertEqual(category_define[cg]['enName'], random_data['enName'])
            self.assertEqual(category_define[cg]['cnName'], random_data['chName'])
        else:
            print "has no category"'''

    def test_04_search_accom(self):
        """ 搜索伴奏 根据伴奏分类"""

        r_list = []
        e_list = []
        expect_data = {
            "accom": [{
            "id": 0,
            "name": "",
            "url": "",
            "duration": 0,
            "size": "",
            "usageCount": 0,                 # 使用次数
            "bpm": "",
            "isCollected": 0,                # 是否收藏过
            }]
        }

        print "---------------------------executing testing:test_04_search_accom-------------------------------"
        api = "/accom/search/category"
        param = {'id': 5, 'size': 50, "category": "jh"}
        isPass = False
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.get(url, params=param, headers=header)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        if data:
            accom = data['data']['accom']
        # random_data = random.choice(category)
        # cg = random_data['category']
            res = self.t.list_dict_keys(accom[0], r_list)
            exp = self.t.list_dict_keys(expect_data, e_list)
            self.t.cmpkeys("test_search_accom", res, exp)
            for i in xrange(len(accom)):
                if accom[i]['name'] == 'Life Is':
                    isPass = True
                    break
                else:
                    continue
            self.assertEqual(isPass, True)
        else:
            print "list is empty"

    '''def test_05_used_accom(self):
        """使用过的伴奏列表"""
        r_list = []
        e_list = []
        expect_data = {
            "accom": [{
                "id": 0,
                "name": "",
                "url": "",
                "duration": 0,
                "size": "",
                "usageCount": 0,  # 使用次数
                "bpm": "",
                "isCollected": 0,  # 是否收藏过
            }]
        }

        print "---------------------------executing testing:test_05_used_accom-------------------------------"
        api = "/accom/used"
        param = {'page': 1, 'size': 10}
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.get(url, params=param, headers=header)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        accom = data['data']['accom']
        if len(accom) > 0:
        # random_data = random.choice(category)
        # cg = random_data['category']
            res = self.t.list_dict_keys(data, r_list)
            exp = self.t.list_dict_keys(expect_data, e_list)
            self.t.cmpkeys("test_search_accom", res, exp)
            self.assertEqual(accom[0]['usageCount'], 5)
        else:
            print "the list is empty"

    def _06_clear_used_accom(self):
        print "---------------------------executing testing:test_06_clear_used_accom-------------------------------"
        api = "/accom/used"
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.delete(url, headers=header)
        self.assertEqual(response.status_code, 200)
        param = {'page': 1, 'size': 10}
        url = self.api.get_baseurl + api
        response = requests.get(url, params=param, headers=header)
        # self.assertEqual(response.status_code, 200)
        data = response.json()
        accom = data['data']['accom']
        self.assertEqual(len(accom), 0)

    def test_07_collect_accom(self):
        print "---------------------------executing testing:test_07_collect_accom-------------------------------"
        accomid = 2
        api = "/accom/collect/%s" % accomid
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.put(url, headers=header)
        self.assertEqual(response.status_code, 200)

        api = "/accom/collect"
        param = {'page': 1, 'size': 10}
        url = self.api.get_baseurl + api
        response = requests.get(url, params=param, headers=header)
        data = response.json()
        accom = data['data']['accom']
        for i in xrange(len(accom)):
            if accom[i]['id'] == accomid:
                self.assertEqual(accom[i]['isCollected'], 1)
                break
            else:
                continue

    def test_08_collect_accom_list(self):
        print "---------------------------executing testing:test_08_collect_accom_list-------------------------------"
        accomid = 3
        isPass = False
        api = "/accom/collect/%s" % accomid
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.put(url, headers=header)
        self.assertEqual(response.status_code, 200)

        api = "/accom/collect"
        url = self.api.get_baseurl + api
        response = requests.get(url, headers=header)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        accom = data['data']['accom']
        for i in xrange(len(accom)):
            if accom[i]['id'] == accomid:
                self.assertEqual(accom[i]['isCollected'], 1)
                isPass = True
                break
            else:
                continue
        self.assertEqual(isPass, True)

    def test_09_cancel_collect_accom(self):
        print "---------------------------executing testing:test_09_cancel_collect_accom-------------------------------"
        isPass = True
        accomid = 4
        api = "/accom/collect/%s" % accomid
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.put(url, headers=header)
        self.assertEqual(response.status_code, 200)

        api = "/accom/collect"
        url = self.api.get_baseurl + api
        response = requests.get(url, headers=header)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        accom = data['data']['accom']
        for i in xrange(len(accom)):
            if accom[i]['id'] == accomid:
                self.assertEqual(accom[i]['isCollected'], 1)
                break
            else:
                continue

        api = "/accom/collect/%s" % accomid
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.delete(url, headers=header)
        self.assertEqual(response.status_code, 200)

        api = "/accom/collect"
        url = self.api.get_baseurl + api
        response = requests.get(url, headers=header)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        accom = data['data']['accom']
        for i in xrange(len(accom)):
            if accom[i]['id'] == accomid:
                isPass = False
                break
            else:
                continue
        self.assertEqual(isPass, True)'''

    def test_10_search_accom_bpm(self):
        """ 按照bpm搜索伴奏"""
        r_list = []
        e_list = []
        expect_data = {
            "accom": [{
            "id": 0,
            "name": "",
            "url": "",
            "duration": 0,
            "size": "",
            "usageCount": 0,                 # 使用次数
            "bpm": "",
            "isCollected": 0,                # 是否收藏过
            }]
        }

        print "---------------------------executing testing:test_10_search_accom-------------------------------"
        api = "/accom/search/bpm"
        isPass = False
        param = {'bpm': 70, 'size': 50}
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.get(url, params=param, headers=header)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        if data['data']:
            accom = data['data']['accom']
        # random_data = random.choice(category)
        # cg = random_data['category']
            res = self.t.list_dict_keys(accom[0], r_list)
            exp = self.t.list_dict_keys(expect_data, e_list)
            self.t.cmpkeys("test_search_accom", res, exp)
            for i in xrange(len(accom)):
                if accom[i]['name'] == 'Pearl':
                    isPass = True
                    break
                else:
                    continue
        else:
            print "search nothing"
        self.assertEqual(isPass, True)

    '''def test_11_collect_constantly_operate(self):
        """连续收藏 取消收藏 收藏 取消收藏"""
        print "---------------------------executing testing:test_11_collect_constantly_operate-------------------------------"
        isPass = False
        accomid = 5
        api = "/accom/collect/%s" % accomid
        url = self.api.get_baseurl + api
        header = self.t.get_header
        response = requests.put(url, headers=header)   # 收藏
        self.assertEqual(response.status_code, 200)

        response = requests.delete(url, headers=header)    # 取消收藏
        self.assertEqual(response.status_code, 200)

        response = requests.put(url, headers=header)  # 收藏
        self.assertEqual(response.status_code, 200)

        response = requests.delete(url, headers=header)  # 取消收藏
        self.assertEqual(response.status_code, 200)

        response = requests.put(url, headers=header)  # 收藏
        self.assertEqual(response.status_code, 200)

        api = "/accom/collect"
        url = self.api.get_baseurl + api
        response = requests.get(url, headers=header)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        accom = data['data']['accom']
        for i in xrange(len(accom)):
            if accom[i]['id'] == accomid:
                isPass = True
                break
            else:
                continue
        self.assertEqual(isPass, True)

    # def test_12_'''

if __name__ == "__main__":
    unittest.main()

