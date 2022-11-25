'''
[NOTE] executor.py is meant to be executed only as an executable, not as a python script!
the below imports are not required by the executor.py but is required by the __modules__ run by dank.tool.py
they are here to be imported by the portable executable
[NOTE] [ exec_mode = "script" ] is used for testing, to be run as a script | It is automatically changed to [ exec_mode = "exe" ] to be run as an executable
'''

from playsound import playsound
from mcstatus import JavaServer
from shutil import unpack_archive
from win10toast import ToastNotifier
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
from dankware import multithread, clr_banner, align, magenta, white, red, reset, github_downloads, github_file_selector, rm_line, random_ip, get_duration

# required imports for executor.py

import os
import sys
import time
import requests
from pypresence import Presence
from packaging.version import parse
from concurrent.futures import ThreadPoolExecutor
from dankware import cls, clr, chdir, title, sys_open, err
session = requests.Session()

# change directory to exe's location

current_version = "1.4"
exec_mode = "exe"
title("𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 [ 𝚒𝚗𝚒𝚝𝚒𝚊𝚕𝚒𝚣𝚒𝚗𝚐 ]"); exec(chdir(exec_mode))
print(clr(f"\n  > Version: {current_version}"))

# get latest version number

def latest_dank_tool_version():
    while True:
        try:
            latest_version = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/executor_version.txt").content.decode()
            if "Not Found" in latest_version: latest_version = "0"
            break
        except: input(clr("\n  > Failed to check for an update! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
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
        except: input(clr("\n  > Failed to download! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
    open("dank.tool-latest.exe","wb").write(data); data = None                                                                                                                                   # removed "start dank.tool.exe"
    open("dankware-updater.cmd","w").write("@echo off\ntitle dankware-updater\ncolor 0a\ntimeout 3\ndel /F dank.tool.exe\nren dank.tool-latest.exe dank.tool.exe\ncls\necho.\necho =======================\necho.\necho    UPDATE COMPLETE\necho.\necho =======================\necho.\necho    Run dank.tool.exe\necho.\necho =======================\necho.\necho  T E R M I N A T I N G\necho.\ntimeout 5\ndel \"%~f0\" >nul 2>&1\nexit")
    print(clr("\n  > Downloaded!\n\n  > Starting in 3s..."))
    time.sleep(3); sys_open("dankware-updater.cmd"); sys.exit()

development_version = False
if parse(latest_version) > parse(current_version):
    print(clr(f"\n  > Update Found: {latest_version}")); download_latest_dank_tool()
elif latest_version == current_version: print(clr(f"\n  > Latest Version!"))
else: print(clr("\n  > Development Version!")); development_version = True

# get main src from github if not dev_ver else locally

if not development_version:
    while True:
        try: code = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/dank.tool.py").content.decode(); break
        except: input(clr("\n  > Failed to get src! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
else:
    while True:
        try: code = open('__src__/dank.tool.py', 'r', encoding='utf-8').read(); break
        except: input(clr("\n  > Failed to get src! Unable to read '__src__/dank.tool.py'! Press [ENTER] to try again... ",2))

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
                buttons = [{"label": "Download", "url": "https://github.com/SirDank/dank.tool"}, {"label": "Discord", "url": "https://allmylinks.com/link/out?id=kdib4s-nu8b-1e19god"}]
            )
            time.sleep(15)
        except: break

try:
    RPC = Presence("1028269752386326538")
    RPC.connect(); discord_rpc_state = "on the main menu"
    ThreadPoolExecutor(10).submit(dank_discord_rpc)
except: pass

# update counter

def dankware_counter():
    try: requests.get("https://api.countapi.xyz/hit/dank.tool")
    except: pass
ThreadPoolExecutor(10).submit(dankware_counter)

# execute, catch errors if any

#time.sleep(3)
title("𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕"); cls()

try: exec(code)
except:
    
    cls(); latest_version = latest_dank_tool_version()
    if not latest_version == current_version:
        print(clr(f"\n  > An error occured! Updating to the latest version...\n\n> Update Found: {latest_version}")); download_latest_dank_tool()
    else:
        err_message = err(sys.exc_info())
        print(clr(err_message, 2))
        while True:
            try: requests.post("https://discord.com/api/webhooks/1038503148681179246/GkOrGGuK3mcYpx3OzDMyqCtcnWbx7cZqSK_PbyIkxIbjizPlmjcHFt2dlPhxSBLf2n38", json={"content": f"```<--- 🚨 ---> Version: {current_version}\n\n{err_message}```"}); break
            except: input(clr(f"\n  > Failed to post error report! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
        input(clr("\n  > Error Reported! If it is an OS error, Please run as admin and try again!\n\n  > If it is a logic error, it will be fixed soon!\n\n  > Press [ENTER] to EXIT..."))