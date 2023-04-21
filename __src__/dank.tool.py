###################################################################################

#                            https://github.com/SirDank                            

###################################################################################

import os
import sys
import time
import requests
from datetime import datetime
from win10toast import ToastNotifier
from dateutil.tz import tzlocal, tzutc
from dankware import align, cls, clr, magenta, white, title, get_duration, multithread, err, rm_line

headers = {"User-Agent": "dank.tool"}
toast = ToastNotifier()
toast.show_toast("SirDank:", "Thank you for using my tool <3\nShare it with your friends!", duration = 10, icon_path = f"{os.path.dirname(__file__)}\\dankware.ico", threaded = True)

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
        
        return f"[ updated {get_duration(date_time_data, datetime.now(tzlocal()), interval='dynamic')} ago ]"
    except: return "[ updated ? ago ]"

# multithread requests

def get_request_responses(task_id):
    
    global request_responses
    
    # get global runs
    
    if task_id == 0: 
        try: request_responses["dankware_runs"] = requests.get("https://api.countapi.xyz/get/dankware", headers=headers, timeout=3).json()['value']
        except: request_responses["dankware_runs"] = "?"
    elif task_id == 1: 
        try: request_responses["danktool_runs"] = requests.get("https://api.countapi.xyz/get/dank.tool2", headers=headers, timeout=3).json()['value']
        except: request_responses["danktool_runs"] = "?"
    elif task_id == 2:
        try:
            tmp = requests.get("https://dank-site.onrender.com/chatroom-users", headers=headers, timeout=3).content.decode()
            if tmp.isdigit() and tmp != "0": request_responses["chatroom_user_count"] = tmp
            else: request_responses["chatroom_user_count"] = "1"
        except: request_responses["chatroom_user_count"] = "?"
        
    # get last update time
    
    elif task_id == 3: request_responses["dank.minecraft-server-builder"] = updated_on("dank.minecraft-server-builder")
    elif task_id == 4: request_responses["dank.minecraft-server-scanner"] = updated_on("dank.minecraft-server-scanner")
    elif task_id == 5: request_responses["SpotX-Win"] = updated_on("https://api.github.com/repos/amd64fox/SpotX/commits?path=Install.ps1&page=1&per_page=1",False)
    elif task_id == 6: request_responses["Spicetify"] = updated_on("https://api.github.com/repos/spicetify/spicetify-cli/commits?path=.&page=1&per_page=1",False)
    elif task_id == 7: request_responses["dank.auto-clicker"] = updated_on("dank.auto-clicker")
    elif task_id == 8: request_responses["dank.browser-backup"] = updated_on("dank.browser-backup")
    elif task_id == 9: request_responses["dank.fusion-fall"] = updated_on("dank.fusion-fall")

# main

