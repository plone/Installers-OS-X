#!/usr/bin/env python
# encoding: utf-8
"""
fixInitPaths.py

Fix the paths in the Plone startup item.

Created by Stephen McMahon on 2008-06-29.
Copyright (c) 2008, Plone Foundation.
"""

import sys, os, os.path

PACKAGE_PATH = sys.argv[1]
PLONE_HOME = sys.argv[2]

print sys.argv[0]

# Figure out whether we're installing a stand-alone
# or cluster instance. Remove installer stub.
if PACKAGE_PATH.endswith('standaloneStartupItem.pkg'):
    installMode = 'Plone-Standalone'
    target = 'zinstance/bin/instance'
    argument = 'start'
elif PACKAGE_PATH.endswith('clusterStartupItem.pkg'):
    installMode = 'Plone-Cluster'
    target = 'zeocluster/bin/startcluster.sh'
    argument = None

# Find Base Resources directory
BASE_RESOURCES = os.path.normpath( 
 os.path.join(PACKAGE_PATH, '../pythonZopePloneBase.pkg/Contents/Resources')  
)

sourceDir = os.path.join(BASE_RESOURCES, 'UnifiedInstaller/init_scripts/OS_X', installMode)
targetDir = '/Library/StartupItems/Plone'

print "PACKAGE_PATH: %s" % PACKAGE_PATH
print "PLONE_HOME: %s" % PLONE_HOME
print "BASE_RESOURCES: %s" % BASE_RESOURCES
print "installMode: %s" % installMode
print "sourceDir: %s" % sourceDir

print "Copying %s to %s" % (sourceDir, targetDir)
status = os.system( 'cp -R "%s" "%s"' % (sourceDir, targetDir) )
if status: sys.exit(status)

# fix permissions
os.system( 'chown -R root:wheel "%s"' % targetDir )
if status: sys.exit(status)

# rewrite init script to fix path
fn = os.path.join(targetDir, 'Plone')
f = open(fn, 'r')
script = f.read()
f.close()
script = script.replace('/opt/Plone-3.0-buildout', PLONE_HOME)
f = open(fn, 'w')
f.write(script)
f.close

status = os.system( 'chmod 755 %s' % fn )
sys.exit(status)
