'''
Created on 2012-9-20

@author: ccf
'''
import os
os.chdir(r'J:/')
bf=open("b.txt","a")
FileName = open(r'C:/Users/ccf/Desktop/list','r')
for line in FileName.readlines()[0:10]:
    line.strip()
    bf.write(line)
FileName.close()
bf.close()

def getFileList(path):
        path = str(path)
        if path=="":
            return [ ]
        path = path.replace( "/","\\")
        if path[ -1] != "\\":
            path = path+"\\"
        a = os.listdir(path)
        b = [ x   for x in a if os.path.isfile(path+ x ) ]
        return b
print   getFileList( "C:\\" )