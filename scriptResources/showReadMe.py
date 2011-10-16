#!/usr/bin/env python
# encoding: utf-8
"""
showReadMe.py

Created by Steve McMahon on 2008-06-29.
Copyright (c) 2008, Plone Foundation.

For use with the OS X Installer.
Cleanup operations including
display of README.txt after install.
"""

import sys, os, os.path

PACKAGE_PATH = sys.argv[1]
PLONE_HOME = sys.argv[2]

print sys.argv[0]


# the installer.app's automatically generated packages
# are just confusing noise for our purposes, and
# may cause problems on update/upgrade.
# Let's delete them.
packageDir = os.path.dirname(PACKAGE_PATH)
packages = [fn for fn in os.listdir(packageDir) if fn.endswith('.pkg')]
for fn in packages:
    receiptName = os.path.join('/Library/Receipts', fn)
    try:
        os.system("rm -rf %s" % receiptName)
    except OSError:
        pass
    receiptName = os.path.join('~/Library/Receipts', fn)
    try:
        os.system("rm -rf %s" % receiptName)
    except OSError:
        pass


# Figure out whether we're installing a stand-alone
# or cluster instance.
if PACKAGE_PATH.endswith('standaloneZope.pkg') or PACKAGE_PATH.endswith('standaloneZope-1.pkg'):
    target = 'zinstance'
elif PACKAGE_PATH.endswith('zeoCluster.pkg') or PACKAGE_PATH.endswith('zeoCluster-1.pkg'):
    target = 'zeocluster'
target = os.path.join(PLONE_HOME, target)

# open the folder
command = "/usr/bin/open %s" % target
print command
os.system(command)

# open the README
command = "/usr/bin/open %s" % os.path.join(target, 'README.html')
print command
os.system(command)

