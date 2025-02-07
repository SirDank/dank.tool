###################################################################################

#                            https://github.com/SirDank                            

###################################################################################

import datetime
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from types import NoneType
import requests
from dateutil.tz import tzlocal, tzutc
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from translatepy import Translator
from win11toast import notify
from dankware import (
    clr,
    cls,
    err,
    get_duration,
    get_path,
    green,
    green_bright,
    multithread,
    red,
    red_normal,
    rm_line,
    title,
    white,
    white_bright,
)

def set_title():
    title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 {DANK_TOOL_VERSION}" + ("" if ONLINE_MODE else " [ 𝙾𝙵𝙵𝙻𝙸𝙽𝙴 ]")) # DANK_TOOL_VERSION defined in executor.py

# dank.tool updater

def dank_tool_installer():

    while True:
        try:
            code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/updater.py", headers=headers, timeout=3).content.decode()
            break
        except Exception as exc:
            input(clr(f"\n  > Failed to get code! {exc} | Press [ENTER] to try again... ",2))
            rm_line(); rm_line()

    try: exec(code)
    except:
        err_message = err(sys.exc_info())
        try: requests.post("https://dankware.onrender.com/dank-tool-errors", headers=headers, timeout=3, data={"text": f"```<--- 🚨🚨🚨 ---> Version: {DANK_TOOL_VERSION}\n\n{err_message}```"})
        except: pass
        input(clr(f"{err_message}\n\n  > Press [ENTER] to EXIT... ",2))
        sys.exit(err_message)

# print coloured and aligned banner

def dank_tool_banner():

    cls()
    banner = '\n   ..                                       ..                  s                                  .. \n dF                                   < .z@8"`                 :8                            x .d88"  \n\'88bu.                     u.    u.    !@88E                  .88           u.          u.    5888R   \n\'*88888bu         u      x@88k u@88c.  \'888E   u             :888ooo  ...ue888b   ...ue888b   \'888R   \n  ^"*8888N     us888u.  ^"8888""8888"   888E u@8NL         -*8888888  888R  888r  888R  888r   888R   \n beWE "888L .@88 "8888"   8888  888R    888E`"88*"           8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E .dN.            8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E~8888            8888     888R  888>  888R  888>   888R   \n 888E  888F 9888  9888    8888  888R    888E \'888&     .    .8888Lu= u8888cJ888  u8888cJ888    888R   \n.888N..888  9888  9888   "*88*" 8888"   888E  9888.  .@8c   ^%888*    "*888*P"    "*888*P"    .888B . \n `"888*""   "888*""888"    ""   \'Y"   \'"888*" 4888" \'%888"    \'Y"       \'Y"         \'Y"       ^*888%  \n    ""       ^Y"   ^Y\'                   ""    ""     ^*                                        "%    \n'
    console = Console(highlight=False)
    console.print(Align.center(banner), style="blink red")
    console.print(Align.center("[bright_white]s i r [red]. [bright_white]d a n k [red]💕\n"), style="blink")

def palestine_banner():

    #cls()
    banner = '\n[red]###[black]###########################################\n[red]#####[black]#########################################\n[red]########[black]######################################\n[red]##########[black]####################################\n[red]############[white]##################################\n[red]##############[white]################################\n[red]################[white]##############################\n[red]##############[white]################################\n[red]############[white]##################################\n[red]##########[green]####################################\n[red]########[green]######################################\n[red]#####[green]#########################################\n[red]###[green]###########################################\n'
    console = Console(highlight=False)
    console.print(Align.center(banner), style="blink")
    console.print(Align.center("[white]U S E [red]. [white]Y O U R [red]. [white]V O I C E\n"), style="blink")

# handle KeyboardInterrupt

def print_warning_symbol():

    cls()
    banner = '\n\n[red]                      ██                      \n[red]                    ██  ██                    \n[red]                  ██      ██                  \n[red]                ██          ██                \n[red]                ██          ██                \n[red]              ██              ██              \n[red]            ██      [bright_white]██████[red]      ██            \n[red]            ██      [bright_white]██████[red]      ██            \n[red]          ██        [bright_white]██████[red]        ██          \n[red]          ██        [bright_white]██████[red]        ██          \n[red]        ██          [bright_white]██████[red]          ██        \n[red]      ██            [bright_white]██████[red]            ██      \n[red]      ██            [bright_white]██████[red]            ██      \n[red]    ██              [bright_white]██████[red]              ██    \n[red]    ██                                  ██    \n[red]  ██                [bright_white]██████[red]                ██  \n[red]  ██                [bright_white]██████[red]                ██  \n[red]██                  [bright_white]██████[red]                  ██\n[red]██                                          ██\n[red]  ██████████████████████████████████████████  \n\n'
    Console().print(Align.center(banner), style="blink", highlight=False)

# get commit date & time

def updated_on(url, dankware_module = True):

    if dankware_module: url = f"https://api.github.com/repos/SirDank/dank.tool/commits?path=__modules__/{url}.py&page=1&per_page=1" + ('' if not DEV_BRANCH else '&sha=dev')
    try:

        response = requests.get(url, headers=headers, timeout=3).json()
        if not response:
            return "[red1][[red] unreleased [red1]]"

        date, time = response[0]["commit"]["author"]["date"].split("T")
        date = date.split("-")
        time = time.replace("Z","").split(":")
        date_time_data = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]), tzinfo=tzutc())
        return f"[bright_green]🔄 {get_duration(date_time_data, datetime.datetime.now(tzlocal()), interval='dynamic-mini')} ago"

    except: return "" # [red1]⚠️

# multithread requests

def get_menu_request_responses(task_id, request_key):

    match task_id:
        case 0 | 1: # get global runs
            match task_id:
                case 0: url = "https://dankware.onrender.com/counter?id=dankware&hit=false"
                case 1: url = "https://dankware.onrender.com/counter?id=dank.tool&hit=false"
            menu_request_responses[request_key] = f"{red_normal}⚠️"
            try:
                result = requests.get(url, headers=headers, timeout=3).content.decode().replace('<pre>','').replace('</pre>','')
                if result.isdigit():
                    menu_request_responses[request_key] = result
            except:
                pass

        case 2: # get motm
            try:
                motm = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/motm.txt", headers=headers, timeout=3).content.decode()
                motm = clr(motm, colour_one=green_bright)
            except:
                motm = f"{red_normal}⚠️"
            menu_request_responses[request_key] = motm

        case 3: # get chatroom user count
            try:
                result = requests.get("https://dankware.onrender.com/chatroom-users", headers=headers, timeout=3).content.decode()
                if result.isdigit():
                    if result != "0": menu_request_responses[request_key] = result
                    else: menu_request_responses[request_key] = "1"
                    menu_request_responses[request_key] = f"[bright_green]{menu_request_responses[request_key]} online{' (you)' if menu_request_responses[request_key] == '1' else ''}"
                else: menu_request_responses[request_key] = "[red1]⚠️"
            except: menu_request_responses[request_key] = "[red1]⚠️"

