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

def updated_on(module):

    date, time = session.get(f"https://api.github.com/repos/SirDank/dank.tool/commits?path=__modules__/{module}.py&page=1&per_page=1").json()[0]["commit"]["author"]["date"].split("T")
    date = date.split("-")
    time = time.replace("Z","").split(":")
    date_time_data = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))

    duration = get_duration(date_time_data, interval='days')
    if duration == 0:
        duration = get_duration(date_time_data, interval='hours')
        if duration == 0:
            duration = get_duration(date_time_data, interval='minutes')
            if duration == 0:
                duration = get_duration(date_time_data, interval='seconds')
                return f"{duration} seconds"
            elif duration == 1: return f"{duration} minute"
            else: return f"{duration} minutes"
        elif duration == 1: return f"{duration} hour"
        else: return f"{duration} hours"
    elif duration == 1: return f"{duration} day"
    else: return f"{duration} days"

# main

while True:
    
    title("dank.tool"); exec_mode = "exe"; exec(chdir(exec_mode)); banner='\n     _             _                      _ \n    | |           | |     _              | |\n  _ | | ____ ____ | |  _ | |_  ___   ___ | |\n / || |/ _  |  _ \\| | / )|  _)/ _ \\ / _ \\| |\n( (_| ( ( | | | | | |< ( | |_| |_| | |_| | |\n \\____|\\_||_|_| |_|_| \\_|_)___)___/ \\___/|_|\n'

    while True: # choose module to execute
        cls(); print(align(clr_banner(banner) + f"\n{white}s i r {magenta}. {white}d a n k {magenta}<3")) # print randomly coloured and aligned banner
        modules = [
            f'Minecraft Server Builder [ updated {updated_on("dank.minecraft-server-builder")} ago ]',
            f'Minecraft Server Scanner [ updated {updated_on("dank.minecraft-server-scanner")} ago ]',
            f'Spotify Ad Blocker [ updated {updated_on("dank.spotx-windows")} ago ]',
            'Software Downloader [ UNFINISHED ]',
        ]
        counter = 1; to_print = ""
        for module in modules: to_print += f"\n\n    {counter} > {module}"; counter += 1
        choice = input(clr(f"\n  - Modules: {to_print}\n\n  - Choice: ") + magenta)
        if choice.isdigit() and int(choice) > 0 and int(choice) < int(len(modules))+1:
            choice = modules[int(choice)-1]; break
        elif choice == 'debug':
            cls()
            while True:
                cmd = input(clr("\n  > ") + white)
                if cmd == 'exit': break
                try: exec(cmd)
                except Exception as exc: print(clr(f"\n  > ERROR: {exc}",2))

    try:
        if "Minecraft Server Builder" in choice: project = "dank.minecraft-server-builder"
        elif "Minecraft Server Scanner" in choice: project = "dank.minecraft-server-scanner"
        elif "Software Downloader" in choice: project = "dank.downloader"
        elif "Spotify Ad Blocker" in choice: project = "dank.spotx-windows"
        # elif "Spotify Downloader" in choice:
        # elif "Instagram Ghostbuster" in choice: project = "dank.insta-tool"
        # elif "Chatbot" in choice: project = "dank.ai"
        # elif "Analyze suspicious file" in choice:
        # elif "Sussy Optimiser" in choice:
        # elif "HWID Spoofer" in choice:
        # elif "Discord Backup" in choice:
        # elif "Youtube Video Downloader" in choice:
        # elif "Temp File Cleaner" in choice:
        else: project = "404"
        
        while True: # get src from github
            try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/main/__modules__/{project}.py").content.decode(); break
            except: wait = input(clr(f"\n  > Failed to get src for {project}! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
        
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
        wait = input(clr(f"\n  > Press [ENTER] to continue: "))

