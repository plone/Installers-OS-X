#!/bin/bash

# Load utils.sh for colors , headers and such stuff
source utils.sh
# we want an error function


# Check if Homebrew is installed
e_header "Check if Homebrew is installed"
#which -s brew
#if [[ $? != 0 ]] ; then
# Install Homebrew
# https://github.com/mxcl/homebrew/wiki/installation
#   e_header "Installing Homebrew"
#   /usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
#   brew doctor
#else
#   e_header "Updating Homebrew"
#   brew update
#fi

# Let us check if we have already some dependencies installed:
e_header "Check Homebrew Packages"

recipes=(
  openssl
  readline
  wget
  dialog
  git
)
list="$(to_install "${recipes[*]}" "$(brew list)")"
if [[ "$list" ]]; then
for item in ${list[@]}
  do
    echo "$item is not on the list"
  done
else
e_arrow "Nothing to install.  You've already got them all."
fi

# Install the Python version we want
e_header "Installing proper Python version with openssl support"
#brew install python --brewed-with-openssl

# Downloading Plone
#e_header "Downloading Plone"

# Unpacking Plone

# Prompt to install.sh

# Watch the output

# Beer
