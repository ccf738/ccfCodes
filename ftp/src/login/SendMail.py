#coding=utf-8
'''
Created on 2013-2-6

@author: ccf
'''
import time
import os.path
import smtplib
from email.Header import Header
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
#############
mailto_list=["1056872606@qq.com"]
mail_host="smtp.sina.com"
mail_user="ccf738"
mail_pass="827385!"
mail_postfix="sina.com"

def send_mail(to_list,sub,content,attfiles):
    '''
    to_list:who you want send mail to
    sub:subject
    content:
    send_mail("aaa@126.com","sub","content")
    '''
    AttInstance = MIMEMultipart()  #creare an instance with attachment
    text_msg = MIMEText(content,'plain','utf-8')
    AttInstance.attach(text_msg)
    if attfiles:
        for attfile in attfiles:
            basename = os.path.basename(attfile)
            att = MIMEText(open(attfile, 'rb').read(), 'base64', 'gb2312')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename=%s' % basename.encode('gb2312')
            AttInstance.attach(att)
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    AttInstance['Subject'] = Header(sub, 'utf-8')
    AttInstance['From'] = me
    AttInstance['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, AttInstance.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    localtime = time.strftime('%Y%m%d',time.localtime())
    subject = localtime + "bancs版本更新" 
    files = [u"D:\\20130205版本清单.xlsx",u"D:\\罗格.txt",u"D:\\20130205版本清单.rar"]
    if send_mail(mailto_list,subject,"don't repley",files):
        print "send successfully"
    else:
        print "failed"