#!/usr/bin/env VERSIONER_PYTHON_PREFER_32_BIT=yes pythonw
# encoding: utf-8
"""
dtest.py

Created by Steve McMahon on 2008-06-29.
Copyright (c) 2008, Plone Foundation.

For use with the OS X Installer.
Make sure we're not going to stomp on an
existing instance.
"""

# Messages
ABORT_TITLE = "Installation Aborted"
PLONE_HOME_EXISTS = \
"""
    %s exists and is not writable.
    
    This may mean that you previously installed
    in server mode and are now trying to update
    the same target in user mode.
    
    Either fix ownership and permissions on
    the installation target, or run the installer
    again and choose server mode.
"""
INSTANCE_EXISTS = \
"""
    %s already exists.
    
    This directory probably contains data and 
    configuration from a previous installation.

    If you do not need that data, delete it and 
    re-run the installer.
"""


import sys, os, os.path


# when invoked by installer,
# $1 is package path
# $2 is install path
PACKAGE_PATH = sys.argv[1]
print "PACKAGE_PATH: %s" % PACKAGE_PATH
PLONE_HOME = sys.argv[2]
print "PLONE_HOME: %s" % PLONE_HOME

# Find Base Resources directory
BASE_RESOURCES = os.path.normpath( 
    os.path.join(PACKAGE_PATH, '../pythonZopePloneBase.pkg/Contents/Resources')  
  )
print "BASE_RESOURCES: %s" % BASE_RESOURCES
# add it to the python path
sys.path.insert(1, BASE_RESOURCES)
import alertDialog


if os.path.exists(PLONE_HOME) and \
   not os.access(PLONE_HOME, os.W_OK | os.X_OK):
    alertDialog.show(PLONE_HOME_EXISTS % PLONE_HOME, ABORT_TITLE)
    exit(1)    
    

if PACKAGE_PATH.endswith('standaloneZope.pkg') or PACKAGE_PATH.endswith('standaloneZope-1.pkg'):
     installMode = 'standalone'
     destination = os.path.join(PLONE_HOME, 'zinstance')
elif PACKAGE_PATH.endswith('zeoCluster.pkg') or PACKAGE_PATH.endswith('zeoCluster-1.pkg'):
     installMode = 'zeo'
     destination = os.path.join(PLONE_HOME, 'zeocluster')

if os.path.exists(destination):
    alertDialog.show(INSTANCE_EXISTS % destination, ABORT_TITLE)
    sys.exit(1)