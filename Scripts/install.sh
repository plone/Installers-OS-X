#!/bin/bash

# Load utils.sh for colors , headers and such stuff
#source utils.sh
# we want an error function

# Fisrt some VARS
# Set Colors
bold=$(tput bold)
underline=$(tput sgr 0 1)
reset=$(tput sgr0)

purple=$(tput setaf 171)
red=$(tput setaf 1)
green=$(tput setaf 76)
tan=$(tput setaf 3)
blue=$(tput setaf 38)

# Headers and Logging
e_header() { printf "\n${bold}${purple}==========  %s  ==========${reset}\n" "$@"
}
e_arrow() { printf "➜ $@\n"
}
e_success() { printf "${green}✔ %s${reset}\n" "$@"
}
e_error() { printf "${red}✖ %s${reset}\n" "$@"
}
e_warning() { printf "${tan}➜ %s${reset}\n" "$@"
}
e_underline() { printf "${underline}${bold}%s${reset}\n" "$@"
}
e_bold() { printf "${bold}%s${reset}\n" "$@"
}
e_note() { printf "${underline}${bold}${blue}Note:${reset}  ${blue}%s${reset}\n" "$@"
}

# Install
function to_install() {
  local debug desired installed i desired_s installed_s remain
  if [[ "$1" == 1 ]]; then debug=1; shift; fi
    # Convert args to arrays, handling both space- and newline-separated lists.
    read -ra desired < <(echo "$1" | tr '\n' ' ')
    read -ra installed < <(echo "$2" | tr '\n' ' ')
    # Sort desired and installed arrays.
    unset i; while read -r; do desired_s[i++]=$REPLY; done < <(
      printf "%s\n" "${desired[@]}" | sort
    )
    unset i; while read -r; do installed_s[i++]=$REPLY; done < <(
      printf "%s\n" "${installed[@]}" | sort
    )
    # Get the difference. comm is awesome.
    unset i; while read -r; do remain[i++]=$REPLY; done < <(
      comm -13 <(printf "%s\n" "${installed_s[@]}") <(printf "%s\n" "${desired_s[@]}")
  )
  [[ "$debug" ]] && for v in desired desired_s installed installed_s remain; do
    echo "$v ($(eval echo "\${#$v[*]}")) $(eval echo "\${$v[*]}")"
  done
  echo "${remain[@]}"

# Check if XCode CommandLine Tools are installed
e_header "Check if XCode-Tools are installed"
if [ ! -d "/Library/Developer/CommandLineTools/" ]; then
    e_header "Installing XCode Tools"
    xcode-select --install
else
# We do nothing and just move on
    .
fi

# Check if Homebrew is installed
e_header "Check if Homebrew is installed"

which -s brew
if [[ $? != 0 ]] ; then
Install Homebrew
# https://github.com/mxcl/homebrew/wiki/installation
   e_header "Installing Homebrew"
   /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew doctor
else
   e_header "Updating Homebrew"
   brew update
fi

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
brew install python --brewed-with-openssl

# Downloading Plone
e_header "Downloading Plone"
wget --no-check-certificate https://launchpad.net/plone/4.3/4.3.3/+download/Plone-4.3.3-UnifiedInstaller.tgz

# Unpacking Plone
tar -xf ${UI_VERSION}.tgz

# Installing Plone
e_header "Installing ... this can take some time"
cd Plone-4.3.3-UnifiedInstaller && ./install.sh standalone

# Watch the output

# Beer
