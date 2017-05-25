# coding=utf-8
# audio_type :串烧 4，独白2, 吐槽 1,rap
from dbManual import DBManual
<<<<<<< HEAD
from interface.LoginAPI import LoginAPI
class testData:
    def __init__(self):
        self.db = DBManual()
        self.login_data = [
            {'phoneNumber': 18782943850, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ',
             'id': 100001775},
            # {'phoneNumber': 18109053700, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ',
            #  'id': 100001776},
        ]
    @property
    def getUserData(self, url):
        lg = LoginAPI(url)
        r = lg.login_Login(self.login_data[0]['phoneNumber'], self.login_data[0]['password'])
=======
import requests

class testData:
    def __init__(self, url):
        self.baseurl = url
        self.db = DBManual()
        self.login_data = [{'phoneNumber': 18782943850, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ',
             'id': 100001775}]

    @property
    def getUserData(self):
        urls = self.baseurl+'/api/user/login'
        postdata = {"terminal": 2, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ',
                    'phone': '18782943850'}
        r = requests.post(urls, json=postdata)
>>>>>>> master
        response = r.json()
        self.login_data[0]['token'] = response['data']['token']
        return self.login_data

    @property
    def getSongIds(self):
        songIds = self.db.getALL('song_basic_info')
        songidList=[]
        for i in range(len(songIds)):
            if songIds[i][12] == 1:   #获取完成的song
                songidList.append(songIds[i][0])
        return songidList

    def getAudios(self):
        sql = 'SELECT * FROM audio_basic_info WHERE upload_time>2017-05-01'
        audios = self.db.getSet(sql)
        audioList = []
        for i in range(len(audios)):
            audioList.append(audios[i])
            # print audios[i]
        return audioList

    def getComments(self):
        cids = self.db.getALL('song_comment_info')
        cidList = []
        for i in range(len(cids)):
            if cids[i][5] == 0:    #获取未删除的评论
                cidList.append(cids[i][0])
            # print audios[i]
        return cidList

    def getMedleyAudio(self):
        sql = 'SELECT * FROM audio_basic_info WHERE audio_duration BETWEEN 3 AND 10 '
        medleySet = self.db.getSet(sql)
        return medleySet

    def getUndoneMedley(self):
        sql = 'SELECT * FROM medley_song_info WHERE curr_participant_count < max_participant_count'
        medleySet = self.db.getSet(sql)
        return medleySet