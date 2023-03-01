import os
import sys
import time
import shutil
import requests
from dankware import title, rm_line, align, cls, clr, white, magenta, red, reset, github_file_selector, multithread, sys_open, err

def print_banner():
    cls(); print(align(clr(banner,4) + f"\n{white}s i r {magenta}. {white}d a n k {magenta}<3\n\n"))

def print_read_me():
    cls(); print(align(read_me.replace(":",f"{reset}:").replace("+",f"{white}+").replace("#",f"{magenta}#")))

def main_one():

    global banner, read_me, name, version, cracked, ram, motd_spaces, playit, extra_flag

    # change dir and print banner

    #exec_mode = "script"; exec(chdir(exec_mode))
    try: os.chdir(os.path.join(os.path.join(os.environ['USERPROFILE']),'Desktop'))
    except: os.chdir("C:\\")
    banner = "\n\n\n   _         _                                 _       _ _   _            ___ \n _| |___ ___| |_   ___ ___ ___ _ _ ___ ___ ___| |_ _ _|_| |_| |___ ___   |_  |\n| . | .'|   | '_|_|_ -| -_|  _| | | -_|  _|___| . | | | | | . | -_|  _|  |_  |\n|___|__,|_|_|_,_|_|___|___|_|  \\_/|___|_|     |___|___|_|_|___|___|_|    |___|\n"
    read_me = '\n\n:::::::::  ::::::::::     :::     :::::::::       ::::    ::::  ::::::::::\n:+:    :+: :+:          :+: :+:   :+:    :+:      +:+:+: :+:+:+ :+:       \n+:+    +:+ +:+         +:+   +:+  +:+    +:+      +:+ +:+:+ +:+ +:+       \n+#++:++#:  +#++:++#   +#++:++#++: +#+    +:+      +#+  +:+  +#+ +#++:++#  \n+#+    +#+ +#+        +#+     +#+ +#+    +#+      +#+       +#+ +#+       \n#+#    #+# #+#        #+#     #+# #+#    #+#      #+#       #+# #+#       \n###    ### ########## ###     ### #########       ###       ### ##########\n\n\n'

    print_banner()

    # get available purpur versions and print

    while True:
        try:
            version_list = requests.get("https://api.purpurmc.org/v2/purpur").json()['versions']
            print(clr(f'  > Available Purpur Versions: {", ".join(version_list)}')); break
        except: input(clr("\n  > Failed to get purpur versions! Make sure you are connected to the internet! Press [ ENTER ] to try again... ",2))

    # user inputs [ name, version, ram, allow_cracked ]

    max_motd_len = 49
    used_motd_len = 10
    print("")
    while True:
        name = input(clr("  > Server Name: ") + magenta)
        if not len(name) > (max_motd_len - used_motd_len): break
        else: rm_line()
    motd_spaces = ' '*int((max_motd_len - used_motd_len - len(name))/4)

    print("")
    while True:
        version = input(clr("  > Version: ") + magenta)
        if version in version_list: break
        else: rm_line()

    title(f"𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚋𝚞𝚒𝚕𝚍𝚎𝚛 [ {name} - {version} ]")

    print("")
    while True:
        cracked = input(clr("  > Allow Cracked Players [ y / n ]: ") + magenta).lower()
        if 'y' in cracked: cracked = True; break
        elif 'n' in cracked: cracked = False; break
        else: rm_line() # BROKEN
        
    # setting extra flags

    if version in ["1.17", "1.18"]: extra_flag = "-Dlog4j2.formatMsgNoLookups=true "
    elif version in ["1.12", "1.13", "1.14", "1.15", "1.16"]: extra_flag = "-Dlog4j.configurationFile=log4j2_112-116.xml "
    elif version in ["1.7", "1.8", "1.9", "1.10", "1.11"]: extra_flag = "-Dlog4j.configurationFile=log4j2_17-111.xml "
    else: extra_flag = ""

    # setting max ram

    print_read_me(); print(clr("\n  > When setting the Xms and Xmx values, if your host says you have 8000M memory, DO NOT USE 8000M! Minecraft (and Java) needs additional memory on top of that Xmx parameter. It is recommended to reduce your Xmx/Xms by about 1000-1500M to avoid running out of memory or \"OOMKiller\" hitting your server. This also leaves room for the Operating System to use memory too. Have 8000M memory? Use 6500M for safety. But you may also ask your host if they will cover this overhead for you and give you 9500M instead. Some hosts will! Just ask. We recommend using at least 6-10GB, no matter how few players! If you can't afford 10GB of memory, give as much as you can. However going out and getting 32GB of RAM for a server will only waste your money with minimal returns."))
    print("")
    while True:
        ram = input(clr("  > RAM in MB [ Leave 1500MB Free ]: ") + magenta)
        if ram.isdigit(): ram = int(ram); break
        else: rm_line()
    if ram < 256: ram = 256

    # use playit.gg

    print_read_me(); print(clr(f"\n  > Great! Now you need to pick a {magenta}host{white} for your mc server!\n\n  > If you are new to hosting and would like to quickly host a server with playit.gg's plugin without port-forwarding\n  - Choose {magenta}Option 1\n\n  > If you are experienced and would like to skip playit.gg and use port-forwarding / alternative hosting methods\n  - Choose {magenta}Option 2"))

    print("")
    while True:
        playit = input(clr("  > Choice [ 1 / 2 ]: ") + magenta)
        if playit in ["1","2"]:
            if playit == "1": playit = True
            else: playit = False
            break
        else: rm_line()

    # create and go to workspace

    dir_name = name
    try: os.mkdir(dir_name)
    except:
        counter = 1
        while True:
            dir_name = name + f"_{counter}"
            try: os.mkdir(dir_name); break
            except: counter += 1

    os.system(f'explorer.exe "{dir_name}"')
    os.chdir(dir_name)

    # create folders

    for folder in ['world/datapacks', 'world_nether/datapacks', 'world_the_end/datapacks', 'plugins/Iris/packs', 'datapacks_backup', 'autoplug']:
        try: os.makedirs(folder)
        except: pass

    # begin preparing downloads

    cls(); print(clr("\n  > Preparing Downloads..."))
    to_download_urls, to_download_file_names = [], []

    # github server-builder files and plugins

    for file in ['server-icon.png', 'log4j2_17-111.xml', 'log4j2_112-116.xml', 'mcMMO.jar', 'Iris.jar']: # 'PublicCrafters.jar' 4.13.5 | Iris 2.3.11 | mcMMO 2.1.217 |
        to_download_urls.append(f"https://github.com/SirDank/dank.tool/raw/main/__assets__/dank.minecraft-server-builder/{file}")
        if '.jar' in file: to_download_file_names.append(f"plugins/{file}")
        elif '.zip' in file: to_download_file_names.append(f"datapacks_backup/{file}")
        else: to_download_file_names.append(file)
        
    # iris packs

    for file in ['newhorizons', 'theend', 'overworld']:
        
        if file == 'overworld': tmp_name = 'stable'
        else: tmp_name = 'main'
        to_download_urls.append(f"https://github.com/IrisDimensions/{file}/archive/refs/heads/{tmp_name}.zip")
        to_download_file_names.append(f"plugins/Iris/packs/{file}.zip")

    # spigot plugins

    spigot_plugins = {
        #"ActionHealth": 2661,
        "BetterSleeping": 60837,
        "BloodEffect": 90955,
        "BloodFading": 99263,
        "ChestSort": 59773,
        #"Chunky": 81534,
        "Corpses": 96774,
        "Log4JExploitFix": 98243,
        "NeoPerformance": 103183,
        "PLayerNPC": 93625,
        "ProtocolLib": 1997,
        "SkinRestorer": 2124,
        "Spark": 57242,
        "TabTPS": 82528,
        "TreeAssist": 67436,
        "LevelledMobs": 74304,
        "PlayTime": 26016,
        "PlaceholderAPI": 6245,
        "LuckyBlock-NTD": 92026,
    }
    
    if playit:
        spigot_plugins["playit-gg"] = 105566

    for plugin in spigot_plugins:
        to_download_urls.append(f"https://api.spiget.org/v2/resources/{spigot_plugins[plugin]}/download")
        to_download_file_names.append(f"plugins/{plugin}.jar")

    # github plugins

    # > EssentialsX
    for file_url in github_file_selector("EssentialsX/Essentials", "remove", ['AntiBuild', 'Discord', 'GeoIP', 'Protect', 'XMPP']):
        to_download_urls.append(file_url)
        to_download_file_names.append(f"plugins/{file_url.split('/')[-1]}")

    # > AutoPlug
    to_download_urls.append("https://github.com/Osiris-Team/AutoPlug-Releases/raw/master/stable-builds/AutoPlug-Client.jar")
    to_download_file_names.append("AutoPlug-Client.jar")

    # > purpur.jar
    to_download_urls.append(f"https://api.purpurmc.org/v2/purpur/{version}/latest/download")
    to_download_file_names.append("purpur.jar")
    
    # > MCAntiMalware.jar
    for file_url in github_file_selector("OpticFusion1/MCAntiMalware", "add", ['MCAntiMalware']):
        to_download_urls.append(file_url)
        to_download_file_names.append(file_url.split('/')[-1])
        
    def file_downloader(url, file_name):

        while True:
            try:
                response = requests.get(url, headers={'user-agent':'dank.tool'}, allow_redirects=True)
                data = response.content
                try: size = '{:.3}'.format(int(response.headers['Content-Length'])/1024000)
                except: size = "?"
                open(file_name,"wb").write(data)
                print(clr(f"\n  > Downloaded [ {file_name} ] [ {size} MB ]")); break
            except: input(clr(f"\n  > Failed [ {file_name} ] Press {white}ENTER{red} to try again... ",2))

    # disabled due to repeated error reports

    '''
    print_read_me(); input(clr("\n  > Try not to use [COPY] or [PASTE] when the download process is running!\n\n  > Press [ ENTER ] to start the download process... "))

    # begin multithreaded downloader | threads = 2
    
    # func

    print(clr("\n  > Starting Multiple Downloads... [ this might take a few minutes ]"))

    while True:
        try:
            start_time = time.time()
            multithread(file_downloader, 2, to_download_urls, to_download_file_names, False)
            time_taken = int(time.time()-start_time)
            break
        except KeyboardInterrupt: input(clr(f"\n  > Failed to download files! Try not to use [COPY] or [PASTE]! Press [ENTER] to try again... ",2)); cls() # rm_line()
    '''

    # begin single threaded downloader
    
    print(clr("\n  > Downloading... [ this might take a few minutes ]"))
    
    start_time = time.time()
    for url, file_name in zip(to_download_urls, to_download_file_names):
        file_downloader(url, file_name)
    time_taken = int(time.time()-start_time)

    print(clr(f"\n  > Finished downloads in {magenta}{time_taken}{white} seconds! Sleeping {magenta}3{white} seconds...")); time.sleep(3)

    # unpacking downloaded archives

    print(clr("\n  > Unpacking..."))
    
    for file in ['newhorizons', 'theend', 'overworld']:

        if file == 'overworld': tmp_name = 'stable'
        else: tmp_name = 'main'

        shutil.unpack_archive(f'plugins/Iris/packs/{file}.zip', 'plugins/Iris/packs', 'zip')
        time.sleep(1)
        try: os.rename(f'plugins/Iris/packs/{file}-{tmp_name}', f'plugins/Iris/packs/{file}')
        except:
            while os.path.exists(f'plugins/Iris/packs/{file}-{tmp_name}'):
                input(clr(f'\n  > ERROR! Please manually rename "plugins/Iris/packs/{file}-{tmp_name}" to "plugins/Iris/packs/{file}"\n\n  > Press [ ENTER ] after doing the above... ',2))
        try: os.remove(f'plugins/Iris/packs/{file}.zip')
        except: pass

