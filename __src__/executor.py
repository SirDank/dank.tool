###################################################################################

#                            https://github.com/SirDank                            

###################################################################################

'''
[NOTE]

- executor.py is meant to be executed only as an executable, not as a python script!
- the below packages are not required by the executor.py script but are required by the various __modules__ run by the dank.tool.exe
- they are listed here to be included in the final build of dank.tool.exe
'''

import os
import sys
import time
import json
import shutil
import psutil
import ctypes
import requests
import pyminizip
import subprocess
import tkinter as tk
from locale import getlocale
from rich.align import Align
from psutil import process_iter
from playsound import playsound
from rich.console import Console
from translatepy import Translator
from gzip import compress, decompress
from dateutil.tz import tzlocal, tzutc
from mcstatus import JavaServer, BedrockServer
from concurrent.futures import ThreadPoolExecutor
from dankware.tkinter import file_selector, folder_selector
from dankware import cls, clr, title, err, multithread, align, github_downloads, github_file_selector, rm_line, random_ip, get_duration, sys_open, is_admin, export_registry_keys, get_path
from dankware import reset, black, blue, cyan, green, magenta, red, white, yellow, black_bright, blue_bright, cyan_bright, green_bright, magenta_bright, red_bright, white_bright, yellow_bright, black_normal, blue_normal, cyan_normal, green_normal, magenta_normal, red_normal, white_normal, yellow_normal, black_dim, blue_dim, cyan_dim, green_dim, magenta_dim, red_dim, white_dim, yellow_dim

# required packages for dank.game.py

import numpy
from ursina import *
from ursina.scripts import *
from ursina.shaders import *
from ursina.prefabs.first_person_controller import FirstPersonController

# required packages for executor.py

from pypresence import Presence
from packaging.version import parse

# windows specific

if os.name == "nt":
    import winreg
    from win11toast import notify

# rediect stderr to a file
#if not os.path.exists('__logs__'): os.mkdir('__logs__')
#sys.stderr = open('__logs__/dank.tool.log', 'w', encoding='utf-8')

# debug env variables

