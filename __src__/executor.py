# [NOTE] executor.py is meant to be executed only as an executable, not as a python script!
# the below imports are not required by the executor.py but is required by dank.tool.py

from keyboard import press
from playsound import playsound
from win10toast import ToastNotifier
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Controller
from webbrowser import open_new_tab as web
from dankware import multithread, clr_banner, align, cls, clr, magenta, white, chdir, title, github_downloads

# required imports for executor.py

import os
import sys
import time
import requests
from packaging.version import parse

def main():
    
    # change directory to exe's location

    project = "dank.tool"
    current_version = "0.1"
    title(f"{project} [ initializing ]"); exec(chdir('exe'))
    print(clr(f"\n  > Version: {current_version}"))

    # get latest version

    while True:
        try:
            latest_version = requests.get(f"https://raw.githubusercontent.com/SirDank/{project}/main/__src__/executor_version.txt").content.decode()
            if "Not Found" in latest_version: latest_version = 0
            #else: latest_version = float(latest_version); break
            else: break
        except: wait = input(clr("\n  > Failed to check for an update! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))

    # version checker / updater: overwrites the existing executable with the latest one using the help of a batch script called dankware-updater.cmd which deletes itself upon completion!

    def download_latest():

        print(clr(f"\n  > Downloading {project}-latest.exe..."))
        while True:
            try: data = requests.get(f"https://github.com/SirDank/{project}/blob/main/{project}.exe?raw=true", allow_redirects=True).content; break
            except: wait = input(clr("\n  > Failed to download! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
        open(f"{project}-latest.exe","wb+").write(data); data = None
        open("dankware-updater.cmd","w+").write(f"@echo off\ntitle dankware-updater\ncolor 0d\ntimeout 3\ndel /F {project}.exe\nren {project}-latest.exe {project}.exe\nstart {project}.exe\ndel \"%~f0\" >nul 2>&1")
        print(clr("\n  > Downloaded!\n\n  > Starting in 3s..."))
        toast = ToastNotifier(); toast.show_toast("dank.tool", "Updating and restarting in 5s...", duration = 3, icon_path = "dankware.ico", threaded = False)
        time.sleep(3); os.system(f"start dankware-updater.cmd"); sys.exit()

    if parse(latest_version) > parse(current_version):
        choice = input(clr(f"\n  > Update Found: {latest_version}\n\n  > Download latest version? [ y / n ]: ")).lower()
        if choice == "y": download_latest()
    elif latest_version == current_version: print(clr(f"\n  > Latest Version!"))
    else: print(clr(f"\n  > Development Version!"))

    # get main src from github

    while True:
        try: code = requests.get(f"https://raw.githubusercontent.com/SirDank/{project}/main/__src__/{project}.py").content.decode(); break
        except: wait = input(clr("\n  > Failed to get src! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))

    # execute, catch errors if any

    time.sleep(3); title(project); cls()

    try: exec(code)
    except Exception as exp:

        cls(); exc_type, exc_obj, exc_tb = sys.exc_info()
        print(clr(f"\n  > Error: {str(exp)} | {exc_type} | Line: {exc_tb.tb_lineno}",2))
        print(clr(f"\n  > Please take a screenshot of this and post it on https://github.com/SirDank/{project}/issues/new"))
        print(clr("\n  > Opening in 3s..."))
        time.sleep(3); web(f"https://github.com/SirDank/{project}/issues/new")

        if not latest_version == current_version:
            choice = input(clr("\n  > Download latest version? [ y / n ]: ")).lower()
            if choice == "y": download_latest()

        wait = input(clr("\n  > Press [ENTER] to continue: "))

if __name__ == "__main__": main()
