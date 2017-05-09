# coding=utf-8
# audio_type :串烧 4，独白2, 吐槽 1,rap
from dbManual import DBManual

class testData:
    def __init__(self):
        self.db=DBManual()


        self.login_data = [
            {'phoneNumber': 18782943850, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ',
             'id': 100001775,
             'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ5MzE3MjkzOCwiaWF0IjoxNDkzMTY5MzM4fQ.eyJpZCI6MTAwMDAxNzc1fQ.Joiw5NCcB6nklHS4QqIMjyTpKOizUzfANlHtClZ9vaM'},
            {'phoneNumber': 18109053700, 'password': 'G1dAKkZ1s34ML1Y02YoGTErwpxVzh0T5kChN5y5OTcJYAqUJfwsjkQ',
             'id': 100001776,
             'token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ5MzE5NjYzNSwiaWF0IjoxNDkzMTkzMDM1fQ.eyJpZCI6MTAwMDAxNzc2fQ.MAFfOaWGyExzSr88kg_FMb_jHE5g07_RH7Lwn-JyuHE'
             },
            {
                'id':100001811,
                'token':'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ5NDIyNjEzNywiaWF0IjoxNDk0MjIyNTM3fQ.eyJpZCI6MTAwMDAxODExfQ.ZXiaeDoQR4aAmbqU9VVP-dyjZruvgPiqIM49n3DINtU'
            }
        ]

    def getUserData(self):
        return self.login_data

    def getSongIds(self):
        songIds = self.db.getALL('song_basic_info')
        songidList=[]
        for i in range(len(songIds)):
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
            cidList.append(cids[i][0])
            # print audios[i]
        return cidList

    def getMedleyAudio(self):
        sql = 'SELECT * FROM audio_basic_info WHERE audio_duration BETWEEN 3 AND 10 '
        medleySet = self.db.getSet(sql)
        return medleySet

    def getUndoneMedley(self):
        sql = 'SELECT * FROM medley_song_info WHERE audio_id=-1 AND curr_participant_count < max_participant_count'
        medleySet = self.db.getSet(sql)
        return medleySet