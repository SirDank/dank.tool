###################################################################################

#                            https://github.com/SirDank                            

###################################################################################

import os
import sys
import time
import requests
from rich.panel import Panel
from datetime import datetime
from rich.columns import Columns
from rich.console import Console
from win10toast import ToastNotifier
from dateutil.tz import tzlocal, tzutc
from dankware import white, white_normal, green, red, red_normal, red_dim
from dankware import align, cls, clr, title, get_duration, multithread, err, rm_line

# get env vars

OFFLINE_DEV = int(os.environ['DANK_TOOL_OFFLINE_DEV'])
ONLINE_DEV = int(os.environ['DANK_TOOL_ONLINE_DEV'])
DANK_TOOL_VERSION = os.environ['DANK_TOOL_VERSION']
ONLINE_MODE = int(os.environ['DANK_TOOL_ONLINE'])
branch = ("main" if not ONLINE_DEV else "dev")
headers = {"User-Agent": "dank.tool"}
os.chdir(os.path.dirname(__file__))

# print randomly coloured and aligned banner

def print_banner():
    
    global banner
    banner = '\n   ..                                       ..                  s                                  .. \n dF                                   < .z@8"`                 :8                            x .d88"  \n\'88bu.                     u.    u.    !@88E                  .88           u.          u.    5888R   \n\'*88888bu         u      x@88k u@88c.  \'888E   u             :888ooo  ...ue888b   ...ue888b   \'888R   \n  ^"*8888N     us888u.  ^"8888""8888"   888E u@8NL         -*8888888  888R  888r  888R  888r   888R   \n beWE "888L .@88 "8888"   8888  888R    888E`"88*"           8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E .dN.            8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E~8888            8888     888R  888>  888R  888>   888R   \n 888E  888F 9888  9888    8888  888R    888E \'888&     .    .8888Lu= u8888cJ888  u8888cJ888    888R   \n.888N..888  9888  9888   "*88*" 8888"   888E  9888.  .@8c   ^%888*    "*888*P"    "*888*P"    .888B . \n `"888*""   "888*""888"    ""   \'Y"   \'"888*" 4888" \'%888"    \'Y"       \'Y"         \'Y"       ^*888%  \n    ""       ^Y"   ^Y\'                   ""    ""     ^*                                        "%    \n'    
    cls(); print(align(clr(banner,4,colours=[white, white_normal, red, red_normal, red_dim]) + f"\n{white}s i r {red}. {white}d a n k {red}💕"))
    
# get commit date & time

def updated_on(url, dankware_module = True):

    if dankware_module: url = f"https://api.github.com/repos/SirDank/dank.tool/commits?path=__modules__/{url}.py&page=1&per_page=1"
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

def get_request_responses(task_id, req_key):
    
    global request_responses
    
    # get global runs
    
    if task_id in (0, 1):

        if task_id == 0: url = "https://api.countapi.xyz/get/dankware"
        elif task_id == 1: url = "https://api.countapi.xyz/get/dank.tool"
        try: request_responses[req_key] = requests.get(url, headers=headers, timeout=3).json()['value']
        except: request_responses[req_key] = f"{red}⚠️"

    elif task_id == 2:

        try:
            tmp = requests.get("https://dank-site.onrender.com/chatroom-users", headers=headers, timeout=3).content.decode()
            if tmp.isdigit() and tmp != "0": request_responses[req_key] = tmp
            else: request_responses[req_key] = "1"
            request_responses[req_key] = f"[bright_green]{request_responses[req_key]} online{' (you)' if request_responses[req_key] == '1' else ''}"
        except: request_responses[req_key] = f"[bright_red]⚠️"
        
    # get last update time
    
    elif task_id in (3, 4, 5):
        
        if task_id == 3: url = "https://api.github.com/repos/amd64fox/SpotX/commits?path=Install.ps1&page=1&per_page=1"
        elif task_id == 4: url = "https://api.github.com/repos/spicetify/spicetify-cli/commits?path=.&page=1&per_page=1"
        elif task_id == 5: url = "https://api.github.com/repos/massgravel/Microsoft-Activation-Scripts/commits?path=MAS/All-In-One-Version/MAS_AIO.cmd&page=1&per_page=1"
        request_responses[req_key] = updated_on(url,False)
        
    elif task_id > 5:
        
        request_responses[req_key] = updated_on(req_key)

# multithreaded script downloader

def download_offline_scripts(project):
    
    code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{branch}/__modules__/{project}.py", headers=headers).content.decode()
    open(f'__modules__/{project}.py', 'w', encoding='utf-8').write(code)

# multithread requests & download offline scripts

request_responses = {}
offline_modules = {

    'Fusion-Fall Modding Tool': {
        'req_resp': '',
        'title': "𝚍𝚊𝚗𝚔.𝚏𝚞𝚜𝚒𝚘𝚗-𝚏𝚊𝚕𝚕",
        'project': "dank.fusion-fall",
        'rpc': "modding fusion-fall"
    },
    
    'Browser Backup': {
        'req_resp': '',
        'title': "𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙",
        'project': "dank.browser-backup",
        'rpc': "backing up a browser"
    }
}

