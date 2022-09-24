import os
import time
import requests
from dankware import title, rm_line, chdir, clr_banner, align, cls, clr, white, magenta, red, reset, github_downloads, multithread

# change dir and print banner

exec_mode = "script"
exec(chdir(exec_mode))
banner = "\n\n\n   _         _                                 _       _ _   _            ___ \n _| |___ ___| |_   ___ ___ ___ _ _ ___ ___ ___| |_ _ _|_| |_| |___ ___   |_  |\n| . | .'|   | '_|_|_ -| -_|  _| | | -_|  _|___| . | | | | | . | -_|  _|  |_  |\n|___|__,|_|_|_,_|_|___|___|_|  \\_/|___|_|     |___|___|_|_|___|___|_|    |___|\n"
read_me = '\n\n:::::::::  ::::::::::     :::     :::::::::       ::::    ::::  ::::::::::\n:+:    :+: :+:          :+: :+:   :+:    :+:      +:+:+: :+:+:+ :+:       \n+:+    +:+ +:+         +:+   +:+  +:+    +:+      +:+ +:+:+ +:+ +:+       \n+#++:++#:  +#++:++#   +#++:++#++: +#+    +:+      +#+  +:+  +#+ +#++:++#  \n+#+    +#+ +#+        +#+     +#+ +#+    +#+      +#+       +#+ +#+       \n#+#    #+# #+#        #+#     #+# #+#    #+#      #+#       #+# #+#       \n###    ### ########## ###     ### #########       ###       ### ##########\n\n\n'

def print_banner():
    cls(); print(align(clr_banner(banner) + f"\n{white}s i r {magenta}. {white}d a n k {magenta}<3\n\n"))

def print_read_me():
    cls(); print(align(read_me.replace(":",f"{reset}:").replace("+",f"{white}+").replace("#",f"{magenta}#")))

print_banner()

# get available papermc versions and print

