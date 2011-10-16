#!/usr/bin/env VERSIONER_PYTHON_PREFER_32_BIT=yes pythonw
# encoding: utf-8
"""
mkinstance.py

Build a Plone Instance as part of an OS X installer
installation using the Unified Installer to
do the real work.

Created by Steve McMahon on 2008-06-29.
Copyright (c) 2008, Plone Foundation.
"""

MY_PYTHON = 'Python-2.6'

STANDALONE_NAME = 'zinstance'
ZEO_NAME = 'zeocluster'

import sys, os, os.path, stat, re, pipes

# OS X installer provides package path and destination
PACKAGE_PATH = sys.argv[1]
PLONE_HOME = sys.argv[2]

# Find Base Resources directory
BASE_RESOURCES = os.path.normpath( 
    os.path.join(PACKAGE_PATH, '../pythonZopePloneBase.pkg/Contents/Resources')  
  )
# add it to the path
sys.path.insert(1, BASE_RESOURCES)
# and import our custom routines
import alertDialog, askPassword, guageApp

# are we installing in admin mode?
haveRoot = os.geteuid() == 0


def die(message):
    message = "%s.\n\nThere may be useful diagnostic information in /var/log/install.log." % message
    alertDialog.show(message, 'Installation Failed')


# Figure out whether we're installing a stand-alone
# or cluster instance. Remove installer stub.
if PACKAGE_PATH.endswith('standaloneZope.pkg') or PACKAGE_PATH.endswith('standaloneZope-1.pkg'):
     installMode = 'standalone'
     instanceName = STANDALONE_NAME
     os.remove(os.path.join(PLONE_HOME,'Standalone Zope'))
elif PACKAGE_PATH.endswith('zeoCluster.pkg') or PACKAGE_PATH.endswith('zeoCluster-1.pkg'):
     installMode = 'zeo'
     instanceName = ZEO_NAME
     os.remove(os.path.join(PLONE_HOME,'ZEO Cluster'))
os.remove(os.path.join(PLONE_HOME,"Python - Zope - Plone Base"))


# diagnostics to /var/log/install.log
print "PACKAGE_PATH: %s" % PACKAGE_PATH
print "PLONE_HOME: %s" % PLONE_HOME
print "BASE_RESOURCES: %s" % BASE_RESOURCES


# ask for a password
sys.path.insert(1, BASE_RESOURCES)
password = askPassword.getPassword()

class InstallApp(guageApp.GuageApp):
    
    def doWork(self):

        self.setGuage(5, 'Unpacking binaries ...')
        # unpack binaries to PLONE_HOME
        print "Unpacking binaries to %s" % PLONE_HOME
        os.chdir(PLONE_HOME)
        status = os.system('tar jxf "%s/binaries.tar.bz2"' % BASE_RESOURCES)
        if status:
            die('Unable to unpack binaries.')
            self.Close()


        # # Make distracting directories invisible
        # # in Finder; they'll still be visible
        # # in the terminal.
        # os.system("SetFile -a V buildout-cache")
        # os.system("SetFile -a V Python*")
        # os.system("SetFile -a V Zope*")


        self.setGuage(25, 'Compiling Python modules ...')
        # binaries are distributed without .pyc files.
        # compile them.
        for d in (MY_PYTHON, 'buildout-cache', 'Zope*'):
            command = '"%s/%s/bin/python" "%s/%s/lib/%s/compileall.py" "%s" > /dev/null' % \
                (PLONE_HOME, MY_PYTHON, PLONE_HOME, MY_PYTHON,
                 MY_PYTHON.lower().replace('-', ''), os.path.join(PLONE_HOME, d))
            print command
            os.system(command)


        self.setGuage(50, 'Fixing script paths ...')
        # Walk the directory tree looking for executable files
        # with #!...python lines. Switch to use the newly installed
        # python.
        print "Fixing shbangs"
        newPython = '#!%s' % os.path.join(PLONE_HOME, MY_PYTHON, 'bin/python')
        pyshebang = re.compile(r'#!.+python[0-9.]*( *.*)$')

        count = 0
        for root, dirs, files in os.walk(PLONE_HOME):
            for cfile in files:
                fullPath = os.path.join(root, cfile)
                if os.access(fullPath, os.X_OK):
                    infile = open(fullPath, 'r')
                    s = infile.readline()
                    mo = pyshebang.match(s)
                    if mo:
                        newshebang = mo.expand("%s\\1\n" % newPython)
                        therest = infile.read()
                        outfile = open(fullPath, 'w')
                        outfile.write(newshebang)
                        outfile.write(therest)
                        outfile.close()
                        count += 1
                    infile.close()
        print "%d script shbangs fixed." % count


        # ownership fixup, if necessary
        if haveRoot:
            egid = os.getegid()
            print "Root installed detected; fixing base component ownership."
            status = os.system( 'chown root:admin "%s"' % PLONE_HOME )
            if status: 
                die('Unable to change file ownership.')
                self.Close()
            status = os.system(
        """
            chown -R root:admin "%s"/Python* \
                "%s/buildout-cache" \
                "%s"/Zope*
        """ % (PLONE_HOME, PLONE_HOME, PLONE_HOME)
            )
            if status:
                die('Unable to change file ownership.')
                self.Close()


        self.setGuage(50, 'Running Unified Installer ...')
        # change to unified installer's directory and run it
        wdir = os.path.join(BASE_RESOURCES, 'UnifiedInstaller')
        print "Changing to %s" % wdir
        os.chdir(wdir)
        print "Running install.sh from %s" % os.getcwd()

        command = """./install.sh %s \
            --skip-tool-tests --libjpeg=no --libz=no \
            --target="%s" \
            --log=%s \
            --password=%s \
            --instance="%s" """ % \
          (installMode, 
           PLONE_HOME, 
           '/tmp/install.log', 
           pipes.quote(password),
           instanceName)
        print command
        status = os.system(command)
        if status:
            die('Unified Installer Failed.')
            self.Close()


        # change to instance directory
        if installMode == 'standalone':
            os.chdir(os.path.join(PLONE_HOME, STANDALONE_NAME))
        else:
            os.chdir(os.path.join(PLONE_HOME, ZEO_NAME))

        # adminPassword.txt is a lot less useful
        # in the OS X installer.
        os.unlink('adminPassword.txt')
        
        # Set a Plone folder icon on instance folder.
        # First, decode our icon file from macbinary
        # into current directory.
        command = 'cat "%s/plonefoldericons.bin" | macbinary decode --stdin' % BASE_RESOURCES
        print command
        os.system(command)
        # mark the folder as having a custom icon
        command = "SetFile -a C ."
        print command
        os.system(command)
    

        self.Close()

app = InstallApp('Installation Progress', 'Install Plone', 'Plone Installer')
app.MainLoop()
