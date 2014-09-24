--OSX Installer for Plone

display dialog "Welcome to the Plone Installer for OSX.
For any help please check https://plone.org/help" with icon alias ((path to me) & "Contents:Resources:plone.icns" as string) buttons {"Cancel", "OK"} default button 2

--Info Txt
display dialog "The installer relies on homebrew and
Xcode to install all needed requirements
If you click Yes the installer will try to figure out what needs to be installed.

In order to do so it will also ask for your sudo passowrd.

If you don't agree please click on No, that will stop this programm
without installing anything on your computer.
Do you want to install Plone ?" buttons {"Yes", "No"} default button 1

--If yes
if result = {button returned:"Yes"} then
    tell application "Terminal"
        do shell script "bash " & POSIX path of (path to me) & "/Contents/Resources/Scripts/foobar.sh"
        --set bashFile to path to resource "foobar.sh"
        --do script "foobar.sh" & quoted form of (POSIX path of bashFile) in shell
    end tell
else
    --If no
    display dialog "Go and install vagrant"
end if
