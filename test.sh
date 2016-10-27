#!/bin/bash
clear

echo Started at $(TZ=America/Chicago date +"%T %Z")
echo ===
echo

python run.py
pyexit=$?

echo
echo ===
echo Exited with code $pyexit

exit $pyexit
