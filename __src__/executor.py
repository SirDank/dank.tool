###################################################################################

#                            https://github.com/SirDank

###################################################################################

"""
[NOTE]

- executor.py is meant to be executed only as an executable, not as a python script!
- the below packages are not required by the executor.py script but are required by the various __modules__ run by the dank.tool.exe
- they are listed here to be included in the final build of dank.tool.exe
"""

import json
import os
import sys
import time
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from locale import getlocale

import numpy
import pyminizip
import requests
import websocket
from dankware import clr, cls, cyan, err, rm_line, title
from dankware.tkinter import file_selector, folder_selector
from dateutil.tz import tzlocal, tzutc
from direct.filter.CommonFilters import CommonFilters
from mcstatus import BedrockServer, JavaServer
from packaging.version import parse
from perlin_noise import PerlinNoise
from PIL import Image
from playsound import playsound
from psutil import process_iter
from rich.align import Align
from rich.console import Console
from socketio import Client
from translatepy import Translator
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from ursina.prefabs.splash_screen import SplashScreen
from ursina.scripts.smooth_follow import SmoothFollow

# windows specific

WINDOWS = os.name == "nt" and "WINELOADER" not in os.environ
if WINDOWS:
    from pypresence import Presence
    from win11toast import notify

# debug env variables


