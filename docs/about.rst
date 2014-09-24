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

We should always keep the description and version files up to date, meaning update them with every release of Plone.
