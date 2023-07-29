@echo off
title package-updater
cd /D "%~dp0"
pip install -U -r requirements.txt
pause