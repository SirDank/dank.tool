import os
import sys
import time
import requests
import subprocess
from random import randint
from rich.align import Align
from rich.console import Console
from translatepy import Translator
from dankware import title, rm_line, cls, clr, github_file_selector, multithread, sys_open, err, get_path, white_bright, red

headers = {'User-Agent': ('dank.tool' if "DANK_TOOL_VERSION" not in os.environ else f'dank.tool {os.environ["DANK_TOOL_VERSION"]}'), 'Content-Type': 'application/json'}

# banners

def print_banner():
    cls()
    banner = "\n\n   _         _                                 _       _ _   _            ___ \n _| |___ ___| |_   ___ ___ ___ _ _ ___ ___ ___| |_ _ _|_| |_| |___ ___   |_  |\n| . | .'|   | '_|_|_ -| -_|  _| | | -_|  _|___| . | | | | | . | -_|  _|  |_  |\n|___|__,|_|_|_,_|_|___|___|_|  \\_/|___|_|     |___|___|_|_|___|___|_|    |___|\n\n\n"
    Console().print(Align.center(banner), style="blink red", highlight=False)

def print_read_me():
    cls()
    read_me = '\n\n:::::::::  ::::::::::     :::     :::::::::       ::::    ::::  ::::::::::\n:+:    :+: :+:          :+: :+:   :+:    :+:      +:+:+: :+:+:+ :+:       \n+:+    +:+ +:+         +:+   +:+  +:+    +:+      +:+ +:+:+ +:+ +:+       \n+#++:++#:  +#++:++#   +#++:++#++: +#+    +:+      +#+  +:+  +#+ +#++:++#  \n+#+    +#+ +#+        +#+     +#+ +#+    +#+      +#+       +#+ +#+       \n#+#    #+# #+#        #+#     #+# #+#    #+#      #+#       #+# #+#       \n###    ### ########## ###     ### #########       ###       ### ##########\n\n\n'
    read_me = read_me.replace(":", "[bright_white]:[/bright_white]").replace("+", "[bright_white]+[/bright_white]").replace("#", "[red]#[/red]")
    Console().print(Align.center(read_me), style='blink', highlight=False)

# translator

def translate(text):
    if DANK_TOOL_LANG:
        try: text = translator.translate(text, DANK_TOOL_LANG, 'en').result
        except: pass
    return text