def get_menu_request_responses_api(task_id, request_key):

    match task_id:
        case 0 | 1 | 2 | 3 | 4: # get last update time for modules based on external repos
            match task_id:
                case 0: url = "https://api.github.com/repos/SpotX-Official/SpotX/commits?path=.&page=1&per_page=1"
                case 1: url = "https://api.github.com/repos/spicetify/spicetify-cli/commits?path=.&page=1&per_page=1"
                case 2: url = "https://api.github.com/repos/massgravel/Microsoft-Activation-Scripts/commits?path=.&page=1&per_page=1"
                case 3: url = "https://api.github.com/repos/Baseult/NetLimiterCrack/commits?path=.&page=1&per_page=1"
                case 4: url = "https://api.github.com/repos/Vendicated/Vencord/commits?path=.&page=1&per_page=1"
            menu_request_responses[request_key] = updated_on(url, False)

        case _: # get last update time for modules based on internal repo
            menu_request_responses[request_key] = updated_on(request_key)

# multithreaded module / asset downloader

def download_offline_modules(project):

    code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__modules__/{project}.py", headers=headers, timeout=3).content.decode()
    with open(f'__modules__/{project}.py', 'w', encoding='utf-8') as file:
        file.write(code)

def download_assets(url, file_name):

    data = requests.get(url, headers=headers, timeout=3).content
    with open(file_name, 'wb') as file:
        file.write(data)

# print modules with index and get choice

def print_modules():

    dank_tool_banner(); print(clr(f"\n  - Modules:{stats}") + red_normal + ('' if ONLINE_MODE else ' OFFLINE') + ('' if not OFFLINE_SRC else ' DEBUG') + ('' if not DEV_BRANCH else ' ONLINE DEBUG') + "\n")
    user_renderables = []
    counter = 1

    # online modules

    for _title, module in modules.items():
        if not module['category']:
            user_renderables.append(f"[b][bright_white]{counter} [red1]- [bright_white]{_title}[/b] {module['info']}")
        else:
            user_renderables.append(f"[b][bright_white]{counter} [red1][ [bright_white]{_title}[/b] [red1]]")
        counter += 1

    # local modules

    for _title in local_modules:
        user_renderables.append(f"[b][bright_white]{counter} [bright_cyan]- [bright_white]{_title}[/b]")
        counter += 1

    Console().print(Panel(title="[red1]> [bright_white][b]M O D U L E S[/b] [red1]<", title_align="center", renderable=Columns(user_renderables, expand=True), style="red", expand=True), highlight=False)
    print()

def print_category_modules(modules):

    dank_tool_banner(); print(clr(f"\n  - Modules:{stats}") + red_normal + ('' if ONLINE_MODE else ' OFFLINE') + ('' if not OFFLINE_SRC else ' DEBUG') + ('' if not DEV_BRANCH else ' ONLINE DEBUG') + "\n")
    user_renderables = []
    counter = 1

    # category modules

    user_renderables.append("[b][bright_white]0 [red1]- [bright_white]Return to menu[/b]")
    for _title, module in modules.items():
        if _title != "category":
            user_renderables.append(f"[b][bright_white]{counter} [red1]- [bright_white]{_title}[/b] {module['info']}")
            counter += 1

    Console().print(Panel(title="[b][red1]> [bright_white]M O D U L E S [red1]- [bright_white]I N [red1]- [bright_white]C A T E G O R Y [red1]<[/b]", title_align="center", renderable=Columns(user_renderables, expand=True), style="red", expand=True), highlight=False)
    print()

# set globals

def set_globals_one():

    global OFFLINE_SRC, DEV_BRANCH, DANK_TOOL_VERSION, ONLINE_MODE, COMPATIBILITY_MODE, DANK_TOOL_LANG, BRANCH, headers

    with open("settings.json", "r", encoding="utf-8") as file:
        settings = json.loads(file.read())

    OFFLINE_SRC = int(settings['offline-src'])
    DEV_BRANCH = int(settings['dev-branch'])
    DANK_TOOL_VERSION = os.environ['DANK_TOOL_VERSION']
    ONLINE_MODE = int(os.environ['DANK_TOOL_ONLINE'])
    COMPATIBILITY_MODE = int(settings['compatibility-mode'])
    try:
        DANK_TOOL_LANG = os.environ['DANK_TOOL_LANG']
        DANK_TOOL_LANG = ('' if DANK_TOOL_LANG == 'en' else DANK_TOOL_LANG)
    except:
        DANK_TOOL_LANG = ''
    BRANCH = ("main" if not DEV_BRANCH else "dev")
    headers = {"User-Agent": f"dank.tool {DANK_TOOL_VERSION}"}

    global offline_modules, offline_scripts

    offline_modules = {

        'OS Tools': {

            'Operating System Repair': {
                'info': '',
                'title': "𝚍𝚊𝚗𝚔.𝚘𝚜-𝚛𝚎𝚙𝚊𝚒𝚛",
                'project': "dank.os-repair",
                'rpc': "repairing windows operating system"    
            },

            'Network Reset': {
                'info': '',
                'title': "𝚍𝚊𝚗𝚔.𝚗𝚎𝚝𝚠𝚘𝚛𝚔-𝚛𝚎𝚜𝚎𝚝",
                'project': "dank.network-reset",
                'rpc': "resetting network settings"
            },

            'Clear Icon & Thumbnail Cache': {
                'info': '',
                'title': "𝚍𝚊𝚗𝚔.𝚌𝚕𝚎𝚊𝚛-𝚒𝚌𝚘𝚗𝚜",
                'project': "dank.clear-icons",
                'rpc': "clearing icon and thumbnail cache"
            },

            'category': True,
        },

        'Software Patchers': {

            'WinRAR': {
                'info': '',
                'title': "𝚍𝚊𝚗𝚔.𝚠𝚒𝚗𝚛𝚊𝚛",
                'project': "dank.winrar",
                'rpc': "patching winrar"
            },

            'Revo Uninstaller Pro': {
                'info': '',
                'title': "𝚍𝚊𝚗𝚔.𝚛𝚎𝚟𝚘-𝚞𝚗𝚒𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚛",
                'project': "dank.revo-uninstaller",
                'rpc': "patching revo uninstaller pro"
            },

            'category': True
        },

        'Browser Backup': {
            'info': '',
            'title': "𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙",
            'project': "dank.browser-backup",
            'rpc': "backing up a browser",
            'category': False,
        },

        'World Exploration Game [red1][[red]BETA[red1]]': {
            'info': '',
            'title': "𝚍𝚊𝚗𝚔.𝚐𝚊𝚖𝚎",
            'project': "dank.game",
            'rpc': "playing a world exploration game",
            'category': False,
        },

        'Settings': {
            'info': '',
            'title': "𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 𝚜𝚎𝚝𝚝𝚒𝚗𝚐𝚜",
            'project': "dank.tool settings",
            'rpc': "changing dank.tool settings",
            'category': False,
        }
    }

    offline_scripts = tuple(("dank.fusion-fall", "dank.browser-backup", "dank.game"))

