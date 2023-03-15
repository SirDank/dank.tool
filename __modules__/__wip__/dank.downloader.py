import os
import sys
import time
import requests
from keyboard import press; press('f11')
from pynput.keyboard import Key, Listener
from webbrowser import open_new_tab as web
from dankware import clr, cls , align, clr_banner, magenta, white, red, multithread

def banner_printer(banner): # print randomly coloured and aligned banner
    cls(); print(align(clr_banner(banner).replace('X',f"{white}s i r {magenta}. {white}d a n k {magenta}<3")))
    print(align(f"{white}/\ {magenta}and {white}\/ {magenta}to navigate{white}, [{magenta}space{white}] {magenta}to select{white}, [{magenta}backspace{white}] {magenta}to go back and {white}[{magenta}esc{white}] {magenta}to exit"))
    print(align(f"\n{magenta}Selected{white}: {magenta}{f'{white}, {magenta}'.join(selected_software)}\n\n"))

def list_printer():

    global software
    global selector_max
    banner_printer(banner)

    if current_category == "":

        for _ in range(selector_max):
            to_print = f"{white}{categories[_]}"
            if _ == selector:to_print = f"{magenta}> {to_print} {magenta}<"
            print(align(to_print) + "\n\n")
        
    else:
        
        if current_category == "Windows Essentials":
            software = [
                "Microsoft Activation Scripts [MAS]",
                "Win10 MediaCreationTool",
                "Win10 Debloat Scripts [Github]",
                "NVCleanstall",
                "Realtek HD Audio Driver"
                ]

        #lif current_category == "Windows Optimization":
        #    software = ["IOBIT Advanced System Care", "IOBIT Driver Booster", "IOBIT Uninstaller", "IOBIT Software Updater"]
        
        elif current_category == "Software":
            software = [
                "Adobe Creative Cloud",
                "Avast",
                "Battle.net",
                "Bitvise SSH Client",
                "Corsair iCUE",
                "CurseForge",
                "Discord",
                "Enigma Virtual Box",
                "Epic Games Launcher",
                "Feather Client",
                "Figma",
                "Firefox",
                "Git",
                "Github Desktop",
                "Google Chrome",
                "Java 8",
                "Logitech G HUB",
                "Lunar Client",
                "MegaSync",
                "Microsoft Activation Script",
                "Minecraft",
                "NVCleanstall",
                "Nahimic",
                "NetLimiter 4",
                "Netflix",
                "Notepad++",
                "Nvidia Control Panel",
                "OBS Studio",
                "Process Hacker",
                "Python 3.10",
                "QBittorrent",
                "Raspberry Pi Imager",
                "Realtek Audio Console",
                "Sandboxie Plus",
                "Spotify",
                "Steam",
                "TeamViewer",
                "Telegram",
                "Tor",
                "VLC Media Player",
                "VMware Workstation Pro",
                "VNC Viewer",
                "Virtualbox",
                "Visual Studio Code",
                "Whatsapp Desktop",
                "WinRAR 6 + Key",
                "WinSCP",
            ]

        elif current_category == "Dankware":
            software = ["dank.resourcepack", "spiral-knights-modpack", "Visit Github"]

        selector_max = len(software)
        for i in range(selector_max):

            to_print = f"{white}{software[i]}"
            if str(software[i]) in selected_software:to_print = f"{magenta}[ {to_print} {magenta}]"
            if i == selector:to_print = f"{magenta}> {to_print} {magenta}<"
            if not current_category == "Software":print(align(to_print) + "\n\n")
            else:print(align(to_print))

#def prepare_downloads(software):

def file_downloader(url, filename):
    try:open(filename,"wb+").write(s.get(url, allow_redirects=True).content); print(align(f"{magenta}> {white}{filename} {magenta}<\n"))
    except:print(align(f"{red}[ {filename} ]\n\n"))

def download_phase():

    start_time = time.time()
    multithread(prepare_downloads, 100, selected_software, progress_bar=False)
    time_taken = time.time() - start_time
    print("\n\n" + align(f"{magenta}[ {white}Done in {{0:.2f}}s {magenta}]").format(time_taken))
    print("\n\n" + align(f"{magenta}[ {white}Starting Multiple Downloads {magenta}]") + "\n\n")
    
    try:os.mkdir("dank.downloader")
    except:pass
    os.chdir("dank.downloader")

    start_time = time.time()
    multithread(file_downloader, 2, to_download_urls, to_download_filenames, progress_bar=False)
    time_taken = int( time.time() - start_time )
    print( "\n\n" + align(f"{magenta}[ {white}Finished All Downloads in {time_taken}s {magenta}]"))
    print( "\n\n" + align(f"{magenta}[ {white}Opening Tabs in 5s {magenta}]"))
    time.sleep(5)

    to_open_urls.append("https://allmylinks.com/sir-dankenstein")
    for url in to_open_urls:time.sleep(0.5); web(url)

    print( "\n\n" + align(f"{magenta}[ {white}Tasks Complete! {magenta}]"))
    os.system(f"explorer.exe \"dank.downloader\"")
    time.sleep(5); cls()
    return False

def on_press(key):
    pass

def on_release(key):
    
    global selector
    global selector_max
    global current_category
    global selected_software
    changes = False

    if key == Key.up:
        if selector > 0:selector -= 1; changes = True
    elif key == Key.down:
        if selector < selector_max-1:selector +=1; changes = True
    elif key == Key.space:
        if current_category == "":current_category = categories[selector]; selector = 0; changes = True
        else:
            if software[selector] in selected_software:selected_software.remove(software[selector]); changes = True
            else:selected_software.append(software[selector]); changes = True
    elif key == Key.backspace:current_category = ""; selector = 0; selector_max = len(categories); changes = True
    elif key == Key.esc:cls(); return False
    elif key == Key.enter:cls(); return False
    
    if current_category != "Download":
        if changes:list_printer()
    else:download_phase()

filepath = os.path.dirname(__file__) # as .py
#filepath = os.path.dirname(sys.argv[0]) # as .exe
os.chdir(filepath)
banner='\n     _             _          _                   _                 _             \n    | |           | |        | |                 | |               | |            \n  _ | | ____ ____ | |  _   _ | | ___  _ _ _ ____ | | ___   ____  _ | | ____  ____ \n / || |/ _  |  _ \\| | / ) / || |/ _ \\| | | |  _ \\| |/ _ \\ / _  |/ || |/ _  )/ ___)\n( (_| ( ( | | | | | |< ( ( (_| | |_| | | | | | | | | |_| ( ( | ( (_| ( (/ /| |    \n \\____|\\_||_|_| |_|_| \\_|_)____|\\___/ \\____|_| |_|_|\\___/ \\_||_|\\____|\\____)_|    \n                                                                                  \n                                                    X                    \n'
categories = ["Windows Essentials", "Software", "Start Download"]
selector = 0; selector_max = len(categories); current_category = ""
software, selected_software, to_download_filenames, to_download_urls, to_open_urls = ([], ) * 5
s = requests.Session()
list_printer()

# Collect events until released

with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()