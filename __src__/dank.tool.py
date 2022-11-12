import os
import sys
import time
import requests
from datetime import datetime
from win10toast import ToastNotifier
from dankware import clr_banner, align, cls, clr, magenta, white, chdir, title, sys_open, get_duration, multithread, err

toast = ToastNotifier()
toast.show_toast("SirDank:", "Thank you for using my tool <3\nShare it with your friends!", duration = 10, icon_path = f"{os.path.dirname(__file__)}\\dankware.ico", threaded = True)

# get commit date & time

def updated_on(url, dankware_module = True):

    if dankware_module: url = f"https://api.github.com/repos/SirDank/dank.tool/commits?path=__modules__/{url}.py&page=1&per_page=1"
    response = requests.get(url).json()
    if response == []: return f"[ unreleased ]"
    else:
        date, time = response[0]["commit"]["author"]["date"].split("T")
        date = date.split("-")
        time = time.replace("Z","").split(":")
        date_time_data = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
    
    return f"[ updated {get_duration(date_time_data, interval='dynamic')} ago ]"

# multithread requests

def get_request_responses(task_id):
    
    global request_responses
    
    # get global runs
    
    if task_id == 0: request_responses["dankware_runs"] = requests.get("https://api.countapi.xyz/get/dankware").json()['value']
    elif task_id == 1: request_responses["danktool_runs"] = requests.get("https://api.countapi.xyz/get/dank.tool").json()['value']
        
    # get updated on time
    
    elif task_id == 2: request_responses["dank.minecraft-server-builder"] = updated_on("dank.minecraft-server-builder")
    elif task_id == 3: request_responses["dank.minecraft-server-scanner"] = updated_on("dank.minecraft-server-scanner")
    elif task_id == 4: request_responses["SpotX-Win"] = updated_on("https://api.github.com/repos/SpotX-CLI/SpotX-Win/commits?path=Install.ps1&page=1&per_page=1",False)
    elif task_id == 5: request_responses["dank.auto-clicker"] = updated_on("dank.auto-clicker")

# main

while True:
    
    title("𝚍𝚊𝚗𝚔.𝚝𝚘𝚘𝚕"); exec_mode = "exe"; exec(chdir(exec_mode)); banner='\n     _             _                      _ \n    | |           | |     _              | |\n  _ | | ____ ____ | |  _ | |_  ___   ___ | |\n / || |/ _  |  _ \\| | / )|  _)/ _ \\ / _ \\| |\n( (_| ( ( | | | | | |< ( | |_| |_| | |_| | |\n \\____|\\_||_|_| |_|_| \\_|_)___)___/ \\___/|_|\n'
    discord_rpc_state = "on the main menu"
    
    # multithread requests
        
    request_responses = {}
    while True:
        try: multithread(get_request_responses, 100, [ _ for _ in range(6) ], progress_bar=False); break
        except: input(clr(f"\n  > Failed to get request responses! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))

    while True:
        
        # print randomly coloured and aligned banner
        
        cls(); print(align(clr_banner(banner) + f"\n{white}s i r {magenta}. {white}d a n k {magenta}<3"))
        
        # global runs
        
        stats = f"\n\n    > Global dankware runs: {request_responses['dankware_runs']}\n\n    > Global dank.tool runs: {request_responses['danktool_runs']}"
            
        # available modules
        
        modules = [
            f'Minecraft Server Builder {request_responses["dank.minecraft-server-builder"]}',
            f'Minecraft Server Scanner {request_responses["dank.minecraft-server-scanner"]}',
            f'Spotify Ad Blocker {request_responses["SpotX-Win"]}',
            f'Auto Clicker {request_responses["dank.auto-clicker"]}',
            'Software Downloader [ UNFINISHED ]',
        ]
        
        # print modules with counter and get choice
        
        counter = 1; modules_to_print = ""
        for module in modules: modules_to_print += f"\n\n    {counter} > {module}"; counter += 1
        choice = input(clr(f"\n  - Stats: {stats}\n\n  - Modules: {modules_to_print}\n\n  - Choice: ") + magenta)
        if choice.isdigit() and int(choice) > 0 and int(choice) < int(len(modules))+1:
            choice = modules[int(choice)-1]; break
        
        # debug menu
        
        elif choice == 'debug':
            cls()
            while True:
                # this variable is long to prevent being changed!
                cmd_to_be_executed = input(clr("\n  > ") + white)
                if cmd_to_be_executed == 'exit': break
                try: exec(cmd_to_be_executed)
                except: print(clr("\n" + err(sys.exc_info()), 2))

    try:
    
        if "Minecraft Server Builder" in choice: project = "dank.minecraft-server-builder"; discord_rpc_state = "building a minecraft server"
        elif "Minecraft Server Scanner" in choice: project = "dank.minecraft-server-scanner"; discord_rpc_state = "scanning for minecraft servers"
        elif "Software Downloader" in choice: project = "dank.downloader"; discord_rpc_state = "bulk downloading software"
        elif "Spotify Ad Blocker" in choice: project = "dank.spotx-windows"; discord_rpc_state = "disabling ads on spotify"
        elif "Auto Clicker" in choice: project = "dank.auto-clicker"; discord_rpc_state = "running auto-clicker"
        # elif "Analyze suspicious file" in choice: project = "dank.virus-total"
        # elif "Sussy Optimiser" in choice: project = "dank.sussy-optimiser"
        # elif "HWID Spoofer" in choice: project = "dank.hwid-spoofer"
        # elif "Temp File Cleaner" in choice: project = "dank.temp-cleaner"
        else: project = "404"
        
        # get src from github if not dev_ver else locally

        if not development_version: # development_version defined in executor.py
            while True:
                try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/main/__modules__/{project}.py").content.decode(); break
                except: input(clr(f"\n  > Failed to get src for {project}! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
        else:
            while True:
                try: code = open(f'__modules__/{project}.py', 'r', encoding='utf-8').read(); break
                except: input(clr(f"\n  > Failed to get src! Unable to read '__modules__/{project}.py'! Press [ENTER] to try again... ",2))

        # execute src
        
        if code == "404: Not Found": print(clr(f"\n  > {project} has not been released yet! Returning to menu in 5s...",2)); time.sleep(5)
        else:
            cls(); exec(code.replace("exec_mode = 'script'", "exec_mode = 'exe'").replace('exec_mode = "script"', 'exec_mode = "exe"'))
            cls(); print(clr(f"\n  > {project} executed successfully! Returning to menu in 5s...")); time.sleep(5)

    except:

        err_message = err(sys.exc_info())
        print(clr(err_message, 2))
        while True:
            try: requests.post("https://discord.com/api/webhooks/1038503148681179246/GkOrGGuK3mcYpx3OzDMyqCtcnWbx7cZqSK_PbyIkxIbjizPlmjcHFt2dlPhxSBLf2n38", json={"content": f"```<--- 🚨 ---> Module: {choice}\n\n{err_message}```"}); break
            except: input(clr(f"\n  > Failed to post error report! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
        print(clr("\n  > Error Reported! It will be fixed soon!"))
        input(clr("\n  > Press [ENTER] to EXIT..."))

