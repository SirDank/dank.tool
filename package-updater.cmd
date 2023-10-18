@echo off
title package-updater
python.exe -m pip install --upgrade pip
cd /D "%~dp0"
pip install -U -r requirements.txt
pause