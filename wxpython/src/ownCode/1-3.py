'''
Created on 2013-3-12

@author: ccf
'''
"""Spare.py is a starting point for a wxPython program."""   #1
import wx
class Frame(wx.Frame):#2
    pass
class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent=None,title="spare")#4
        self.frame.Show()
        self.SetTopWindow(self.frame)#5
        return True

if __name__ == "__main__":#6
    app = App()
    app.MainLoop()