while True:

    title(f"𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕 {current_version}") # current_version defined in executor.py
    os.chdir(os.path.dirname(__file__)) # exec_mode = "exe"; exec(chdir(exec_mode))
    discord_rpc_state = "on the main menu"
    #old_banner='\n     _             _                      _ \n    | |           | |     _              | |\n  _ | | ____ ____ | |  _ | |_  ___   ___ | |\n / || |/ _  |  _ \\| | / )|  _)/ _ \\ / _ \\| |\n( (_| ( ( | | | | | |< ( | |_| |_| | |_| | |\n \\____|\\_||_|_| |_|_| \\_|_)___)___/ \\___/|_|\n'
    banner = '\n   ..                                       ..                  s                                  .. \n dF                                   < .z@8"`                 :8                            x .d88"  \n\'88bu.                     u.    u.    !@88E                  .88           u.          u.    5888R   \n\'*88888bu         u      x@88k u@88c.  \'888E   u             :888ooo  ...ue888b   ...ue888b   \'888R   \n  ^"*8888N     us888u.  ^"8888""8888"   888E u@8NL         -*8888888  888R  888r  888R  888r   888R   \n beWE "888L .@88 "8888"   8888  888R    888E`"88*"           8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E .dN.            8888     888R  888>  888R  888>   888R   \n 888E  888E 9888  9888    8888  888R    888E~8888            8888     888R  888>  888R  888>   888R   \n 888E  888F 9888  9888    8888  888R    888E \'888&     .    .8888Lu= u8888cJ888  u8888cJ888    888R   \n.888N..888  9888  9888   "*88*" 8888"   888E  9888.  .@8c   ^%888*    "*888*P"    "*888*P"    .888B . \n `"888*""   "888*""888"    ""   \'Y"   \'"888*" 4888" \'%888"    \'Y"       \'Y"         \'Y"       ^*888%  \n    ""       ^Y"   ^Y\'                   ""    ""     ^*                                        "%    \n'
    
    # multithread requests
        
    request_responses = {}
    while True:
        try: multithread(get_request_responses, 50, [ _ for _ in range(10) ], progress_bar=False); break
        except KeyboardInterrupt: input(clr(f"\n  > Failed to get request responses! Try not to use [COPY] or [PASTE]! Press [ENTER] to try again... ",2))
        except: input(clr(f"\n  > Failed to get request responses! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
    
    # global runs
    
    stats = f"dankware runs: {request_responses['dankware_runs']} | dank.tool runs: {request_responses['danktool_runs']}"
        
    # available modules
    
    modules = [
        f'Minecraft Server Builder {request_responses["dank.minecraft-server-builder"]}',
        f'Minecraft Server Scanner {request_responses["dank.minecraft-server-scanner"]}',
        f'Fusion-Fall Modding Tool {request_responses["dank.fusion-fall"]}',
        f'SpotX {request_responses["SpotX-Win"]} + Spicetify {request_responses["Spicetify"]} Installer',
        f'Browser Backup {request_responses["dank.browser-backup"]}',
        f'Auto Clicker {request_responses["dank.auto-clicker"]} [WIP]',
        f'Chatroom [ {request_responses["chatroom_user_count"]} online ]',
    ]
    
    # print modules with counter and get choice
    
    while True:
        
        # print randomly coloured and aligned banner
    
        cls(); print(align(clr(banner,4) + f"\n{white}s i r {magenta}. {white}d a n k {magenta}<3\n"))
        
        counter = 1; modules_to_print = ""
        for module in modules: modules_to_print += f"\n    {counter} > {module}"; counter += 1
        print(clr(f"\n  - Stats: {stats}\n\n  - Modules: {clr('DEBUG MODE ENABLED',2) if development_version else ''}\n{modules_to_print}\n"))
        
        choice = input(clr("  - Choice: ") + magenta)
        if choice.isdigit() and int(choice) >= 1 and int(choice) <= int(len(modules)):
            choice = modules[int(choice)-1]; break
        
        elif choice == 'debug': # debug menu
            cls()
            while True:
                # this variable is long to prevent it from being changed!
                cmd_to_be_executed = input(clr("\n  > ") + white)
                if cmd_to_be_executed == 'exit': break
                try: exec(cmd_to_be_executed)
                except: print(clr("\n" + err(sys.exc_info()), 2))
        
        else: rm_line()

    try:
    
        if "Minecraft Server Builder" in choice: project, discord_rpc_state = "dank.minecraft-server-builder", "building a minecraft server"
        elif "Minecraft Server Scanner" in choice: project, discord_rpc_state = "dank.minecraft-server-scanner", "scanning for minecraft servers"
        elif "Software Downloader" in choice: project, discord_rpc_state = "dank.downloader", "bulk downloading software"
        elif "SpotX" in choice: project, discord_rpc_state = "dank.spotify", "installing SpotX and Spicetify"
        elif "Auto Clicker" in choice: project, discord_rpc_state = "_dank.auto-clicker", "running auto-clicker"
        elif "Browser Backup" in choice: project, discord_rpc_state = "dank.browser-backup", "backing up a browser"
        elif "Chatroom" in choice: project, discord_rpc_state = "dank.chatroom", "messaging in the chatroom"
        elif "Fusion-Fall" in choice: project, discord_rpc_state = "dank.fusion-fall", "modding Fusion-Fall"
        # elif "Analyze suspicious file" in choice: project = "dank.virus-total"
        # elif "Sussy Optimiser" in choice: project = "dank.sussy-optimiser"
        # elif "HWID Spoofer" in choice: project = "dank.hwid-spoofer"
        # elif "Temp File Cleaner" in choice: project = "dank.temp-cleaner"
        # elif "Software Updater" in choice: project = "dank.software-updater"
        else: project, discord_rpc_state = "404", "404"
        
        # get src from github if not dev_ver else get src locally

        if not development_version: # development_version defined in executor.py
            while True:
                try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/main/__modules__/{project}.py", headers=headers).content.decode(); break
                except: input(clr(f"\n  > Failed to get code for {project}! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
        else:
            while True:
                try: code = open(f'__modules__/{project}.py', 'r', encoding='utf-8').read(); break
                except: input(clr(f"\n  > Failed to get code! Unable to read '__modules__/{project}.py'! Press [ENTER] to try again... ",2))

        # execute src
        
        if code == "404: Not Found": print(clr(f"\n  > {project} has not been released yet! Returning to menu in 5s...",2)); time.sleep(5)
        else:
            cls(); exec(code) #.replace("exec_mode = 'script'", "exec_mode = 'exe'").replace('exec_mode = "script"', 'exec_mode = "exe"')
            cls(); print(clr(f"\n  > {project} executed successfully! Returning to menu in 5s...")); time.sleep(5)

    except:

        err_message = err(sys.exc_info())
        print(clr(err_message, 2))
        #user_message = input(clr("\n  > Briefly explain what you were doing when this error occurred [ sent to the developer ]: ",2) + white)
        while True:
            try:
                #if user_message == "": content = f"```<--- 🚨 ---> Module: {choice}\n\n{err_message}```"
                #else: content = f"```<--- 🚨 ---> Module: {choice}\n\n{err_message}\n\n  > Message: {user_message}```"
                # > updated to custom url to prevent webhook spamming
                requests.post("https://dank-site.onrender.com/dank-tool-errors", headers=headers, data={"text": f"```<--- 🚨 ---> Module: {choice}\n\n{err_message}```"})
                break
            except: input(clr(f"\n  > Failed to post error report! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
        input(clr("\n  > Error Reported! If it is an OS error, Please run as admin and try again!\n\n  > If it is a logic error, it will be fixed soon!\n\n  > Press [ENTER] to EXIT... "))

