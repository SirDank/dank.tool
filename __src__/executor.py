###################################################################################

#                            https://github.com/SirDank                            

###################################################################################

'''
[NOTE]

- executor.py is meant to be executed only as an executable, not as a python script!
- the below packages are not required by the executor.py script but is required by the various __modules__ run by the dank.tool.exe
- they are listed here to be included in the final build of dank.tool.exe
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
from locale import getlocale
from win11toast import notify
from psutil import process_iter
from playsound import playsound
from mcstatus import JavaServer
from translatepy import Translator
from gzip import compress, decompress
from dateutil.tz import tzlocal, tzutc
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
from dankware import cls, err, multithread, align, github_downloads, github_file_selector, rm_line, random_ip, get_duration, sys_open, is_admin, export_registry_keys, file_selector, folder_selector, get_path
from dankware import reset, black, blue, cyan, green, magenta, red, white, yellow, black_normal, blue_normal, cyan_normal, green_normal, magenta_normal, red_normal, white_normal, yellow_normal, black_dim, blue_dim, cyan_dim, green_dim, magenta_dim, red_dim, white_dim, yellow_dim

# required packages for dank.fusion-fall.py

from unitypackff.asset import Asset
from unitypackff.export import OBJMesh
from unitypackff.object import FFOrderedDict, ObjectPointer
from unitypackff.modding import import_texture, import_mesh, import_audio

# required packages for executor.py

import requests
from pypresence import Presence
from dankware import clr, title
from packaging.version import parse
from concurrent.futures import ThreadPoolExecutor

# variables

DANK_TOOL_VERSION = "3.1.2"
session = requests.Session()
executor = ThreadPoolExecutor(10)
headers = {"User-Agent": "dank.tool"}
os.environ['DANK_TOOL_VERSION'] = DANK_TOOL_VERSION

os.chdir(os.path.dirname(__file__))
title("𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 [ 𝚒𝚗𝚒𝚝𝚒𝚊𝚕𝚒𝚣𝚒𝚗𝚐 ]")
print(clr(f"\n  > Version: {DANK_TOOL_VERSION}"))

# rediect stderr to a file
#if not os.path.exists('__logs__'): os.mkdir('__logs__')
#sys.stderr = open('__logs__/dank.tool.log', 'w', encoding='utf-8')

# debug env variables

os.environ['DANK_TOOL_OFFLINE_DEV'] = ("1" if os.path.isfile('debug') else "0")
os.environ['DANK_TOOL_ONLINE_DEV'] = ("1" if os.path.isfile('debug-online') else "0")
ONLINE_DEV = int(os.environ['DANK_TOOL_ONLINE_DEV'])
OFFLINE_DEV = int(os.environ['DANK_TOOL_OFFLINE_DEV'])
branch = ("main" if not ONLINE_DEV else "dev")

# handle KeyboardInterrupt

def print_warning_symbol():
    
    warning_symbol = f'\n\n{red}                      ██                      \n{red}                    ██  ██                    \n{red}                  ██      ██                  \n{red}                ██          ██                \n{red}                ██          ██                \n{red}              ██              ██              \n{red}            ██      {white}██████{red}      ██            \n{red}            ██      {white}██████{red}      ██            \n{red}          ██        {white}██████{red}        ██          \n{red}          ██        {white}██████{red}        ██          \n{red}        ██          {white}██████{red}          ██        \n{red}      ██            {white}██████{red}            ██      \n{red}      ██            {white}██████{red}            ██      \n{red}    ██              {white}██████{red}              ██    \n{red}    ██                                  ██    \n{red}  ██                {white}██████{red}                ██  \n{red}  ██                {white}██████{red}                ██  \n{red}██                  {white}██████{red}                  ██\n{red}██                                          ██\n{red}  ██████████████████████████████████████████  \n'
    cls(); print(align(warning_symbol))

# get latest version number

def latest_dank_tool_version():
    
    try:
        LATEST_VERSION = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{branch}/__src__/executor_version.txt", headers=headers).content.decode()
        os.environ['DANK_TOOL_ONLINE'] = "1"
    except:
        LATEST_VERSION = "0"
        os.environ['DANK_TOOL_ONLINE'] = "0"
        os.environ['DANK_TOOL_ONLINE_DEV'] = "0"
    return LATEST_VERSION

LATEST_VERSION = latest_dank_tool_version()
ONLINE_MODE = int(os.environ['DANK_TOOL_ONLINE'])
ONLINE_DEV = int(os.environ['DANK_TOOL_ONLINE_DEV'])
branch = ("main" if not ONLINE_DEV else "dev")

# version checker / updater

def dank_tool_installer():

    while True:
        try:
            code = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{branch}/__src__/updater.py", headers=headers).content.decode()
            break
        except: input(clr("\n  > Failed to get code! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
    
    try: exec(code)
    except:
        err_message = err(sys.exc_info())
        try: session.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": f"```<--- 🚨🚨🚨 ---> Version: {DANK_TOOL_VERSION}\n\n{err_message}```"})
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

else: # LATEST VERSION IS LOWER THAN CURRENT VERSION
    print(clr("\n  > Development Version!"))

# check windows language

def check_windows_language():
    
    locale_name = getlocale()[0]
    if '-' in locale_name and not '_' in locale_name:
        locale_name = locale_name.split('-')[0]
    elif '_' in locale_name and not '-' in locale_name:
        locale_name = locale_name.split('_')[0]
    else:
        for _ in locale_name:
            if _ == '-':
                locale_name = locale_name.split('-')[0]
                break
            elif _ == '_':
                locale_name = locale_name.split('_')[0]
                break
    
    if not locale_name.lower().startswith('en'):
        translator = Translator()
        result = translator.translate("Would you like to enable the translate feature?", source_language='en', destination_language=locale_name)
        print(clr(f"\n  > Your windows language is set to '{cyan}{locale_name}'!"))
        if input(clr(f"\n  > {result} [y/n]:", colour_one=cyan)).lower() == 'y':
            os.environ['DANK_TOOL_LANG'] = locale_name
        else:
            os.environ['DANK_TOOL_LANG'] = "en"
    else:
        os.environ['DANK_TOOL_LANG'] = "en" 

if ONLINE_MODE:
    check_windows_language()
else:
    os.environ['DANK_TOOL_LANG'] = "en"

# get and save dank.tool.py

if not os.path.exists('__src__'): os.mkdir('__src__')
if not os.path.exists('__modules__'): os.mkdir('__modules__')
if not os.path.exists('__local_modules__'): os.mkdir('__local_modules__')

if not OFFLINE_DEV and ( ONLINE_MODE or not os.path.exists('__src__/dank.tool.py') ):
    while True:
        try: code = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{branch}/__src__/dank.tool.py", headers=headers).content.decode(); break
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
        os.environ['DISCORD_RPC'] = "on the main menu"
        RPC = Presence("1028269752386326538")
        RPC.connect()
        executor.submit(dank_tool_discord_rpc)
    except: pass

# update counter

def dank_tool_runs_counter():

    fail_counter = 0
    session = requests.Session()
    while True:
        if fail_counter > 3: break
        try: session.get("https://dank-site.onrender.com/counter?id=dank.tool&hit=true", headers=headers); break
        except: fail_counter += 1
        time.sleep(60)
        
if ONLINE_MODE:
    executor.submit(dank_tool_runs_counter)

# chatroom user validator

def dank_tool_chatroom():
    
    fail_counter = 0
    session = requests.Session()
    while True:
        if fail_counter > 2: break
        try: session.post("https://dank-site.onrender.com/chatroom-users", headers=headers); fail_counter = 0 # do not add a break here! (keeps user validated)
        except: fail_counter += 1
        time.sleep(240)

if ONLINE_MODE:
    executor.submit(dank_tool_chatroom)

# execute, catch errors if any

title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 {DANK_TOOL_VERSION}")

if not ONLINE_MODE:
    time.sleep(5)

try: exec(code)
except:

    cls()
    err_message = err(sys.exc_info())
    print(clr(err_message, 2))
    LATEST_VERSION = latest_dank_tool_version()
    
    if "Error Type: KeyboardInterrupt" in err_message:
        print_warning_symbol()
        print(clr("\n  > Please select text first and then use [ CTRL + C ]!"))
    
    elif parse(LATEST_VERSION) > parse(DANK_TOOL_VERSION):
        print(clr(f"\n  > Updating to the latest version...\n\n  > Update Found: {LATEST_VERSION}"))
        dank_tool_installer()

    elif ONLINE_MODE:
        while True:
            try:
                session.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": f"```<--- 🚨🚨🚨 ---> Version: {DANK_TOOL_VERSION}\n\n{err_message}```"})
                break
            except: input(clr(f"\n  > Failed to post error report! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
        print(clr("\n  > Error Reported! If it is an OS error, Please run as admin and try again!\n\n  > If it is a logic error, it will be fixed soon!"))
    
    input(clr("\n  > Press [ENTER] to EXIT... "))
    os.system("taskkill /f /im dank.tool.exe")

