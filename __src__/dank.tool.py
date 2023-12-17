###################################################################################

#                            https://github.com/SirDank                            

###################################################################################

import os
import sys
import json
import time
import requests
from rich.panel import Panel
from win11toast import notify
from datetime import datetime
from rich.columns import Columns
from rich.console import Console
from translatepy import Translator
from packaging.version import parse
from dateutil.tz import tzlocal, tzutc
from concurrent.futures import ThreadPoolExecutor
from dankware import white, white_normal, green, red, red_normal, red_dim
from dankware import align, cls, clr, title, get_duration, multithread, err, rm_line

os.chdir(os.path.dirname(__file__))

# dank.tool updater

def dank_tool_installer():

    while True:
        try:
            code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/updater.py", headers=headers).content.decode()
            break
        except: input(clr("\n  > Failed to get code! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
    
    try: exec(code)
    except:
        err_message = err(sys.exc_info())
        try: requests.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": f"```<--- 🚨🚨🚨 ---> Version: {DANK_TOOL_VERSION}\n\n{err_message}```"})
        except: pass
        input(clr(f"{err_message}\n\n  > Press [ENTER] to EXIT... ",2))
        sys.exit(err_message)
    
    sys.exit("Updated!")

# print randomly coloured and aligned banner

def dank_tool_banner():
    
    banner = '\n   ..                                       ..                  s                                  .. \n dF                                   < .z@8"`                 :8                            x .d88"  \n\'88bu.                     u.    u.    !@88E                  .88           u.          u.    5888R   \n\'*88888bu         u      x@88k u@88c.  \'888E   u             :888ooo  ...ue888b   ...ue888b   \'888R   \n  ^"*8888N     us888u.  ^"8888""8888"   888E u@8NL         -*8888888  888R  888r  888R  888r   888R   \n beWE "888L .@88 "8888"   8888  888R    888E`"88*"           8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E .dN.            8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E~8888            8888     888R  888>  888R  888>   888R   \n 888E  888F 9888  9888    8888  888R    888E \'888&     .    .8888Lu= u8888cJ888  u8888cJ888    888R   \n.888N..888  9888  9888   "*88*" 8888"   888E  9888.  .@8c   ^%888*    "*888*P"    "*888*P"    .888B . \n `"888*""   "888*""888"    ""   \'Y"   \'"888*" 4888" \'%888"    \'Y"       \'Y"         \'Y"       ^*888%  \n    ""       ^Y"   ^Y\'                   ""    ""     ^*                                        "%    \n'    
    cls(); print(align(clr(banner,4,colours=[white, white_normal, red, red, red, red, red_normal, red_dim]) + f"\n{white}s i r {red}. {white}d a n k {red}💕"))

# handle KeyboardInterrupt

def print_warning_symbol():
    
    warning_symbol = f'\n\n{red}                      ██                      \n{red}                    ██  ██                    \n{red}                  ██      ██                  \n{red}                ██          ██                \n{red}                ██          ██                \n{red}              ██              ██              \n{red}            ██      {white}██████{red}      ██            \n{red}            ██      {white}██████{red}      ██            \n{red}          ██        {white}██████{red}        ██          \n{red}          ██        {white}██████{red}        ██          \n{red}        ██          {white}██████{red}          ██        \n{red}      ██            {white}██████{red}            ██      \n{red}      ██            {white}██████{red}            ██      \n{red}    ██              {white}██████{red}              ██    \n{red}    ██                                  ██    \n{red}  ██                {white}██████{red}                ██  \n{red}  ██                {white}██████{red}                ██  \n{red}██                  {white}██████{red}                  ██\n{red}██                                          ██\n{red}  ██████████████████████████████████████████  \n'
    cls(); print(align(warning_symbol))

# get commit date & time

def updated_on(url, dankware_module = True):

    if dankware_module: url = f"https://api.github.com/repos/SirDank/dank.tool/commits?path=__modules__/{url}.py&page=1&per_page=1" + ('' if not DEV_BRANCH else '&sha=dev')
    try:

        response = requests.get(url, headers=headers, timeout=3).json()
        if response == []: return f"[ unreleased ]"
        else:
            date, time = response[0]["commit"]["author"]["date"].split("T")
            date = date.split("-")
            time = time.replace("Z","").split(":")
            date_time_data = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]), tzinfo=tzutc())
        
        return f"[bright_green]{get_duration(date_time_data, datetime.now(tzlocal()), interval='dynamic-mini')}" # 🔄

    except: return "" # [bright_red]⚠️

# multithread requests

