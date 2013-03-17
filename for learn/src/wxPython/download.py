'''
Created on 2012-8-7

@author: ccf
'''
import urllib2
  
re = urllib2.Request(r'http://img1.douban.com/view/photo/photo/public/p1649785311.jpg')  
rs = urllib2.urlopen(re).read()  
open('123.jpg', 'wb').write(rs)