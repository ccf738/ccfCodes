'''
Created on 2012-8-14

@author: ccf
'''
import django
import sys
import string
import datetime

a = '3'
b = string.atoi(a)
date = datetime.datetime.now() + datetime.timedelta(hours = 2)
maxdate = datetime.datetime.max
print maxdate
print django.VERSION
print sys.path