def get_menu_request_responses(task_id, request_key):
    
    # get global runs
    
    if task_id in (0, 1):
        if task_id == 0: url = "https://dank-site.onrender.com/counter?id=dankware&hit=false"
        elif task_id == 1: url = "https://dank-site.onrender.com/counter?id=dank.tool&hit=false"
        try: menu_request_responses[request_key] = requests.get(url, headers=headers, timeout=3).content.decode().replace('<pre>','').replace('</pre>','')
        except: menu_request_responses[request_key] = f"{red}⚠️"
    
    # get motd
    
    elif task_id == 2:
        try:
            motd = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/motd.txt", headers=headers, timeout=3).content.decode()
            motd = clr(motd, colour_one=green)
        except:
            motd = f"{red}⚠️"
        menu_request_responses[request_key] = motd

    # get chatroom user count

    elif task_id == 3:
        try:
            tmp = requests.get("https://dank-site.onrender.com/chatroom-users", headers=headers, timeout=3).content.decode()
            if tmp.isdigit() and tmp != "0": menu_request_responses[request_key] = tmp
            else: menu_request_responses[request_key] = "1"
            del tmp
            menu_request_responses[request_key] = f"[bright_green]{menu_request_responses[request_key]} online{' (you)' if menu_request_responses[request_key] == '1' else ''}"
        except: menu_request_responses[request_key] = "" # [bright_red]⚠️
        
    # get last update time for modules based on external repos
    
    elif task_id in (4, 5, 6):
        if task_id == 4: url = "https://api.github.com/repos/SpotX-Official/SpotX/commits?path=run.ps1&page=1&per_page=1"
        elif task_id == 5: url = "https://api.github.com/repos/spicetify/spicetify-cli/commits?path=.&page=1&per_page=1"
        elif task_id == 6: url = "https://api.github.com/repos/massgravel/Microsoft-Activation-Scripts/commits?path=MAS/All-In-One-Version/MAS_AIO.cmd&page=1&per_page=1"
        menu_request_responses[request_key] = updated_on(url, False)
        
    # get last update time for modules
        
    elif task_id > 6:
        menu_request_responses[request_key] = updated_on(request_key)

# multithreaded module / asset downloader

def download_offline_modules(project):
    
    code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__modules__/{project}.py", headers=headers).content.decode()
    open(f'__modules__/{project}.py', 'w', encoding='utf-8').write(code)

def download_assets(url, file_name):

    data = requests.get(url, headers=headers).content
    open(file_name, 'wb').write(data)

# print modules with index and get choice

def print_modules():
    
    dank_tool_banner(); print(clr(f"\n  - Modules:{stats}") + red + ('' if ONLINE_MODE else ' OFFLINE') + ('' if not OFFLINE_SRC else ' DEBUG') + ('' if not DEV_BRANCH else ' ONLINE DEBUG') + "\n")
    user_renderables = []
    console = Console()
    counter = 1
    
    # online modules
    
    for title, module in modules.items():
        if not module['category']:
            user_renderables.append(f"[b][bright_white]{counter} [bright_red]- [bright_white]{title}[/b] {module['info']}")
        else:
            user_renderables.append(f"[b][bright_white]{counter} [bright_red][ [bright_white]{title}[/b] [bright_red]]")
        counter += 1
        
    # local modules
        
    for title in local_modules.keys():
        user_renderables.append(f"[b][bright_white]{counter} [bright_cyan]- [bright_white]{title}[/b]")
        counter += 1

    console.print(Panel(title=f"[red1]> [bright_white][b]M O D U L E S[/b] [red1]<", title_align="center", renderable=Columns(user_renderables, expand=True), style="bright_red", expand=True))
    print()

def print_category_modules(modules):
    
    dank_tool_banner(); print(clr(f"\n  - Modules:{stats}") + red + ('' if ONLINE_MODE else ' OFFLINE') + ('' if not OFFLINE_SRC else ' DEBUG') + ('' if not DEV_BRANCH else ' ONLINE DEBUG') + "\n")
    user_renderables = []
    console = Console()
    counter = 1
    
    # category modules
    
    user_renderables.append(f"[b][bright_white]0 [bright_red]- [bright_white]Return to menu[/b]")
    for title, module in modules.items():
        if title != "category":
            user_renderables.append(f"[b][bright_white]{counter} [bright_red]- [bright_white]{title}[/b] {module['info']}")
            counter += 1

    console.print(Panel(title=f"[b][red1]> [bright_white]M O D U L E S [red1]- [bright_white]I N [red1]- [bright_white]C A T E G O R Y [red1]<[/b]", title_align="center", renderable=Columns(user_renderables, expand=True), style="bright_red", expand=True))
    print()

# set globals

