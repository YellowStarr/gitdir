#coding=utf-8

import requests, time, os


class MyAPI:
    # def __init__(self):

    def hotsinger(self, listen, fans, like, repo):
        lt = [listen, fans, like, repo]
        lt = map(float, lt)
        singerScore = lt[0] + 2*lt[1] + 3*lt[2] + 4*lt[3]
        return singerScore

    def hotWork(self, listen, praise, repo, collect):
        lt = [listen, praise, repo, collect]
        lt = map(float, lt)
        songScore = lt[0] + 2*lt[1] + 3*lt[2] + 4*lt[3]
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

        s = r.json()
        repostNum = s['data']['repostCount']
        return repostNum

    def writeLog(self, func, obj):    # 该函数的作用是新建一个log.txt，记录response.text

        '''functime = time.strftime("%H:%M:%S", time.localtime())
        path = os.getcwd()
        logname = path + '\Log\log.txt'
        f = open(logname, 'a+')
        f.write("------------------------------------%s:%s-----------------------------------------------"
                % (func, functime) + '\n')
        f.write(obj.encode('utf-8') + '\n')
        f.close()'''
        functime = time.strftime("%H:%M:%S", time.localtime())
        path = os.getcwd()

        logpth = os.path.join(path, 'log')
        logname = os.path.join(logpth, 'log.txt')
        
        f = open(logname, 'a+')
        f.write("------------------------------------%s:%s-----------------------------------------------"
                % (func, functime) + '\n')
        f.write(obj.encode('utf-8') + '\n')
        f.close()
