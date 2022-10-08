# [NOTE] executor.py is meant to be executed only as an executable, not as a python script!
# the below imports are not required by the executor.py but is required by dank.tool.py

from playsound import playsound
from mcstatus import JavaServer
from pypresence import Presence
from shutil import unpack_archive
from win10toast import ToastNotifier
from concurrent.futures import ThreadPoolExecutor
from dankware import multithread, clr_banner, align, cls, clr, magenta, white, red, reset, chdir, title, github_downloads, github_file_selector, rm_line, random_ip, sys_open, get_duration

# required imports for executor.py

import os
import sys
import time
import requests
from packaging.version import parse
session = requests.Session()

# change directory to exe's location

current_version = "1.2"
exec_mode = "exe"
title("dank.tool [ initializing ]"); exec(chdir(exec_mode))
print(clr(f"\n  > Version: {current_version}"))

# get latest version

def latest_dank_tool_version():
    while True:
        try:
            latest_version = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/executor_version.txt").content.decode()
            if "Not Found" in latest_version: latest_version = "0"
            break
        except: wait = input(clr("\n  > Failed to check for an update! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
    return latest_version

latest_version = latest_dank_tool_version()

# version checker / updater: overwrites the existing executable with the latest one using the help of a batch script called 'dankware-updater.cmd' which deletes itself upon completion!

def download_latest_dank_tool():
    
    if not os.path.isfile("dank.tool.exe"):
        print(clr('\n  > Rename this executable back to "dank.tool.exe" for it to update properly!\n\n  > Exiting in 25 seconds...',2))
        time.sleep(25); sys.exit()
    print(clr("\n  > Downloading dank.tool-latest.exe..."))
    while True:
        try: data = session.get("https://github.com/SirDank/dank.tool/blob/main/dank.tool.exe?raw=true", allow_redirects=True).content; break
        except: wait = input(clr("\n  > Failed to download! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
    open("dank.tool-latest.exe","wb+").write(data); data = None                                                                                                                                   # removed "start dank.tool.exe"
    open("dankware-updater.cmd","w+").write("@echo off\ntitle dankware-updater\ncolor 0a\ntimeout 3\ndel /F dank.tool.exe\nren dank.tool-latest.exe dank.tool.exe\ncls\necho.\necho =======================\necho.\necho    UPDATE COMPLETE\necho.\necho =======================\necho.\necho    Run dank.tool.exe\necho.\necho =======================\necho.\necho  T E R M I N A T I N G\necho.\ntimeout 10\ndel \"%~f0\" >nul 2>&1\nexit")
    print(clr("\n  > Downloaded!\n\n  > Starting in 3s..."))
    time.sleep(3); sys_open("dankware-updater.cmd"); sys.exit()

if parse(latest_version) > parse(current_version):
    print(clr(f"\n  > Update Found: {latest_version}")); download_latest_dank_tool()
elif latest_version == current_version: print(clr(f"\n  > Latest Version!"))
else: print(clr("\n  > Development Version!"))

# get main src from github

while True:
    try: code = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/dank.tool.py").content.decode(); break
    except: wait = input(clr("\n  > Failed to get src! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))

# start discord rpc

def dank_discord_rpc():

    start = int(time.time())
    while True:
        try:
            RPC.update(
                large_image = "dankware",
                large_text = "dank.tool",
                details = "running dank.tool",
                state = discord_rpc_state,
                start = start,
                buttons = [{"label": "Download", "url": "https://github.com/SirDank/dank.tool"}, {"label": "Discord", "url": "https://discord.gg/jqj7CFx"}]
            )
            time.sleep(15)
        except: break

try:
    RPC = Presence("1028269752386326538")
    RPC.connect(); discord_rpc_state = "on the main menu"
    ThreadPoolExecutor(1).submit(dank_discord_rpc)
except: pass

# execute, catch errors if any

time.sleep(3); title("dank.tool"); cls()

try: exec(code)
except Exception as exp:

    cls(); latest_version = latest_dank_tool_version()
    if not latest_version == current_version:
        print(clr(f"\n  > An error occured! Updating to the latest version...\n\n> Update Found: {latest_version}")); download_latest_dank_tool()
    else:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(clr(f"\n  > Version: {current_version} | Error: {str(exp)} | {exc_type} | Line: {exc_tb.tb_lineno}",2))
        print(clr("\n  > Please take a screenshot of this and post it on https://github.com/SirDank/dank.tool/issues/new\n\n> Opening in 3s..."))
        time.sleep(3); sys_open("https://github.com/SirDank/dank.tool/issues/new")
    wait = input(clr("\n  > Press [ENTER] to continue: "))

