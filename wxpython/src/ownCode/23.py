'''
Created on 2013-3-14

@author: ccf
'''
#!usr/bin/env python
import wx
import images
class toolBarFrame(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'toolBars',size=(300,200))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('White')
        statusBar = self.CreateStatusBar()
        toolBar = self.CreateToolBar()
        toolBar.AddSimpleTool(wx.NewId(),images.getNewBitmap(),"New","Long help for 'New'")
        toolBar.Realize()
        menuBar = wx.MenuBar()
    
        menu1 = wx.Menu()
        menuBar.Append(menu1,'')
        menu2 = wx.Menu()
        menu2.Append(wx.NewId()," ","Copy in status bar")
        menu2.Append(wx.NewId(),"C","")
        menu2.Append(wx.NewId(),"Paste","")
        menuBar.AppendSeparator()
        menu2.Append(wx.NewId()," ","Display Options")
        menuBar.Append(menu2,' ')
        self.SetMenuBar(menuBar)
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = toolBarFrame(parent=None,id=-1)
    frame.Show()
    app.MainLoop()    