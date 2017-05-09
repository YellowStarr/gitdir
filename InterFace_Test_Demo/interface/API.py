#coding=utf-8

import requests,time

class MyAPI:
    # def __init__(self):
    def hotSinger(self,listen,fans,like,repo):
        singerScore=listen+2*fans+3*like+4*repo
        return singerScore

    def hotWork(self,listen,praise,repo,collect):
        songScore=listen+2*praise+3*repo+4*collect
        return songScore

    def getTokenAndId(self):
        postdata = {'terminal': '0', 'phone': '18782943850',
                    "password": "G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ=="}
        url = self.baseurl + '/api/user/login'
        r = requests.post(url, json=postdata)
        # print r.text
        # self.assertEqual(200, r.status_code)
        data = r.json()

        if 0 == data['status']:
            token = data['data']['token']
            id = data['data']['user']['id']
            return {'token': token, 'id': id}
        else:
            return False

    def getRepostNum(self, id):
        u'''获取歌曲转发数'''
        param = {'id': id}
        url = self.baseurl + '/api/user/statistic'
        r = requests.get(url, params=param)
        print r.url
        # self.assertEqual(200, r.status_code)
        s = r.json()
        repostNum = s['data']['repostCount']
        return repostNum



    def writeLog(self,func,obj):
        t=time.strftime("%Y%m%d-%H",time.localtime())
        funct=time.strftime("%H:%M:%S",time.localtime())
        logname=r'C:\Users\uncle\PycharmProjects\InterFace_Test_Demo\Log\log%s' % t+'.txt'
        f = open(logname, 'a+')
        f.write("------------------------------------%s:%s-----------------------------------------------" % (func,funct) + '\n')
        # f.write(obj.encode('utf-8') + '\n')
        if isinstance(obj,dict):
            f.write('msg: %s' % obj['msg'].encode('utf-8') + '\n')
            f.write('status: %s' % obj['status'] + '\n')

            f.write('data: %s' % obj['data'] + '\n')
        else:
            f.write(obj + '\n')
        f.close()