def set_globals_one():
    
    global ONLINE_MODE, OFFLINE_SRC, DEV_BRANCH, DANK_TOOL_VERSION, DANK_TOOL_LANG, BRANCH, headers

    OFFLINE_SRC = int(os.environ['DANK_TOOL_OFFLINE_SRC'])
    DEV_BRANCH = int(os.environ['DANK_TOOL_DEV_BRANCH'])
    DANK_TOOL_VERSION = os.environ['DANK_TOOL_VERSION']
    ONLINE_MODE = int(os.environ['DANK_TOOL_ONLINE'])
    DANK_TOOL_LANG = os.environ['DANK_TOOL_LANG']
    DANK_TOOL_LANG = ('' if DANK_TOOL_LANG == 'en' else DANK_TOOL_LANG)
    BRANCH = ("main" if not DEV_BRANCH else "dev")
    headers = {"User-Agent": "dank.tool"}
    
    global offline_modules, offline_scripts
    
    offline_modules = {
        
        'Windows OS Tools': {

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
        
        'Browser Backup': {
            'info': '',
            'title': "𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙",
            'project': "dank.browser-backup",
            'rpc': "backing up a browser",
            'category': False,
        },
        
        'Fusion-Fall Modding Tool': {
            'info': '',
            'title': "𝚍𝚊𝚗𝚔.𝚏𝚞𝚜𝚒𝚘𝚗-𝚏𝚊𝚕𝚕",
            'project': "dank.fusion-fall",
            'rpc': "modding fusion-fall",
            'category': False,
        },
        
        'World Exploration Game [bright_red][[red1]BETA[bright_red]]': {
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

        stats = f" [ dankware runs: {green}{menu_request_responses['dankware_runs']} | dank.tool runs: {green}{menu_request_responses['danktool_runs']} | motd: {menu_request_responses['motd']} ]"
        #try: stats = f" [ dankware runs: {green}{menu_request_responses['dankware_runs']} | dank.tool runs: {green}{menu_request_responses['danktool_runs']} | motd: {menu_request_responses['motd']} ]"
        #except Exception as exc:
        #    try: requests.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": f"```<--- 🚨🚨🚨 --->\n\n  - Error: {exc}\n\n  - Data:\n\n{json.dumps(menu_request_responses, indent=2)}```"})
        #    except: pass
        #    stats = " [ ERROR ON STATS ⚠️ ]"
            
        global online_modules
        
        online_modules = {
            
            translate('Minecraft Tools'): {
                
                translate('Minecraft Server Builder'): {
                    'info': menu_request_responses["dank.minecraft-server-builder"],
                    'title': "𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚋𝚞𝚒𝚕𝚍𝚎𝚛",
                    'project': "dank.minecraft-server-builder",
                    'rpc': "building a minecraft server"
                },

                translate('Minecraft Server Scanner'): {
                    'info': menu_request_responses["dank.minecraft-server-scanner"],
                    'title': "𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚜𝚌𝚊𝚗𝚗𝚎𝚛",
                    'project': "dank.minecraft-server-scanner",
                    'rpc': "scanning for minecraft servers"
                },
                
                'category': True,
            },
            
            translate('Windows OS Tools'): {
                
                translate('Software Downloader / Updater'): {
                    'info': menu_request_responses["dank.winget"],
                    'title': "𝚍𝚊𝚗𝚔.𝚠𝚒𝚗𝚐𝚎𝚝",
                    'project': "dank.winget",
                    'rpc': "installing / updating software"
                },
                
                translate('Windows / Office Activator'): {
                    'info': menu_request_responses["Microsoft-Activation-Scripts"],
                    'title': "𝚍𝚊𝚗𝚔.𝚠𝚒𝚗-𝚊𝚌𝚝𝚒𝚟𝚊𝚝𝚎",
                    'project': "dank.win-activate",
                    'rpc': "activating windows / office"
                },
                
                translate('Operating System Repair'): {
                    'info': '',
                    'title': "𝚍𝚊𝚗𝚔.𝚘𝚜-𝚛𝚎𝚙𝚊𝚒𝚛",
                    'project': "dank.os-repair",
                    'rpc': "repairing windows operating system"    
                },
                
                translate('Network Reset'): {
                    'info': '',
                    'title': "𝚍𝚊𝚗𝚔.𝚗𝚎𝚝𝚠𝚘𝚛𝚔-𝚛𝚎𝚜𝚎𝚝",
                    'project': "dank.network-reset",
                    'rpc': "resetting network settings"
                },
                
                translate('Clear Icon & Thumbnail Cache'): {
                    'info': '',
                    'title': "𝚍𝚊𝚗𝚔.𝚌𝚕𝚎𝚊𝚛-𝚒𝚌𝚘𝚗𝚜",
                    'project': "dank.clear-icons",
                    'rpc': "clearing icon and thumbnail cache"
                },
                
                'category': True,
                
            },

            translate('SpotX + Spicetify Installer'): {
                'info': (f'{menu_request_responses["Spicetify"]}, {menu_request_responses["SpotX-Win"]}' if menu_request_responses["Spicetify"] and menu_request_responses["SpotX-Win"] else ""),
                'title': "𝚍𝚊𝚗𝚔.𝚜𝚙𝚘𝚝𝚒𝚏𝚢",
                'project': "dank.spotify",
                'rpc': "installing spotx and spicetify",
                'category': False,
            },

            translate('Browser Backup'): {
                'info': menu_request_responses["dank.browser-backup"],
                'title': "𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙",
                'project': "dank.browser-backup",
                'rpc': "backing up a browser",
                'category': False,
            },
            
            translate('Fusion-Fall Modding Tool'): {
                'info': menu_request_responses["dank.fusion-fall"],
                'title': "𝚍𝚊𝚗𝚔.𝚏𝚞𝚜𝚒𝚘𝚗-𝚏𝚊𝚕𝚕",
                'project': "dank.fusion-fall",
                'rpc': "modding fusion-fall",
                'category': False,
            },
            
            translate('World Exploration Game [bright_red][[red1]BETA[bright_red]]'): {
                'info': menu_request_responses["dank.game"],
                'title': "𝚍𝚊𝚗𝚔.𝚐𝚊𝚖𝚎",
                'project': "dank.game",
                'rpc': "playing a world exploration game",
                'category': False,
            },

            #'Auto Clicker [bright_red][[red1]WIP[bright_red]]': {
            #    'info': menu_request_responses["dank.auto-clicker"],
            #    'title': "𝚍𝚊𝚗𝚔.𝚊𝚞𝚝𝚘-𝚌𝚕𝚒𝚌𝚔𝚎𝚛",
            #    'project': "dank.auto-clicker",
            #    'rpc': "running auto-clicker"
            #},

            'Chatroom': {
                'info': menu_request_responses["chatroom_user_count"],
                'title': "𝚍𝚊𝚗𝚔.𝚌𝚑𝚊𝚝𝚛𝚘𝚘𝚖",
                'project': "dank.chatroom",
                'rpc': "chatting in the chatroom",
                'category': False,
            },
            
            'Discord / Telegram / Website': {

                'Discord Server': {
                    'info': '[bright_green]Join Now!',
                    'project': "Dankware Inc. Discord Server",
                },
                
                'Telegram Group': {
                    'info': '[bright_green]Join Now!',
                    'project': "Dankware Inc. Telegram Group",
                },
                
                'Website': {
                    'info': '[bright_green]Visit Now!',
                    'project': "Dankware Inc. Website",
                },
                
                'category': True
            },
            
            'Settings': {
                'info': '',
                'title': "𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 𝚜𝚎𝚝𝚝𝚒𝚗𝚐𝚜",
                'project': "dank.tool settings",
                'rpc': "changing dank.tool settings",
                'category': False,
            }
        }
    
    else: stats = ""

# translator

def translate(text):

    if DANK_TOOL_LANG and ONLINE_MODE:
        try: text = translator.translate(text, source_language='en', destination_language=DANK_TOOL_LANG)
        except: pass
    return text

if __name__ == "__main__":

    set_globals_one()
    translator = Translator()

    # multithreaded requests responses, download modules / assets

    if ONLINE_MODE:

        print(clr(f"\n  - {translate('Downloading modules')}..."))
        
        if not os.path.isdir("__modules__"): os.mkdir("__modules__")

        while True:
            try:
                multithread(download_offline_modules, 50, offline_scripts, progress_bar=False)
                break
            except:
                input(clr(f"\n  > {translate('Failed to download modules! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
                rm_line(); rm_line()
                
        # download assets

        if not os.path.isdir("ursina"): os.mkdir("ursina")
        if not os.path.isfile("ursina/assets.json"): open("ursina/assets.json", "w").write("{}")
        
        local_assets_json = json.loads(open("ursina/assets.json", "r").read())
        
        while True:
            try: latest_assets_json = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__assets__/dank.game/assets.json", headers=headers).json(); break
            except:
                input(clr(f"\n  > {translate('Failed to get latest assets! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
                rm_line(); rm_line()
                
        asset_urls = []
        file_names = []
        
        for folder in latest_assets_json:
            if not os.path.isdir(f"ursina/{folder}"):
                os.makedirs(f"ursina/{folder}")
            if not folder in local_assets_json.keys():
                local_assets_json[folder] = {}
            for asset in latest_assets_json[folder]:
                if not asset in local_assets_json[folder].keys() or local_assets_json[folder][asset] < latest_assets_json[folder][asset]:
                    asset_urls.append(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__assets__/dank.game/{folder}/{asset}")
                    file_names.append(f"ursina/{folder}/{asset}")
        
        if asset_urls:
                
            print(clr(f"\n  - {translate('Downloading game assets')}...\n"))
            
            while True:
                try:
                    multithread(download_assets, 50, asset_urls, file_names)
                    break
                except:
                    input(clr(f"\n  > {translate('Failed to download assets! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
                    rm_line(); rm_line()
            
            open("ursina/assets.json", "w").write(json.dumps(latest_assets_json, indent=4))
        
        del local_assets_json, latest_assets_json, asset_urls, file_names

        # multithreaded request responses
        
        print(clr(f"\n  - {translate('Getting request responses')}...\n"))
        
        global menu_request_responses
        menu_request_responses = {}
        
        # KEEP request_keys IN ORDER!

        request_keys = tuple(
            (
                "dankware_runs",
                "danktool_runs",
                "motd",
                "chatroom_user_count",
                "SpotX-Win",
                "Spicetify",
                "Microsoft-Activation-Scripts",
                "dank.minecraft-server-builder",
                "dank.minecraft-server-scanner",
                "dank.auto-clicker",
                "dank.browser-backup",
                "dank.fusion-fall",
                "dank.game",
                "dank.winget"
            )
        )

        while True:
            try:
                multithread(get_menu_request_responses, 50, tuple(_ for _ in range(len(request_keys))), request_keys)
                del request_keys
                break
            except:
                input(clr(f"\n  > {translate('Failed to get request responses! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
                rm_line(); rm_line()

    del updated_on
    del download_assets
    del download_offline_modules
    del get_menu_request_responses

    # main

    executor = ThreadPoolExecutor(10)
    executor.submit(notify, '[ SirDank ]',
        translate('Thank you for using my tool ❤️\nShare it with your friends!'),
        icon = {'src': f'{os.path.dirname(__file__)}\\dankware.ico', 'placement': 'appLogoOverride'} if os.path.exists(f'{os.path.dirname(__file__)}\\dankware.ico') else None,
        image = f'{os.path.dirname(__file__)}\\red.png' if os.path.exists('red.png') else None
    )

    while True:
        
        # reset
        
        set_globals_one()
        set_globals_two()

        title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 {DANK_TOOL_VERSION}" + ("" if ONLINE_MODE else " [ 𝙾𝙵𝙵𝙻𝙸𝙽𝙴 ]")) # DANK_TOOL_VERSION defined in executor.py
        os.environ['DISCORD_RPC'] = "on the main menu"
        os.chdir(os.path.dirname(__file__))
            
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
        
        while True:
            
            # user input
            
            choice = input(clr("  > Choice: ") + red)
            if choice.isdigit() and int(choice) >= 1 and int(choice) <= int(len(modules) + len(local_modules)):
                
                if int(choice) <= len(modules):
                    choice = modules[list(modules.keys())[int(choice) - 1]]
                    LOCAL_MODULE = False
                else:
                    choice = local_modules[list(local_modules.keys())[int(choice) - len(modules) - 1]]
                    LOCAL_MODULE = True
                
                if not LOCAL_MODULE and choice['category']:

                    print_category_modules(choice)
                    
                    while True:
                        _choice = input(clr("  > Choice: ") + red)
                        if _choice == '0':
                            print_modules()
                            break
                        elif _choice.isdigit() and int(_choice) >= 1 and int(_choice) <= (len(choice) - 1):
                            choice = choice[list(choice.keys())[int(_choice) - 1]]
                            break
                        else: rm_line()
                        
                    if not 'category' in choice.keys():
                        break
                        
                else:
                    
                    break

            elif choice == 'refresh': # re-align ui
                print_modules()
            
            elif choice == 'debug': # debug menu
                cls()
                while True:
                    # this variable is long to prevent it from being changed!
                    cmd_to_be_executed = input(clr("\n  > ") + white)
                    if cmd_to_be_executed == 'exit': print_modules(); break
                    elif cmd_to_be_executed == 'env':
                        print()
                        for key, val in os.environ.items(): print(clr(key, colour_one=green, colour_two=green) + f"{white}:{green} " + clr(val, colour_one=green, colour_two=green))
                        continue
                    try: exec(cmd_to_be_executed)
                    except: print(clr("\n" + err(sys.exc_info()), 2))
            
            elif choice == 'exit':
                os.system("taskkill /f /im dank.tool.exe")
            
            else: rm_line()

        try:

            if "Discord" in choice['project']:
                os.system(f'start https://allmylinks.com/link/out?id=kdib4s-nu8b-1e19god')
                continue
            elif "Telegram" in choice['project']:
                os.system(f'start https://t.me/+18tWHJ_g2g4yZWI1')
                continue
            elif "Website" in choice['project']:
                os.system(f'start https://dank-site.onrender.com/')
                continue
            else:
                title(choice['title'])
                project = choice['project']
                os.environ['DISCORD_RPC'] = choice['rpc']
                
            # settings menu
                
            if "dank.tool settings" in choice['project']:
                
                try: runs = open(os.path.join(os.path.expandvars("%LOCALAPPDATA%\\Dankware"), "runs.txt"), 'r').read()
                except: runs = "?"

                while True:
                    
                    cls(); print(clr(f"\n  - Settings: [ {translate('restart for changes to take effect')} ]\n\n  - dank.tool run counter: {runs}\n"))
                    
                    settings = json.loads(open("settings.json", "r", encoding="utf-8").read())
                    update_settings = False
                    
                    if os.path.isfile("force-startup-audio"):
                        if not int(settings["force-startup-audio"]):
                            settings["force-startup-audio"] = "1"
                            update_settings = True
                    else:
                        if int(settings["force-startup-audio"]):
                            settings["force-startup-audio"] = "0"
                            update_settings = True
                    if os.path.isfile("disable-startup-audio"):
                        if not int(settings["disable-startup-audio"]):
                            settings["disable-startup-audio"] = "1"
                            update_settings = True
                    else:
                        if int(settings["disable-startup-audio"]):
                            settings["disable-startup-audio"] = "0"
                            update_settings = True
                    
                    if update_settings:
                        open("settings.json", "w", encoding="utf-8").write(json.dumps(settings, indent=4))
                    
                    print(clr(f"  [0] Return to menu"))
                    
                    counter = 1
                    for name, value in settings.items():
                        print(clr(f"  [{counter}] {name}: {'True' if int(value) else 'False'}"))
                        counter += 1
                    
                    choice = input(clr("\n  > Choice: ") + red).lower() 
                    
                    if choice.isdigit() and int(choice) >= 0 and int(choice) <= int(len(settings)):
                        
                        if choice == '0': break
                        
                        settings = list(settings.items())
                        settings[int(choice) - 1] = (settings[int(choice) - 1][0], str(int(not int(settings[int(choice) - 1][1]))))
                        settings = dict(settings)
                        
                        if int(settings["force-startup-audio"]):
                            if not os.path.isfile("force-startup-audio"):
                                open("force-startup-audio", "w", encoding="utf-8").write("")
                        else:
                            if os.path.isfile("force-startup-audio"):
                                os.remove("force-startup-audio")
                        if int(settings["disable-startup-audio"]):
                            if not os.path.isfile("disable-startup-audio"):
                                open("disable-startup-audio", "w", encoding="utf-8").write("")
                        else:
                            if os.path.isfile("disable-startup-audio"):
                                os.remove("disable-startup-audio")
                        
                        open("settings.json", "w", encoding="utf-8").write(json.dumps(settings, indent=4))

                continue
        
            elif "dank.os-repair" in choice['project']:
                
                cls(); input(clr(f"\n  [ DISCLAIMER ]\n\n  - {translate('Do not use this module if you do not know what you are doing')}!\n  - {translate('Close all other applications before continuing')}!\n  - {translate('This tool is not responsible for any damage to your system')}!\n  - {translate('This tool is not responsible for any data loss')}!\n\n  > Press [ENTER] to continue... "))
                cls(); print(clr(f"""
  [ COMMANDS ]

  - [0] Return to menu

  - [1] {clr('DISM /online /cleanup-image /restorehealth',2)} : {translate('This command uses the Deployment Image Servicing and Management (DISM) tool to scan the health of your Windows image and, if necessary, restore it. The /online option targets the running operating system, /cleanup-image specifies that you are servicing an image, and /restorehealth checks for component store corruption and performs repair operations automatically')}.
  
  - [2] {clr('sfc /scannow',2)} : {translate('This command initiates the System File Checker (SFC) tool to scan all protected system files and replace incorrect versions with correct Microsoft versions. The /scannow option scans all protected system files immediately')}.
  
  - [3] {clr('chkdsk C: /x /r',2)} : {translate('This command uses the Check Disk (chkdsk) utility to check the file system and file system metadata of a volume for logical and physical errors. C: specifies the drive you want to check, /x forces the volume to dismount before it is checked (necessary for fixing certain errors), and /r locates bad sectors and recovers readable information')}.

  - [4] Run all commands
"""))
                
                while True:

                    choice = input(clr("  > Choice: ") + red).lower()
                    if choice.isdigit() and int(choice) >= 0 and int(choice) <= 4:
                        
                        cls()

                        if choice in ('1', '4'):
                            print(clr(f"\n\n  [ DISM /online /cleanup-image /restorehealth ]"))
                            os.system("DISM /online /cleanup-image /restorehealth")
                        if choice in ('2', '4'):
                            print(clr(f"\n\n  [ sfc /scannow ]"))
                            os.system("sfc /scannow")
                        if choice in ('3', '4'):
                            print(clr(f"\n\n  [ chkdsk C: /x /r ]"))
                            os.system("chkdsk C: /x /r")
                        
                        input(clr("\n  > Press [ENTER] to continue... "))
                        
                        break
                    
                    else: rm_line()
                
                continue
            
            elif "dank.network-reset" in choice['project']:
                
                cls(); input(clr(f"\n  [ DISCLAIMER ]\n\n  - {translate('Do not use this module if you do not know what you are doing')}!\n  - {translate('Close all other applications before continuing')}!\n  - {translate('This tool is not responsible for any damage to your system')}!\n  - {translate('This tool is not responsible for any data loss')}!\n\n  > Press [ENTER] to continue... "))
                cls(); print(clr(f"""
  [ COMMANDS ]

  - [0] Return to menu

  - [1] {clr('ipconfig /flushdns',2)} : {translate('This command purges the DNS Resolver cache. The DNS Resolver cache stores the IP addresses for websites that your computer has recently accessed, which can speed up subsequent accesses to the same websites. Flushing this cache can help resolve any outdated or incorrect DNS information')}.

  - [2] {clr('ipconfig /registerdns',2)} : {translate('This command refreshes all DHCP leases and re-registers DNS names. This is useful if you have changed your DNS server or refreshed your IP address and want to update the DNS records')}.

  - [3] {clr('ipconfig /release',2)} : {translate('This command releases the IP address for the specified adapter. This is typically used when you are having issues with your current IP address and want to acquire a new one from your DHCP server')}.

  - [4] {clr('ipconfig /renew',2)} : {translate('This command renews the IP address for the specified adapter. You would typically use this after releasing an IP address to get a new one')}.

  - [5] {clr('netsh winsock reset',2)} : {translate('This command resets the Winsock Catalog to a clean state. All Winsock Layered Service Providers (LSPs) are removed from the Winsock catalog. Any LSPs that are installed will need to be re-installed. This is useful if you are experiencing networking issues due to corrupt LSPs or Winsock settings')}.

  - [6] Run all commands
"""))
                
                while True:

                    choice = input(clr("  > Choice: ") + red).lower()
                    if choice.isdigit() and int(choice) >= 0 and int(choice) <= 6:
                        
                        cls()

                        if choice in ('1', '6'):
                            print(clr(f"\n\n  [ ipconfig /flushdns ]"))
                            os.system("ipconfig /flushdns")
                        if choice in ('2', '6'):
                            print(clr(f"\n\n  [ ipconfig /registerdns ]"))
                            os.system("ipconfig /registerdns")
                        if choice in ('3', '6'):
                            print(clr(f"\n\n  [ ipconfig /release ]"))
                            os.system("ipconfig /release")
                        if choice in ('4', '6'):
                            print(clr(f"\n\n  [ ipconfig /renew ]"))
                            os.system("ipconfig /renew")
                        if choice in ('5', '6'):
                            print(clr(f"\n\n  [ netsh winsock reset ]"))
                            os.system("netsh winsock reset")
                        
                        input(clr("\n  > Press [ENTER] to continue... "))
                        
                        break
                    
                    else: rm_line()
                
                continue
            
            elif "dank.clear-icons" in choice['project']:
                
                #cls(); input(clr(f"\n  [ DISCLAIMER ]\n\n  - {translate('Do not use this module if you do not know what you are doing')}!\n  - {translate('Close all other applications before continuing')}!\n  - {translate('This tool is not responsible for any damage to your system')}!\n  - {translate('This tool is not responsible for any data loss')}!\n\n  > Press [ENTER] to continue... "))
                cls(); print(clr(f"""
  [ COMMANDS ]
  
  - [0] Return to menu
  
  - [1] {clr('Clear Icon Cache',2)} : {translate('This task clears the icon cache for the current user. This is useful if you are experiencing issues with icons not displaying correctly')}.
  
  - [2] {clr('Clear Thumbnail Cache',2)} : {translate('This task clears the thumbnail cache for the current user. This is useful if you are experiencing issues with thumbnails not displaying correctly')}.
  
  - [3] Run all tasks
"""))
                
                while True:

                    choice = input(clr("  > Choice: ") + red).lower()
                    if choice.isdigit() and int(choice) >= 0 and int(choice) <= 3:
                        
                        if choice != '0':
                            cls()
                            print(clr(f"\n  [ Terminating Explorer.exe ]"))
                            os.system("taskkill /f /im explorer.exe >nul 2>&1")
                            os.chdir(os.path.expandvars("%userprofile%\\AppData\\Local\\Microsoft\\Windows\\Explorer"))

                        if choice in ('1', '3'):
                            print(clr(f"\n  [ Clearing Icon Cache ]\n"))
                            os.system(r"attrib -h iconcache*")
                            for file in os.listdir():
                                if file.startswith("iconcache") and file.endswith(".db"):
                                    try: 
                                        os.remove(file)
                                        print(clr(f"  - deleted {file}"))
                                    except:
                                        print(clr(f"  - failed to delete {file}",2))
                        if choice in ('2', '3'):
                            print(clr(f"\n  [ Clearing Thumbnail Cache ]\n"))
                            os.system(r"attrib -h thumbcache*")
                            for file in os.listdir():
                                if file.startswith("thumbcache") and file.endswith(".db"):
                                    try: 
                                        os.remove(file)
                                        print(clr(f"  - deleted {file}"))
                                    except:
                                        print(clr(f"  - failed to delete {file}",2))
                        
                        if choice != '0':
                            os.chdir(os.path.dirname(__file__))
                            print(clr(f"\n  [ Starting Explorer.exe ]"))
                            os.system("start explorer.exe")
                            input(clr("\n  > Press [ENTER] to continue... "))
                        
                        break
                    
                    else: rm_line()
                
                continue
                
            if LOCAL_MODULE:
                
                # get src from local_module
                
                while True:
                    try: code = open(f'__local_modules__/{project}.py', 'r', encoding='utf-8').read(); break
                    except:
                        translation = translate(f"Failed to get code! Unable to read '__local_modules__/{project}.py'! Press [ENTER] to try again")
                        input(clr(f"\n  > {translation}... ",2))
                        rm_line(); rm_line()
                
            else:

                # get src from github if not debug mode else get src locally

                if not OFFLINE_SRC and ( ONLINE_MODE or not os.path.exists(f'__modules__/{project}.py') ): # OFFLINE_SRC / ONLINE_MODE defined in executor.py
                    
                    # check for update before getting src
                    
                    while True:
                        try:
                            LATEST_VERSION = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__src__/executor_version.txt", headers=headers).content.decode()
                            if parse(LATEST_VERSION) > parse(DANK_TOOL_VERSION):
                                cls(); print(clr(f"\n  - Updating to the latest version...\n\n  - Update Found: {LATEST_VERSION}"))
                                dank_tool_installer()
                            else:
                                break
                        except:
                            input(clr(f"\n  > {translate('Failed to get latest version! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
                            rm_line(); rm_line()
                    
                    while True:
                        try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{BRANCH}/__modules__/{project}.py", headers=headers).content.decode(); break
                        except:
                            input(clr(f"\n  > {translate(f'Failed to get code for {project}! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
                            rm_line(); rm_line()
                else:
                    while True:
                        try: code = open(f'__modules__/{project}.py', 'r', encoding='utf-8').read(); break
                        except:
                            translation = translate(f"Failed to get code! Unable to read '__modules__/{project}.py'! Press [ENTER] to try again")
                            input(clr(f"\n  > {translation}... ",2))
                            rm_line(); rm_line()

            # execute src
            
            if code == "404: Not Found":
                if project.startswith('_'):
                    print(clr(f"\n  - {translate(f'{project[1:]} has been disabled! Returning to menu in 5 seconds')}...",2))
                else:
                    print(clr(f"\n  - {translate(f'{project} has not been released yet! Returning to menu in 5 seconds')}...",2))
                time.sleep(5)
            else:
                cls(); exec(code)
                cls(); print(clr(f"\n  - {translate(f'{project} executed successfully! Returning to menu in 3 seconds')}...")); time.sleep(3)

        except:

            err_message = err(sys.exc_info())
            print(clr(err_message, 2))
        
            if "Error Type: KeyboardInterrupt" in err_message:
                
                print_warning_symbol()
                print(clr(f"\n  - {translate('Please select text first and then use [ CTRL + C ]')}!"))
                
            elif ONLINE_MODE and not LOCAL_MODULE:
                while True:
                    try: requests.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": f"```<--- 🚨 ---> Module: {choice['title']}\n\n{err_message}```"}); break
                    except:
                        input(clr(f"\n  > {translate('Failed to post error report! Make sure you are connected to the internet! Press [ENTER] to try again')}... ",2))
                        rm_line(); rm_line()
                print(clr(f"\n  > {translate('Error Reported! If it is an OS error, Please run as admin and try again!')}\n\n  > {translate('If it is a logic error, it will be fixed soon!')}"))
            
            input(clr("\n  > Press [ENTER] to return to the menu... "))
            #os.system("taskkill /f /im dank.tool.exe")
