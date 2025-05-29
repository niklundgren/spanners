#!/bin/bash

if grep -q HISTSIZE ${HOME}/.bashrc
then
    printf "Hey we found it!"
    read -p "Would you like to overwrite the arguments? (Y/N)" overwrite_hist
    if [overwrite_hist=="Y"]
    then
        sed 
