#!/bin/sh

# script to build a DMG-ready folder for an OS X installer.

# assumes binaries.tar.bz2 already in baseResources

# specify version below; it should match the name of
# the Unified Installer.
VERSION=4.1.4

TARGET_DIR=Plone-${VERSION}

# build an installer package and dmg-ready directory
# if possible.
if [ -x /Developer/usr/bin/packagemaker ]; then    

  echo "Preparing package"

  if [ ! -d $TARGET_DIR ]; then
      echo "Creating $TARGET_DIR"
      mkdir $TARGET_DIR
  fi

  # echo 'Running PackageMaker; "require admin" and "no sub-choice" warnings are normal.'
  # /Developer/usr/bin/packagemaker --doc Plone.pmdoc --out $TARGET_DIR/$TARGET_DIR.mpkg

  echo "Adding readme and license files"
  cp generalResources/ReadMe.html $TARGET_DIR
  cp -r baseResources/UnifiedInstaller/Licenses $TARGET_DIR

  echo 'Clonning Plone'
  if [ ! -d baseResources/Plone ]
  then
    cd baseResources
    git clone git://github.com/plone/Plone.git
    cd ..
  fi
  
  echo 'Moving to right tag'
  cd baseResources/Plone
  git checkout ${VERSION}

  cd ../../

  echo 'Prepare docs'
  if [ ! -d $TARGET_DIR/Plone-docs ]
  then  
    mkdir -p $TARGET_DIR/Plone-docs
  fi
  cp -R baseResources/Plone/docs/* $TARGET_DIR/Plone-docs/

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
    echo "If we're running on Tiger, that's no surprise."
    echo "Transfer binaries.tgz to a machine with packagemaker"
    echo "and run packageme.sh."
fi
