#!/usr/bin/env VERSIONER_PYTHON_PREFER_32_BIT=yes pythonw

"""
    Use wxWidgets (built into MacPython) to display an alert dialog.

    import alertDialog
    alertDialog.show(message, title, caption='Alert', okText='OK')
"""

import sys

print >> sys.stderr, "Initializing alertDialog"

try:
    import wx
    HAVE_WX = True
except ImportError:
    HAVE_WX = False

print >> sys.stderr, "HAVE_WX: %s" % HAVE_WX

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

            btn = wx.Button(panel, -1, app.okText)
            btn.SetDefault()
            self.Bind(wx.EVT_BUTTON, self.OnClose, btn)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
            sizer.Add(description, 0, wx.LEFT | wx.RIGHT, 10)
            sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
            panel.SetSizer(sizer)
            panel.Layout()
            panel.Fit()
            self.Fit()

        def OnClose(self, evt):
            self.Close()

    class MyApp(wx.App):

        def __init__(self, message, title, caption, okText):
            self.message = message
            self.title = title
            self.caption = caption
            self.okText = okText
            wx.App.__init__(self, redirect=False)

        def OnInit(self):
            self.result = None

            frame = MyFrame(None, self)
            self.SetTopWindow(frame)

            frame.Center(wx.BOTH)
            frame.Show(True)
            wx.Bell()
            return True


def show(message, title, caption='Alert', okText='OK'):
    if HAVE_WX:
        app = MyApp(message, title, caption, okText)
        app.MainLoop()
    else:
        print >> sys.stderr, "%s: %s" % (sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    show(sys.argv[1], sys.argv[2], okText='OK')