offline_scripts = ["dank.fusion-fall", "dank.browser-backup"]

if ONLINE_MODE:

    if not os.path.isdir("__modules__"): os.mkdir("__modules__")
    
    print(clr("\n  > Downloading scripts..."))

    while True:
        try:
            multithread(download_offline_scripts, 50, [_ for _ in offline_scripts], progress_bar=False)
            break
        except KeyboardInterrupt:
            input(clr(f"\n  > Failed to get request responses! Try not to use [COPY] or [PASTE]! Press [ENTER] to try again... ",2))
        except:
            input(clr(f"\n  > Failed to download scripts! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

    print(clr("\n  > Getting request responses..."))

    while True:
        try:
            # KEEP request_keys IN ORDER!
            request_keys = ["dankware_runs", "danktool_runs", "chatroom_user_count", "SpotX-Win", "Spicetify", "dank.win-activate", "dank.minecraft-server-builder", "dank.minecraft-server-scanner", "dank.auto-clicker", "dank.browser-backup", "dank.fusion-fall"]
            multithread(get_request_responses, 50, [_ for _ in range(len(request_keys))], [_ for _ in request_keys], progress_bar=False)
            break
        except KeyboardInterrupt:
            input(clr(f"\n  > Failed to get request responses! Try not to use [COPY] or [PASTE]! Press [ENTER] to try again... ",2))
        except:
            input(clr(f"\n  > Failed to get request responses! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

# main

toast = ToastNotifier()
toast.show_toast("SirDank:", "Thank you for using my tool ❤️\nShare it with your friends!", duration = 10, icon_path = f"{os.path.dirname(__file__)}\\dankware.ico", threaded = True)

while True:

    title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 {DANK_TOOL_VERSION}" + ("" if ONLINE_MODE else " | 𝙾𝙵𝙵𝙻𝙸𝙽𝙴")) # version defined in executor.py
    os.environ['DISCORD_RPC'] = "on the main menu"
    os.chdir(os.path.dirname(__file__))

    # global runs
    
    stats = "" if not ONLINE_MODE else f" [ dankware runs: {green}{request_responses['dankware_runs']} | dank.tool runs: {green}{request_responses['danktool_runs']} ]"
        
    # available modules
    
    modules = offline_modules if not ONLINE_MODE else {

        'Minecraft Server Builder': {
            'req_resp': request_responses["dank.minecraft-server-builder"],
            'title': "𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚋𝚞𝚒𝚕𝚍𝚎𝚛",
            'project': "dank.minecraft-server-builder",
            'rpc': "building a minecraft server"
        },

        'Minecraft Server Scanner': {
            'req_resp': request_responses["dank.minecraft-server-scanner"],
            'title': "𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚜𝚌𝚊𝚗𝚗𝚎𝚛",
            'project': "dank.minecraft-server-scanner",
            'rpc': "scanning for minecraft servers"
        },

        'Fusion-Fall Modding Tool': {
            'req_resp': request_responses["dank.fusion-fall"],
            'title': "𝚍𝚊𝚗𝚔.𝚏𝚞𝚜𝚒𝚘𝚗-𝚏𝚊𝚕𝚕",
            'project': "dank.fusion-fall",
            'rpc': "modding fusion-fall"
        },

        'SpotX + Spicetify Installer': {
            'req_resp': f'{request_responses["Spicetify"]}, {request_responses["SpotX-Win"]}',
            'title': "𝚍𝚊𝚗𝚔.𝚜𝚙𝚘𝚝𝚒𝚏𝚢",
            'project': "dank.spotify",
            'rpc': "installing spotx and spicetify"
        },

        'Browser Backup': {
            'req_resp': request_responses["dank.browser-backup"],
            'title': "𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙",
            'project': "dank.browser-backup",
            'rpc': "backing up a browser"
        },

        'Windows / Office Activator': {
            'req_resp': request_responses["dank.win-activate"],
            'title': "𝚍𝚊𝚗𝚔.𝚠𝚒𝚗-𝚊𝚌𝚝𝚒𝚟𝚊𝚝𝚎",
            'project': "dank.win-activate",
            'rpc': "activating windows / office"
        },

        #'Auto Clicker [bright_red][[red1]WIP[bright_red]]': {
        #    'req_resp': request_responses["dank.auto-clicker"],
        #    'title': "𝚍𝚊𝚗𝚔.𝚊𝚞𝚝𝚘-𝚌𝚕𝚒𝚌𝚔𝚎𝚛",
        #    'project': "dank.auto-clicker",
        #    'rpc': "running auto-clicker"
        #},

        'Chatroom': {
            'req_resp': request_responses["chatroom_user_count"],
            'title': "𝚍𝚊𝚗𝚔.𝚌𝚑𝚊𝚝𝚛𝚘𝚘𝚖",
            'project': "dank.chatroom",
            'rpc': "chatting in the chatroom"
        },
    
        'Discord Server': {
            'req_resp': '[bright_green]Join Now!',
            'project': "Dank.Bois Discord Server",
        }
    }
    
    local_modules = {}
    
    if not os.path.exists('__local_modules__'):
        os.mkdir('__local_modules__')
    for module in os.listdir("__local_modules__"):
        if module.endswith(".py") and os.path.isfile(f"__local_modules__/{module}"):
            name = module.replace('.py','')
            local_modules[name] = {
                'title': name,
                'project': name,
                'rpc': f'running "{module}"'}
    
    # print modules with index and get choice
    
    def print_modules():
        
        print_banner(); print(clr(f"\n  - Modules:{stats}") + red + ('' if ONLINE_MODE else ' OFFLINE') + ('' if not OFFLINE_DEV else ' DEBUG') + ('' if not ONLINE_DEV else ' ONLINE DEBUG') + "\n")
        user_renderables = []
        console = Console()
        counter = 1
        
        for _title, module in modules.items():
            user_renderables.append(f"[b][bright_white]{counter} [bright_red]> [bright_white]{_title}[/b] {module['req_resp']}")
            counter += 1
            
        for _title in local_modules.keys():
            user_renderables.append(f"[b][bright_white]{counter} [bright_cyan]> [bright_white]{_title}[/b]")
            counter += 1

        console.print(Panel(title=f"[red1]> [bright_white][b]M O D U L E S[/b] [red1]<", title_align="center", renderable=Columns(user_renderables, expand=True), style="bright_red", expand=True))
        print()

    print_modules()
    
    while True:
        
        choice = input(clr("  - Choice: ") + red)
        if choice.isdigit() and int(choice) >= 1 and int(choice) <= int(len(modules) + len(local_modules)):
            if int(choice) <= len(modules):
                choice = modules[list(modules.keys())[int(choice) - 1]]
                LOCAL_MODULE = False
            else:
                choice = local_modules[list(local_modules.keys())[int(choice) - len(modules) - 1]]
                LOCAL_MODULE = True
            break
        
        elif choice == 'refresh':
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
                try: exec(cmd_to_be_executed)
                except: print(clr("\n" + err(sys.exc_info()), 2))
        
        else: rm_line()

    try:
        
        if "Discord" in choice['project']:
            os.system(f'start https://allmylinks.com/link/out?id=kdib4s-nu8b-1e19god'); continue
        
        else:
            title(choice['title'])
            project = choice['project']
            os.environ['DISCORD_RPC'] = choice['rpc']
            
        if LOCAL_MODULE:
            
            # get src from local_module
            
            while True:
                try: code = open(f'__local_modules__/{project}.py', 'r', encoding='utf-8').read(); break
                except: input(clr(f"\n  > Failed to get code! Unable to read '__local_modules__/{project}.py'! Press [ENTER] to try again... ",2))
                rm_line(); rm_line()
            
        else:

            # get src from github if not debug mode else get src locally

            if not OFFLINE_DEV and ( ONLINE_MODE or not os.path.exists(f'__modules__/{project}.py') ): # OFFLINE_DEV defined in executor.py
                while True:
                    try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/{branch}/__modules__/{project}.py", headers=headers).content.decode(); break
                    except: input(clr(f"\n  > Failed to get code for {project}! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
                    rm_line(); rm_line()
            else:
                while True:
                    try: code = open(f'__modules__/{project}.py', 'r', encoding='utf-8').read(); break
                    except: input(clr(f"\n  > Failed to get code! Unable to read '__modules__/{project}.py'! Press [ENTER] to try again... ",2))
                    rm_line(); rm_line()

        # execute src
        
        if code == "404: Not Found":
            print(clr(f"\n  > {project} has not been released yet! Returning to menu in 5s...",2)); time.sleep(5)
        else:
            cls(); exec(code)
            cls(); print(clr(f"\n  > {project} executed successfully! Returning to menu in 5s...")); time.sleep(5)

    except:

        err_message = err(sys.exc_info())
        print(clr(err_message, 2))
        if ONLINE_MODE:
            if "Error Type: KeyboardInterrupt" in err_message:
                user_message = input(clr("\n  > Briefly explain what you were doing when this error occurred [ this will be sent to the developer ]: ",2) + white)
                if user_message == "": content = f"```<--- 🚨 ---> Module: {choice}\n\n{err_message}```"
                else: content = f"```<--- 🚨 ---> Module: {choice}\n\n{err_message}\n\n  > User Message: {user_message}```"
            while True:
                try: requests.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": content}); break
                except:
                    input(clr(f"\n  > Failed to post error report! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
                    rm_line(); rm_line()
            print(clr("\n  > Error Reported! If it is an OS error, Please run as admin and try again!\n\n  > If it is a logic error, it will be fixed soon!"))
        input(clr("\n  > Press [ENTER] to EXIT... "))
        os.system("taskkill /f /im dank.tool.exe")

