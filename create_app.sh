#!/bin/bash
# This will create a Apple Bundle App for installing Plone on OSX
# Dependencies: osacompile

# Declare some VARS
APP_NAME="PloneOSX-WIP.app"
SOURCE_SCRIPT="install.plone.applescript"

# Create the dir structure
/usr/bin/osacompile -o "$APP_NAME" "$SOURCE_SCRIPT"

# Copy applet.icns to the right place
cp applet.icns "$APP_NAME"/Contents/Resources

# Copy Plone icon, which we use for Displays
cp plone.icns "$APP_NAME"/Contents/Resources

# Copy scripts to Resources
cp Scripts/* "$APP_NAME"/Contents/Resources/Scripts
