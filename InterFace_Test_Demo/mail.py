# coding:utf-8

import os
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

reportPath = os.path.join(os.getcwd(), 'report')  # 测试报告的路径
logPath = os.path.join(os.getcwd(), 'Log')
print("打印路径：")

print(reportPath)

# reportPath = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'report')

class SendMail:
    def __init__(self, recver=None):
        """接收邮件的人：list or tuple"""
        if recver is None:
            self.sendTo = ['263697396@qq.com']  # 收件人这个参数，可以是list，或者tulp，以便发送给多人
        else:
            self.sendTo = recver

    def get_report(self):  # 该函数的作用是为了在测试报告的路径下找到最新的测试报告
        dirs = os.listdir(reportPath)  #获取测试报告文件目录下的文件
        dirs.sort()
        newreportname = dirs[-1]
        print'The new report name: %s' % format(newreportname)
        return newreportname  # 返回的是测试报告的名字

    def get_log(self):
        dirs = os.listdir(logPath)
        dirs.sort()
        newlogname = dirs[-1]
        print'The log name: %s' % format(newlogname)
        return newlogname  # 返回的是测试报告的名字

    def take_messages(self):  # 该函数的目的是为了 准备发送邮件的的消息内容
        newreport = self.get_report()
        newlog = self.get_log()
        self.msg = MIMEMultipart()
        self.msg['Subject'] = '测试报告主题'  # 邮件的标题
        self.msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

        with open(os.path.join(reportPath, newreport), 'rb') as f:
            mailbody = f.read()  # 读取测试报告的内容
        html = MIMEText(mailbody, _subtype='html', _charset='utf-8')  # 将测试报告的内容放在 邮件的正文当中
        self.msg.attach(html)  # 将html附加在msg里

        # html附件    下面是将测试报告放在附件中发送
        att1 = MIMEText(mailbody, 'base64', 'gb2312')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="reporter.html"'  # 这里的filename可以任意写，写什么名字，附件的名字就是什么
        self.msg.attach(att1)

        with open(os.path.join(logPath, newlog), 'rb') as f:
            mailbody1 = f.read()  # 读取log中的内容
        html1 = MIMEText(mailbody1, _subtype='txt', _charset='utf-8')  # 将测试报告的内容放在 邮件的正文当中
        self.msg.attach(html1)  # 将html附加在msg里
        # txt附件    下面是将日志放在附件中发送
        att2 = MIMEText(mailbody1, 'base64', 'gb2312')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="log.txt"'  # 这里的filename可以任意写，写什么名字，附件的名字就是什么
        self.msg.attach(att2)

    def send(self):
        self.take_messages()
        self.msg['from'] = 'sillyapplemi@126.com'  # 发送邮件的人
        for i in range(len(self.sendTo)):
            self.msg['to'] = self.sendTo[i]     # 收件人和发送人必须这里定义一下，执行才不会报错。
        #smtp = smtplib.SMTP('smtp.163.com', 25)  # 连接服务器
        smtp = smtplib.SMTP()
        smtp.connect('smtp.126.com')
        smtp.login('sillyapplemi@126.com', 'a^2+b^2=c^2')  # 登录的用户名和密码（注意密码是设置客户端授权码，因为使用用户密码不稳听，有时无法认证成功，导致登录不上，故无法发送邮件。）
        smtp.sendmail(self.msg['from'], self.msg['to'], self.msg.as_string())  # 发送邮件
        smtp.close()
        print'sendmail success'


if __name__ == '__main__':
    sendMail = SendMail()
    sendMail.send()
