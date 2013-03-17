'''
Created on 2012-7-11

@author: ccf
'''
import telnetlib
d5 = telnetlib.Telnet('10.20.117.17')
d5.read_until("login: ")
d5.write("fnsonld5" + '\n')
d5.read_until("fnsonld5's Password: ")
d5.write("fnsonld5" + '\n')
d5.write('ls' + '\n')
d5.write('bancs.kill' + '\n')
d5.close()