def set_globals_two():

    global stats

    if ONLINE_MODE:

        global online_modules

        stats = f" [ dankware runs: {menu_request_responses['dankware_runs']} | dank.tool runs: {menu_request_responses['danktool_runs']} | motm: {menu_request_responses['motm']} ]"

        online_modules = {

            _translate('Minecraft Tools'): {

                _translate('Minecraft Server Builder'): {
                    'info': menu_request_responses["dank.minecraft-server-builder"],
                    'title': "𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚋𝚞𝚒𝚕𝚍𝚎𝚛",
                    'project': "dank.minecraft-server-builder",
                    'rpc': _translate("building a minecraft server")
                },

                _translate('Minecraft Server Scanner'): {
                    'info': menu_request_responses["dank.minecraft-server-scanner"],
                    'title': "𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚜𝚌𝚊𝚗𝚗𝚎𝚛",
                    'project': "dank.minecraft-server-scanner",
                    'rpc': _translate("scanning for minecraft servers")
                },

                'category': True
            },

            _translate('OS Tools'): {

                _translate('Software Installer / Updater'): {
                    'info': menu_request_responses["dank.winget"],
                    'title': "𝚍𝚊𝚗𝚔.𝚠𝚒𝚗𝚐𝚎𝚝",
                    'project': "dank.winget",
                    'rpc': _translate("installing / updating software")
                },

                _translate('Windows / Office Activator'): {
                    'info': menu_request_responses["Microsoft-Activation-Scripts"],
                    'title': "𝚍𝚊𝚗𝚔.𝚠𝚒𝚗-𝚊𝚌𝚝𝚒𝚟𝚊𝚝𝚎",
                    'project': "dank.win-activate",
                    'rpc': _translate("activating windows / office")
                },

                _translate('Operating System Repair'): {
                    'info': '',
                    'title': "𝚍𝚊𝚗𝚔.𝚘𝚜-𝚛𝚎𝚙𝚊𝚒𝚛",
                    'project': "dank.os-repair",
                    'rpc': _translate("repairing windows operating system")
                },

                _translate('Network Reset'): {
                    'info': '',
                    'title': "𝚍𝚊𝚗𝚔.𝚗𝚎𝚝𝚠𝚘𝚛𝚔-𝚛𝚎𝚜𝚎𝚝",
                    'project': "dank.network-reset",
                    'rpc': _translate("resetting network settings")
                },

                _translate('Clear Icon & Thumbnail Cache'): {
                    'info': '',
                    'title': "𝚍𝚊𝚗𝚔.𝚌𝚕𝚎𝚊𝚛-𝚒𝚌𝚘𝚗𝚜",
                    'project': "dank.clear-icons",
                    'rpc': _translate("clearing icon and thumbnail cache")
                },

                'category': True

            },

            _translate('Software Patchers'): {

                'Spotify': {
                    'info': (f'{menu_request_responses["Spicetify"]}, {menu_request_responses["SpotX"]}' if menu_request_responses["Spicetify"] and menu_request_responses["SpotX"] else ""),
                    'title': "𝚍𝚊𝚗𝚔.𝚜𝚙𝚘𝚝𝚒𝚏𝚢",
                    'project': "dank.spotify",
                    'rpc': _translate("patching spotify using spotx and spicetify")
                },

                'Vencord': {
                    'info': menu_request_responses["Vencord"],
                    'title': "𝚍𝚊𝚗𝚔.𝚟𝚎𝚗𝚌𝚘𝚛𝚍",
                    'project': "dank.vencord",
                    'rpc': _translate("patching discord using vencord")
                },

                'NetLimiter Pro': {
                    'info': menu_request_responses["NetLimiter"],
                    'title': "𝚍𝚊𝚗𝚔.𝚗𝚎𝚝𝚕𝚒𝚖𝚒𝚝𝚎𝚛",
                    'project': "dank.netlimiter",
                    'rpc': _translate("patching netlimiter pro")
                },

                'WinRAR': {
                    'info': '',
                    'title': "𝚍𝚊𝚗𝚔.𝚠𝚒𝚗𝚛𝚊𝚛",
                    'project': "dank.winrar",
                    'rpc': _translate("patching winrar")
                },

                'Revo Uninstaller Pro': {
                    'info': '',
                    'title': "𝚍𝚊𝚗𝚔.𝚛𝚎𝚟𝚘-𝚞𝚗𝚒𝚗𝚜𝚝𝚊𝚕𝚕𝚎𝚛",
                    'project': "dank.revo-uninstaller",
                    'rpc': _translate("patching revo uninstaller pro")
                },

                'category': True

            },

            _translate('Browser Backup'): {
                'info': menu_request_responses["dank.browser-backup"],
                'title': "𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙",
                'project': "dank.browser-backup",
                'rpc': _translate("backing up a browser"),
                'category': False
            },

            _translate('World Exploration Game') + ' [red1][[red]BETA[red1]]': {
                'info': menu_request_responses["dank.game"],
                'title': "𝚍𝚊𝚗𝚔.𝚐𝚊𝚖𝚎",
                'project': "dank.game",
                'rpc': _translate("playing a world exploration game"),
                'category': False
            },

            #'Auto Clicker [red1][[red]WIP[red1]]': {
            #    'info': menu_request_responses["dank.auto-clicker"],
            #    'title': "𝚍𝚊𝚗𝚔.𝚊𝚞𝚝𝚘-𝚌𝚕𝚒𝚌𝚔𝚎𝚛",
            #    'project': "dank.auto-clicker",
            #    'rpc': "running auto-clicker"
            #},

            # _translate('Chatroom'): {
            #     'info': menu_request_responses["chatroom_user_count"],
            #     'title': "𝚍𝚊𝚗𝚔.𝚌𝚑𝚊𝚝𝚛𝚘𝚘𝚖",
            #     'project': "dank.chatroom",
            #     'rpc': _translate("chatting in the chatroom"),
            #     'category': False
            # },

            'Discord / Telegram': {

                'Discord Server': {
                    'info': '[bright_green]Join Now!',
                    'project': "Discord Server"
                },

                'Telegram Group': {
                    'info': '[bright_green]Join Now!',
                    'project': "Telegram Group"
                },

                'YouTube': {
                    'info': '[bright_green]Subscribe!',
                    'project': "YouTube"
                },

                'Website': {
                    'info': '[bright_green]Visit Now!',
                    'project': "Website"
                },

                'category': True
            },

            _translate('Settings'): {
                'info': '',
                'title': "𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 𝚜𝚎𝚝𝚝𝚒𝚗𝚐𝚜",
                'project': "dank.tool settings",
                'rpc': _translate("changing dank.tool settings"),
                'category': False
            }
        }

    else:

        stats = ""
        online_modules = {}

# translator

def _translate(text):

    if DANK_TOOL_LANG and ONLINE_MODE:
        try: text = _translator.translate(text, DANK_TOOL_LANG, 'en').result
        except: pass
    return text

# built-in modules

def debug_mode():

    cls(); title("𝚍𝚎𝚋𝚞𝚐 𝚖𝚘𝚍𝚎")
    while True:
        # this variable is long to prevent it from being changed!
        cmd_to_be_executed = input(clr("\n  > ") + white_bright)
        match cmd_to_be_executed:
            case 'exit' | 'EXIT' | 'stop' | 'STOP': print_modules(); break
            case 'env' | 'globals':
                print()
                if cmd_to_be_executed == 'env':
                    for key, val in os.environ.items():
                        print(f"{green_bright}{key}{white}: {green}{val}")
                elif cmd_to_be_executed == 'globals':
                    for key, val in globals().items():
                        if key == "code": val = "<code is too long to display>"
                        print(f"{green_bright}{key}{white}: {green}{val}\n")
                continue
        try: exec(cmd_to_be_executed)
        except: print(clr("\n" + err(sys.exc_info()), 2))
    set_title()

