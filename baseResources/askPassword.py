#!/usr/bin/env VERSIONER_PYTHON_PREFER_32_BIT=yes pythonw

"""
    Use wxWidgets (built into MacPython) to ask for a password.
    
    import askPassword
    password = askPassword.getPassword()
"""


FRAME_CAPTION = "Password Choice"
MAIN_CAPTION = """Pick an Administrative Password"""
DESCRIPTION = \
    """
    Enter the password you wish to use for the initial "admin" user
    for Zope and Plone. Please note that passwords are case-sensitive.
    You may change this password via the Zope Management Interface.
    """

USER_ID_LABEL = "User Id"
USER_ID = "admin"

PASSWORD_LABEL = "Password"
CONFIRM_LABEL = "Confirm"
OK_TEXT = "OK"
NO_MATCH_CAPTION = "Please Try Again"
NO_MATCH_MESSAGE = \
    """
    The password and confirmation must match.
    """
NO_SPACES_CAPTION = "Please Try Again"
NO_SPACES_MESSAGE = \
    """
    Passwords should not have spaces.
    """


import wx


class MyFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, title, app):
        self.app = app
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(-1, -1), size=(35, 20),
                          style= wx.CAPTION )        

        panel = wx.Panel(self)

        title = wx.StaticText(panel, -1, MAIN_CAPTION)
        title.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        title.SetSize(title.GetBestSize())

        description = wx.StaticText(panel, -1, DESCRIPTION)
        description.SetSize(description.GetBestSize())

        l0 = wx.StaticText(panel, -1, USER_ID_LABEL)
        l0.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        t0 = wx.StaticText(panel, -1, USER_ID)

        l1 = wx.StaticText(panel, -1, PASSWORD_LABEL)
        l1.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        t1 = wx.TextCtrl(panel, -1, "", size=(125, -1), style=wx.TE_PASSWORD)
        self.tc1 = t1

        l2 = wx.StaticText(panel, -1, CONFIRM_LABEL)
        l2.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        t2 = wx.TextCtrl(panel, -1, "", size=(125, -1), style=wx.TE_PASSWORD)
        self.tc2 = t2

        btn = wx.Button(panel, -1, OK_TEXT)
        btn.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.OnClose, btn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizer.Add(description, 0, wx.LEFT | wx.RIGHT, 10)
        fsizer = wx.FlexGridSizer(cols=2)
        fsizer.Add(l0, 0, wx.ALL, 10)
        fsizer.Add(t0, 0, wx.ALL, 10)
        fsizer.Add(l1, 0, wx.ALL, 10)
        fsizer.Add(t1, 0, wx.ALL, 10)
        fsizer.Add(l2, 0, wx.ALL, 10)
        fsizer.Add(t2, 0, wx.ALL, 10)
        sizer.Add(fsizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        panel.SetSizer(sizer)
        panel.Layout()
        panel.Fit()
        self.Fit()
        
        self.result = None


    def OnClose(self, evt):
        t1 = self.tc1.GetValue().strip()
        t2 = self.tc2.GetValue().strip()
        if t1 != t2:
            wx.MessageBox(NO_MATCH_MESSAGE, NO_MATCH_CAPTION, style=wx.ICON_ERROR)
            return
        if t1.find(' ') >= 0:
            wx.MessageBox(NO_SPACES_MESSAGE, NO_SPACES_CAPTION, style=wx.ICON_ERROR)
            return
        self.app.result = self.tc1.GetValue()
        self.Close()


class MyApp(wx.App):
    def OnInit(self):
        self.result = None
        
        frame = MyFrame(None, FRAME_CAPTION, self)
        self.SetTopWindow(frame)

        frame.Center(wx.BOTH)
        frame.Show(True)
        return True

def getPassword():
    app = MyApp(redirect=False)
    app.MainLoop()
    return app.result

if __name__ == '__main__':
    print getPassword()