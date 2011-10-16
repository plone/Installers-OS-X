#!/usr/bin/env VERSIONER_PYTHON_PREFER_32_BIT=yes pythonw

import sys

try:
    import wx
    HAVE_WX = True
except ImportError:
    HAVE_WX = False
print >> sys.stderr, "guageApp.py HAVE_WX: %s" % HAVE_WX

if HAVE_WX:
    class MyFrame(wx.Frame):
        """
        This is MyFrame.  It just shows a few controls on a wxPanel,
        and has a simple menu.
        """
        def __init__(self, parent, app):
            self.app = app
            wx.Frame.__init__(self, parent, -1, app.caption,
                              pos=(-1, -1), size=(35, 20),
                              style=wx.CAPTION)

            panel = wx.Panel(self)

            title = wx.StaticText(panel, -1, app.title)
            title.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
            title.SetSize(title.GetBestSize())
            description = wx.StaticText(panel, -1, app.message)
            description.SetSize(description.GetBestSize())

            self.guage = wx.Gauge(self, -1, 100, (110, 50), (250, 25))

            self.status = wx.StaticText(panel, -1, '')
            self.status.SetSize(self.status.GetBestSize())

            # btn = wx.Button(panel, -1, app.okText)
            # btn.SetDefault()
            # self.Bind(wx.EVT_BUTTON, self.OnClose, btn)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
            sizer.Add(description, 0, wx.LEFT | wx.RIGHT, 10)
            sizer.Add(self.guage, 0, wx.LEFT | wx.RIGHT, 10)
            sizer.Add(self.status, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
            # sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
            panel.SetSizer(sizer)
            panel.Layout()
            panel.Fit()
            self.Fit()

        def OnClose(self, evt):
            self.Close()

    class GuageApp(wx.App):

        def __init__(self, message, title, caption, okText='Cancel'):
            self.message = message
            self.title = title
            self.caption = caption
            self.okText = okText
            wx.App.__init__(self, redirect=False)

        def OnInit(self):
            self.result = None

            self.frame = MyFrame(None, self)
            self.SetTopWindow(self.frame)

            self.frame.Center(wx.BOTH)
            self.frame.Show(True)

            self.doWork()

            return True

        def Close(self):
            self.frame.Close()

        def setGuage(self, count, statusmsg=''):
            self.frame.guage.SetValue(count)
            self.frame.status.SetLabel(statusmsg)
            self.frame.Update()
            wx.Yield()

        def doWork(self):
            """ Override me """
            pass

else:  # no wx
    class GuageApp():

        def __init__(self, message, title, caption, okText='Cancel'):
            print >> sys.stderr, "Initializing Progress Guage"
            self.message = message
            self.title = title
            self.caption = caption
            self.okText = okText

        def OnInit(self):
            return True

        def Close(self):
            return

        def setGuage(self, count, statusmsg=''):
            print >> sys.stderr, "Progress Guage: %s, %s" % (count, statusmsg)

        def doWork(self):
            """ Override me """
            pass

        def MainLoop(self):
            print >> sys.stderr, "GuageApp Main Loop"
            self.doWork()


if __name__ == '__main__':

    class TestApp(GuageApp):
        def doWork(self):
            self.setGuage(5, 'Five')
            if HAVE_WX:
                wx.Sleep(1)
            self.setGuage(25, 'Twentyfive')
            if HAVE_WX:
                wx.Sleep(1)
            self.setGuage(50, 'Fifty')
            if HAVE_WX:
                wx.Sleep(1)
            self.setGuage(75, 'Seventyfive')
            if HAVE_WX:
                wx.Sleep(1)
            self.setGuage(100, 'One Hundred')
            if HAVE_WX:
                wx.Sleep(1)
            self.Close()

    app = TestApp('message', 'title', 'caption')
    app.MainLoop()
