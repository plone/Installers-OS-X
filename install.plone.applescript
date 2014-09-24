--OSX INstaller for Plone

--Welcome Txt
display dialog "Welcome to the Installer for Plone on OSX
For any help please check the documentation on docs.plone.org
The installer relies on homebrew to install all needed requirements"

--Do you really want to install
display dialog "Do yo want to continue" buttons {"Yes", "No"} default button 1

--If yes
if result = {button returned:"Yes"} then
    tell application "Terminal"
        set bashFile to path to resource "foobar.sh"
        do script "foobar.sh" & quoted form of (POSIX path of bashFile) in shell
    end tell
else
    --If no
    display dialog "Go and install vagrant"
end if