def dank_tool_settings():

    try:
        with open(os.path.join(os.path.expandvars("%LOCALAPPDATA%\\Dankware"), "runs.txt"), 'r', encoding='utf-8') as file:
            runs = file.read()
    except:
        runs = "?"

    while True:

        cls(); print(clr(f"\n  - Settings: [ {_translate('restart for all changes to take effect')} ]\n\n  - dank.tool run counter: {runs}\n\n  - {_translate('do not use')}: offline-src, offline-mode, dev-branch!\n\n  [0] {_translate('Return to menu')}"))

        with open("settings.json", "r", encoding="utf-8") as file:
            settings = json.loads(file.read())

        counter = 1
        for name, value in settings.items():
            print(clr(f"  [{counter}] {name}: {'True' if int(value) else 'False'}"))
            counter += 1
        choice = input(clr("\n  > Choice: ") + red).lower()

        if not isinstance(choice, NoneType) and choice.isdigit() and 0 <= int(choice) <= int(len(settings)):

            choice = int(choice)
            if not choice: break
            settings = list(settings.items())
            setting_key = settings[choice - 1][0]
            settings[choice - 1] = (setting_key, str(int(not int(settings[choice - 1][1]))))
            settings = dict(settings)

            if int(settings[setting_key]):
                match setting_key:
                    case "force-startup-audio" | "disable-startup-audio" | "force-translate" | "disable-translate":
                        if "force" in setting_key:
                            settings[setting_key.replace('force', 'disable')] = "0"
                        elif "disable" in setting_key:
                            settings[setting_key.replace('disable', 'force')] = "0"

            with open("settings.json", "w", encoding="utf-8") as file:
                file.write(json.dumps(settings, indent=4))

        elif choice.lower() == "exit":
            break

def dank_win_activate():

    banner = "\n\n                                                          __    _______ _______ _______ \n.--------.---.-.-----.-----.-----.----.---.-.--.--.-----.|  |  |   |   |   _   |     __|\n|        |  _  |__ --|__ --|  _  |   _|  _  |  |  |  -__||  |__|       |       |__     |\n|__|__|__|___._|_____|_____|___  |__| |___._|\\___/|_____||__|__|__|_|__|___|___|_______|\n                           |_____|                                                      \n"
    cls(); Console().print(Align.center(banner), style="blink red", highlight=False)
    print(clr(f"\n  - {_translate('Credits to massgravel team!')}"))
    input(clr(f"\n  > {_translate('Hit [ ENTER ] to begin Microsoft-Activation-Script...')} "))
    cls(); print(clr(f"\n  - {_translate('Exit inside the MAS window to return to the menu...')}"))
    os.system('powershell -Command "irm https://get.activated.win | iex"')

def dank_os_repair():

    cls(); input(clr(f"\n  [ DISCLAIMER ]\n\n  - {_translate('Do not use this module if you do not know what you are doing')}!\n  - {_translate('Close all other applications before continuing')}!\n  - {_translate('This tool is not responsible for any damage to your system')}!\n  - {_translate('This tool is not responsible for any data loss')}!\n\n  > Press [ENTER] to continue... "))
    cls(); print(clr("""
  [ COMMANDS ]

  - [0] Return to menu

  - [1] """) + clr('DISM /online /cleanup-image /restorehealth',2) + clr(f""" : {_translate('This command uses the Deployment Image Servicing and Management (DISM) tool to scan the health of your Windows image and, if necessary, restore it. The /online option targets the running operating system, /cleanup-image specifies that you are servicing an image, and /restorehealth checks for component store corruption and performs repair operations automatically')}.
  
  - [2] """) + clr('sfc /scannow',2) + clr(f""" : {_translate('This command initiates the System File Checker (SFC) tool to scan all protected system files and replace incorrect versions with correct Microsoft versions. The /scannow option scans all protected system files immediately')}.
  
  - [3] """) + clr('chkdsk C: /x /r',2) + clr(f""" : {_translate('This command uses the Check Disk (chkdsk) utility to check the file system and file system metadata of a volume for logical and physical errors. C: specifies the drive you want to check, /x forces the volume to dismount before it is checked (necessary for fixing certain errors), and /r locates bad sectors and recovers readable information')}.

  - [4] Run all commands
"""))

    while True:
        choice = input(clr("  > Choice: ") + red).lower()
        if choice.isdigit() and 0 <= int(choice) <= 4:
            if choice == '0': break
            cls()
            if choice in ('1', '4'):
                print(clr("\n\n  [ DISM /online /cleanup-image /restorehealth ]"))
                os.system("DISM /online /cleanup-image /restorehealth")
            if choice in ('2', '4'):
                print(clr("\n\n  [ sfc /scannow ]"))
                os.system("sfc /scannow")
            if choice in ('3', '4'):
                print(clr("\n\n  [ chkdsk C: /x /r ]"))
                os.system("chkdsk C: /x /r")
            input(clr("\n  > Press [ENTER] to return to the menu... "))
            break
        rm_line()

def dank_network_reset():

    cls(); input(clr(f"\n  [ DISCLAIMER ]\n\n  - {_translate('Do not use this module if you do not know what you are doing')}!\n  - {_translate('Close all other applications before continuing')}!\n  - {_translate('This tool is not responsible for any damage to your system')}!\n  - {_translate('This tool is not responsible for any data loss')}!\n\n  > Press [ENTER] to continue... "))
    cls(); print(clr("""
  [ COMMANDS ]

  - [0] Return to menu

  - [1] """) + clr('ipconfig /flushdns',2) + clr(f""" : {_translate('This command purges the DNS Resolver cache. The DNS Resolver cache stores the IP addresses for websites that your computer has recently accessed, which can speed up subsequent accesses to the same websites. Flushing this cache can help resolve any outdated or incorrect DNS information')}.

  - [2] """) + clr('ipconfig /registerdns',2) + clr(f""" : {_translate('This command refreshes all DHCP leases and re-registers DNS names. This is useful if you have changed your DNS server or refreshed your IP address and want to update the DNS records')}.

  - [3] """) + clr('ipconfig /release',2) + clr(f""" : {_translate('This command releases the IP address for the specified adapter. This is typically used when you are having issues with your current IP address and want to acquire a new one from your DHCP server')}.

  - [4] """) + clr('ipconfig /renew',2) + clr(f""" : {_translate('This command renews the IP address for the specified adapter. You would typically use this after releasing an IP address to get a new one')}.

  - [5] """) + clr('netsh winsock reset',2) + clr(f""" : {_translate('This command resets the Winsock Catalog to a clean state. All Winsock Layered Service Providers (LSPs) are removed from the Winsock catalog. Any LSPs that are installed will need to be re-installed. This is useful if you are experiencing networking issues due to corrupt LSPs or Winsock settings')}.

  - [6] Run all commands
"""))

    while True:
        choice = input(clr("  > Choice: ") + red).lower()
        if choice.isdigit() and 0 <= int(choice) <= 6:
            if choice == '0': break
            cls()
            if choice in ('1', '6'):
                print(clr("\n\n  [ ipconfig /flushdns ]"))
                os.system("ipconfig /flushdns")
            if choice in ('2', '6'):
                print(clr("\n\n  [ ipconfig /registerdns ]"))
                os.system("ipconfig /registerdns")
            if choice in ('3', '6'):
                print(clr("\n\n  [ ipconfig /release ]"))
                os.system("ipconfig /release")
            if choice in ('4', '6'):
                print(clr("\n\n  [ ipconfig /renew ]"))
                os.system("ipconfig /renew")
            if choice in ('5', '6'):
                print(clr("\n\n  [ netsh winsock reset ]"))
                os.system("netsh winsock reset")
            input(clr("\n  > Press [ENTER] to return to the menu... "))
            break
        rm_line()

