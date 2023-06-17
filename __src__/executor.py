###################################################################################

#                            https://github.com/SirDank                            

###################################################################################

'''
[NOTE]

- executor.py is meant to be executed only as an executable, not as a python script!
- the below imports are not required by executor.py but is required by the __modules__ run by dank.tool.py
- they are here to be imported by the installable / portable executable
'''

import os
import sys
import time
import json
import shutil
import ctypes
import winreg
import sqlite3
import pyminizip
import subprocess
import tkinter as tk
from psutil import process_iter
from playsound import playsound
from mcstatus import JavaServer
from win10toast import ToastNotifier
from gzip import compress, decompress
from dateutil.tz import tzlocal, tzutc
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
from dankware import cls, err, multithread, align, github_downloads, github_file_selector, rm_line, random_ip, get_duration, sys_open, is_admin, export_registry_keys, file_selector, folder_selector, get_path
from dankware import reset, black, blue, cyan, green, magenta, red, white, yellow, black_normal, blue_normal, cyan_normal, green_normal, magenta_normal, red_normal, white_normal, yellow_normal, black_dim, blue_dim, cyan_dim, green_dim, magenta_dim, red_dim, white_dim, yellow_dim

# required imports for dank.fusion-fall.py

from unitypackff.asset import Asset
from unitypackff.export import OBJMesh
from unitypackff.object import FFOrderedDict, ObjectPointer
from unitypackff.modding import import_texture, import_mesh, import_audio

# required imports for executor.py

import requests
from pypresence import Presence
from dankware import clr, title
from packaging.version import parse
from concurrent.futures import ThreadPoolExecutor

# variables

DANK_TOOL_VERSION = "3.0"
session = requests.Session()
executor = ThreadPoolExecutor(10)
headers = {"User-Agent": "dank.tool"}
os.environ['DANK_TOOL_VERSION'] = DANK_TOOL_VERSION

os.chdir(os.path.dirname(__file__))
title("𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 [ 𝚒𝚗𝚒𝚝𝚒𝚊𝚕𝚒𝚣𝚒𝚗𝚐 ]")
print(clr(f"\n  > Version: {DANK_TOOL_VERSION}"))

# debug env variables

os.environ['DANK_TOOL_OFFLINE_DEV'] = ("1" if os.path.isfile('debug') else "0")
os.environ['DANK_TOOL_ONLINE_DEV'] = ("1" if os.path.isfile('debug-online') else "0")
OFFLINE_DEV = int(os.environ['DANK_TOOL_OFFLINE_DEV'])

# get latest version number

def latest_dank_tool_version():
    
    try:
        LATEST_VERSION = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/executor_version{'' if not ONLINE_DEV else '_dev'}.txt", headers=headers).content.decode()
        os.environ['DANK_TOOL_ONLINE'] = "1"
    except:
        LATEST_VERSION = "0"
        os.environ['DANK_TOOL_ONLINE'] = "0"
        os.environ['DANK_TOOL_ONLINE_DEV'] = "0"
    return LATEST_VERSION

LATEST_VERSION = latest_dank_tool_version()
ONLINE_MODE = int(os.environ['DANK_TOOL_ONLINE'])
ONLINE_DEV = int(os.environ['DANK_TOOL_ONLINE_DEV'])

# version checker / updater

