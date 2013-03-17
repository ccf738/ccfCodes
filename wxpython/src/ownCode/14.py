'''
Created on 2013-3-12

@author: ccf
'''
#!/usr/bin/env python
import wx
class Frame(wx.Frame):
    """Frame class that display's an image"""
    def __init__(self,image,parent=None,id=-1,
                 pos=wx.DefaultPosition,title="hello wxPython"):
        """create a frame instance and display image"""
        temp = image.ConvertToBitmap()
        size = temp.GetWidth(),temp.GetHeight()
        wx.Frame.__init__(self,parent,id,title,pos,size)
        self.bmp = wx.StaticBitmap(parent=self,bitmap=temp)
class App(wx.App):
    def OnInit(self):
        image = wx.Image(r'C:\Users\ccf\Desktop\cartoon\test.jpg',wx.BITMAP_TYPE_JPEG)
        self.frame = Frame(image)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
def main():
    app = App()
    app.MainLoop()
if __name__ == "__main__":
    main()