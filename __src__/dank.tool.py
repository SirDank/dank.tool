import sys
import time
import requests
from webbrowser import open_new_tab as web
from dankware import clr_banner, align, cls, clr, magenta, white, chdir, title

# main

while True:
    
    title("dank.tool"); exec(chdir('exe')); banner='\n     _             _                      _ \n    | |           | |     _              | |\n  _ | | ____ ____ | |  _ | |_  ___   ___ | |\n / || |/ _  |  _ \\| | / )|  _)/ _ \\ / _ \\| |\n( (_| ( ( | | | | | |< ( | |_| |_| | |_| | |\n \\____|\\_||_|_| |_|_| \\_|_)___)___/ \\___/|_|\n'

    while True: # choose module to execute
        cls(); print(align(clr_banner(banner) + f"\n{white}s i r {magenta}. {white}d a n k {magenta}<3")) # print randomly coloured and aligned banner
        modules = [
            'Minecraft Server Builder',
            'Software Downloader [UNFINISHED]'
        ]
        counter = 1; to_print = ""
        for module in modules: to_print += f"\n\n    {counter} > {module}"; counter += 1
        choice = input(clr(f"\n  - Modules: {to_print}\n\n  - Choice: ") + white)
        if choice.isdigit() and int(choice) > 0 and int(choice) < int(len(modules))+1: break

    choice = modules[int(choice)-1]

    try:
        if "Minecraft Server Builder" in choice: project = "dank.minecraft-server-builder"
        elif "Software Downloader" in choice: project = "dank.downloader"
        # elif "Instagram Ghostbuster" in choice: project = "dank.insta-tool"
        # elif "Chatbot" in choice: project = "dank.ai"
        # elif "Analyze suspicious file" in choice:
        # elif "Sussy Optimiser" in choice:
        # elif "HWID Spoofer" in choice:
        # elif "Discord Backup" in choice:
        # elif "Spotify Ad Blocker" in choice:
        # elif "Spotify Downloader" in choice:
        # elif "Youtube Video Downloader" in choice:
        # elif "Temp File Cleaner" in choice:
        else: project = "404"
        
        while True: # get src from github
            try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/main/__modules__/{project}.py").content.decode(); break
            except: wait = input(clr(f"\n  > Failed to get src for {project}! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
        
        if code == "404: Not Found": print(clr(f"\n  > {project} has not yet been released! Returning to menu in 5s...",2)); time.sleep(5)
        else:
            exec(code.replace("exec_mode = 'script'", 'exec_mode = "exe"').replace('exec_mode = "script"', 'exec_mode = "exe"'))
            cls(); print(clr(f"\n  > {project} executed successfully! Returning to menu in 5s...")); time.sleep(5)

    except Exception as exp:
        
        cls(); exc_type, exc_obj, exc_tb = sys.exc_info()
        print(clr(f"\n  > Error: {str(exp)} | {exc_type} | Line: {exc_tb.tb_lineno}",2))
        print(clr(f"\n  > Please take a screenshot of this and post it on > https://github.com/SirDank/dank.tool/issues/new"))
        print(clr("\n  > Opening in 3s..."))
        time.sleep(3); web("https://github.com/SirDank/dank.tool/issues/new")
        wait = input(clr(f"\n  > Press [ENTER] to continue: "))

