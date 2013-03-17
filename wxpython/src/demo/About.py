import sys

import wx                  # This module uses the new wx namespace
import wx.html
import wx.lib.wxpTag

#---------------------------------------------------------------------------

class MyAboutBox(wx.Dialog):
    text = '''
<html>
<body bgcolor="#AC76DE">
<center><table bgcolor="#458154" width="100%%" cellspacing="0"
cellpadding="0" border="1">
<tr>
    <td align="center">
    <h1>wxPython %s</h1>
    (%s)<br>
    Running on Python %s<br>
    </td>
</tr>
</table>

<p><b>wxPython</b> is a Python extension module that
encapsulates the wxWindows GUI classes.</p>

<p>This demo shows off some of the capabilities
of <b>wxPython</b>.  Select items from the menu or tree control,
sit back and enjoy.  Be sure to take a peek at the source code for each
demo item so you can learn how to use the classes yourself.</p>

<p><b>wxPython</b> is brought to you by <b>Robin Dunn</b> and<br>
<b>Total Control Software,</b> Copyright (c) 1997-2011.</p>

<p>
<font size="-1">Please see <i>license.txt</i> for licensing information.</font>
</p>

<p><wxp module="wx" class="Button">
    <param name="label" value="Okay">
    <param name="id"    value="ID_OK">
</wxp></p>
</center>
</body>
</html>
'''
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About the wxPython demo',)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
        py_version = sys.version.split()[0]
        txt = self.text % (wx.VERSION_STRING,
                           ", ".join(wx.PlatformInfo[1:]),
                           py_version
                           )
        html.SetPage(txt)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)

#---------------------------------------------------------------------------



if __name__ == '__main__':
    app = wx.PySimpleApp()
    dlg = MyAboutBox(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()
	
	50131000008045940 ccf100  bbb444
	20113000008030591
	20113000008013633
    20113000008030240
	
	9430227

	
	14927 2016/11/16
	
	
	cat ccf123|xargs compilecob
	
	19913000008030761  CNY0
	
	select * FROM SORD WHERE FROM_ACCT_NO='3011300000803075'
	
	
	8060 teller 9700152 branch 31137 braft_no yc011 - yc020  10124215096694015
	cta 70131000008024825

	update invm set acct_type='3201',int_cat='0101' where key_1='0031012421509669401'

3504      0136

50113000008046098   QA DEP FOR BGD ISSUE

50131000008047120 C BGD ISSUE
50131000008044209 C DEP FOR BGD ISSUE

50131000008034541 8060 dep aaa100
1111111117
17000010


create temporary table in db2 
declare global temporary table temp_cusm(customer_name varchar(60),customer_balance decimal(17,2)) on commit preserve rows not logged

DTEP