def dank_clear_icons():

    #cls(); input(clr(f"\n  [ DISCLAIMER ]\n\n  - {translate('Do not use this module if you do not know what you are doing')}!\n  - {translate('Close all other applications before continuing')}!\n  - {translate('This tool is not responsible for any damage to your system')}!\n  - {translate('This tool is not responsible for any data loss')}!\n\n  > Press [ENTER] to continue... "))
    cls(); print(clr("""
  [ COMMANDS ]
  
  - [0] Return to menu
  
  - [1] """) + clr('Clear Icon Cache',2) + clr(f""" : {_translate('This task clears the icon cache for the current user. This is useful if you are experiencing issues with icons not displaying correctly')}.
  
  - [2] """) + clr('Clear Thumbnail Cache',2) + clr(f""" : {_translate('This task clears the thumbnail cache for the current user. This is useful if you are experiencing issues with thumbnails not displaying correctly')}.
  
  - [3] Run all tasks
"""))

    while True:

        choice = input(clr("  > Choice: ") + red).lower()
        if choice.isdigit() and 0 <= int(choice) <= 3:

            if choice == '0': break

            cls()
            print(clr(f"\n  [ {_translate('Terminating Explorer.exe')} ]"))
            os.system("taskkill /f /im explorer.exe >nul 2>&1")
            os.chdir(os.path.expandvars("%userprofile%\\AppData\\Local\\Microsoft\\Windows\\Explorer"))

            if choice in ('1', '3'):
                print(clr(f"\n  [ {_translate('Clearing Icon Cache')} ]\n"))
                os.system(r"attrib -h iconcache*")
                for file in os.listdir():
                    if file.startswith("iconcache") and file.endswith(".db"):
                        try:
                            os.remove(file)
                            print(clr(f"  - {_translate('deleted')} {file}"))
                        except:
                            print(clr(f"  - {_translate('failed to delete')} {file}",2))

            if choice in ('2', '3'):
                print(clr(f"\n  [ {_translate('Clearing Thumbnail Cache')} ]\n"))
                os.system(r"attrib -h thumbcache*")
                for file in os.listdir():
                    if file.startswith("thumbcache") and file.endswith(".db"):
                        try:
                            os.remove(file)
                            print(clr(f"  - {_translate('deleted')} {file}"))
                        except:
                            print(clr(f"  - {_translate('failed to delete')} {file}",2))

            os.chdir(os.path.dirname(__file__))
            print(clr(f"\n  [ {_translate('Starting Explorer.exe')} ]"))
            os.system("start explorer.exe")
            input(clr(f"\n  > {_translate('Press [ENTER] to return to the menu...')} "))
            break

        rm_line()