def main_one():

    global name, version, cracked, install_Via, ram, motd_spaces, playit, extra_flag, dir_name, latest_java_version, translator, DANK_TOOL_LANG

    # check if translator is enabled (dank.tool.exe)

    try:
        DANK_TOOL_LANG = os.environ['DANK_TOOL_LANG']
        if DANK_TOOL_LANG == 'en':
            DANK_TOOL_LANG = ''
        else:
            translator = Translator()
    except:
        DANK_TOOL_LANG = ''

    title("𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚋𝚞𝚒𝚕𝚍𝚎𝚛")

    # change dir and print banner

    try: os.chdir(get_path('Desktop'))
    except:
        try: os.chdir(get_path('Documents'))
        except: os.chdir("C:\\")

    # install java if not installed

    while True:
        try:
            latest_java_version = "21"
            #latest_java_version = requests.get("https://api.adoptium.net/v3/info/available_releases", headers=headers, timeout=3).json()['most_recent_feature_release']
            break
        except Exception as exc:
            input(clr(f"\n  > {translate('Failed to get latest java version!')} {exc} | {translate('Press [ ENTER ] to try again')}... ",2))
            rm_line(); rm_line()

    try:
        subprocess.run(['java', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print_read_me()
        if input(clr(f"\n  - {translate('Java is not installed!')}\n\n  > {translate(f'Install Adoptium JRE {latest_java_version}?')} [ y / n ]: ") + red).lower() == 'y':
            print()
            os.system(f"winget install EclipseAdoptium.Temurin.{latest_java_version}.JRE")

    print_banner()

    # get available purpur versions and print

    while True:
        try:
            version_list = requests.get("https://api.purpurmc.org/v2/purpur", headers=headers, timeout=3).json()['versions']
            print(clr(f'  - {translate("Available Purpur Versions")}: {", ".join(version_list)}')); break
        except Exception as exc:
            input(clr(f"\n  > {translate(f'Failed to get purpur versions! {exc} | Press [ ENTER ] to try again')}... ",2))
            rm_line(); rm_line()

    # user inputs

    print("")
    while True:
        version = input(clr(f"  > {translate('Version')}: ") + red)
        if version in version_list: break
        rm_line()

    max_motd_len = 49
    used_motd_len = 10
    print("")
    while True:
        name = input(clr(f"  > {translate('Server Name')}: ") + red)
        if not len(name) > (max_motd_len - used_motd_len): break
        rm_line()
    motd_spaces = ' '*int((max_motd_len - used_motd_len - len(name))/4)

    title(f"𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚋𝚞𝚒𝚕𝚍𝚎𝚛 [ {name} - {version} ]")

    print("")
    while True:
        cracked = input(clr(f"  > {translate('Allow Cracked Players?')} [ y / n ]: ") + red).lower()
        match cracked:
            case 'y': cracked = True; break
            case 'n': cracked = False; break
        rm_line()

    string = translate('The following plugins allow older / newer clients to join your server')
    print_read_me(); print(clr(f"\n  - {string}!"))
    print("")
    while True:
        install_Via = input(clr(f"  > {translate('Download ViaVersion & ViaBackwards?')} [ y / n ]: ") + red).lower()
        match install_Via:
            case 'y': install_Via = True; break
            case 'n': install_Via = False; break
        rm_line()

    # setting extra flags

    patched = False

    for _ in ("1.17", "1.18"):
        if version.startswith(_):
            extra_flag = "-Dlog4j2.formatMsgNoLookups=true "
            patched = True
            break

    if not patched:
        for _ in ("1.12", "1.13", "1.14", "1.15", "1.16"):
            if version.startswith(_):
                extra_flag = "-Dlog4j.configurationFile=log4j2_112-116.xml "
                patched = True
                break

    if not patched:
        for _ in ("1.7", "1.8", "1.9", "1.10", "1.11"):
            if version.startswith(_):
                extra_flag = "-Dlog4j.configurationFile=log4j2_17-111.xml "
                patched = True
                break

    if not patched:
        extra_flag = ""

    # setting max ram

    string = translate('When setting the Xms and Xmx values, if your host says you have 8000M memory, DO NOT USE 8000M! Minecraft (and Java) needs additional memory on top of that Xmx parameter. It is recommended to reduce your Xmx/Xms by about 1000-1500M to avoid running out of memory or "OOMKiller" hitting your server. This also leaves room for the Operating System to use memory too. Have 8000M memory? Use 6500M for safety. But you may also ask your host if they will cover this overhead for you and give you 9500M instead. Some hosts will! Just ask. We recommend using at least 6-10GB, no matter how few players! If you cannot afford 10GB of memory, give as much as you can. However going out and getting 32GB of RAM for a server will only waste your money with minimal returns.')
    print_read_me(); print(clr(f"\n  - {string}"))
    print("")
    while True:
        ram = input(clr("  > RAM in MB [ Leave 1500MB Free ]: ") + red)
        if ram.isdigit(): ram = int(ram); break
        rm_line()
    ram = max(ram, 256)

    # use playit.gg

    print_read_me(); print(clr(f"\n  - {translate('Great! Now you need to pick a host for your mc server!')}\n\n  - {translate('If you are new to hosting and would like to quickly host a server with the playit.gg plugin without port-forwarding')}\n  - {translate('Choose Option 1')}\n\n  - {translate('If you are experienced and would like to skip playit.gg and use port-forwarding or alternative hosting methods')}\n  - {translate('Choose Option 2')}"))

    print("")
    while True:
        playit = input(clr("  > Choice [ 1 / 2 ]: ") + red)
        if playit in ("1","2"):
            playit = bool(playit == "1")
            break
        rm_line()

    # create and go to workspace

    if os.path.exists(name):
        counter = 2
        dir_name = f"{name}_{counter}"
        while os.path.exists(dir_name):
            counter += 1
            dir_name = f"{name}_{counter}"
    else:
        dir_name = name
    os.makedirs(dir_name)
    os.system(f'explorer.exe "{dir_name}"')
    os.chdir(dir_name)

    # create folders

    for folder in (
        'autoplug',
        'world/datapacks',
        'world_nether/datapacks',
        'world_the_end/datapacks',
        'plugins/BetterStructures/imports',
        'plugins/BetterStructures/schematics/default',
        'plugins/BetterStructures/schematics/exploration',
        'plugins/BetterStructures/schematics/BetterStructures Free Elite Shrines',
        'plugins/BetterStructures/elitemobs/powers/BetterStructures Free Elite Shrines',
        'plugins/BetterStructures/elitemobs/customitems/BetterStructures Free Elite Shrines',
        'plugins/BetterStructures/elitemobs/custombosses/BetterStructures Free Elite Shrines',
        'plugins/EliteMobs/imports'):
        try: os.makedirs(folder)
        except: pass

    # begin preparing downloads

    cls(); print(clr(f"\n  - {translate('Preparing Downloads...')}"))
    to_download_urls, to_download_file_names = [], []
    url = "https://github.com/SirDank/dank.tool/raw/main/__assets__/dank.minecraft-server-builder"

    # github server-builder files and plugins

    for file in ['server-icon.png']:
        to_download_urls.append(f"{url}/{file}")
        to_download_file_names.append(file)

    if extra_flag:
        for file in ('log4j2_17-111.xml', 'log4j2_112-116.xml'):
            to_download_urls.append(f"{url}/{file}")
            to_download_file_names.append(file)

    for file in ('BetterStructures Default Pack.zip', 'BetterStructures Exploration Pack.zip', 'BetterStructures Free Elite Shrines Pack.zip'):
        to_download_urls.append(f"{url}/{file}")
        to_download_file_names.append(f"plugins/BetterStructures/imports/{file}")

    for file in ('Adventurers_Guild.zip', 'em_dark_cathedral.zip', 'em_enchantment_sanctums_free.zip', 'em_events_craftenmines_creations.zip', 'em_fireworks.zip', 'em_hallosseum.zip', 'em_id_the_cave.zip', 'em_id_the_climb.zip', 'em_id_the_mines.zip', 'em_knights_castle_v6.zip', 'em_north_pole.zip', 'em_sewers.zip', 'em_shadow_of_the_binder_of_worlds.zip', 'em_the_binder_of_worlds.zip', 'em_the_steamworks.zip'):
        to_download_urls.append(f"{url}/{file}")
        to_download_file_names.append(f"plugins/EliteMobs/imports/{file}")

    # spigot / bukkit plugins

    spigot_plugins = {
        #"dankchatroom": 112398, Needs to be updated
        #"ActionHealth": 2661,
        "BetterSleeping": 60837,
        "BloodEffect": 90955,
        "BloodFading": 99263,
        "ChestSort": 59773,
        #"Chunky": 81534,
        #"Corpses": 96774, # breaks on latest # disabled config
        #"NeoPerformance": 103183, # removed from spigot? # disabled config
        "PLayerNPC": 93625,
        "ProtocolLib": 1997,
        "SkinRestorer": 2124,
        "Spark": 57242,
        "TabTPS": 82528,
        #"TreeAssist": 67436,
        #"SmoothTimber": 39965,
        #"LevelledMobs": 74304, # scaling needs to be improved
        "PlayTime": 26016,
        "PlaceholderAPI": 6245,
        "LuckyBlock-NTD": 92026,
        #"Multiverse-Core": 390,
        "BetterRTP": 36081,
        "ChatFeelings": 12987,
        "BetterStructures": 103241,
        "EliteMobs": 40090,
        "SilkSpawners": 60063,
        "FancyPhysics": 110500
    }

    bukkit_plugins = [
        "worldguard"
    ]

    if extra_flag:
        spigot_plugins["Log4JExploitFix"] = 98243
    if playit:
        spigot_plugins["playit-gg"] = 105566
    if install_Via:
        spigot_plugins["ViaVersion"] = 19254
        spigot_plugins["ViaBackwards"] = 27448

    for plugin, id in spigot_plugins.items():
        to_download_urls.append(f"https://api.spiget.org/v2/resources/{id}/download")
        to_download_file_names.append(f"plugins/{plugin}.jar")

    for plugin in bukkit_plugins:
        to_download_urls.append(f"https://dev.bukkit.org/projects/{plugin}/files/latest")
        to_download_file_names.append(f"plugins/{plugin}.jar")

    # github plugins

    file_urls = github_file_selector("EssentialsX/Essentials", "remove", ['AntiBuild', 'Discord', 'GeoIP', 'Protect', 'XMPP']) \
              + github_file_selector("IntellectualSites/FastAsyncWorldEdit", "add", ['FastAsyncWorldEdit']) \
              #+ github_file_selector("XZot1K/PhysicsToGo", "add", ['PhysicsToGo']) \
              #+ github_file_selector("SirDank/Iris-AutoCompile", "add", ['Iris']) \
              #+ github_file_selector("SirDank/Adapt-AutoCompile", "add", ['Adapt']) \
              #+ github_file_selector("MediumCraft/mcMMO", "remove", ['original']) \
              #+ github_file_selector("jpenilla/TabTPS", "add", ['tabtps-spigot']) \

    for file_url in file_urls:
        to_download_urls.append(file_url)
        to_download_file_names.append(f"plugins/{file_url.split('/')[-1]}")

    # - MCAntiMalware.jar
    for file_url in github_file_selector("OpticFusion1/MCAntiMalware", "add", ['MCAntiMalware']):
        to_download_urls.append(file_url)
        to_download_file_names.append(file_url.split('/')[-1])

    # - AutoPlug
    to_download_urls.append("https://github.com/Osiris-Team/AutoPlug-Releases/raw/master/stable-builds/AutoPlug-Client.jar")
    to_download_file_names.append("AutoPlug-Client.jar")

    # - purpur.jar
    to_download_urls.append(f"https://api.purpurmc.org/v2/purpur/{version}/latest/download")
    to_download_file_names.append("purpur.jar")

    def file_downloader(url, file_name):
        while True:
            try:
                response = requests.get(url, headers=headers, timeout=3, allow_redirects=True)
                data = response.content
                try: size = '{:.3}'.format(int(response.headers['Content-Length'])/1024000)
                except: size = "?"
                with open(file_name,"wb") as file:
                    file.write(data)
                print(clr(f"  - {translate('Downloaded')} [ {file_name} ] [ {size} MB ]\n")); break
            except:
                print(clr(f"  > {translate('Failed')} [ {file_name} ] Retrying...\n",2))

    # disabled due to repeated error reports

    translated = translate('Do not use [ Ctrl + C ]!\n\n  > Press [ ENTER ] to start the multithreaded download process')
    print_read_me(); input(clr(f"\n  - {translated}... "))

    # begin multithreaded downloader

    print(clr(f"\n  - {translate('Starting Multiple Downloads... [ this might take a few minutes ]')}\n"))

    while True:
        try:
            start_time = time.time()
            multithread(file_downloader, 5, to_download_urls, to_download_file_names)
            time_taken = int(time.time()-start_time)
            break
        except: input(clr(f"\n  > {translate('Failed to download files! Do not use [ Ctrl + C ]! Press [ENTER] to try again...')} ",2)); cls()

    print(clr(f"\n  - {translate(f'Finished downloads in {time_taken} seconds! Sleeping for 3 seconds...')}")); time.sleep(3)

main_one()

# creating local files

cls(); print(clr(f"\n  - {translate('Creating local files...')}"))

with open('eula.txt','w',encoding='utf-8') as file:
    file.write('eula=true')

with open('start_server.cmd', 'w', encoding='utf-8') as file:
    file.write(f'''
@echo off
title Minecraft Server Console [ {name} - {version} ]
java -Dfile.encoding=UTF-8 -jar AutoPlug-Client.jar
pause
''')

with open('start_server.sh', 'wb') as file:
    file.write('''
#!/bin/sh
java -jar AutoPlug-Client.jar
'''.encode().replace(b'\r\n',b'\n'))

with open('mc-anti-malware.cmd', 'w', encoding='utf-8') as file:
    file.write('''@echo off
title Minecraft Anti-Malware
java -Dfile.encoding=UTF-8 -jar MCAntiMalware.jar
pause
''')

with open('mc-anti-malware.sh', 'wb') as file:
    file.write('''
#!/bin/sh
java -jar MCAntiMalware.jar
'''.encode().replace(b'\r\n',b'\n'))

with open('quick_install_java.cmd', 'w', encoding='utf-8') as file:
    file.write(f'''@echo off
title Java {latest_java_version} Installer
winget install --accept-source-agreements --interactive --id EclipseAdoptium.Temurin.{latest_java_version}.JRE
pause
''')

with open('quick_install_java.sh', 'wb') as file:
    file.write(f"""
#!/bin/sh
sudo apt install -y wget apt-transport-https
sudo mkdir -p /etc/apt/keyrings
sudo wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | sudo tee /etc/apt/keyrings/adoptium.asc
sudo echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{{print$2}}' /etc/os-release) main" | sudo tee /etc/apt/sources.list.d/adoptium.list
sudo apt update
sudo apt install temurin-{latest_java_version}-jre
""".encode().replace(b'\r\n',b'\n'))

# creating autoplug configs

with open('autoplug/logger.yml', 'w', encoding='utf-8') as file:
    file.write('''
logger: 
  tasks: 
    live-tasks: 
      enable: true
''')

with open('autoplug/backup.yml', 'w', encoding='utf-8') as file:
    file.write('''
backup: 
  enable: false
  cool-down: 1440
''')

with open('autoplug/general.yml', 'w', encoding='utf-8') as file:
    file.write(f'''
general: 
  autoplug: 
    target-software: MINECRAFT_SERVER
    start-on-boot: false
    system-tray: 
      enable: false
  server: 
    start-command: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true {extra_flag}--add-modules=jdk.incubator.vector -Dpaper.disable-plugin-rewriting=true -jar purpur.jar -nogui
  directory-cleaner:
    enabled: true
    max-days: 3
    list: 
      - true ./autoplug/logs
      - ./autoplug/downloads
''')

# WORKING: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true {extra_flag}--add-modules=jdk.incubator.vector -jar purpur.jar -nogui
# BROKEN: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -Dterminal.jline=false -Dterminal.ansi=true -XX:+UnlockDiagnosticVMOptions -XX:-UseBiasedLocking -XX:UseAVX=3 -XX:+UseStringDeduplication -XX:+UseFastUnorderedTimeStamps -XX:+UseAES -XX:+UseAESIntrinsics -XX:UseSSE=4 -XX:+UseFMA -XX:AllocatePrefetchStyle=1 -XX:+UseLoopPredicate -XX:+RangeCheckElimination -XX:+EliminateLocks -XX:+DoEscapeAnalysis -XX:+UseCodeCacheFlushing -XX:+SegmentedCodeCache -XX:+UseFastJNIAccessors -XX:+OptimizeStringConcat -XX:+UseCompressedOops -XX:+UseThreadPriorities -XX:+OmitStackTraceInFastThrow -XX:+TrustFinalNonStaticFields -XX:ThreadPriorityPolicy=1 -XX:+UseInlineCaches -XX:+RewriteBytecodes -XX:+RewriteFrequentPairs -XX:+UseNUMA -XX:-DontCompileHugeMethods -XX:+UseFPUForSpilling -XX:+UseFastStosb -XX:+UseNewLongLShift -XX:+UseVectorCmov -XX:+UseXMMForArrayCopy -XX:+UseXmmI2D -XX:+UseXmmI2F -XX:+UseXmmLoadAndClearUpper -XX:+UseXmmRegToRegMoveAll -Dfile.encoding=UTF-8 -Xlog:async -Djava.security.egd=file:/dev/urandom {extra_flag}--add-modules=jdk.incubator.vector -jar purpur.jar -nogui

with open('autoplug/updater.yml', 'w', encoding='utf-8') as file:
    file.write(f'''
updater: 
  java-updater: 
    enable: true
    profile: AUTOMATIC
    version: {latest_java_version}
  server-updater: 
    enable: true
    profile: AUTOMATIC
    software: purpur
    version: {version}
  plugins-updater: 
    enable: true
    profile: AUTOMATIC
    web-database: 
      enable: false
  mods-updater: 
    enable: false
    profile: AUTOMATIC
''')

with open('autoplug/plugins.yml', 'w', encoding='utf-8') as file:
    file.write('''
plugins: 
  general: 
    keep-removed: true
  ActionHealth: 
    exclude: false
    spigot-id: 2661
    alternatives: 
      github: 
        repo-name: zeshan321/ActionHealth
        asset-name: ActionHealth
  ChestSort: 
    spigot-id: 59773
  Essentials: 
    alternatives: 
      #github: 
      #  repo-name: EssentialsX/Essentials
      #  asset-name: EssentialsX
      jenkins: 
        project-url: https://ci.ender.zone/job/EssentialsX/
        artifact-name: EssentialsX
  EssentialsChat: 
    alternatives: 
      #github: 
      #  repo-name: EssentialsX/Essentials
      #  asset-name: EssentialsXChat
      jenkins: 
        project-url: https://ci.ender.zone/job/EssentialsX/
        artifact-name: EssentialsXChat
  EssentialsSpawn: 
    alternatives: 
      #github: 
      #  repo-name: EssentialsX/Essentials
      #  asset-name: EssentialsXSpawn
      jenkins: 
        project-url: https://ci.ender.zone/job/EssentialsX/
        artifact-name: EssentialsXSpawn
  Iris: 
    #spigot-id: 84586
    alternatives: 
      github: 
        repo-name: SirDank/Iris-AutoCompile
        asset-name: Iris
  Adapt: 
    #spigot-id: 103790
    alternatives: 
      github: 
        repo-name: SirDank/Adapt-AutoCompile
        asset-name: Adapt
  Log4JExploitFix: 
    exclude: false
    spigot-id: 98243
  mcMMO: 
    #spigot-id: 64348
    alternatives: 
      github: 
        repo-name: MediumCraft/mcMMO
        asset-name: mcMMO
  PlayerNPC: 
    spigot-id: 93625
    alternatives: 
      github: 
        repo-name: SergiFerry/PlayerNPC
        asset-name: PlayerNPC
  playit-gg: 
    spigot-id: 105566
  SkinsRestorer: 
    spigot-id: 2124
    alternatives: 
      github: 
        repo-name: SkinsRestorer/SkinsRestorerX
        asset-name: SkinsRestorer
  ProtocolLib: 
    spigot-id: 1997
    alternatives: 
      #github: 
      #  repo-name: dmulloy2/ProtocolLib
      #  asset-name: ProtocolLib
      jenkins: 
        project-url: https://ci.dmulloy2.net/job/ProtocolLib
        artifact-name: ProtocolLib
  NeoPerformance: 
    spigot-id: 103183
  BetterSleeping4: 
    spigot-id: 60837
    alternatives: 
      github: 
        repo-name: Nuytemans-Dieter/BetterSleeping
        asset-name: BetterSleeping
  TabTPS: 
    spigot-id: 82528
    alternatives: 
      github: 
        repo-name: jpenilla/TabTPS
        asset-name: tabtps-spigot
  BloodEffect: 
    spigot-id: 90955
  BloodFading: 
    spigot-id: 99263
    alternatives: 
      github: 
        repo-name: ventureoo/BloodFading
        asset-name: BloodFading
  LevelledMobs: 
    spigot-id: 74304
    alternatives: 
      github: 
        repo-name: ArcanePlugins/LevelledMobs
        asset-name: LevelledMobs
  PlayTime: 
    spigot-id: 26016
  ntdLuckyBlock: 
    spigot-id: 92026
  Multiverse-Core:
    spigot-id: 390
    alternatives: 
      github: 
        repo-name: Multiverse/Multiverse-Core
        asset-name: multiverse-core
  ViaVersion:
    spigot-id: 19254
  ViaBackwards:
    spigot-id: 27448
  DankChatroom: 
    spigot-id: 112398
    custom-download-url: https://github.com/SirDank/dank.chatroom-plugin/raw/main/Visual%20Bukkit%20Project/Build/target/dankchatroom.jar
  VisualBukkit: 
    exclude: false
    alternatives: 
      github: 
        repo-name: OfficialDonut/VisualBukkit
        asset-name: VisualBukkitPlugin
  FastAsyncWorldEdit: 
    spigot-id: 13932
    alternatives: 
      #github: 
      #  repo-name: IntellectualSites/FastAsyncWorldEdit
      #  asset-name: FastAsyncWorldEdit-Bukkit
      jenkins: 
        project-url: https://ci.athion.net/job/FastAsyncWorldEdit/
        artifact-name: FastAsyncWorldEdit-Bukkit
  SmoothTimber:
    spigot-id: 39965
  EliteMobs:
    alternatives: 
      github: 
        repo-name: MagmaGuy/EliteMobs
        asset-name: EliteMobs
  WorldGuard:
    exclude: false
    bukkit-id: 31054
  FancyPhysics:
    spigot-id: 110500
    alternatives: 
      github: 
        repo-name: max1mde/FancyPhysics
        asset-name: FancyPhysics
  SilkSpawners_v2:
    exclude: false
    spigot-id: 60063
''')

# start server and shutdown server for optimizing the below settings and configuring

configs = {

    # server configs

    "config/paper-world-defaults.yml": {
        "prevent-moving-into-unloaded-chunks: false": "prevent-moving-into-unloaded-chunks: true",
        "alt-item-despawn-rate:\n      enabled: false\n      items:\n        cobblestone: 300": "alt-item-despawn-rate:\n      enabled: true\n      items:\n        cobblestone: 300\n        netherrack: 300\n        sand: 300\n        red_sand: 300\n        gravel: 300\n        dirt: 300\n        grass: 300\n        pumpkin: 300\n        melon_slice: 300\n        kelp: 300\n        bamboo: 300\n        sugar_cane: 300\n        twisting_vines: 300\n        weeping_vines: 300\n        oak_leaves: 300\n        spruce_leaves: 300\n        birch_leaves: 300\n        jungle_leaves: 300\n        acacia_leaves: 300\n        dark_oak_leaves: 300\n        mangrove_leaves: 300\n        cactus: 300\n        diorite: 300\n        granite: 300\n        andesite: 300\n        scaffolding: 600",
        "redstone-implementation: VANILLA": "redstone-implementation: ALTERNATE_CURRENT",
        "optimize-explosions: false": "optimize-explosions: true",
        "max-auto-save-chunks-per-tick: 24": "max-auto-save-chunks-per-tick: 8",
        "entity-per-chunk-save-limit:\n    arrow: -1\n    ender_pearl: -1\n    experience_orb: -1\n    fireball: -1\n    small_fireball: -1\n    snowball: -1": "entity-per-chunk-save-limit:\n    area_effect_cloud: 8\n    arrow: 16\n    dragon_fireball: 3\n    egg: 8\n    ender_pearl: 8\n    experience_bottle: 3\n    experience_orb: 16\n    eye_of_ender: 8\n    fireball: 8\n    firework_rocket: 8\n    llama_spit: 3\n    potion: 8\n    shulker_bullet: 8\n    small_fireball: 8\n    snowball: 8\n    spectral_arrow: 16\n    trident: 16\n    wither_skull: 4",
        "despawn-ranges:\n      ambient:\n        hard: 128\n        soft: 32\n      axolotls:\n        hard: 128\n        soft: 32\n      creature:\n        hard: 128\n        soft: 32\n      misc:\n        hard: 128\n        soft: 32\n      monster:\n        hard: 128\n        soft: 32\n      underground_water_creature:\n        hard: 128\n        soft: 32\n      water_ambient:\n        hard: 64\n        soft: 32\n      water_creature:\n        hard: 128\n        soft: 32": "despawn-ranges:\n      ambient:\n        hard: 56\n        soft: 30\n      axolotls:\n        hard: 56\n        soft: 30\n      creature:\n        hard: 56\n        soft: 30\n      misc:\n        hard: 56\n        soft: 30\n      monster:\n        hard: 56\n        soft: 30\n      underground_water_creature:\n        hard: 56\n        soft: 30\n      water_ambient:\n        hard: 56\n        soft: 30\n      water_creature:\n        hard: 56\n        soft: 30",
        "fix-climbing-bypassing-cramming-rule: false": "fix-climbing-bypassing-cramming-rule: true",
        "non-player-arrow-despawn-rate: default": "non-player-arrow-despawn-rate: 20",
        "creative-arrow-despawn-rate: default": "creative-arrow-despawn-rate: 20",
    },

    "purpur.yml": {
        "use-alternate-keepalive: false": "use-alternate-keepalive: true",
        "aggressive-towards-villager-when-lagging: true": "aggressive-towards-villager-when-lagging: false",
        "brain-ticks: 1": "brain-ticks: 2",
        "lobotomize:\n          enabled: false": "lobotomize:\n          enabled: true",
        "teleport-if-outside-border: false": "teleport-if-outside-border: true",
    },

    "server.properties": {
        "simulation-distance=10": "simulation-distance=4",
        "motd=A Minecraft Server": f"motd=\\u00A7a{motd_spaces}---\\u00A76>\\u00A7b\\u00A7l {motd_spaces + name + motd_spaces} \\u00A76<\\u00A7a---\\u00A7r\\{motd_spaces}\\n   \\u00A76\\u00A7l\\u00A7m-----\\u00A79\\u00A78\\u00A7l[\\u00A75 Made with \\u00A7ddank\\u00A7f.\\u00A7dtool \\u00A78\\u00A7l]\\u00A76\\u00A7l\\u00A7m-----",
        "server-name=Unknown Server": f"server-name={name}",
        "require-resource-pack=false": "require-resource-pack=true",
        'resource-pack-prompt=': 'resource-pack-prompt={"text":"github.com/SirDank/dank.resource-pack","color":"light_purple"}',
        "resource-pack=": "resource-pack=https://github.com/SirDank/dank.resource-pack/raw/main/dank.resource-pack.zip",
        "enable-query=false": "enable-query=true",
        "max-players=20": "max-players=69",
        # "view-distance=10": "view-distance=8",
        # "resource-pack-sha1=": "resource-pack-sha1=3c0e42f1e8194fb47475558a9e827a3128adef2f",
        "spawn-protection=16": "spawn-protection=0",
        "max-world-size=29999984": "max-world-size=1000500",
    },

    "spigot.yml": {
        "merge-radius:\n      item: 2.5\n      exp: 3.0": "merge-radius:\n      item: 3.5\n      exp: 4.0",
        # "mob-spawn-range: 8": "mob-spawn-range: 2",
        "entity-activation-range:\n      animals: 32\n      monsters: 32\n      raiders: 48\n      misc: 16\n      water: 16\n      villagers: 32\n      flying-monsters: 32": "entity-activation-range:\n      animals: 16\n      monsters: 24\n      raiders: 48\n      misc: 8\n      water: 8\n      villagers: 16\n      flying-monsters: 32"
    },

    "bukkit.yml": {
        "ticks-per:\n  animal-spawns: 400\n  monster-spawns: 1\n  water-spawns: 1\n  water-ambient-spawns: 1\n  water-underground-creature-spawns: 1\n  axolotl-spawns: 1\n  ambient-spawns: 1": "ticks-per:\n  animal-spawns: 400\n  monster-spawns: 10\n  water-spawns: 400\n  water-ambient-spawns: 400\n  water-underground-creature-spawns: 400\n  axolotl-spawns: 400\n  ambient-spawns: 400",
    },

    #"pufferfish.yml": {
    #    "dab:\n  enabled: false\n  start-distance: 12\n  max-tick-freq: 20\n  activation-dist-mod: 8": "dab:\n  enabled: true\n  start-distance: 12\n  max-tick-freq: 20\n  activation-dist-mod: 7",
    #    "inactive-goal-selector-throttle: false": "inactive-goal-selector-throttle: true",
    #    #"max-loads-per-projectile: 10": "max-loads-per-projectile: 8",
    #},

    # plugins

    "plugins/ChestSort/config.yml": {
        "use-permissions: true": "use-permissions: false",
        "sorting-enabled-by-default: false": "sorting-enabled-by-default: true",
        "inv-sorting-enabled-by-default: false": "inv-sorting-enabled-by-default: true",
    },

    "plugins/Essentials/config.yml": {
        "nickname-prefix: '~'": "nickname-prefix: ''",
        "ignore-colors-in-max-nick-length: false": "ignore-colors-in-max-nick-length: true",
        'custom-join-message: "none"': 'custom-join-message: "&8&l[&a+&8&l]&a&l {PLAYER}"',
        'custom-quit-message: "none"': 'custom-quit-message: "&8&l[&c-&8&l]&c&l {PLAYER}"',
        "format: '<{DISPLAYNAME}> {MESSAGE}'": "format: '&6[&a{DISPLAYNAME}&6] ➤ &b{MESSAGE}'",
        "announce-format: '&dWelcome {DISPLAYNAME}&d to the server!'": "announce-format: '&dWelcome &6&l{DISPLAYNAME}&d to the server!'",
        "use-bukkit-permissions: true": "use-bukkit-permissions: false",
        "player-commands:\n": "player-commands:\n  - playtime.check\n  - playtime.checkothers\n  - playtime.checktop\n  - playtime.uptime\n",
    },

    "plugins/ntdLuckyBlock/config.yml": {
        "break-permissions: true": "break-permissions: false",
    },

    "plugins/BetterStructures/config.yml": {
        "warnAdminsAboutNewBuildings: true": "warnAdminsAboutNewBuildings: false"
    }

    #"plugins/Corpses/config.yml": {
    #    "secondsToDisappear: 300": "secondsToDisappear: 3600",
    #},

    #"plugins/LevelledMobs/rules.yml": {
    #    "&8&l༺ %tiered%Lvl %mob-lvl%&8 | &f%displayname%&8 | &f%entity-health-rounded% %tiered%%heart_symbol% &r%health-indicator% &8&l༻": "%tiered%%mob-lvl% &r%health-indicator%",
    #    "&8&l༺ %tiered%Lvl %mob-lvl%&8 | &f%displayname%&8 | &f%entity-health-rounded%&8/&f%entity-max-health-rounded% %tiered%%heart_symbol% &8&l༻": "%tiered%%mob-lvl%&8 &f%entity-health-rounded%",
    #    "&8&l༺ &f%displayname%&8 | &f%entity-health-rounded%&8/&f%entity-max-health-rounded% %tiered%%heart_symbol% &8&l༻": "&f%entity-health-rounded% %tiered%%heart_symbol%",
    #    "- nametag_using_numbers": "#- nametag_using_numbers",
    #    "#- nametag_using_indicator": "- nametag_using_indicator",
    #    "- weighted_random_Levelling": "#- weighted_random_Levelling",
    #    "#- ycoord_Levelling": "- ycoord_Levelling",
    #},

    #"plugins/LevelledMobs/settings.yml": {
    #    "mobs-multiply-head-drops: false": "mobs-multiply-head-drops: true",
    #},

    #"plugins/NeoPerformance/performanceConfig.yml": {
    #    "broadcastHalt: false": "broadcastHalt: true",
    #},

    #"plugins/PhysicsToGo/config.yml": {
    #    "tree-regeneration: true": "tree-regeneration: false",
    #    "explosive-regeneration: true": "explosive-regeneration: false"
    #},

}

if cracked:
    configs["server.properties"]["online-mode=true"] = "online-mode=false"

if extra_flag:
    configs["plugins/Log4JExploitFix/config.yml"] = {"enabled: false": "enabled: true"}

def main_two():

    string = f'''

  [ Scripts ]
  - quick_install_java.cmd / quick_install_java.sh : {translate('Script to install Temurin JRE')}
  - mc-anti-malware.cmd / mc-anti-malware.sh : {translate('Script to start mc-anti-malware')}
  - start_server.cmd / start_server.sh : {translate('Script to start your server')}
  
  [ Autoplug Commands ]
  - ".check java" : {translate('Command to install Java VM')}
  - ".start" : {translate('Command to start the server')}
  - ".stop" : {translate('Command to stop the server')}
  - ".stop both" : {translate('Command to stop the server and Autoplug')}
  - ".check plugins" : {translate('Command to update configured plugins')}
  - ".help" : {translate('Command to display all available commands')}
  
  '''

    with open('readme.txt', 'w', encoding='utf-8') as file:
        file.write(string)

    print_read_me(); input(clr(f"  - {translate('Start the server using: start_server.cmd ( it will stop automatically on the first run ) to generate config files to be optimized')}" + string + f"> {translate('After your server has run at least once, press [ ENTER ] to apply custom configuration...')} "))

    def config_updater(path):
        with open(path, 'r', encoding='utf-8') as file:
            config_data = file.read()
        for setting in configs[path]:
            #if setting in config_data:
            #    config_data = config_data.replace(configs[path][setting], setting)
            config_data = config_data.replace(setting, configs[path][setting])
        with open(path, 'w', encoding='utf-8') as file:
            file.write(config_data)

    # [ updating configs ] try all without ignoring errors

    for path in configs:
        while True:
            try: config_updater(path); break
            except:
                string = translate('Press [ ENTER ] to retry or type "skip" to skip')
                choice = input(clr(f"\n{err(sys.exc_info(),'mini')}\n\n  > {string}: ", 2) + white_bright)
                if choice == "skip": break

    string = f'''
  - {translate('Follow these steps to enable custom world generation')}:

  [1] {translate('Start the server again using the following command')}: .start
  [2] {translate('After it has properly started, copy and paste the following command')}: iris create name=world-iris seed={randint(1,9999999999)}
  [3] {translate('Wait for it to complete then stop the server using the following command')}: .stop

  > {translate('Press [ ENTER ] after you have followed the steps...')} '''

    #while not os.path.isdir("world-iris"):
    #    print_read_me(); input(clr(string))

    #shutil.move("world/datapacks", "world-iris/datapacks")
    #shutil.rmtree("world")
    #os.rename("world_nether", "world-iris_nether")
    #os.rename("world_the_end", "world-iris_the_end")

    #with open('server.properties', 'r', encoding='utf-8') as file:
    #    data = file.read().replace("level-name=world", "level-name=world-iris")

    #with open('server.properties', 'w', encoding='utf-8') as file:
    #    file.write(data)

    if playit:

        string = f'''
  - {translate('It is extremely easy to setup the playit.gg plugin')}
  
  - {translate('After server setup is complete, start your server.')}
  
  - {translate('Click on the URL displayed on the console.')}
  
  - {translate("Create an account and login if you haven't already to save the tunnel on playit.gg")}
  
  - {translate('Click "Add Agent"')}
  
  - {translate("A tunnel will be created and your server's public ip will be displayed: example.craft.playit.gg")}
  
  > {translate('Press [ ENTER ] after you have read the message...')} '''

        print_read_me(); input(clr(string))
    else:
        print_read_me(); print(clr(f"\n  - {translate('As you have not selected playit.gg as a host, To allow players to connect to your server over the internet, you could follow this tutorial on port-forwarding.')}"))
        if input(clr(f"\n  > {translate('Open port forwarding tutorial on youtube?')} [ y / n ]: ") + red).lower() == "y":
            sys_open('https://youtu.be/X75GbRaGzu8')

    tmp_path = f'{dir_name}\\autoplug\\updater.yml'
    string = f'''
  - {translate(f'If you would like to transfer the server to a linux system and run it there, set "build-id: 0" inside "{tmp_path}"')}

  - {translate('After you move the folder to a linux system, run "sudo chmod +x *.sh" to make all .sh files executable')}

  - {translate('Run "start_server.sh" and then install JVM with the ".check java" command')}

  > {translate('Press [ ENTER ] after you have read the message...')} '''

    print_read_me(); input(clr(string))

    # done!

    title("𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚋𝚞𝚒𝚕𝚍𝚎𝚛 [ 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎! ]")
    complete_banner = "\n\n\n\n ___  ___ _ ____   _____ _ __                 \n/ __|/ _ \\ '__\\ \\ / / _ \\ '__|                \n\\__ \\  __/ |   \\ V /  __/ |                   \n|___/\\___|_|    \\_/ \\___|_|                   \n\n                     _   _                    \n  ___ _ __ ___  __ _| |_(_) ___  _ __         \n / __| '__/ _ \\/ _` | __| |/ _ \\| '_ \\        \n| (__| | |  __/ (_| | |_| | (_) | | | |       \n \\___|_|  \\___|\\__,_|\\__|_|\\___/|_| |_|       \n\n                           _      _         _ \n  ___ ___  _ __ ___  _ __ | | ___| |_ ___  / \\\n / __/ _ \\| '_ ` _ \\| '_ \\| |/ _ \\ __/ _ \\/  /\n| (_| (_) | | | | | | |_) | |  __/ ||  __/\\_/ \n \\___\\___/|_| |_| |_| .__/|_|\\___|\\__\\___\\/   \n                    |_|                       \n\n"
    cls(); Console().print(Align.center(complete_banner), style="blink red", highlight=False); time.sleep(5)
    #sys_open('https://allmylinks.com/sir-dankenstein')

main_two()

if __name__ == "__main__" and "DANK_TOOL_VERSION" in os.environ:
    for _ in ('name', 'version', 'cracked', 'install_Via', 'ram', 'motd_spaces', 'playit', 'extra_flag', 'dir_name', 'configs', 'headers', 'latest_java_version', 'translator', 'print_banner', 'print_read_me', 'main_one', 'main_two', 'translate'):
        if _ in globals(): del globals()[_]
