# coding=utf-8
# audio_type :串烧 4，独白2, 吐槽 1,rap
from dbManual import DBManual

class testData:
    def __init__(self):
        self.db=DBManual()
        self.login_data = [
            {'phoneNumber': 18782943850, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ',
             'id': 100001775,
             'token': '70ScZB4na1obGZKlUdetrA=='},
            {'phoneNumber': 18109053700, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ',
             'id': 100001776,
             'token': 'kmIBqtaMBT4WbNBwaGjNsA=='
             },
        ]
    @property
    def getUserData(self):
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
        audios = self.db.getALL('audio_basic_info')
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