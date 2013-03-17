'''
Created on 2013-3-12

@author: ccf
'''
#!/usr/bin/env python

import wx,sys

class Frame(wx.Frame):
    def __init__(self,parent,id,title):
        print "frame __init__"
        wx.Frame.__init__(self,parent,id,title)
class App(wx.App):
    def __init__(self,redirect=True,filename="123321"):
        print "App __init__"
        wx.App.__init__(self,redirect, filename)
        
    def OnInit(self):
        print "OnInit"
        self.frame = Frame(parent=None,id=-1,title="Startup")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        print sys.stderr,"A pretent error message"
        return True
    def OnExit(self):
        print "OnExit"
        
if __name__ == "__main__":
    app = App(redirect=True)
    print "before main loop"
    app.MainLoop()
    print "After main loop"
