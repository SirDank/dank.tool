import os
import sys
import time
import requests
from webbrowser import open_new_tab as web
from dankware import clr_banner, align, cls, clr, magenta, white, chdir

def get_src(project): # get src from github
    while True:
        try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/dank.tool/main/__modules__/{project}.py").content.decode(); break
        except: wait = input(clr(f"\n  > Failed to get src for {project}! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
    return code

def main(): # choose module to execute
    
    exec(chdir('exe'))

    #banner='\n     _             _                      _ \n    | |           | |     _              | |\n  _ | | ____ ____ | |  _ | |_  ___   ___ | |\n / || |/ _  |  _ \\| | / )|  _)/ _ \\ / _ \\| |\n( (_| ( ( | | | | | |< ( | |_| |_| | |_| | |\n \\____|\\_||_|_| |_|_| \\_|_)___)___/ \\___/|_|\n                                            \n\n'
    banner='\n     _             _                      _ \n    | |           | |     _              | |\n  _ | | ____ ____ | |  _ | |_  ___   ___ | |\n / || |/ _  |  _ \\| | / )|  _)/ _ \\ / _ \\| |\n( (_| ( ( | | | | | |< ( | |_| |_| | |_| | |\n \\____|\\_||_|_| |_|_| \\_|_)___)___/ \\___/|_|\n                                            \n                    X      \n'

    while True:
        cls(); print(align(clr_banner(banner).replace('X',f"{white}s i r {magenta}. {white}d a n k {magenta}<3"))) # print randomly coloured and aligned banner
        modules = [
            'Software Downloader [UNFINISHED]',
            'Minecraft Paper Server Builder [UNFINISHED]'
        ]
        counter = 1; to_print = ""
        for module in modules: to_print += f"\n\n  {counter} > {module}"; counter += 1
        choice = input(clr(f"Modules: {to_print}\n\nChoice: "))
        if choice.isdigit() and int(choice) > 0 and int(choice) < int(len(modules))+1: break
    
    choice = modules[int(choice)-1]
 
    try:
        if choice == "Software Downloader": project = "dank.downloader"
        elif choice == "Minecraft Paper Server Builder": project = "dank.server-builder"
        # elif choice == "Instagram Ghostbuster": project = "dank.insta-tool"
        # elif choice == "Chatbot": project = "dank.ai"
        # elif choice == "Analyze suspicious file":
        # elif choice == "Sussy Optimiser":
        # elif choice == "HWID Spoofer":
        # elif choice == "Discord Backup":
        # elif choice == "Spotify Ad Blocker":
        # elif choice == "Spotify Downloader":
        # elif choice == "Youtube Music Downloader":
        # elif choice == "Youtube Video Downloader":
        # elif choice == "Temp File Cleaner":
        code = get_src(project)
        if code == "404: Not Found": print(clr(f"  > {project} has not yet been released! Returning to menu in 5s...",2)); time.sleep(5)
        else: exec(code); cls(); print(clr(f"\n  > {project} executed successfully! Returning to menu in 5s...")); time.sleep(5)

    except Exception as exp:
        
        cls(); exc_type, exc_obj, exc_tb = sys.exc_info()
        print(clr(f"\n  > Error: {str(exp)} | {exc_type} | Line: {exc_tb.tb_lineno}",2))
        print(clr(f"\n  > Please take a screenshot of this and post it on > https://github.com/SirDank/dank.tool/issues/new"))
        print(clr("\n  > Opening in 3s..."))
        time.sleep(3); web("https://github.com/SirDank/dank.tool/issues/new")
        wait = input(clr(f"\n  > Press [ENTER] to continue: "))

if __name__ == '__main__':
    while True: main()
