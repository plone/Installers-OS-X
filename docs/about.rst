How is this Installer build
===========================

The Installer is build out f a mix from AppleScript and Bash, the intention is to keep AppleScript to a minimum and use Bash where it is possible.

Structure
=========

AppleScript is used to give the User a 'more typical Apple feeling'. It will give the User a more shinny Application Bundle with nice icons, looking 'typical Mac'.

In the background, the script is calling different BashScripts for doing the actual work.

The scripts in the background will check, if there are already all dependencies installed and if not it will ask for permissions to install them.
If permissions are granted the script will detect install missing dependencies [via homebrew] and afterwards it will run the normal Unified Installer buildout.

If permissions are not granted the script will stop with a warning message and will give links to other possibilities to install Plone and for getting support.

The directory structure should setup in the way that it is 'OK' with the typical structure for Apple Bundles, so that we can build the bundle later from
command line [jenkins?]

Building
========

If you want to build a new release, you need to addjust Scripts/install.sh with the right version numbers and download links, further you have to change the name in the build script [create_bundle.sh].
In a later stage we should change that to have this settings as variables in the build script.

If these changes are done, just run: ./create_bundle.sh and you will get the Installer.app.


