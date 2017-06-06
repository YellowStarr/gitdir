# coding=utf-8
#!/usr/bin/python
#导入os模块
import os
#导入时间模块
import time
#导入sys模块
import sys
#追加mysql的bin目录到环境变量
sys.path.append(r'G:\MySQL\mysql-5.6.35-winx64\bin')
import MySQLdb
from config.DBConfig import DBConfig

class DBManual:
    def __init__(self):
        self.db = DBConfig().get_db()
        self.conn = MySQLdb.connect(host=self.db['host'],
                                    port=int(self.db['port']),
                                    user=self.db['user'],
                                    passwd=self.db['pwd'],
                                    db=self.db['db'])
        self.cur = self.conn.cursor()

    def backupDatabase(self):
        t = time.strftime("%Y%m%d-%H%M%S",time.localtime(time.time()))
        if not os.path.exists(r'G:\workspace\GitDir\InterFace_Test_Demo\backup'):
            os.mkdir('G:\workspace\GitDir\InterFace_Test_Demo\backup')
        # 切换到新建的文件夹中
        os.chdir('G:\workspace\GitDir\InterFace_Test_Demo\backup')
        # def tuplesql(command,server,user,passwd,db,table,filename):
        #   return (mysqlcomm,dbserver,dbuser,dbpasswd,dbname,dbtable,exportfile)
        # 定义一系列参数
        mysqlcomm = 'mysqldump'
        exportfile = 'G:\workspace\GitDir\InterFace_Test_Demo\backup\backup%s.sql'%t
        # 定义sql的格式
        sqlfromat = "%s -h%s -u%s -p%s %s  >%s"
        # 生成相应的sql语句
        sql = (sqlfromat % (mysqlcomm, self.db['host'], self.db['user'], self.db['pwd'], self.db['db'], exportfile))
        # 判断是否已经有相应的sql文件生成；如果有，就按时间重命名该文件
        if os.path.exists(exportfile):
            print(time.ctime())
            os.rename('backup1.sql', 'backup' + str(time.time()) + '.sql')
            print('backup' + str(time.time) + '.sql')
        # 执行sql并获取语句，os.system和subprocess.Popen执行该sql无效果，不知道是怎么回事，后续会继续关注
        result = os.popen(sql)
        # 对sql执行进行判断
        if result:
            print("backup completed!")
        else:
            print("I'm sorry!!!,backup failed!")

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
            print n
            return n
        except MySQLdb.Error, e:
            print "Select a set of datas wrong %s" % e

    def getSet(self, sql):
        '''获取表中的一组'''
        cur = self.cur
        try:
            n = cur.execute(sql)
            if n == None:
                return False
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