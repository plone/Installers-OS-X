#!/bin/sh

# script to build a DMG-ready folder for an OS X installer.

# Prepare by placing a copy of the current Unified Installer tarball
# in this directory. It's used to build the binaries and
# for several of its scripts.

# specify version below; it should match the name of
# the Unified Installer.
VERSION=4.1.2

# override if you want to create the output folder somewhere else
TARGET_DIR=Plone-${VERSION}

# if [ -e /opt/local ]; then
#     echo "Please temporarily move /opt/local so that we don't link against MacPorts libraries."
#     exit 1
# fi

rm -rf Plone-${VERSION}-UnifiedInstaller
echo "Unpacking Unified Installer"
tar zxf Plone-${VERSION}-UnifiedInstaller.tgz

rm -rf work-build

cd Plone-${VERSION}-UnifiedInstaller

echo "Running Unified Installer"
# the key things to note here are:
# 1) we're building zeo, so that we get the zeocluster recipe eggs
# 2) we're incorporating readline because of Leopard's awful
#    readline bug.
# 3) we're incorporating libjpeg, as it's not standard on OS X
./install.sh zeo --libjpeg=yes \
  --readline=yes --password=admin \
  --target=../work-build \
  $EXFLAGS

if [ $? -gt 0 ]; then
    echo 'Unified Installer build failed; check install.log.'
    exit 1
fi

# move the unified installer, minus packages, into the work build
rm install.log
rm -r packages/*
cd ..
mv Plone-${VERSION}-UnifiedInstaller work-build/UnifiedInstaller

cd work-build

# force lxml static build
cd zeocluster
bin/buildout -c lxml_static.cfg
if [ $? -gt 0 ]; then
    echo 'Static lxml build failed; check install.log.'
    exit 1
fi
cd ..

echo "Moving results into PackageMaker resource directories"
# don't copy the instance
rm -r zeocluster
# don't include the dist files
rm -r buildout-cache/downloads/dist/*
rm -r buildout-cache/downloads/cmmi
# no need to transport .pyc files; we'll rebuild them on install
find . -name "*.py[co]" -exec rm {} \;
tar jcf ../baseResources/binaries.tar.bz2 *
cd ..


# build an installer package and dmg-ready directory
# if possible.
if [ -x /Developer/usr/bin/packagemaker ]; then    

    echo "Preparing package"

    if [ ! -d $TARGET_DIR ]; then
        echo "Creating $TARGET_DIR"
        mkdir $TARGET_DIR
    fi

    echo 'Running PackageMaker; "require admin" and "no sub-choice" warnings are normal.'
    /Developer/usr/bin/packagemaker --doc Plone.pmdoc --out $TARGET_DIR/$TARGET_DIR.mpkg

    echo "Adding readme and license files"
    cp generalResources/ReadMe.html $TARGET_DIR
    cp -r work-build/UnifiedInstaller/Licenses $TARGET_DIR
    cp -r work-build/UnifiedInstaller/Plone-docs $TARGET_DIR
    

    echo "Attaching installer icon"
    # mount disk image with folder with icon resource
    hdiutil attach generalResources/icons.dmg
    # copy the resource to our mpkg folder
    cp /Volumes/icons/InstallerIconFolder/* $TARGET_DIR/$TARGET_DIR.mpkg/
    umount /Volumes/icons
    # Set custom icon attribute
    SetFile -a C $TARGET_DIR/$TARGET_DIR.mpkg

    echo "$TARGET_DIR should be ready to become a .dmg"
else
    echo "Can't find packagemaker; can't build package."
fi
