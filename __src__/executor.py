###################################################################################

#                            https://github.com/SirDank                            

###################################################################################

'''
[NOTE]

- executor.py is meant to be executed only as an executable, not as a python script!
- the below imports are not required by executor.py but is required by the __modules__ run by dank.tool.py
- they are here to be imported by the installable / portable executable
- [ exec_mode = "script" ] is used for testing, to be run as a script | It is automatically changed to [ exec_mode = "exe" ] to be run as an executable
'''

import shutil
import ctypes
import winreg
import pyminizip
import subprocess
from psutil import process_iter
from playsound import playsound
from mcstatus import JavaServer
from win10toast import ToastNotifier
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
from dankware import multithread, align, magenta, white, red, reset, github_downloads, github_file_selector, rm_line, random_ip, get_duration, chdir, sys_open, is_admin, export_registry_keys

# required imports for executor.py

import os
import sys
import time
import requests
#from hashlib import sha1
from pypresence import Presence
from packaging.version import parse
from concurrent.futures import ThreadPoolExecutor
from dankware import cls, clr, title, err

# variables

session = requests.Session()
executor = ThreadPoolExecutor(10)

current_version = "2.2"
title("𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 [ 𝚒𝚗𝚒𝚝𝚒𝚊𝚕𝚒𝚣𝚒𝚗𝚐 ]")
print(clr(f"\n  > Version: {current_version}"))

# get latest version number and valid checksums

def latest_dank_tool_version():

    while True:
        try:
            latest_version = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/executor_version.txt").content.decode()
            #checksums = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/checksums.txt").content.decode()
            if "Not Found" in latest_version: latest_version = "0"
            break
        except:
            if "debug" in input(clr("\n  > Failed to check for an update! Make sure you are connected to the internet! Press [ENTER] to try again... ",2)):
                latest_version = "0"; break
    return latest_version #, checksums

latest_version = latest_dank_tool_version()

'''
# check if executable checksum exists in valid list

def check_file_integrity():

    global current_version

    if file_name.endswith('.exe'):
        checksum = sha1(open(file_name,'rb').read()).hexdigest()
        if not checksum in checksums:
            warning_banner = '\n\n\n\n888       888        d8888 8888888b.  888b    888 8888888 888b    888  .d8888b.  888 \n888   o   888       d88888 888   Y88b 8888b   888   888   8888b   888 d88P  Y88b 888 \n888  d8b  888      d88P888 888    888 88888b  888   888   88888b  888 888    888 888 \n888 d888b 888     d88P 888 888   d88P 888Y88b 888   888   888Y88b 888 888        888 \n888d88888b888    d88P  888 8888888P"  888 Y88b888   888   888 Y88b888 888  88888 888 \n88888P Y88888   d88P   888 888 T88b   888  Y88888   888   888  Y88888 888    888 Y8P \n8888P   Y8888  d8888888888 888  T88b  888   Y8888   888   888   Y8888 Y88b  d88P  "  \n888P     Y888 d88P     888 888   T88b 888    Y888 8888888 888    Y888  "Y8888P88 888 \n\n\n'
            cls(); print(clr(align(warning_banner) + "\n  > Integrity check failure! This may indicate that the software has been tampered with.\n\n  > As a precaution, I recommend that you check your system for malware.", 2))
            if 'debug' not in input(clr("\n  > Press [ ENTER ] to force update dank.tool... ")): current_version = "0"
            cls()
    
check_file_integrity()
'''

# version checker / updater

def dank_tool_installer():

    while True:
        try: code = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/updater.py").content.decode(); break
        except: input(clr("\n  > Failed to get code! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
    try: exec(code)
    except:
        err_message = err(sys.exc_info())
        try: requests.post("https://dank-site.onrender.com/dank-tool-errors", data={"text": f"```<--- 🚨 ---> Version: {current_version}\n\n{err_message}```"})
        except: pass
        print(clr(err_message, 2))
        input(clr("\n  > Press [ENTER] to EXIT... ",2))
        sys.exit(1)
    sys.exit("Updated!")

if os.path.exists('debug'): development_version = True
else: development_version = False
if parse(latest_version) > parse(current_version):
    print(clr(f"\n  > Update Found: {latest_version}")); dank_tool_installer()
elif latest_version == current_version: print(clr(f"\n  > Latest Version!"))
else: print(clr("\n  > Development Version!")); development_version = True

# get main code from github if development_version = False else locally

if development_version:
    while True:
        try: code = open('__src__/dank.tool.py', 'r', encoding='utf-8').read(); break
        except: input(clr("\n  > Failed to get code! Unable to read '__src__/dank.tool.py'! Press [ENTER] to try again... ",2))
else:
    while True:
        try: code = session.get("https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/dank.tool.py").content.decode(); break
        except: input(clr("\n  > Failed to get code! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

# start discord rpc

def dank_tool_discord_rpc():

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
    executor.submit(dank_tool_discord_rpc)
except: pass

# update counter

def dank_tool_runs_counter():
    while True:
        try: requests.get("https://api.countapi.xyz/hit/dank.tool2"); break
        except: pass
executor.submit(dank_tool_runs_counter)

# chatroom user validator

def dank_tool_chatroom():
    session = requests.Session()
    while True:
        try: session.post("https://dank-site.onrender.com/chatroom-users")
        except: pass
        time.sleep(240)
executor.submit(dank_tool_chatroom)

# execute, catch errors if any

title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 [{current_version}]"); cls()

try: exec(code)
except:

    cls(); latest_version = latest_dank_tool_version()
    if not latest_version == current_version:
        print(clr(f"\n  > An error occured! Updating to the latest version...\n\n  > Update Found: {latest_version}")); dank_tool_installer()
    else:
        err_message = err(sys.exc_info())
        print(clr(err_message, 2))
        #user_message = input(clr("\n  > Briefly explain what you were doing when this error occurred [ sent to the developer ]: ",2) + white)
        while True:
            try:
                #if user_message == "": content = f"```<--- 🚨 ---> Version: {current_version}\n\n{err_message}```"
                #else: content = f"```<--- 🚨 ---> Version: {current_version}\n\n{err_message}\n\n  > Message: {user_message}```"
                # > updated to custom url to prevent webhook spamming
                requests.post("https://dank-site.onrender.com/dank-tool-errors", data={"text": f"```<--- 🚨 ---> Version: {current_version}\n\n{err_message}```"})
                break
            except: input(clr(f"\n  > Failed to post error report! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
        cls(); input(clr("\n  > Error Reported! If it is an OS error, Please run as admin and try again!\n\n  > If it is a logic error, it will be fixed soon!\n\n  > Press [ENTER] to EXIT... ",2))

