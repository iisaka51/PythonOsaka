#!/bin/bash

# read -p  "Are you ready? [Y/n] " ans 2>&1
echo -n  "Are you ready? [Y/n] " ; read ans
case ${ans} in
n|N)    ;;
y|Y|*)  echo "OK. bye-bye." ;;
esac
