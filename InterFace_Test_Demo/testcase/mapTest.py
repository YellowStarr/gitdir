#coding=utf-8

import sys
sys.path.append('./interface')
import unittest
from interface.mapAPI import MapAPI
from interface.API import MyAPI
import data_init, dbManual

class MapTest(unittest.TestCase):
    def setUp(self):
        self.baseurl = 'http://test.rapself.com:9091'
        d = data_init.testData()
        self.data = d.getUserData
        self.verificationErrors = []
        self.accept_next_alert = True
        self.api = MyAPI()
        self.db = dbManual.DBManual()
        self.user = MapAPI(self.baseurl)
        # self.err=[]

    def test_Near_success(self):
        latitude = 30.56088604184985
        longitude = 104.05446182158
        radius = 5000
        addition = radius/(1000*111)
        medley_sql = 'SELECT COUNT(*) FROM song_basic_info WHERE create_latitude < %s AND create_longitude <%s ' \
              'and create_latitude> %s and create_longitude >%s and song_status=1 or song_status =5 and audio_type=4'\
              % (latitude+addition, longitude+addition,latitude-addition,longitude-addition)
        complaint_sql = 'SELECT COUNT(*) FROM song_basic_info WHERE create_latitude < %s AND create_longitude <%s ' \
                     'and create_latitude> %s and create_longitude >%s and song_status=1 and audio_type=1' \
                     % (latitude + addition, longitude + addition, latitude - addition, longitude - addition)
        rap_sql = 'SELECT COUNT(*) FROM song_basic_info WHERE create_latitude < %s AND create_longitude <%s ' \
                     'and create_latitude> %s and create_longitude >%s and song_status=1 and audio_type=2' \
                     % (latitude + addition, longitude + addition, latitude - addition, longitude - addition)
        medley = self.db.getSet(medley_sql)
        complaint = self.db.getSet(medley_sql)
        rap = self.db.getSet(rap_sql)
        medleynum = medley[0][0]
        complaintnum = complaint[0][0]
        rapnum = rap[0][0]
        response = self.user.map_Near(latitude, longitude, radius, '')
        args = {'latitude': latitude, 'longitude': longitude, 'radius': radius}
        try:
            self.assertEqual(200, response.status_code)
            r = response.json()
            self.api.writeLog(sys._getframe().f_code.co_name, response.text)
            self.assertEqual(0, r['status'])
            self.assertEqual(medleynum,len(r['data']['songs']['medleys']))
            self.assertEqual(complaintnum,len(r['data']['songs']['complaints']))
            self.assertEqual(rapnum,len(r['data']['songs']['raps']))
        except:
            print 'status code:%s' % response.status_code
            raise
        finally:
            self.api.writeLog(sys._getframe().f_code.co_name,
                             'args:%s\napi: %s\nstatus_code: %s\ntext: %s' % (args,
                             response.url, response.status_code, response.text))

    '''def test_Near_all_null(self):
        """所有参数为空"""
        response = self.user.map_Near('', '', '', '')
        r = response.json()
        self.api.writeLog(sys._getframe().f_code.co_name, response.text)
        self.assertEqual(116, r['status'])
        self.assertEqual(u"参数longitude不是<type 'float'>.", r['msg'])

    def test_Near_type_error(self):
        """参数类型错误"""s
        response = self.user.map_Near('a', '104.05446182158', '1', '')
        r = response.json()
        self.assertEqual(116, r['status'])
        self.assertEqual(u"参数latitude不是<type 'float'>.", r['msg'])

    def test_Near_radius_error(self):
        """半径范围错误"""

        response = self.user.map_Near('30.56088604184985', '104.05446182158', '1', '')
        r = response.json()
        self.assertEqual(110, r['status'])
        self.assertEqual(u"半径=1.0应该在[10, 10000]米范围内", r['msg'])'''