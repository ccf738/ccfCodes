'''
Created on 2012-11-14

@author: ccf
'''
import os
import win32com.client
name = 'ED0010.COB'
vss = win32com.client.Dispatch('SourceSafe') 
vss.Open(r"\\10.188.208.100\SRCB Document Management\srcsafe.ini","chenchf","1234")
aaa = "$/BANCS_SRCB_SIT/BANCS/control/r/src/" + name
print aaa
#path=vss.VSSItem("$/BANCS_SRCB_SIT/BANCS/control/r/src/BR0001.COB")
path=vss.VSSItem(aaa)
path.Get("H:\\ED0010.COB")
print os.listdir("c:\\")