main_one()

# creating local files

cls(); print(clr("\n  > Creating local files..."))

open('eula.txt','w').write('eula=true')

open('start_server.cmd', 'w').write(f'''@echo off
COLOR 0F
title Minecraft Server Console [ {name} - {version} ]
java -jar AutoPlug-Client.jar
''')

open('start_server.sh', 'wb').write(f'''#!/bin/sh
java -jar AutoPlug-Client.jar
'''.encode().replace(b'\r\n',b'\n'))

open('anti-malware.cmd', 'w').write(f'''@echo off
COLOR 0F
title Minecraft Anti-Malware [ {name} - {version} ]
java -jar MCAntiMalware.jar
pause
''')

open('anti-malware.sh', 'wb').write(f'''#!/bin/sh
java -jar MCAntiMalware.jar
'''.encode().replace(b'\r\n',b'\n'))

# creating autoplug configs

open('autoplug/general.yml', 'w').write(f'''
general: 
  autoplug: 
    target-software: MINECRAFT_SERVER
    start-on-boot: false
    system-tray: 
      enable: false
  server: 
    start-command: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true {extra_flag}--add-modules=jdk.incubator.vector -jar purpur.jar -nogui
''')

# WORKING: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true {extra_flag}--add-modules=jdk.incubator.vector -jar purpur.jar -nogui
# BROKEN: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -Dterminal.jline=false -Dterminal.ansi=true -XX:+UnlockDiagnosticVMOptions -XX:-UseBiasedLocking -XX:UseAVX=3 -XX:+UseStringDeduplication -XX:+UseFastUnorderedTimeStamps -XX:+UseAES -XX:+UseAESIntrinsics -XX:UseSSE=4 -XX:+UseFMA -XX:AllocatePrefetchStyle=1 -XX:+UseLoopPredicate -XX:+RangeCheckElimination -XX:+EliminateLocks -XX:+DoEscapeAnalysis -XX:+UseCodeCacheFlushing -XX:+SegmentedCodeCache -XX:+UseFastJNIAccessors -XX:+OptimizeStringConcat -XX:+UseCompressedOops -XX:+UseThreadPriorities -XX:+OmitStackTraceInFastThrow -XX:+TrustFinalNonStaticFields -XX:ThreadPriorityPolicy=1 -XX:+UseInlineCaches -XX:+RewriteBytecodes -XX:+RewriteFrequentPairs -XX:+UseNUMA -XX:-DontCompileHugeMethods -XX:+UseFPUForSpilling -XX:+UseFastStosb -XX:+UseNewLongLShift -XX:+UseVectorCmov -XX:+UseXMMForArrayCopy -XX:+UseXmmI2D -XX:+UseXmmI2F -XX:+UseXmmLoadAndClearUpper -XX:+UseXmmRegToRegMoveAll -Dfile.encoding=UTF-8 -Xlog:async -Djava.security.egd=file:/dev/urandom {extra_flag}--add-modules=jdk.incubator.vector -jar purpur.jar -nogui