def dank_tool_installer():

    while True:
        try:
            code = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/updater{'' if not ONLINE_DEV else '_dev'}.py", headers=headers).content.decode()
            break
        except: input(clr("\n  > Failed to get code! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
    
    try: exec(code)
    except:
        err_message = err(sys.exc_info())
        try: session.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": f"```<--- 🚨 ---> Version: {DANK_TOOL_VERSION}\n\n{err_message}```"})
        except: pass
        input(clr(f"{err_message}\n\n  > Press [ENTER] to EXIT... ",2))
        sys.exit(err_message)
    
    sys.exit("Updated!")

# update environment variables

if parse(LATEST_VERSION) > parse(DANK_TOOL_VERSION) or os.path.isfile('force-update'):
    print(clr(f"\n  > Update Found: {LATEST_VERSION}" + ("" if not os.path.isfile('force-update') else " [ FORCED ]")))
    dank_tool_installer()
elif LATEST_VERSION == DANK_TOOL_VERSION:
    if not ONLINE_DEV:
        print(clr(f"\n  > Latest Version!"))
    else:
        print(clr(f"\n  > Online Development Mode!"))
elif LATEST_VERSION == "0":
    print(clr("\n  > Offline Mode!"))
else: # LATEST VERSION IS LESS THAN CURRENT VERSION
    print(clr("\n  > Development Mode!"))
    os.environ['DANK_TOOL_OFFLINE_DEV'] = "1"
    OFFLINE_DEV = 1

# get and save dank.tool.py

if not os.path.exists('__src__'): os.mkdir('__src__')
if not os.path.exists('__modules__'): os.mkdir('__modules__')

if not OFFLINE_DEV and ( ONLINE_MODE or not os.path.exists('__src__/dank.tool.py') ):
    while True:
        try: code = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/main/__src__/dank.tool{'' if not ONLINE_DEV else '_dev'}.py", headers=headers).content.decode(); break
        except: input(clr("\n  > Failed to get code! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
    open('__src__/dank.tool.py', 'w', encoding='utf-8').write(code)
else:
    while True:
        try: code = open('__src__/dank.tool.py', 'r', encoding='utf-8').read(); break
        except: input(clr("\n  > Failed to get code! Unable to read '__src__/dank.tool.py'! Press [ENTER] to try again... ",2))

# start discord rpc

def dank_tool_discord_rpc():

    start = int(time.time())
    while True:
        try:
            RPC.update(
                large_image = "dankware",
                large_text = "dankware",
                details = f"[ dank.tool {DANK_TOOL_VERSION} ]",
                state = os.environ['DISCORD_RPC'],
                start = start,
                buttons = [{"label": "Download", "url": "https://github.com/SirDank/dank.tool"}, {"label": "Discord", "url": "https://allmylinks.com/link/out?id=kdib4s-nu8b-1e19god"}]
            )
            time.sleep(15)
        except: break

if ONLINE_MODE:
    try:
        RPC = Presence("1028269752386326538")
        RPC.connect(); os.environ['DISCORD_RPC'] = "on the main menu"
        executor.submit(dank_tool_discord_rpc)
    except: pass

# update counter

def dank_tool_runs_counter():
    session = requests.Session()
    while True:
        try: session.get("https://api.countapi.xyz/hit/dank.tool2", headers=headers); break
        except: pass
        time.sleep(240)
        
if ONLINE_MODE:
    executor.submit(dank_tool_runs_counter)

# chatroom user validator

def dank_tool_chatroom():
    session = requests.Session()
    while True:
        try: session.post("https://dank-site.onrender.com/chatroom-users", headers=headers)
        except: pass
        time.sleep(240)

if ONLINE_MODE:
    executor.submit(dank_tool_chatroom)

# execute, catch errors if any

title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 {DANK_TOOL_VERSION}")

try: exec(code)
except:

    cls()
    err_message = err(sys.exc_info())
    print(clr(err_message, 2))
    LATEST_VERSION = latest_dank_tool_version()
    if parse(LATEST_VERSION) > parse(DANK_TOOL_VERSION):
        print(clr(f"\n  > Updating to the latest version...\n\n  > Update Found: {LATEST_VERSION}"))
        dank_tool_installer()
    else:
        if ONLINE_MODE:
            #user_message = input(clr("\n  > Briefly explain what you were doing when this error occurred [ sent to the developer ]: ",2) + white)
            while True:
                try:
                    #if user_message == "": content = f"```<--- 🚨 ---> Version: {DANK_TOOL_VERSION}\n\n{err_message}```"
                    #else: content = f"```<--- 🚨 ---> Version: {DANK_TOOL_VERSION}\n\n{err_message}\n\n  > Message: {user_message}```"
                    session.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": f"```<--- 🚨 ---> Version: {DANK_TOOL_VERSION}\n\n{err_message}```"})
                    break
                except: input(clr(f"\n  > Failed to post error report! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
            print(clr("\n  > Error Reported! If it is an OS error, Please run as admin and try again!\n\n  > If it is a logic error, it will be fixed soon!"))
        input(clr("\n  > Press [ENTER] to EXIT... "))

