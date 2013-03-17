'''
Created on 2013-1-28

@author: ccf
'''

import telnetlib
#import time
def compilecob(program):
    qa.write("compilecob " + program + "\n")
    result = qa.read_until("/tmp/fnsonlq/" + program + ".out")
    if result.count("error(s) in compilation: /fns/q/r/int/" + program):
        print "not SUCCESSFUL " + program
    else:
        print "successful " + program
host = "10.20.112.55"
user = "fnsonlq"
password = "fnsqa"
qa = telnetlib.Telnet(host)
qa.read_until("login:", 3)
qa.write(user + '\n')
qa.read_until("Password:", 3)
qa.write(password + '\n')
compilecob("BR0001")
compilecob("BR0024")
compilecob("DB24DB2")
compilecob("DB24DB22")
compilecob("DBSQLDB2")
compilecob("DBSQLDB22")
compilecob("RR0020")
compilecob("UT0110")
qa.close()