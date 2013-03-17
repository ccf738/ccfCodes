'''
Created on 2012-8-5

@author: ccf
'''
import wx

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame("HELLO WORLD",(50,50),(450,340))
        frame.Show()
        self.SetTopWindow(frame)
        return True
        
class MyFrame(wx.Frame):
    def __init__(self,title,pos,size):
        wx.Frame.__init__(self,None,-1,title,pos,size)
        menu = wx.Menu()
        menu.Append(1,"About")
        menu.AppendSeparator()
        menu.Append(2,"Exit")
        menuBar = wx.MenuBar()
        menuBar.Append(menu,"&file")
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        self.SetStatusText("ccf's own editor")
        self.Bind(wx.EVT_MENU,self.OnAbout,id = 1)
        self.Bind(wx.EVT_MENU,self.OnExit,id = 2)
    
    def OnExit(self,event):
        self.close()
    
    def OnAbout(self,event):
        wx.MessageBox("ccf's sample","about the hello world",wx.OK|wx.ICON_INFORMATION,self)
        
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
        

