# coding=utf-8

import MySQLdb

HOST = 'rm-m5eigc4v1r5u7l4xqo.mysql.rds.aliyuncs.com'
PORT = 3306
USER = 'autorap'
PASSWD = 'TUya2016'
DB = 'rap'
TABLENAME = 'violation_report'


class DBManual:
    def __init__(self):
        print DB
        self.conn = MySQLdb.connect(host=HOST,
                                    port=PORT,
                                    user=USER,
                                    passwd=PASSWD,
                                    db=DB)
        self.cur = self.conn.cursor()

    def insertDB(self, sql, data):
        cur = self.cur
        #  insert='insert into table_test values(null,%s,%s)'
        if isinstance(data, list):
            if len(data) > 1:
                try:
                    cur.executemany(sql, data)
                    self.conn.commit()
                except MySQLdb.Error, e:
                    self.conn.rollback()
                    print 'insert into table wrong %s'% e
            elif len(data) == 1:
                d = data[0]
                try:
                    cur.execute(sql, d)
                    self.conn.commit()
                except MySQLdb.Error:
                    self.conn.rollback()
                    print "insert into table wrong"
            else:
                print 'list is null'
                # cur.close()

    def getALL(self, tablename):
        '''获取表中的全部数据'''
        cur = self.cur
        try:
            cur.execute('select * from %s' % tablename)
        except:
            print "Execute mysql wrong"
        datas = cur.fetchall()
        return datas

    def excuteSQL(self,sql):
        cur = self.cur
        try:
            n = cur.execute(sql)
            return n
        except MySQLdb.Error, e:
            print "Select a set of datas wrong %s" % e

    def getSet(self,sql):
        '''获取表中的一组'''
        cur = self.cur
        try:
            n = cur.execute(sql)
            datas = cur.fetchmany(n)
            return datas
        except MySQLdb.Error, e:
            print "Select a set of datas wrong %s" % e

    def getSingle(self, sql):
        cur = self.cur
        try:
            cur.execute(sql)
            data = cur.fetchone()
            return data
        except MySQLdb.Error, e:
            print "Execute mysql wrong %s"% e


    def closeDB(self):
        self.cur.close()
        self.conn.close()