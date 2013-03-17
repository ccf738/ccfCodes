'''
Created on 2013-3-14

@author: ccf
'''
#!usr/bin/env python
import wx
class insertFrame(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,"Frame with button",size=(300,100))
        panel = wx.Panel(self)
        button = wx.Button(panel,label='close',pos=(125,10),size=(50,50))
        self.Bind(wx.EVT_BUTTON, self.onCloseMe, button)
        self.Bind(wx.EVT_CHOICE, self.onCloseWindow)
    def onCloseMe(self,event):
        self.Close(True)
    def onCloseWindow(self,event):
        self.Destroy()
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = insertFrame(parent=None,id=-1)
    frame.Show()
    app.MainLoop()