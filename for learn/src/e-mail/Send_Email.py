'''
Created on 2012-9-6

@author: ccf
'''
import smtplib,config,email,sys
from email.Message import Message

def connect():
    "connect to smtp server and return a smtplib.SMTP instance object"
    server=smtplib.SMTP(config.smtpserver,config.smtpport)
    server.ehlo()
    server.login(config.smtpuser,config.smtppass)
    return server
    
def sendmessage(server,to,subj,content):
    "using server send a email"
    msg = Message()
    msg['Mime-Version']='1.0'
    msg['From']    = config.smtpuser
    msg['To']      = to
    msg['Subject'] = subj
    msg['Date']    = email.Utils.formatdate()          # curr datetime, rfc2822
    msg.set_payload(content)
    try:    
        failed = server.sendmail(config.smtpuser,to,str(msg))   # may also raise exc
    except Exception ,ex:
        print Exception,ex
        print 'Error - send failed'
    else:
        print "send success!"

if __name__=="__main__":
    #frm=raw_input('From? ').strip()
    to=raw_input('To? ').strip()
    subj=raw_input('Subj? ').strip()   
    print 'Type message text, end with line="."'
    text = ''
    while True:
        line = sys.stdin.readline()
        if line == 'end': break
        text += line
    server=connect()
    sendmessage(server,to,subj,text)