def dank_github_software(software):

    # dir

    path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    if os.path.isdir(path):
        os.chdir(path)
    else:
        os.chdir(get_path('Temp'))

    session = requests.Session()
    match software:
        case 'netlimiter':
            banner = "\n\n     __     _     __ _           _ _                   ___           \n  /\\ \\ \\___| |_  / /(_)_ __ ___ (_) |_ ___ _ __       / _ \\_ __ ___  \n /  \\/ / _ \\ __|/ / | | '_ ` _ \\| | __/ _ \\ '__|____ / /_)/ '__/ _ \\ \n/ /\\  /  __/ |_/ /__| | | | | | | | ||  __/ | |_____/ ___/| | | (_) |\n\\_\\ \\/ \\___|\\__\\____/_|_| |_| |_|_|\\__\\___|_|       \\/    |_|  \\___/ \n\n\n"
        case 'vencord':
            banner = "\n\n                                                                         \n                                                                     _|  \n _|      _|    _|_|    _|_|_|      _|_|_|    _|_|    _|  _|_|    _|_|_|  \n _|      _|  _|_|_|_|  _|    _|  _|        _|    _|  _|_|      _|    _|  \n   _|  _|    _|        _|    _|  _|        _|    _|  _|        _|    _|  \n     _|        _|_|_|  _|    _|    _|_|_|    _|_|    _|          _|_|_|  \n\n\n"
    cls(); Console().print(Align.center(banner), style="blink red", highlight=False)

    # main

    match software:
        case 'netlimiter':
            print(clr(f"\n  - {_translate('Credits to')} Baseult!"))
            if os.path.isfile(r"C:\Program Files\Locktime Software\NetLimiter\NetLimiter.dll"):
                print(clr(f"\n  - {_translate('NetLimiter found!')}"))
            else:
                print(clr(f"\n  - {_translate('NetLimiter not found!')}\n\n  - {_translate('Downloading NetLimiter...')}"))
                url = 'https://download.netlimiter.com' + session.get("https://www.netlimiter.com/download").content.decode().split('https://download.netlimiter.com',1)[1].split('"',1)[0]
                data = session.get(url, headers=headers).content
                with open('netlimiter.exe', 'wb') as file:
                    file.write(data)
                os.system('netlimiter.exe')
                input(clr(f"\n  > {_translate('Press [ ENTER ] after installing NetLimiter...')} "))
            sha = session.get("https://api.github.com/repos/Baseult/NetLimiterCrack/commits?path=NetLimiter%20Crack.exe&page=1&per_page=1", headers=headers).json()[0]['sha']
        case 'vencord':
            print(clr(f"\n  - {_translate('Credits to')} Vendicated!"))
            if os.path.isfile(f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Discord\\Update.exe"):
                print(clr(f"\n  - {_translate('Discord found!')}"))
            else:
                print(clr(f"\n  - {_translate('Discord not found!')}\n\n  - {_translate('Downloading Discord...')}\n"))
                os.system("winget install --accept-source-agreements --interactive --id Discord.Discord")
                input(clr(f"\n  > {_translate('Press [ ENTER ] after installing Discord...')} "))
            asset = [_ for _ in session.get("https://api.github.com/repos/Vencord/Installer/releases/latest").json()["assets"] if _["browser_download_url"].endswith("VencordInstaller.exe")][0]
            browser_download_url = asset["browser_download_url"]
            version = browser_download_url.split('/')[-2]

    def get_patcher():
        match software:
            case 'netlimiter':
                data = session.get("https://github.com/Baseult/NetLimiterCrack/raw/main/NetLimiter%20Crack.exe", headers=headers).content
                print(clr(f"\n  - {_translate('NetLimiter-Patcher downloaded successfully!')}"))
                while True:
                    try:
                        with open('netlimiter-patcher.exe', 'wb') as file:
                            file.write(data)
                        print(clr(f"\n  - {_translate('NetLimiter-Patcher saved successfully!')}"))
                        break
                    except Exception as exc:
                        input(clr(f"\n  > {_translate('Failed to save NetLimiter-Patcher!')} {exc} | {_translate('Press [ ENTER ] to try again...')} ",2))
                        rm_line(); rm_line()
            case 'vencord':
                data = session.get(browser_download_url, headers=headers).content
                print(clr(f"\n  - {_translate('Vencord downloaded successfully!')}"))
                while True:
                    try:
                        with open('vencord.exe', 'wb') as file:
                            file.write(data)
                        print(clr(f"\n  - {_translate('Vencord saved successfully!')}"))
                        break
                    except Exception as exc:
                        input(clr(f"\n  > {_translate('Failed to save Vencord!')} {exc} | {_translate('Press [ ENTER ] to try again...')} ",2))
                        rm_line(); rm_line()

    match software:
        case 'netlimiter':
            if os.path.isfile('netlimiter-patcher.exe'):
                with open('netlimiter-patcher-sha.txt', 'r', encoding='utf-8') as file:
                    _sha = file.read()
                if _sha == sha:
                    print(clr(f"\n  - {_translate('NetLimiter-Patcher is up-to-date!')}"))
                else:
                    print(clr(f"\n  - {_translate('Updating NetLimiter-Patcher...')}"))
                    get_patcher()
                    with open('netlimiter-patcher-sha.txt', 'w', encoding='utf-8') as file:
                        file.write(sha)
            else:
                print(clr(f"\n  - {_translate('Downloading NetLimiter-Patcher...')}"))
                get_patcher()
                with open('netlimiter-patcher-sha.txt', 'w', encoding='utf-8') as file:
                    file.write(sha)
        case 'vencord':
            if os.path.isfile('vencord.exe'):
                with open('vencord-version.txt', 'r', encoding='utf-8') as file:
                    _version = file.read()
                if _version == version:
                    print(clr(f"\n  - {_translate('Vencord is up-to-date!')}"))
                else:
                    print(clr(f"\n  - {_translate('Updating Vencord...')}"))
                    get_patcher()
                    with open('vencord-version.txt', 'w', encoding='utf-8') as file:
                        file.write(version)
            else:
                print(clr(f"\n  - {_translate('Downloading Vencord...')}"))
                get_patcher()
                with open('vencord-version.txt', 'w', encoding='utf-8') as file:
                    file.write(version)

    print(clr(f"\n  - {_translate('You may need to exclude the patcher from your antivirus for it to work!')}"))
    match software:
        case 'netlimiter':
            input(clr(f"\n  > {_translate('Hit [ ENTER ] to start NetLimiter-Patcher...')} "))
        case 'vencord':
            input(clr(f"\n  > {_translate('Hit [ ENTER ] to start Vencord...')} "))
    cls()
    if software == 'vencord':
        print(clr(f"\n  - {_translate('Click Install')}"))
        print(clr(f"\n  - {_translate('Click Install OpenAsar')}"))
    print(clr(f"\n  - {_translate('Close the patcher to return to the menu...')}"))
    match software:
        case 'netlimiter':
            os.system('netlimiter-patcher.exe')
        case 'vencord':
            os.system('vencord.exe')

def dank_winrar_patcher():

    cls()
    path = os.path.expandvars("%appdata%\\WinRAR")

    def patch():
        with open("__assets__/dank.winrar/rarreg_1.key", 'r', encoding='utf-8') as file:
            key1 = file.read()
        with open("__assets__/dank.winrar/rarreg_2.key", 'r', encoding='utf-8') as file:
            key2 = file.read()
        try: os.chdir(path)
        except FileNotFoundError:
            os.makedirs(path)
            os.chdir(path)
        if os.path.isfile("rarreg.key"):
            try:
                with open("rarreg.key", 'r', encoding='utf-8') as file:
                    existing_data = file.read()
            except UnicodeDecodeError:
                print(clr(f"\n  - {_translate('Failed to read rarreg.key!')}",2))
                existing_data = None
            if existing_data in (key1, key2):
                print(clr(f"\n  - {_translate('WinRAR already patched!')}"))
            else:
                print(clr(f"\n  - {_translate('WinRAR already activated? (found rarreg.key)')}"))
                if input(clr(f"\n  > {_translate('Would you like to patch WinRAR anyway?')} [y/n]: ") + red).lower() == 'y':
                    if os.path.isfile("rarreg.key.bak"):
                        os.remove("rarreg.key.bak")
                    os.rename("rarreg.key", "rarreg.key.bak")
                    with open("rarreg.key", 'w', encoding='utf-8') as file:
                        file.write(key1)
                    print(clr(f"\n  - {_translate('WinRAR patched!')}"))
        else:
            with open("rarreg.key", 'w', encoding='utf-8') as file:
                file.write(key1)
            print(clr(f"\n  - {_translate('WinRAR patched!')}"))
        os.chdir(os.path.dirname(__file__))

    if os.path.isdir(path):
        patch()
    else:
        print(clr(f"\n  - {_translate('WinRAR not installed!')}"))
        if ONLINE_MODE:
            print(clr(f"\n  - {_translate('Downloading WinRAR...')}\n"))
            os.system("winget install --accept-source-agreements --interactive --id RARLab.WinRAR")
            input(clr(f"\n  > {_translate('Press [ENTER] after installing WinRAR to start patching...')} "))
            patch()
    input(clr(f"\n  > {_translate('Press [ENTER] to return to the menu...')} "))

def dank_revo_patcher():

    cls()
    path = os.path.expandvars("%ProgramData%\\VS Revo Group\\Revo Uninstaller Pro")

    def patch():
        with open("__assets__/dank.revo-uninstaller/revouninstallerpro5.lic", 'rb') as file:
            key = file.read()
        try: os.chdir(path)
        except FileNotFoundError:
            os.makedirs(path)
            os.chdir(path)
        if os.path.isfile("revouninstallerpro5.lic"):
            try:
                with open("revouninstallerpro5.lic", 'rb') as file:
                    existing_data = file.read()
            except UnicodeDecodeError:
                print(clr(f"\n  - {_translate('Failed to read revouninstallerpro5.lic!')}",2))
                existing_data = None
            if existing_data == key:
                print(clr(f"\n  - {_translate('RevoUninstallerPro already patched!')}"))
            else:
                print(clr(f"\n  - {_translate('RevoUninstaller installed? (found revouninstallerpro5.lic)')}"))
                if input(clr(f"\n  > {_translate('Would you like to patch RevoUninstallerPro?')} [y/n]: ") + red).lower() == 'y':
                    if os.path.isfile("revouninstallerpro5.lic.bak"):
                        os.remove("revouninstallerpro5.lic.bak")
                    os.rename("revouninstallerpro5.lic", "revouninstallerpro5.lic.bak")
                    with open("revouninstallerpro5.lic", 'wb') as file:
                        file.write(key)
                    print(clr(f"\n  - {_translate('RevoUninstallerPro patched!')}"))
        else:
            with open("revouninstallerpro5.lic", 'wb') as file:
                file.write(key)
            print(clr(f"\n  - {_translate('RevoUninstallerPro patched!')}"))
        os.chdir(os.path.dirname(__file__))

    if os.path.isdir(path):
        patch()
    else:
        print(clr(f"\n  - {_translate('RevoUninstallerPro not installed!')}"))
        if ONLINE_MODE:
            print(clr(f"\n  - {_translate('Downloading RevoUninstallerPro...')}\n"))
            os.system("winget install --accept-source-agreements --interactive --id RevoUninstaller.RevoUninstallerPro")
            input(clr(f"\n  > {_translate('Press [ENTER] after installing RevoUninstallerPro to start patching...')} "))
            patch()
    input(clr(f"\n  > {_translate('Press [ENTER] to return to the menu...')} "))

if __name__ == "__main__":

    os.chdir(os.path.dirname(__file__))
    set_globals_one()
    _translator = Translator()
    palestine_banner() # 🍉

    # multithreaded requests responses, download modules / assets

    if ONLINE_MODE:

        print(clr(f"\n  - {_translate('Downloading modules...')}"))

        if not os.path.isdir("__modules__"): os.mkdir("__modules__")

        while True:
            try: multithread(download_offline_modules, 50, offline_scripts, progress_bar=False); break
            except:
                input(clr(f"\n  > {_translate('Failed to download modules! Make sure you are connected to the internet! Press [ENTER] to try again...')} ",2))
                rm_line(); rm_line()

        # download assets

        if not os.path.isdir("ursina"): os.mkdir("ursina")
        if not os.path.isdir("__assets__"): os.mkdir("__assets__")
        for _ in ("dank.winrar", "dank.revo-uninstaller"):
            if not os.path.isdir(f"__assets__/{_}"): os.mkdir(f"__assets__/{_}")
        if not os.path.isfile("ursina/assets.json"):
            with open("ursina/assets.json", "w", encoding="utf-8") as _:
                _.write("{}")
        with open("ursina/assets.json", "r", encoding="utf-8") as _:
            local_assets_json = json.loads(_.read())

        while True:
            try: latest_assets_json = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__assets__/dank.game/assets.json", headers=headers, timeout=3).json(); break
            except Exception as exc:
                input(clr(f"\n  > {_translate(f'Failed to fetch assets.json! {exc} | Press [ENTER] to try again...')} ",2))
                rm_line(); rm_line()

        asset_urls = []
        file_names = []

        for _ in ("dank.winrar/rarreg_1.key", "dank.winrar/rarreg_2.key", "dank.revo-uninstaller/revouninstallerpro5.lic"):
            if not os.path.isfile(f"__assets__/{_}"):
                asset_urls.append(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__assets__/{_}")
                file_names.append(f"__assets__/{_}")

        for folder in latest_assets_json:
            if not os.path.isdir(f"ursina/{folder}"):
                os.makedirs(f"ursina/{folder}")
            if folder not in local_assets_json:
                local_assets_json[folder] = {}
            for asset in latest_assets_json[folder]:
                if asset not in local_assets_json[folder] or local_assets_json[folder][asset] < latest_assets_json[folder][asset]:
                    asset_urls.append(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__assets__/dank.game/{folder}/{asset}")
                    file_names.append(f"ursina/{folder}/{asset}")

        if asset_urls:

            print(clr(f"\n  - {_translate('Downloading assets...')}\n"))

            while True:
                try:
                    multithread(download_assets, 50, asset_urls, file_names, progress_bar=not COMPATIBILITY_MODE)
                    break
                except:
                    input(clr(f"\n  > {_translate('Failed to download assets! Make sure you are connected to the internet! Press [ENTER] to try again...')} ",2))
                    rm_line(); rm_line()

            with open("ursina/assets.json", "w", encoding="utf-8") as _:
                _.write(json.dumps(latest_assets_json, indent=4))

        del local_assets_json, latest_assets_json, asset_urls, file_names

        # multithreaded request responses

        print(clr(f"\n  - {_translate('Getting request responses...')}\n"))

        global menu_request_responses
        menu_request_responses = {}

        # KEEP request_keys IN ORDER!

        request_keys = (
            "dankware_runs",
            "danktool_runs",
            "motm",
            "chatroom_user_count"
        )

        request_keys_api = (
            "SpotX",
            "Spicetify",
            "Microsoft-Activation-Scripts",
            "NetLimiter",
            "Vencord",
            "dank.minecraft-server-builder",
            "dank.minecraft-server-scanner",
            #"dank.auto-clicker",
            "dank.browser-backup",
            "dank.game",
            "dank.winget"
        )

        while True:
            try:
                multithread(get_menu_request_responses, 50, tuple(_ for _ in range(len(request_keys))), request_keys, progress_bar=not COMPATIBILITY_MODE)
                break
            except:
                input(clr(f"\n  > {_translate('Failed to get request responses! Make sure you are connected to the internet! Press [ENTER] to try again...')} ",2))
                rm_line(); rm_line()

        for _ in ("dankware_runs", "danktool_runs"): # don't add motm
            if '⚠️' not in menu_request_responses[_]:
                menu_request_responses[_] = green_bright + menu_request_responses[_]

        # hourly limit on github api

        github_api = False
        if not os.path.isfile("github_api.json"):
            with open("github_api.json", "w", encoding="utf-8") as _:
                _.write("{}")
            github_api = True

        with open("github_api.json", "r", encoding="utf-8") as _:
            github_api_json = json.loads(_.read())
        if "updated_on" not in github_api_json or github_api_json["updated_on"] < (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%d-%m-%Y %H:%M"):
            github_api = True

        for key in request_keys_api:
            if key not in github_api_json:
                github_api = True
                break

        if github_api:

            while True:
                try:
                    multithread(get_menu_request_responses_api, 50, tuple(_ for _ in range(len(request_keys_api))), request_keys_api, progress_bar=not COMPATIBILITY_MODE)
                    break
                except:
                    input(clr(f"\n  > {_translate('Failed to get github api request responses! Make sure you are connected to the internet! Press [ENTER] to try again...')} ",2))
                    rm_line(); rm_line()

            github_api_json["updated_on"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

            for key in request_keys_api:
                github_api_json[key] = menu_request_responses[key]

            with open("github_api.json", "w", encoding="utf-8") as _:
                _.write(json.dumps(github_api_json, indent=4))

        else:

            for key in request_keys_api:
                menu_request_responses[key] = github_api_json[key]

        del request_keys, request_keys_api, github_api

    else:

        del dank_win_activate, dank_github_software

    del updated_on, download_assets, download_offline_modules, get_menu_request_responses

    # main

    ThreadPoolExecutor().submit(notify, '[ SirDank ]',
        _translate('Thank you for using my tool ❤️\nShare it with your friends!'),
        icon = {'src': f'{os.path.dirname(__file__)}\\dankware.ico', 'placement': 'appLogoOverride'} if os.path.exists(f'{os.path.dirname(__file__)}\\dankware.ico') else None,
        image = f'{os.path.dirname(__file__)}\\red.png' if os.path.exists('red.png') else None
    )

    while True:

        # reset

        set_title()
        os.environ['DISCORD_RPC'] = "on the main menu"
        os.chdir(os.path.dirname(__file__))

        set_globals_one()
        set_globals_two()

        # print available modules

        modules = (offline_modules if not ONLINE_MODE else online_modules)
        local_modules = {}

        if not os.path.isdir('__local_modules__'):
            os.mkdir('__local_modules__')

        for module in os.listdir("__local_modules__"):
            if os.path.isfile(f"__local_modules__/{module}") and module.endswith(".py"):
                name = module.replace('.py','')
                local_modules[name] = {
                    'title': name,
                    'project': name,
                    'rpc': f'running "{module}"'}

        print_modules()

        while True: # user input

            _choice = input(clr("  > Choice: ") + red)

            if isinstance(_choice, NoneType):

                os.system("taskkill /f /t /im dank.tool.exe")

            elif _choice.isdigit() and 1 <= int(_choice) <= int(len(modules) + len(local_modules)):

                if int(_choice) <= len(modules):
                    _choice = modules[list(modules)[int(_choice) - 1]]
                    LOCAL_MODULE = False
                else:
                    _choice = local_modules[list(local_modules)[int(_choice) - len(modules) - 1]]
                    LOCAL_MODULE = True

                if not LOCAL_MODULE and _choice['category']:

                    print_category_modules(_choice)

                    while True:
                        __choice = input(clr("  > Choice: ") + red)
                        if __choice == '0':
                            print_modules()
                            break
                        if __choice.isdigit() and 1 <= int(__choice) <= (len(_choice) - 1):
                            _choice = _choice[list(_choice)[int(__choice) - 1]]
                            break
                        rm_line()

                    if 'category' not in _choice:
                        break

                else:
                    break

            else:

                match _choice.lower().strip():
                    case 'refresh': # re-align ui
                        print_modules()
                    case 'debug': # debug menu
                        debug_mode()
                    case 'exit' | 'stop':
                        os.system("taskkill /f /t /im dank.tool.exe")
                    case _:
                        rm_line()

        try:

            # built-in modules

            match _choice['project']:
                case "Discord Server":
                    os.system('start https://dankware.onrender.com/discord')
                    continue
                case "Telegram Group":
                    os.system('start https://t.me/+18tWHJ_g2g4yZWI1')
                    continue
                case "YouTube":
                    os.system('start https://dankware.onrender.com/youtube')
                    continue
                case "Website":
                    os.system('start https://dankware.onrender.com/')
                    continue

            TITLE = _choice['title']
            PROJECT = _choice['project']
            os.environ['DISCORD_RPC'] = _choice['rpc']

            # built-in modules

            match PROJECT:
                case "dank.tool settings":
                    dank_tool_settings()
                    continue
                case "dank.win-activate":
                    dank_win_activate()
                    continue
                case "dank.os-repair":
                    dank_os_repair()
                    continue
                case "dank.network-reset":
                    dank_network_reset()
                    continue
                case "dank.clear-icons":
                    dank_clear_icons()
                    continue
                case "dank.vencord":
                    dank_github_software("vencord")
                    continue
                case "dank.netlimiter":
                    dank_github_software("netlimiter")
                    continue
                case "dank.winrar":
                    dank_winrar_patcher()
                    continue
                case "dank.revo-uninstaller":
                    dank_revo_patcher()
                    continue

            if LOCAL_MODULE: # get src from local_module

                while True:
                    try:
                        with open(f'__local_modules__/{PROJECT}.py', 'r', encoding='utf-8') as _:
                            code = _.read(); break
                    except:
                        translation = _translate(f"Failed to get code! Unable to read '__local_modules__/{PROJECT}.py'! Press [ENTER] to try again")
                        input(clr(f"\n  > {translation}... ",2)); del translation
                        rm_line(); rm_line()

            else: # get src from github if not debug mode else get src locally

                if not OFFLINE_SRC and ( ONLINE_MODE or not os.path.exists(f'__modules__/{PROJECT}.py') ): # OFFLINE_SRC / ONLINE_MODE defined in executor.py

                    # [NOTE] check for update before getting src ( enable this for a short while before release )

                    #while True:
                    #    try:
                    #        LATEST_VERSION = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/executor_version.txt", headers=headers, timeout=3).content.decode()
                    #        if parse(LATEST_VERSION) > parse(DANK_TOOL_VERSION):
                    #            cls(); print(clr(f"\n  - Update Found: {LATEST_VERSION}"))
                    #            dank_tool_installer()
                    #        else:
                    #            break
                    #    except Exception as exc:
                    #        input(clr(f"\n  > {_translate(f'Failed to get latest version! {exc} | Press [ENTER] to try again...')} ",2))
                    #        rm_line(); rm_line()

                    while True:
                        try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__modules__/{PROJECT}.py", headers=headers, timeout=3).content.decode(); break
                        except Exception as exc:
                            input(clr(f"\n  > {_translate(f'Failed to get code for {PROJECT}! {exc} | Press [ENTER] to try again...')} ",2))
                            rm_line(); rm_line()

                else:
                    while True:
                        try:
                            with open(f'__modules__/{PROJECT}.py', 'r', encoding='utf-8') as _:
                                code = _.read(); break
                        except:
                            translation = _translate(f"Failed to get code! Unable to read '__modules__/{PROJECT}.py'! Press [ENTER] to try again")
                            input(clr(f"\n  > {translation}... ",2)); del translation
                            rm_line(); rm_line()

            # execute src

            if code == "404: Not Found":
                if PROJECT.startswith('_'):
                    print(clr(f"\n  - {_translate(f'{PROJECT[1:]} has been disabled! Returning to menu in 5 seconds...')}",2))
                else:
                    print(clr(f"\n  - {_translate(f'{PROJECT} has not been released yet! Returning to menu in 5 seconds...')}",2))
                time.sleep(5)
            else:
                cls(); exec(code)
                cls(); print(clr(f"\n  - {_translate(f'{PROJECT} executed successfully! Returning to menu in 3 seconds...')}"))
                time.sleep(3)

        except:

            err_message = err(sys.exc_info(), 'mini')
            print(clr(err_message, 2))

            if "- SystemExit" in err_message:
                os.system("taskkill /f /t /im dank.tool.exe")
            elif "- EOFError" in err_message:
                print_warning_symbol()
                print(clr(f"\n  - {_translate('No input provided!')}"))
            elif "- KeyboardInterrupt" in err_message:
                print_warning_symbol()
                print(clr(f"\n  - {_translate('Please select text first and then use [ CTRL + C ]!')}"))

            elif ONLINE_MODE: # and not LOCAL_MODULE (removed to report all errors)
                while True:
                    try:
                        requests.post("https://dankware.onrender.com/dank-tool-errors", headers=headers, timeout=3, data={"text": f"```<--- 🚨 ---> {TITLE}\n\n{err_message}```"}) # pylint: disable=used-before-assignment
                        break
                    except Exception as exc:
                        input(clr(f"\n  > {_translate(f'Failed to post error report! {exc} | Press [ENTER] to try again...')} ",2))
                        rm_line(); rm_line()
                print(clr(f"\n  > {_translate('Error Reported! If it is a logic error, it will be fixed soon!')}"))

            input(clr("\n  > Press [ENTER] to return to the menu... "))
