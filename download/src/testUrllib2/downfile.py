'''
Created on 2012-7-14

@author: ccf
'''
import urllib2
def downloadfile():
    re = urllib2.Request(r'http://zhangmenshiting2.baidu.com/data2/music/13801499/13801499.mp3?xcode=d81c47c741bd706d273650a58d1b4b7f&mid=0.21028021832653')
    rs = urllib2.urlopen(re).read()
    open('those years.mp3','wb').write(rs)

if __name__ == '__main__':
    downloadfile()