open('autoplug/updater.yml', 'w').write(f'''
updater: 
  java-updater: 
    enable: true
    profile: AUTOMATIC
    version: 17
  server-updater: 
    enable: true
    profile: AUTOMATIC
    software: purpur
    version: {version}
  plugins-updater: 
    enable: true
    profile: AUTOMATIC
  mods-updater: 
    enable: false
    profile: AUTOMATIC
''')

open('autoplug/plugins.yml', 'w').write('''
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
      github: 
        repo-name: EssentialsX/Essentials
        asset-name: EssentialsX
      jenkins: 
        project-url: https://ci.ender.zone/job/EssentialsX/
        artifact-name: EssentialsX
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
  Iris: 
    spigot-id: 84586
    custom-download-url: https://github.com/SirDank/dank.tool/raw/main/__assets__/dank.minecraft-server-builder/Iris.jar
  Log4JExploitFix: 
    exclude: false
    spigot-id: 98243
  mcMMO: 
    spigot-id: 64348
    custom-download-url: https://github.com/SirDank/dank.tool/raw/main/__assets__/dank.minecraft-server-builder/mcMMO.jar
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
      github: 
        repo-name: dmulloy2/ProtocolLib
        asset-name: ProtocolLib
      jenkins: 
        project-url: https://ci.dmulloy2.net/job/ProtocolLib
        artifact-name: ProtocolLib
  NeoPerformance: 
    spigot-id: 103183
  BetterSleeping4: 
    alternatives: 
      github: 
        repo-name: Nuytemans-Dieter/BetterSleeping
        asset-name: BetterSleeping
  TabTPS: 
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
''')

