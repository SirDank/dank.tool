import os
import sys
import time
import requests
from datetime import datetime
from win10toast import ToastNotifier
from dankware import clr_banner, align, cls, clr, magenta, white, chdir, title, sys_open, get_duration

session = requests.Session()
toast = ToastNotifier()
toast.show_toast("SirDank:", "Thank you for using my tool <3\nShare it with your friends!", duration = 10, icon_path = f"{os.path.dirname(__file__)}\\dankware.ico", threaded = True)

# get commit date & time

def updated_on(url, dankware_module = True):
    
    while True:
        try:
            if dankware_module: url = f"https://api.github.com/repos/SirDank/dank.tool/commits?path=__modules__/{url}.py&page=1&per_page=1"
            response = session.get(url).json()
            if response == []: return f"[ unreleased ]"
            else:
                date, time = response[0]["commit"]["author"]["date"].split("T")
                date = date.split("-")
                time = time.replace("Z","").split(":")
                date_time_data = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
                break
        except: input(clr(f"\n  > Failed to get commit date & time! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))

    return f"[ updated {get_duration(date_time_data, interval='dynamic')} ago ]"

# main

while True:
    
    title("dank.tool"); exec_mode = "exe"; exec(chdir(exec_mode)); banner='\n     _             _                      _ \n    | |           | |     _              | |\n  _ | | ____ ____ | |  _ | |_  ___   ___ | |\n / || |/ _  |  _ \\| | / )|  _)/ _ \\ / _ \\| |\n( (_| ( ( | | | | | |< ( | |_| |_| | |_| | |\n \\____|\\_||_|_| |_|_| \\_|_)___)___/ \\___/|_|\n'
    discord_rpc_state = "on the main menu"

    while True:
        
        # print randomly coloured and aligned banner
        
        cls(); print(align(clr_banner(banner) + f"\n{white}s i r {magenta}. {white}d a n k {magenta}<3"))

        # get global runs
        
        while True:
            try:
                dankware_runs = session.get("https://api.countapi.xyz/get/dankware").json()['value']
                danktool_runs = session.get("https://api.countapi.xyz/get/dank.tool").json()['value']
                stats = f"\n\n    > Global dankware runs: {dankware_runs}\n\n    > Global dank.tool runs: {danktool_runs}"
                break
            except: input(clr(f"\n  > Failed to get runs! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
            
        # available modules
        
        modules = [
            f'Minecraft Server Builder {updated_on("dank.minecraft-server-builder")}',
            f'Minecraft Server Scanner {updated_on("dank.minecraft-server-scanner")}',
            f'Spotify Ad Blocker {updated_on("https://api.github.com/repos/SpotX-CLI/SpotX-Win/commits?path=Install.ps1&page=1&per_page=1",False)}',
            f'Auto Clicker {updated_on("dank.auto-clicker")}',
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
                except Exception as exc: print(clr(f"\n  > ERROR: {exc}",2))

    try:
    
        if "Minecraft Server Builder" in choice: project = "dank.minecraft-server-builder"; discord_rpc_state = "building a minecraft server"
        elif "Minecraft Server Scanner" in choice: project = "dank.minecraft-server-scanner"; discord_rpc_state = "scanning for minecraft servers"
        elif "Software Downloader" in choice: project = "dank.downloader"; discord_rpc_state = "bulk downloading software"
        elif "Spotify Ad Blocker" in choice: project = "dank.spotx-windows"; discord_rpc_state = "disabling ads on spotify"
        elif "Auto Clicker" in choice: project = "dank.auto-clicker"; discord_rpc_state = "running auto-clicker"
        # elif "Spotify Downloader" in choice: project = "dank.spotiflyer"
        # elif "Instagram Ghostbuster" in choice: project = "dank.insta-tool"
        # elif "Chatbot" in choice: project = "dank.ai"
        # elif "Analyze suspicious file" in choice: project = "dank.virus-total"
        # elif "Sussy Optimiser" in choice: project = "dank.sussy-optimiser"
        # elif "HWID Spoofer" in choice: project = "dank.hwid-spoofer"
        # elif "Discord Backup" in choice: project = "dank.discord-backup"
        # elif "Youtube Video Downloader" in choice: project = "dank.yt-downloader"
        # elif "Temp File Cleaner" in choice: project = "dank.temp-cleaner"
        else: project = "404"
        
        # get src from github if not dev_ver else locally

        if not development_version:
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

    except Exception as exp:
        
        cls(); exc_type, exc_obj, exc_tb = sys.exc_info()
        print(clr(f"\n  > Error: {str(exp)} | {exc_type} | Line: {exc_tb.tb_lineno}",2))
        print(clr(f"\n  > Please take a screenshot of this and post it on > https://github.com/SirDank/dank.tool/issues/new"))
        print(clr("\n  > Opening in 3s..."))
        time.sleep(3); sys_open("https://github.com/SirDank/dank.tool/issues/new")
        input(clr(f"\n  > Press [ENTER] to continue: "))

