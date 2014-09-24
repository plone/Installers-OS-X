#!/bin/bash

source utils.sh

e_header "Check Homebrew Packages"

recipes=(
  A-random-package
  bash
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
