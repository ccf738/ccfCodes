'''
Taken from wxPython wiki at http://wiki.wxpython.org/ModelViewController/.
Used to verify that wx.lib.pubsub uses v1 API by default since it has the
autosetuppubsubv1 module.

Notes:
- this code is probably not a good example to follow, see instead
  basic_kwargs/wx_*.py.
- this example assumes that pubsub package (in src) has been copied into
  wx.lib, and that the module _autosetuppubsubv1, in this copy, has been
  renamed by removing the prefix '_' in the file name.

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
'''

import wx

from wx.lib.pubsub import Publisher


class Model:
  def __init__(self):
    self.myMoney = 0

  def addMoney(self, value):
    self.myMoney += value
    #now tell anyone who cares that the value has been changed
    Publisher.sendMessage("MONEY CHANGED", self.myMoney)

  def removeMoney(self, value):
    self.myMoney -= value
    #now tell anyone who cares that the value has been changed
    Publisher.sendMessage("MONEY CHANGED", self.myMoney)


class View(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, parent, -1, "Main View")

    sizer = wx.BoxSizer(wx.VERTICAL)
    text = wx.StaticText(self, -1, "My Money")
    ctrl = wx.TextCtrl(self, -1, "")
    sizer.Add(text, 0, wx.EXPAND|wx.ALL)
    sizer.Add(ctrl, 0, wx.EXPAND|wx.ALL)

    self.moneyCtrl = ctrl
    ctrl.SetEditable(False)
    self.SetSizer(sizer)

  def SetMoney(self, money):
    self.moneyCtrl.SetValue(str(money))

class ChangerWidget(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, parent, -1, "Main View")

    sizer = wx.BoxSizer(wx.VERTICAL)
    self.add = wx.Button(self, -1, "Add Money")
    self.remove = wx.Button(self, -1, "Remove Money")
    sizer.Add(self.add, 0, wx.EXPAND|wx.ALL)
    sizer.Add(self.remove, 0, wx.EXPAND|wx.ALL)
    self.SetSizer(sizer)

class Controller:
  def __init__(self, app):
    self.model = Model()

    #set up the first frame which displays the current Model value
    self.view1 = View(None)
    self.view1.SetMoney(self.model.myMoney)

    #set up the second frame which allows the user to modify the Model's value
    self.view2 = ChangerWidget(self.view1)
    self.view2.add.Bind(wx.EVT_BUTTON, self.AddMoney)
    self.view2.remove.Bind(wx.EVT_BUTTON, self.RemoveMoney)
    #subscribe to all "MONEY CHANGED" messages from the Model
    #to subscribe to ALL messages (topics), omit the second argument below
    Publisher().subscribe(self.MoneyChanged, "MONEY CHANGED")

    self.view1.Show()
    self.view2.Show()

  def AddMoney(self, evt):
    self.model.addMoney(10)

  def RemoveMoney(self, evt):
    self.model.removeMoney(10)

  def MoneyChanged(self, message):
    """
    This method is the handler for "MONEY CHANGED" messages,
    which pubsub will call as messages are sent from the model.

    We already know the topic is "MONEY CHANGED", but if we
    didn't, message.topic would tell us.
    """
    self.view1.SetMoney(message.data)


if __name__ == "__main__":
    app = wx.App()
    Controller(app)
    app.MainLoop()
    