def settings_json():

    overwrite = False
    default_settings = {
        "offline-src": "0",
        "offline-mode": "0",
        "dev-branch": "0",
        "force-update": "0",
        "force-translate": "0",
        "disable-translate": "0",
        "compatibility-mode": "0",
        "force-startup-audio": "0",
        "disable-startup-audio": "0",
    }

    if not os.path.isfile('settings.json'):
        overwrite = True
    else:
        with open('settings.json', 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
        for key in default_settings:
            if key not in data:
                overwrite = True
            else:
                default_settings[key] = data[key]

    default_settings["force-translate"] = ("1" if os.path.isfile("force-translate") else "0")
    default_settings["disable-translate"] = ("1" if os.path.isfile("disable-translate") else "0")
    default_settings["compatibility-mode"] = ("1" if os.path.isfile("compatibility-mode") else "0")
    default_settings["force-startup-audio"] = ("1" if os.path.isfile("force-startup-audio") else "0")
    default_settings["disable-startup-audio"] = ("1" if os.path.isfile("disable-startup-audio") else "0")

    if not overwrite and default_settings != data:
        overwrite = True

    if overwrite:
        with open('settings.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(default_settings, indent=4))

settings_json()
del settings_json

with open('settings.json', 'r', encoding='utf-8') as _:
    DANK_TOOL_SETTINGS = json.loads(_.read())
os.environ['DANK_TOOL_COMPATIBILITY_MODE'] = DANK_TOOL_SETTINGS['compatibility-mode']
os.environ['DANK_TOOL_OFFLINE_SRC'] = DANK_TOOL_SETTINGS['offline-src']
os.environ['DANK_TOOL_DEV_BRANCH'] = DANK_TOOL_SETTINGS['dev-branch']
OFFLINE_SRC = int(DANK_TOOL_SETTINGS['offline-src'])
DEV_BRANCH = int(DANK_TOOL_SETTINGS['dev-branch'])
BRANCH = ("main" if not DEV_BRANCH else "dev")

# compatability mode

if int(DANK_TOOL_SETTINGS['compatibility-mode']) or (os.getlogin() == 'xuser' and os.getenv("COMPUTERNAME") == 'LOCALHOST'):

    # https://no-color.org/
    os.environ['NO_COLOR'] = '1'
    import dankware
    dankware.reset = ''
    dankware.black = ''
    dankware.blue = ''
    dankware.cyan = ''
    dankware.green = ''
    dankware.magenta = ''
    dankware.red = ''
    dankware.white = ''
    dankware.yellow = ''
    dankware.black_bright = ''
    dankware.blue_bright = ''
    dankware.cyan_bright = ''
    dankware.green_bright = ''
    dankware.magenta_bright = ''
    dankware.red_bright = ''
    dankware.white_bright = ''
    dankware.yellow_bright = ''
    dankware.black_normal = ''
    dankware.blue_normal = ''
    dankware.cyan_normal = ''
    dankware.green_normal = ''
    dankware.magenta_normal = ''
    dankware.red_normal = ''
    dankware.white_normal = ''
    dankware.yellow_normal = ''
    dankware.black_dim = ''
    dankware.blue_dim = ''
    dankware.cyan_dim = ''
    dankware.green_dim = ''
    dankware.magenta_dim = ''
    dankware.red_dim = ''
    dankware.white_dim = ''
    dankware.yellow_dim = ''
    dankware.clr = lambda *args: args[0]
    from dankware import clr, reset, black, blue, cyan, green, magenta, red, white, yellow, black_bright, blue_bright, cyan_bright, green_bright, magenta_bright, red_bright, white_bright, yellow_bright, black_normal, blue_normal, cyan_normal, green_normal, magenta_normal, red_normal, white_normal, yellow_normal, black_dim, blue_dim, cyan_dim, green_dim, magenta_dim, red_dim, white_dim, yellow_dim # pylint: disable=reimported

# variables

DANK_TOOL_VERSION = "3.2.6"
session = requests.Session()
_executor = ThreadPoolExecutor(10)
headers = {"User-Agent": f"dank.tool {DANK_TOOL_VERSION}"}
os.environ['DANK_TOOL_VERSION'] = DANK_TOOL_VERSION

os.chdir(os.path.dirname(__file__))
title("𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 [ 𝚒𝚗𝚒𝚝𝚒𝚊𝚕𝚒𝚣𝚒𝚗𝚐 ]")
print(clr(f"\n  - Version: {DANK_TOOL_VERSION}"))

# handle KeyboardInterrupt

def print_warning_symbol():

    cls()
    banner = '\n\n[red]                      ██                      \n[red]                    ██  ██                    \n[red]                  ██      ██                  \n[red]                ██          ██                \n[red]                ██          ██                \n[red]              ██              ██              \n[red]            ██      [bright_white]██████[red]      ██            \n[red]            ██      [bright_white]██████[red]      ██            \n[red]          ██        [bright_white]██████[red]        ██          \n[red]          ██        [bright_white]██████[red]        ██          \n[red]        ██          [bright_white]██████[red]          ██        \n[red]      ██            [bright_white]██████[red]            ██      \n[red]      ██            [bright_white]██████[red]            ██      \n[red]    ██              [bright_white]██████[red]              ██    \n[red]    ██                                  ██    \n[red]  ██                [bright_white]██████[red]                ██  \n[red]  ██                [bright_white]██████[red]                ██  \n[red]██                  [bright_white]██████[red]                  ██\n[red]██                                          ██\n[red]  ██████████████████████████████████████████  \n\n'
    Console().print(Align.center(banner), style="blink", highlight=False)

# get latest version number

def latest_dank_tool_version():

    global BRANCH

    if int(DANK_TOOL_SETTINGS['offline-mode']):
        LATEST_VERSION = "0"
        os.environ['DANK_TOOL_ONLINE'] = "0"
        os.environ['DANK_TOOL_DEV_BRANCH'] = "0"
    else:
        try:
            while True:
                LATEST_VERSION = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/executor_version.txt", headers=headers, timeout=3).content.decode()
                if 'Not Found' in LATEST_VERSION:
                    print(clr("\n  - Please do not use the dev-branch, it is meant for testing/debugging only!",2))
                    BRANCH = "main"
                    os.environ['DANK_TOOL_DEV_BRANCH'] = "0"
                    with open('settings.json', 'r', encoding='utf-8') as file:
                        tmp = file.read().replace('"dev-branch": "1"', '"dev-branch": "0"')
                    with open('settings.json', 'w', encoding='utf-8') as file:
                        file.write(tmp); del tmp
                else:
                    break
            os.environ['DANK_TOOL_ONLINE'] = "1"
        except:
            LATEST_VERSION = "0"
            os.environ['DANK_TOOL_ONLINE'] = "0"
            os.environ['DANK_TOOL_DEV_BRANCH'] = "0"
    return LATEST_VERSION

LATEST_VERSION = latest_dank_tool_version()
ONLINE_MODE = int(os.environ['DANK_TOOL_ONLINE'])
DEV_BRANCH = int(os.environ['DANK_TOOL_DEV_BRANCH'])
BRANCH = ("main" if not DEV_BRANCH else "dev")

# version checker / updater

def dank_tool_installer():

    while True:
        try:
            code = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/updater.py", headers=headers, timeout=3).content.decode()
            break
        except Exception as exc:
            input(clr(f"\n  > Failed to get code! {exc} | Press [ENTER] to try again... ",2))
            rm_line(); rm_line()

    try: exec(code)
    except:
        err_message = err(sys.exc_info())
        try: session.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, timeout=3, data={"text": f"```<--- 🚨🚨🚨 ---> Version: {DANK_TOOL_VERSION}\n\n{err_message}```"})
        except: pass
        input(clr(f"{err_message}\n\n  > Press [ENTER] to EXIT... ",2))
        sys.exit(err_message)

# update environment variables

if parse(LATEST_VERSION) > parse(DANK_TOOL_VERSION) or (ONLINE_MODE and int(DANK_TOOL_SETTINGS['force-update'])):
    print(clr(f"\n  - Update Found: {LATEST_VERSION}" + ("" if not int(DANK_TOOL_SETTINGS['force-update']) else " [ FORCED ]")))
    if int(DANK_TOOL_SETTINGS['force-update']):
        with open('settings.json', 'r', encoding='utf-8') as _:
            settings = json.loads(_.read())
            settings['force-update'] = "0"
        with open('settings.json', 'w', encoding='utf-8') as _:
            _.write(json.dumps(settings, indent=4))
    dank_tool_installer()

elif LATEST_VERSION == DANK_TOOL_VERSION:
    if not DEV_BRANCH:
        print(clr("\n  - Latest Version!"))
    else:
        print(clr("\n  - Development Branch!"))

elif LATEST_VERSION == "0":
    print(clr("\n  - Offline Mode!"))

else: # LATEST VERSION IS LOWER THAN CURRENT VERSION
    print(clr("\n  - Development Version!"))

if OFFLINE_SRC:
    print(clr("\n  - Offline SRC!"))

# check windows language

def check_system_language():

    locale_name = str(getlocale()[0])
    if '-' in locale_name and '_' not in locale_name:
        locale_name = locale_name.split('-',1)[0]
    elif '_' in locale_name and '-' not in locale_name:
        locale_name = locale_name.split('_',1)[0]
    else:
        for _ in locale_name:
            if _ == '-':
                locale_name = locale_name.split('-',1)[0]
                break
            if _ == '_':
                locale_name = locale_name.split('_',1)[0]
                break

    if not locale_name.lower().startswith('en'):
        if int(DANK_TOOL_SETTINGS['force-translate']):
            os.environ['DANK_TOOL_LANG'] = locale_name
        elif not int(DANK_TOOL_SETTINGS['disable-translate']):
            translator = Translator()
            result = translator.translate("Would you like to enable the translate feature?", locale_name, 'en').result
            print(clr(f"\n  - Your system language is set to '{cyan}{locale_name}'!"))
            if input(clr(f"\n  > {result} [y/n]: ", colour_one=cyan) + cyan).lower() == 'y':
                result = translator.translate("You can force enable the translate feature in the settings menu", locale_name, 'en').result
                print(clr(f"\n  > {result}!"))
                os.environ['DANK_TOOL_LANG'] = locale_name
                time.sleep(6.5)
            else:
                os.environ['DANK_TOOL_LANG'] = "en"
    else:
        os.environ['DANK_TOOL_LANG'] = "en"

if ONLINE_MODE:
    check_system_language()
else:
    os.environ['DANK_TOOL_LANG'] = "en"
del check_system_language

# get and save dank.tool.py

if not os.path.isdir('__src__'): os.mkdir('__src__')
if not os.path.isdir('__modules__'): os.mkdir('__modules__')
if not os.path.isdir('__local_modules__'): os.mkdir('__local_modules__')

if not OFFLINE_SRC and ONLINE_MODE:
    while True:
        try: code = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/dank.tool.py", headers=headers, timeout=3).content.decode(); break
        except Exception as exc:
            input(clr(f"\n  > Failed to get code! {exc} | Press [ENTER] to try again... ",2))
            rm_line(); rm_line()
    with open('__src__/dank.tool.py', 'w', encoding='utf-8') as _:
        _.write(code)
else:
    while True:
        try:
            with open('__src__/dank.tool.py', 'r', encoding='utf-8') as _:
                code = _.read(); break
        except:
            input(clr("\n  > Failed to get code! Unable to read '__src__/dank.tool.py'! Press [ENTER] to try again... ",2))
            rm_line(); rm_line()

# start discord rpc

def dank_tool_discord_rpc():

    os.environ['DISCORD_RPC'] = "on the main menu"
    fail_counter = 0

    while True:
        if fail_counter >= 3: break
        try:
            RPC = Presence("1028269752386326538")
            RPC.connect()
            fail_counter = 0
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
        except:
            fail_counter += 1
            time.sleep(60)

if ONLINE_MODE:
    _executor.submit(dank_tool_discord_rpc)
else:
    del dank_tool_discord_rpc

# update counter

def dank_tool_runs_counter():

    fail_counter = 0
    session = requests.Session()
    while True:
        if fail_counter >= 3: break
        try: session.get("https://dank-site.onrender.com/counter?id=dank.tool&hit=true", headers=headers, timeout=3); break
        except: fail_counter += 1
        time.sleep(60)
    del globals()['dank_tool_runs_counter']

if ONLINE_MODE:
    _executor.submit(dank_tool_runs_counter)
else:
    del dank_tool_runs_counter

# chatroom user validator

def dank_tool_chatroom():

    fail_counter = 0
    session = requests.Session()
    while True:
        if fail_counter >= 3: break
        try: session.post("https://dank-site.onrender.com/chatroom-users", headers=headers, timeout=3); fail_counter = 0 # do not add a break here! (keeps user validated)
        except: fail_counter += 1
        time.sleep(240)
    del globals()['dank_tool_chatroom']

if ONLINE_MODE:
    _executor.submit(dank_tool_chatroom)
else:
    del dank_tool_chatroom

# execute, catch errors if any

title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 {DANK_TOOL_VERSION}")

if not ONLINE_MODE and not OFFLINE_SRC:
    time.sleep(2)

try: exec(code)
except:

    cls()
    err_message = err(sys.exc_info(), 'mini')
    print(clr(err_message, 2))
    LATEST_VERSION = latest_dank_tool_version()

    if "- SystemExit" in err_message:
        os.system("taskkill /f /t /im dank.tool.exe")
    elif "- EOFError" in err_message:
        print_warning_symbol()
        print(clr("\n  - No input provided!"))
    elif "- KeyboardInterrupt" in err_message:
        print_warning_symbol()
        print(clr("\n  - Please select text first and then use [ CTRL + C ]!"))

    elif parse(LATEST_VERSION) > parse(DANK_TOOL_VERSION):
        print(clr(f"\n  - Update Found: {LATEST_VERSION}"))
        dank_tool_installer()

    elif ONLINE_MODE:
        while True:
            try:
                requests.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, timeout=3, data={"text": f"```<--- 🚨🚨🚨 ---> v{DANK_TOOL_VERSION}{' OFFLINE_SRC' if OFFLINE_SRC else ''} BRANCH: {BRANCH}\n\n{err_message}```"})
                break
            except Exception as exc:
                input(clr(f"\n  > Failed to post error report! {exc} | Press [ENTER] to try again... ",2))
                rm_line(); rm_line()
        print(clr("\n  - Error Reported! If it is a logic error, it will be fixed soon!"))

    input(clr("\n  > Press [ENTER] to EXIT... "))
    os.system("taskkill /f /t /im dank.tool.exe")