def settings_json():
    overwrite = False
    settings = {
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

    # wine support

    if (os.name == "posix") or ("WINELOADER" in os.environ) or os.getlogin() == "xuser" or ("USERNAME" in os.environ and os.environ["USERNAME"] == "xuser") or ("NO_COLOR" in os.environ):
        settings["compatibility-mode"] = "1"
        os.environ["COMPATIBILITY-MODE"] = "1"

    if not os.path.isfile("settings.json"):
        overwrite = True
    else:
        with open("settings.json", "r", encoding="utf-8") as file:
            data = json.loads(file.read())
        for key in settings:
            if key not in data:
                overwrite = True
            else:
                settings[key] = data[key]
        if settings != data:
            overwrite = True

    if overwrite:
        with open("settings.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(settings, indent=4))


settings_json()
del settings_json

with open("settings.json", "r", encoding="utf-8") as _:
    DANK_TOOL_SETTINGS = json.loads(_.read())
OFFLINE_SRC = int(DANK_TOOL_SETTINGS["offline-src"])
DEV_BRANCH = int(DANK_TOOL_SETTINGS["dev-branch"])
BRANCH = "main" if not DEV_BRANCH else "dev"

# compatability mode

if int(DANK_TOOL_SETTINGS["compatibility-mode"]):
    # https://no-color.org/
    os.environ["NO_COLOR"] = "1"
    import dankware

    dankware.reset = ""
    dankware.black = ""
    dankware.blue = ""
    dankware.cyan = ""
    dankware.green = ""
    dankware.magenta = ""
    dankware.red = ""
    dankware.white = ""
    dankware.yellow = ""
    dankware.black_bright = ""
    dankware.blue_bright = ""
    dankware.cyan_bright = ""
    dankware.green_bright = ""
    dankware.magenta_bright = ""
    dankware.red_bright = ""
    dankware.white_bright = ""
    dankware.yellow_bright = ""
    dankware.black_normal = ""
    dankware.blue_normal = ""
    dankware.cyan_normal = ""
    dankware.green_normal = ""
    dankware.magenta_normal = ""
    dankware.red_normal = ""
    dankware.white_normal = ""
    dankware.yellow_normal = ""
    dankware.black_dim = ""
    dankware.blue_dim = ""
    dankware.cyan_dim = ""
    dankware.green_dim = ""
    dankware.magenta_dim = ""
    dankware.red_dim = ""
    dankware.white_dim = ""
    dankware.yellow_dim = ""
    dankware.clr = lambda text, preset=None, colour_one=None, colour_two=None, colours=None: text
    from dankware import (  # pylint: disable=reimported
        black,
        black_bright,
        black_dim,
        black_normal,
        blue,
        blue_bright,
        blue_dim,
        blue_normal,
        clr,
        cyan,
        cyan_bright,
        cyan_dim,
        cyan_normal,
        green,
        green_bright,
        green_dim,
        green_normal,
        magenta,
        magenta_bright,
        magenta_dim,
        magenta_normal,
        red,
        red_bright,
        red_dim,
        red_normal,
        reset,
        white,
        white_bright,
        white_dim,
        white_normal,
        yellow,
        yellow_bright,
        yellow_dim,
        yellow_normal,
    )

# variables

DANK_TOOL_VERSION = "3.2.9"
session = requests.Session()
_executor = ThreadPoolExecutor(10)
headers = {"User-Agent": f"dank.tool {DANK_TOOL_VERSION}"}
os.environ["DANK_TOOL_VERSION"] = DANK_TOOL_VERSION

title("𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 [ 𝚒𝚗𝚒𝚝𝚒𝚊𝚕𝚒𝚣𝚒𝚗𝚐 ]")
print(clr(f"\n  - Version: {DANK_TOOL_VERSION}"))

# handle KeyboardInterrupt


def print_warning_symbol():
    cls()
    banner = "\n\n[red]                      ██                      \n[red]                    ██  ██                    \n[red]                  ██      ██                  \n[red]                ██          ██                \n[red]                ██          ██                \n[red]              ██              ██              \n[red]            ██      [bright_white]██████[red]      ██            \n[red]            ██      [bright_white]██████[red]      ██            \n[red]          ██        [bright_white]██████[red]        ██          \n[red]          ██        [bright_white]██████[red]        ██          \n[red]        ██          [bright_white]██████[red]          ██        \n[red]      ██            [bright_white]██████[red]            ██      \n[red]      ██            [bright_white]██████[red]            ██      \n[red]    ██              [bright_white]██████[red]              ██    \n[red]    ██                                  ██    \n[red]  ██                [bright_white]██████[red]                ██  \n[red]  ██                [bright_white]██████[red]                ██  \n[red]██                  [bright_white]██████[red]                  ██\n[red]██                                          ██\n[red]  ██████████████████████████████████████████  \n\n"
    Console().print(Align.center(banner), style="blink", highlight=False)


# get latest version number


def latest_dank_tool_version():
    global BRANCH

    if int(DANK_TOOL_SETTINGS["offline-mode"]):
        LATEST_VERSION = "0"
        os.environ["DANK_TOOL_ONLINE"] = "0"
    else:
        try:
            while True:
                LATEST_VERSION = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/executor_version.txt", headers=headers, timeout=3).content.decode()
                if "Not Found" in LATEST_VERSION:
                    print(clr("\n  - Please do not use the dev-branch, it is meant for testing/debugging only!", 2))
                    BRANCH = "main"
                    with open("settings.json", "r", encoding="utf-8") as file:
                        tmp = file.read().replace('"dev-branch": "1"', '"dev-branch": "0"')
                    with open("settings.json", "w", encoding="utf-8") as file:
                        file.write(tmp)
                        del tmp
                else:
                    break
            os.environ["DANK_TOOL_ONLINE"] = "1"
        except:
            LATEST_VERSION = "0"
            os.environ["DANK_TOOL_ONLINE"] = "0"
    return LATEST_VERSION


LATEST_VERSION = latest_dank_tool_version()
ONLINE_MODE = int(os.environ["DANK_TOOL_ONLINE"])
with open("settings.json", "r", encoding="utf-8") as file:
    DEV_BRANCH = int(json.loads(file.read())["dev-branch"])
BRANCH = "main" if not DEV_BRANCH else "dev"

# version checker / updater


def dank_tool_installer():
    while True:
        try:
            code = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/updater.py", headers=headers, timeout=3).content.decode()
            break
        except Exception as exc:
            input(clr(f"\n  > Failed to get code! {exc} | Press [ENTER] to try again... ", 2))
            rm_line()
            rm_line()

    try:
        exec(code)
    except Exception as exc:
        error = err((type(exc), exc, exc.__traceback__), "mini")
        try:
            session.post("https://dankware.onrender.com/dank-tool-errors", headers=headers, timeout=3, data={"text": f"🚨🚨🚨 Version: {DANK_TOOL_VERSION}\n\n{error}"})
        except:
            pass
        input(clr(f"{error}\n\n  > Press [ENTER] to EXIT... ", 2))
        sys.exit(error)


# update environment variables

if parse(LATEST_VERSION) > parse(DANK_TOOL_VERSION) or (ONLINE_MODE and int(DANK_TOOL_SETTINGS["force-update"])):
    print(clr(f"\n  - Update Found: {LATEST_VERSION}" + ("" if not int(DANK_TOOL_SETTINGS["force-update"]) else " [ FORCED ]")))
    if int(DANK_TOOL_SETTINGS["force-update"]):
        with open("settings.json", "r", encoding="utf-8") as _:
            settings = json.loads(_.read())
            settings["force-update"] = "0"
        with open("settings.json", "w", encoding="utf-8") as _:
            _.write(json.dumps(settings, indent=4))
    dank_tool_installer()

elif LATEST_VERSION == DANK_TOOL_VERSION:
    if not DEV_BRANCH:
        print(clr("\n  - Latest Version!"))
    else:
        print(clr("\n  - Development Branch!"))

elif LATEST_VERSION == "0":
    print(clr("\n  - Offline Mode!"))

else:  # LATEST VERSION IS LOWER THAN CURRENT VERSION
    print(clr("\n  - Development Version!"))

if OFFLINE_SRC:
    print(clr("\n  - Offline SRC!"))

# check windows language


def check_system_language():
    locale_name = str(getlocale()[0])
    if "-" in locale_name and "_" not in locale_name:
        locale_name = locale_name.split("-", 1)[0]
    elif "_" in locale_name and "-" not in locale_name:
        locale_name = locale_name.split("_", 1)[0]
    else:
        for _ in locale_name:
            if _ == "-":
                locale_name = locale_name.split("-", 1)[0]
                break
            if _ == "_":
                locale_name = locale_name.split("_", 1)[0]
                break

    if not locale_name.lower().startswith("en"):
        if int(DANK_TOOL_SETTINGS["force-translate"]):
            os.environ["DANK_TOOL_LANG"] = locale_name
        elif not int(DANK_TOOL_SETTINGS["disable-translate"]):
            translator = Translator()
            result = translator.translate("Would you like to enable the translate feature?", locale_name, "en").result
            print(clr(f"\n  - Your system language is set to '{cyan}{locale_name}'!"))
            if input(clr(f"\n  > {result} [y/n]: ", colour_one=cyan) + cyan).lower() == "y":
                result = translator.translate("You can force enable the translate feature in the settings menu", locale_name, "en").result
                print(clr(f"\n  > {result}!"))
                os.environ["DANK_TOOL_LANG"] = locale_name
                time.sleep(6.5)
            else:
                os.environ["DANK_TOOL_LANG"] = "en"
    else:
        os.environ["DANK_TOOL_LANG"] = "en"


if ONLINE_MODE:
    check_system_language()
else:
    os.environ["DANK_TOOL_LANG"] = "en"
del check_system_language

# get and save dank.tool.py

if not os.path.isdir("__src__"):
    os.mkdir("__src__")
if not os.path.isdir("__modules__"):
    os.mkdir("__modules__")
if not os.path.isdir("__local_modules__"):
    os.mkdir("__local_modules__")

if not OFFLINE_SRC and ONLINE_MODE:
    while True:
        try:
            code = session.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/dank.tool.py", headers=headers, timeout=3).content.decode()
            break
        except Exception as exc:
            input(clr(f"\n  > Failed to get code! {exc} | Press [ENTER] to try again... ", 2))
            rm_line()
            rm_line()
    with open("__src__/dank.tool.py", "w", encoding="utf-8") as _:
        _.write(code)
else:
    while True:
        try:
            with open("__src__/dank.tool.py", "r", encoding="utf-8") as _:
                code = _.read()
                break
        except:
            input(clr("\n  > Failed to get code! Unable to read '__src__/dank.tool.py'! Press [ENTER] to try again... ", 2))
            rm_line()
            rm_line()

# start discord rpc


def dank_tool_discord_rpc():
    os.environ["DISCORD_RPC"] = "on the main menu"
    fail_counter = 0

    while True:
        if fail_counter >= 3:
            break
        try:
            RPC = Presence("1028269752386326538")
            RPC.connect()
            fail_counter = 0
            start = int(time.time())
            while True:
                try:
                    RPC.update(
                        large_image="dankware",
                        large_text="dankware",
                        details=f"[ dank.tool {DANK_TOOL_VERSION} ]",
                        state=os.environ["DISCORD_RPC"],
                        start=start,
                        buttons=[{"label": "Download", "url": "https://github.com/SirDank/dank.tool"}, {"label": "Discord", "url": "https://allmylinks.com/link/out?id=kdib4s-nu8b-1e19god"}],
                    )
                    time.sleep(15)
                except:
                    break
        except:
            fail_counter += 1
            time.sleep(60)


if ONLINE_MODE and WINDOWS:
    _executor.submit(dank_tool_discord_rpc)
else:
    del dank_tool_discord_rpc

# update counter


def dank_tool_runs_counter():
    fail_counter = 0
    session = requests.Session()
    while True:
        if fail_counter >= 3:
            break
        try:
            # for an upcoming stats feature
            response = session.get("http://ipwho.is", timeout=3).json()
            response = {"continent": response["continent"], "continent_code": response["continent_code"], "country": response["country"], "country_code": response["country_code"], "region": response["region"], "region_code": response["region_code"], "city": response["city"]}
            session.post("https://dankware.onrender.com/counter?id=dank.tool&hit=true", headers=headers, json=response, timeout=10)
            break
        except:
            fail_counter += 1
        time.sleep(60)
    del globals()["dank_tool_runs_counter"]


if ONLINE_MODE:
    _executor.submit(dank_tool_runs_counter)
else:
    del dank_tool_runs_counter

# chatroom user validator


def dank_tool_chatroom():
    fail_counter = 0
    session = requests.Session()
    while True:
        if fail_counter >= 3:
            break
        try:
            session.post("https://dankware.onrender.com/chatroom-users", headers=headers, timeout=3)
            fail_counter = 0  # do not add a break here! (keeps user validated)
        except:
            fail_counter += 1
        time.sleep(240)
    del globals()["dank_tool_chatroom"]


if ONLINE_MODE:
    _executor.submit(dank_tool_chatroom)
else:
    del dank_tool_chatroom

# execute, catch errors if any

title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 {DANK_TOOL_VERSION}")

if not ONLINE_MODE and not OFFLINE_SRC:
    time.sleep(2)

try:
    exec(code)
except Exception as exc:
    cls()
    error = err((type(exc), exc, exc.__traceback__), "mini")
    print(clr(error, 2))
    LATEST_VERSION = latest_dank_tool_version()

    if "- SystemExit" in error:
        os.system("taskkill /f /t /im dank.tool.exe")
    elif "- EOFError" in error:
        print_warning_symbol()
        print(clr("\n  - No input provided!"))
    elif "- KeyboardInterrupt" in error:
        print_warning_symbol()
        print(clr("\n  - Please select text first and then use [ CTRL + C ]!"))

    elif parse(LATEST_VERSION) > parse(DANK_TOOL_VERSION):
        print(clr(f"\n  - Update Found: {LATEST_VERSION}"))
        dank_tool_installer()

    elif ONLINE_MODE:
        while True:
            try:
                requests.post("https://dankware.onrender.com/dank-tool-errors", headers=headers, timeout=3, data={"text": f"🚨🚨🚨 v{DANK_TOOL_VERSION}{' OFFLINE_SRC' if OFFLINE_SRC else ''} BRANCH: {BRANCH}\n\n{error}"})
                break
            except Exception as exc:
                input(clr(f"\n  > Failed to post error report! {exc} | Press [ENTER] to try again... ", 2))
                rm_line()
                rm_line()
        print(clr("\n  - Error Reported! If it is a logic error, it will be fixed soon!"))

    input(clr("\n  > Press [ENTER] to EXIT... "))
    os.system("taskkill /f /t /im dank.tool.exe")