# start server and shutdown server for optimizing the below settings and configuring

configs = {

    # paper config

    "config/paper-world-defaults.yml": {
        "prevent-moving-into-unloaded-chunks: false": "prevent-moving-into-unloaded-chunks: true",
        "alt-item-despawn-rate:\n      enabled: false\n      items:\n        cobblestone: 300": "alt-item-despawn-rate:\n      enabled: true\n      items:\n        cobblestone: 300\n        netherrack: 300\n        sand: 300\n        red_sand: 300\n        gravel: 300\n        dirt: 300\n        grass: 300\n        pumpkin: 300\n        melon_slice: 300\n        kelp: 300\n        bamboo: 300\n        sugar_cane: 300\n        twisting_vines: 300\n        weeping_vines: 300\n        oak_leaves: 300\n        spruce_leaves: 300\n        birch_leaves: 300\n        jungle_leaves: 300\n        acacia_leaves: 300\n        dark_oak_leaves: 300\n        mangrove_leaves: 300\n        cactus: 300\n        diorite: 300\n        granite: 300\n        andesite: 300\n        scaffolding: 600",
        "redstone-implementation: VANILLA": "redstone-implementation: ALTERNATE_CURRENT",
        "optimize-explosions: false": "optimize-explosions: true",
        # "max-auto-save-chunks-per-tick: 24": "max-auto-save-chunks-per-tick: 8",
    },

    # plugins

    "plugins/ChestSort/config.yml": {
        "use-permissions: true": "use-permissions: false",
        "sorting-enabled-by-default: false": "sorting-enabled-by-default: true",
        "inv-sorting-enabled-by-default: false": "inv-sorting-enabled-by-default: true",
    },

    "plugins/Corpses/config.yml": {
        "secondsToDisappear: 300": "secondsToDisappear: 3600",
    },

    "plugins/Essentials/config.yml": {
        "nickname-prefix: '~'": "nickname-prefix: ''",
        "ignore-colors-in-max-nick-length: false": "ignore-colors-in-max-nick-length: true",
        'custom-join-message: "none"': 'custom-join-message: "&8&l[&a+&8&l]&a&l {PLAYER}"',
        'custom-quit-message: "none"': 'custom-quit-message: "&8&l[&c-&8&l]&c&l {PLAYER}"',
        "format: '<{DISPLAYNAME}> {MESSAGE}'": "format: '&6[&a{DISPLAYNAME}&6] ➤ &b{MESSAGE}'",
        "announce-format: '&dWelcome {DISPLAYNAME}&d to the server!'": "announce-format: '&dWelcome &6&l{DISPLAYNAME}&d to the server!'",
        "use-bukkit-permissions: true": "use-bukkit-permissions: false",
        "  - playtime.check\n  - playtime.uptime\n  - afk": "  - afk", # to prevent multiple entries
        "  - afk": "  - playtime.check\n  - playtime.uptime\n  - afk",
    },

    #"plugins/Log4JExploitFix/config.yml": {
    #    "enabled: false": "enabled: true"
    #},

    "plugins/LevelledMobs/rules.yml": {
        " | &f%displayname%": "",
    },

    # server configs

    "pufferfish.yml": {
        "dab:\n  enabled: false": "dab:\n  enabled: true",
        "inactive-goal-selector-throttle: false": "inactive-goal-selector-throttle: true",
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
        "motd=A Minecraft Server": f"motd={motd_spaces}\\u00A7a---\\u00A76>\\u00A7b\\u00A7l {motd_spaces + name + motd_spaces} \\u00A76<\\u00A7a---\\u00A7r\{motd_spaces}\\n   \\u00A76\\u00A7l\\u00A7m-----\\u00A79\\u00A78\\u00A7l[\\u00A75 Made with \\u00A7ddank\\u00A7f.\\u00A7dserverbuilder \\u00A78\\u00A7l]\\u00A76\\u00A7l\\u00A7m-----",
        "server-name=Unknown Server": f"server-name={name}",
        "require-resource-pack=false": "require-resource-pack=true",
        'resource-pack-prompt={"text":"github.com/SirDank/dank.resourcepack","color":"light_purple"}': 'resource-pack-prompt=', # to prevent multiple entries
        'resource-pack-prompt=': 'resource-pack-prompt={"text":"github.com/SirDank/dank.resourcepack","color":"light_purple"}',
        "resource-pack=https://github.com/SirDank/dank.resourcepack/raw/main/dank.resourcepack.zip": "resource-pack=", # to prevent multiple entries
        "resource-pack=": "resource-pack=https://github.com/SirDank/dank.resourcepack/raw/main/dank.resourcepack.zip",
        "enable-query=false": "enable-query=true",
        "max-players=20": "max-players=69",
        # "view-distance=10": "view-distance=8",
        # "resource-pack-sha1=": "resource-pack-sha1=3c0e42f1e8194fb47475558a9e827a3128adef2f"
    },

    "spigot.yml": {
        "merge-radius:\n      item: 2.5\n      exp: 3.0": "merge-radius:\n      item: 3.5\n      exp: 4.0",
        # "mob-spawn-range: 8": "mob-spawn-range: 2",
        # "entity-activation-range\n      animals: 32\n      monsters: 32\n      raiders: 48\n      misc: 16\n      water: 16\n      villagers: 32\n      flying-monsters: 32": "entity-activation-range\n      animals: 16\n      monsters: 24\n      raiders: 48\n      misc: 8\n      water: 8\n      villagers: 16\n      flying-monsters: 32"
    },

}