while True:
    try:
        version_list = requests.get("https://papermc.io/api/v2/projects/paper/").json()['versions']
        print(clr(f'  > Available Paper Versions: {", ".join(version_list)}')); break
    except: wait = input(clr("\n  > Failed to get paper versions! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))

# user inputs [ name, version, ram, allow_cracked ]

name = input(clr("\n  > Server Name: ") + magenta)

print(""); success = False
while not success:
    version = input(clr("  > Version: ") + magenta)
    if version in version_list: success = True
    else: rm_line()

title(f"dank.serverbuilder [ {name} - {version} ]")

print("")
while True:
    cracked = input(clr("  > Allow Cracked Players [ y / n ]: ") + magenta).lower()
    if 'y' in cracked: cracked = True; break
    elif 'n' in cracked: cracked = False; break
    else: rm_line() # BROKEN

# setting max ram

print_read_me(); print(clr("\n  > When setting the Xms and Xmx values, if your host says you have 8000M memory, DO NOT USE 8000M! Minecraft (and Java) needs additional memory on top of that Xmx parameter. It is recommended to reduce your Xmx/Xms by about 1000-1500M to avoid running out of memory or \"OOMKiller\" hitting your server. This also leaves room for the Operating System to use memory too. Have 8000M memory? Use 6500M for safety. But you may also ask your host if they will cover this overhead for you and give you 9500M instead. Some hosts will! Just ask. We recommend using at least 6-10GB, no matter how few players! If you can't afford 10GB of memory, give as much as you can. However going out and getting 32GB of RAM for a server will only waste your money with minimal returns."))
print("")
while True:
    ram = input(clr("  > RAM in MB [ Leave 1500MB Free ]: ") + magenta)
    if ram.isdigit(): ram = int(ram); break
    else: rm_line()
if ram < 256: ram = 256

# hosting methods

print_read_me(); print(clr(f"\n  > Great! Now you need to pick a {magenta}host{white} for your mc server!\n\n  > If you are experienced and would like to skip playit.gg and use port-forwarding / alternative hosting methods, Choose {magenta}Option 1\n\n  > If you are new to hosting and would like to quickly host a server with playit.gg's tunnel without port-forwarding, Choose {magenta}Option 2"))

print("")
while True:
    playit = input(clr("  > Choice [ 1 / 2 ]: ") + magenta)
    if playit in ["1","2"]:
        if playit == "2": playit = True
        else: playit = False
        break
    else: rm_line()

# go to workspace

dir_name = name
try: os.mkdir(dir_name)
except:
    counter = 1
    while True:
        dir_name = name + f"_{counter}"
        try: os.mkdir(dir_name); break
        except: counter += 1
os.system(f'explorer.exe "{dir_name}"'); os.chdir(dir_name)

# create folders

for folder in ['world', 'world/datapacks', 'plugins', 'autoplug']:
    try: os.mkdir(folder)
    except: pass

# begin preparing downloads

cls(); print(clr("\n  > Preparing Downloads..."))

session = requests.Session()
to_download_urls, to_download_filenames = [], []

# github server-builder files

for file in ['server-icon.png', 'log4j2_17-111.xml', 'log4j2_112-116.xml', 'Clearlag.jar', 'mcMMO.jar', 'TreeAssist.jar', 'Iris.jar']: # Iris 2.3.2
    to_download_urls.append(f"https://github.com/SirDank/dank.tool/raw/main/__assets__/dank.minecraft-server-builder/{file}")
    if '.jar' in file: to_download_filenames.append(f"plugins/{file}")
    else: to_download_filenames.append(file)

# github plugins

def github_file_selector(url, mode, name_list, plugin = True):
    
    for file_url in github_downloads(f"https://api.github.com/repos/{url}/releases/latest"):
        if mode == "add": valid = False
        elif mode == "remove": valid = True
        for name in name_list:
            if name in file_url:
                if mode == "add": valid = True
                elif mode == "remove": valid = False
        if valid:
            to_download_urls.append(file_url)
            if plugin: to_download_filenames.append(f"plugins/{file_url.split('/')[-1]}")
            else: to_download_filenames.append(file_url.split('/')[-1])

# > EssentialsX
github_file_selector("EssentialsX/Essentials", "remove", ['AntiBuild', 'Discord', 'GeoIP', 'Protect', 'XMPP'])

# > ProtocolLib.jar
github_file_selector("dmulloy2/ProtocolLib", "add", ['ProtocolLib.jar'])

# > tabtps
github_file_selector("jpenilla/TabTPS", "add", ['spigot'])

# > BetterSleeping
github_file_selector("Nuytemans-Dieter/BetterSleeping", "add", ['BetterSleeping'])
# github_file_selector("Nuytemans-Dieter/BetterSleeping", "remove", []) WORKS AS WELL!

# > ActionHealth
github_file_selector("zeshan321/ActionHealth", "add", ['ActionHealth'])
# github_file_selector("zeshan321/ActionHealth", "remove", []) WORKS AS WELL!

# > SkinRestorer
github_file_selector("SkinsRestorer/SkinsRestorerX", "add", ['SkinsRestorer'])
# github_file_selector("SkinsRestorer/SkinsRestorerX", "remove", []) WORKS AS WELL!

# > PlayerNPC API
github_file_selector("SergiFerry/PlayerNPC", "add", ['PlayerNPC'])
# github_file_selector("SergiFerry/PlayerNPC", "remove", []) WORKS AS WELL!

# > playit.gg tunnel prorgram
if playit: github_file_selector("playit-cloud/playit-agent", "remove", ['apple-intel', 'apple-m1', 'unsigned', 'dmg'], False)

# > AutoPlug
to_download_urls.append("https://github.com/Osiris-Team/AutoPlug-Releases/raw/master/stable-builds/AutoPlug-Client.jar")
to_download_filenames.append("AutoPlug-Client.jar")

# > paper.jar
paper_build = session.get(f"https://papermc.io/api/v2/projects/paper/versions/{version}").json()['builds'][-1]
to_download_urls.append(f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds/{paper_build}/downloads/paper-{version}-{paper_build}.jar")
to_download_filenames.append("paper.jar")

# begin downloads

print(clr("\n  > Starting Multiple Downloads... [ this might take a few seconds ]"))

def downloader(url, filename):
    
    while True:
        try:
            data = requests.get(url, allow_redirects=True).content
            open(filename,"wb").write(data); data = ""
            print(clr(f"\n  > Completed [ {filename} ]")); break
        except: wait = input(clr(f"\n  > Failed [ {filename} ]! Press {white}ENTER{red} to try again!",2))

start_time = time.time()
multithread(downloader, 2, to_download_urls, to_download_filenames, False)
time_taken = int(time.time()-start_time)

cls(); print(clr(f"\n  > Finished downloads in {magenta}{time_taken}{white} seconds! Sleeping 5 seconds...")); time.sleep(5)

# creating local files

cls(); print(clr("\n  > Creating local files..."))

open('eula.txt','w+').write('eula=true')

if version in ["1.17", "1.18"]: extra_flag = "-Dlog4j2.formatMsgNoLookups=true "
elif version in ["1.12", "1.13", "1.14", "1.15", "1.16"]: extra_flag = "-Dlog4j.configurationFile=log4j2_112-116.xml "
elif version in ["1.7", "1.8", "1.9", "1.10", "1.11"]: extra_flag = "-Dlog4j.configurationFile=log4j2_17-111.xml "
else: extra_flag = ""

open('start_server.cmd', 'w+').write(f'''@echo off
title Minecraft Server Console [ {name} - {version} ]
java -jar AutoPlug-Client.jar
''')

open('start_server.sh', 'wb+').write(f'''
#!/bin/sh
java -jar AutoPlug-Client.jar
'''.encode().replace(b'\r\n',b'\n'))

open('autoplug/general.yml', 'w+').write(f'''
general: 
  autoplug: 
    target-software: MINECRAFT_SERVER
    start-on-boot: false
    system-tray: 
      enable: false
  server: 
    start-command: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true {extra_flag}-jar paper.jar -nogui
''')

# WORKING: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true {extra_flag}-jar paper.jar -nogui
# BROKEN: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -Dterminal.jline=false -Dterminal.ansi=true -XX:+UnlockDiagnosticVMOptions -XX:-UseBiasedLocking -XX:UseAVX=3 -XX:+UseStringDeduplication -XX:+UseFastUnorderedTimeStamps -XX:+UseAES -XX:+UseAESIntrinsics -XX:UseSSE=4 -XX:+UseFMA -XX:AllocatePrefetchStyle=1 -XX:+UseLoopPredicate -XX:+RangeCheckElimination -XX:+EliminateLocks -XX:+DoEscapeAnalysis -XX:+UseCodeCacheFlushing -XX:+SegmentedCodeCache -XX:+UseFastJNIAccessors -XX:+OptimizeStringConcat -XX:+UseCompressedOops -XX:+UseThreadPriorities -XX:+OmitStackTraceInFastThrow -XX:+TrustFinalNonStaticFields -XX:ThreadPriorityPolicy=1 -XX:+UseInlineCaches -XX:+RewriteBytecodes -XX:+RewriteFrequentPairs -XX:+UseNUMA -XX:-DontCompileHugeMethods -XX:+UseFPUForSpilling -XX:+UseFastStosb -XX:+UseNewLongLShift -XX:+UseVectorCmov -XX:+UseXMMForArrayCopy -XX:+UseXmmI2D -XX:+UseXmmI2F -XX:+UseXmmLoadAndClearUpper -XX:+UseXmmRegToRegMoveAll -Dfile.encoding=UTF-8 -Xlog:async -Djava.security.egd=file:/dev/urandom --add-modules jdk.incubator.vector {extra_flag}-jar paper.jar -nogui

open('autoplug/updater.yml', 'w+').write(f'''
updater: 
  java-updater: 
    enable: true
    profile: AUTOMATIC
    version: 17
  server-updater: 
    enable: true
    profile: AUTOMATIC
    software: paper
    version: {version}
  plugins-updater: 
    enable: true
    profile: AUTOMATIC
  mods-updater: 
    enable: true
    profile: AUTOMATIC
''')

open('autoplug/plugins.yml', 'w+').write('''
plugins: 
  general: 
    keep-removed: false
  ActionHealth: 
    exclude: false
    spigot-id: 2661
    alternatives: 
      github: 
        repo-name: zeshan321/ActionHealth
        asset-name: ActionHealth
  EssentialsChat: 
    alternatives: 
      github: 
        repo-name: EssentialsX/Essentials
        asset-name: EssentialsXChat
      jenkins: 
        project-url: https://ci.ender.zone/job/EssentialsX/
        artifact-name: EssentialsXChat
  EssentialsSpawn: 
    alternatives: 
      github: 
        repo-name: EssentialsX/Essentials
        asset-name: EssentialsXSpawn
      jenkins: 
        project-url: https://ci.ender.zone/job/EssentialsX/
        artifact-name: EssentialsXSpawn
  mcMMO: 
    spigot-id: 64348
    custom-download-url: https://github.com/SirDank/dank.tool/raw/main/__assets__/dank.minecraft-server-builder/mcMMO.jar
  PlayerNPC: 
    spigot-id: 93625
  SkinsRestorer: 
    spigot-id: 2124
''')

# one-time setup

if playit:

    for file in github_downloads("https://api.github.com/repos/playit-cloud/playit-agent/releases/latest"):
        if "signed" in file: playit_filename = str(file.split('/')[-1])
    open("start_tunnel.cmd","w+").write(f'@echo off\ntitle Minecraft Java Playit.gg Tunnel [ {name} - {version} ] Keep me running to allow players to join your server!\n{playit_filename}\npause')

    time.sleep(3); print_read_me(); print(clr(f"\n  > To allow players to connect to your server you first need to create a tunnel.\n\n  > Follow the steps on {magenta}imgur{white} and complete the one-time setup.\n\n  > If it does not open, please go to [ https://imgur.com/a/W30s7bw ] and [ https://playit.gg/manage ] manually.\n\n  > Opening in 10s..."))
    time.sleep(10); os.system("start https://imgur.com/a/W30s7bw")
    time.sleep(10); os.system("start https://playit.gg/manage")
    print(clr("\n  > To start your server, run start_server.cmd\n\n  > To start your tunnel so people can connect over the internet, run start_tunnel.cmd"))
    wait = input(clr("\n  > After you have read the above and created a tunnel, press [ ENTER ] "))
 
else:
    
    print(clr("\n  > As you have not selected playit.gg as a host, To allow players to connect to your server over the internet, follow this tutorial on port-forwarding."))
    if input(clr("\n  > Open port forwarding tutorial on youtube? [ y / n ]: ") + magenta).lower() == "y": os.system("start https://youtu.be/X75GbRaGzu8")

# start server and shutdown server

# done!

os.system(f"title dank.serverbuilder [ complete! ]")
complete = "\n\n\n\n ___  ___ _ ____   _____ _ __                 \n/ __|/ _ \\ '__\\ \\ / / _ \\ '__|                \n\\__ \\  __/ |   \\ V /  __/ |                   \n|___/\\___|_|    \\_/ \\___|_|                   \n\n                     _   _                    \n  ___ _ __ ___  __ _| |_(_) ___  _ __         \n / __| '__/ _ \\/ _` | __| |/ _ \\| '_ \\        \n| (__| | |  __/ (_| | |_| | (_) | | | |       \n \\___|_|  \\___|\\__,_|\\__|_|\\___/|_| |_|       \n\n                           _      _         _ \n  ___ ___  _ __ ___  _ __ | | ___| |_ ___  / \\\n / __/ _ \\| '_ ` _ \\| '_ \\| |/ _ \\ __/ _ \\/  /\n| (_| (_) | | | | | | |_) | |  __/ ||  __/\\_/ \n \\___\\___/|_| |_| |_| .__/|_|\\___|\\__\\___\\/   \n                    |_|                       \n\n"
cls(); print(align(clr_banner(complete)))
time.sleep(5); os.system("start https://allmylinks.com/sir-dankenstein")