def main_two():

    print_read_me(); input(clr("\n  > Start the server once ( it will stop automatically on the first run ) to generate config files to be optimized\n\n  > Start your server once using start_server.cmd\n\n  > If you don't have JDK installed, type \".check java\" in the console window to download it\n\n  > Type \".start\" to start the server\n\n  > Type \".stop\" to stop the server\n\n  > Type \".stop both\" to stop the server and autoplug\n\n  > Type \".check plugins\" to update configured plugins\n\n  > After your server has stopped, press [ ENTER ] to begin configuration... "))

    def config_updater(path):
        config_data = open(path, 'r', encoding='utf-8').read()
        for setting in configs[path]: config_data = config_data.replace(setting, configs[path][setting])
        if path == "server.properties" and cracked: config_data = config_data.replace("online-mode=true","online-mode=false")
        open(path, 'w', encoding='utf-8').write(config_data)

    # [ updating configs ] try all and ignore errors

    for path in configs:
        try: config_updater(path)
        except: pass

    # [ updating configs ] try all without ignoring errors

    for path in configs:
        while True:
            try: config_updater(path); break
            except:
                choice = input(clr(f"\n{err(sys.exc_info())}\n\n  > Press [ ENTER ] to retry or type \"skip\" to skip: ", 2))
                if choice == "skip": break

    if playit:
        print_read_me(); input(clr("\n  > It is extremely easy to setup playit.gg\n\n  > After server setup is complete, start your server.\n\n  > Click on the URL displayed on the console.\n\n  > Create an account and login if you haven't already to save the tunnel.\n\n  > Click \"Add Agent\"\n\n  > A tunnel will be created and your server's public ip will be displayed: example.craft.playit.gg\n\n  > Press [ ENTER ] after you have read the message... "))  
    else:
        print(clr("\n  > As you have not selected playit.gg as a host, To allow players to connect to your server over the internet, follow this tutorial on port-forwarding."))
        if input(clr("\n  > Open port forwarding tutorial on youtube? [ y / n ]: ") + magenta).lower() == "y":
            sys_open('https://youtu.be/X75GbRaGzu8')

    print_read_me(); input('\n  > If you would like to transfer the server to a linux system and run it there, set "build-id: 0" inside "autoplug\\updater.yml"\n\n  > After you move the folder to a linux system, run "sudo chmod -R 777 folder_name"\n\n  > Run start_server.sh and then install jdk with ".check java"\n\n  > Press [ ENTER ] after you have read the message... ')

    # done!

    title("𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚋𝚞𝚒𝚕𝚍𝚎𝚛 [ 𝚌𝚘𝚖𝚙𝚕𝚎𝚝𝚎! ]")
    complete_banner = "\n\n\n\n ___  ___ _ ____   _____ _ __                 \n/ __|/ _ \\ '__\\ \\ / / _ \\ '__|                \n\\__ \\  __/ |   \\ V /  __/ |                   \n|___/\\___|_|    \\_/ \\___|_|                   \n\n                     _   _                    \n  ___ _ __ ___  __ _| |_(_) ___  _ __         \n / __| '__/ _ \\/ _` | __| |/ _ \\| '_ \\        \n| (__| | |  __/ (_| | |_| | (_) | | | |       \n \\___|_|  \\___|\\__,_|\\__|_|\\___/|_| |_|       \n\n                           _      _         _ \n  ___ ___  _ __ ___  _ __ | | ___| |_ ___  / \\\n / __/ _ \\| '_ ` _ \\| '_ \\| |/ _ \\ __/ _ \\/  /\n| (_| (_) | | | | | | |_) | |  __/ ||  __/\\_/ \n \\___\\___/|_| |_| |_| .__/|_|\\___|\\__\\___\\/   \n                    |_|                       \n\n"
    cls(); print(align(clr(complete_banner,4))); time.sleep(5)
    sys_open('https://allmylinks.com/sir-dankenstein')

main_two()
