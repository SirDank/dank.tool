import os
import sys
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

# get available purpur versions and print

while True:
    try:
        version_list = requests.get("https://api.purpurmc.org/v2/purpur").json()['versions']
        print(clr(f'  > Available Purpur Versions: {", ".join(version_list)}')); break
    except: wait = input(clr("\n  > Failed to get purpur versions! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))

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

for file in ['server-icon.png', 'log4j2_17-111.xml', 'log4j2_112-116.xml', 'mcMMO.jar', 'Iris.jar']: # Iris 2.3.2
    to_download_urls.append(f"https://github.com/SirDank/dank.tool/raw/main/__assets__/dank.minecraft-server-builder/{file}")
    if '.jar' in file: to_download_filenames.append(f"plugins/{file}")
    else: to_download_filenames.append(file)

# spigot plugins 

spigot_plugins = {
  "ActionHealth": 2661,
  "BetterSleeping": 60837,
  "ChestSort": 59773,
  "Chunky": 81534,
  "Corpses": 96774,
  "Log4JExploitFix": 98243,
  "NeoPerformance": 103183,
  "PLayerNPC": 93625,
  "ProtocolLib": 1997,
  "SkinRestorer": 2124,
  "Spark": 57242,
  "TabTPS": 82528,
  "TreeAssist": 67436,
}

for plugin in spigot_plugins:
    to_download_urls.append(f"https://api.spiget.org/v2/resources/{spigot_plugins[plugin]}/download")
    to_download_filenames.append(f"plugins/{plugin}.jar")

def github_file_selector(url, mode, name_list, plugin = True):
    
    for file_url in github_downloads(f"https://api.github.com/repos/{url}/releases/latest"):
        if mode == "add": valid = False
        elif mode == "remove": valid = True
        for name in name_list:
            if name in file_url.split('/')[-1]:
                if mode == "add": valid = True
                elif mode == "remove": valid = False
        if valid:
            to_download_urls.append(file_url)
            if plugin: to_download_filenames.append(f"plugins/{file_url.split('/')[-1]}")
            else: to_download_filenames.append(file_url.split('/')[-1])

# github plugins

# > EssentialsX
github_file_selector("EssentialsX/Essentials", "remove", ['AntiBuild', 'Discord', 'GeoIP', 'Protect', 'XMPP'])
# > ProtocolLib.jar > github_file_selector("dmulloy2/ProtocolLib", "add", ['ProtocolLib.jar'])
# > tabtps > github_file_selector("jpenilla/TabTPS", "add", ['spigot'])
# > BetterSleeping > github_file_selector("Nuytemans-Dieter/BetterSleeping", "add", ['BetterSleeping']) # "remove", [] WORKS AS WELL!
# > ActionHealth > github_file_selector("zeshan321/ActionHealth", "add", ['ActionHealth']) # "remove", [] WORKS AS WELL!
# > SkinRestorer > github_file_selector("SkinsRestorer/SkinsRestorerX", "add", ['SkinsRestorer']) # "remove", [] WORKS AS WELL!
# > PlayerNPC > github_file_selector("SergiFerry/PlayerNPC", "add", ['PlayerNPC']) # "remove", []) WORKS AS WELL!

# > playit.gg tunnel prorgram
if playit: github_file_selector("playit-cloud/playit-agent", "remove", ['apple-intel', 'apple-m1', 'unsigned', 'dmg'], False)

# > AutoPlug
to_download_urls.append("https://github.com/Osiris-Team/AutoPlug-Releases/raw/master/stable-builds/AutoPlug-Client.jar")
to_download_filenames.append("AutoPlug-Client.jar")

# > purpur.jar
to_download_urls.append(f"https://api.purpurmc.org/v2/purpur/{version}/latest/download")
to_download_filenames.append("purpur.jar")

# begin downloads

print(clr("\n  > Starting Multiple Downloads... [ this might take a few seconds ]"))

def downloader(url, filename):
    
    while True:
        try:
            data = requests.get(url, headers={'user-agent':'dankware'}, allow_redirects=True).content
            open(filename,"wb+").write(data); data = ""
            print(clr(f"\n  > Completed [ {filename} ]")); break
        except: wait = input(clr(f"\n  > Failed [ {filename} ]! Press {white}ENTER{red} to try again... ",2))

start_time = time.time()
multithread(downloader, 2, to_download_urls, to_download_filenames, False)
time_taken = int(time.time()-start_time)

cls(); print(clr(f"\n  > Finished downloads in {magenta}{time_taken}{white} seconds! Sleeping {magenta}5{white} seconds...")); time.sleep(5)

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
    start-command: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true {extra_flag}-jar purpur.jar -nogui
''')

# WORKING: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true {extra_flag}-jar purpur.jar -nogui
# BROKEN: java -Xms256M -Xmx{ram}M -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:MaxGCPauseMillis=200 -XX:+DisableExplicitGC -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCLiveThresholdPercent=90 -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -Dterminal.jline=false -Dterminal.ansi=true -XX:+UnlockDiagnosticVMOptions -XX:-UseBiasedLocking -XX:UseAVX=3 -XX:+UseStringDeduplication -XX:+UseFastUnorderedTimeStamps -XX:+UseAES -XX:+UseAESIntrinsics -XX:UseSSE=4 -XX:+UseFMA -XX:AllocatePrefetchStyle=1 -XX:+UseLoopPredicate -XX:+RangeCheckElimination -XX:+EliminateLocks -XX:+DoEscapeAnalysis -XX:+UseCodeCacheFlushing -XX:+SegmentedCodeCache -XX:+UseFastJNIAccessors -XX:+OptimizeStringConcat -XX:+UseCompressedOops -XX:+UseThreadPriorities -XX:+OmitStackTraceInFastThrow -XX:+TrustFinalNonStaticFields -XX:ThreadPriorityPolicy=1 -XX:+UseInlineCaches -XX:+RewriteBytecodes -XX:+RewriteFrequentPairs -XX:+UseNUMA -XX:-DontCompileHugeMethods -XX:+UseFPUForSpilling -XX:+UseFastStosb -XX:+UseNewLongLShift -XX:+UseVectorCmov -XX:+UseXMMForArrayCopy -XX:+UseXmmI2D -XX:+UseXmmI2F -XX:+UseXmmLoadAndClearUpper -XX:+UseXmmRegToRegMoveAll -Dfile.encoding=UTF-8 -Xlog:async -Djava.security.egd=file:/dev/urandom --add-modules jdk.incubator.vector {extra_flag}-jar purpur.jar -nogui

open('autoplug/updater.yml', 'w+').write(f'''
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
''')

# one-time setup

if playit:

    for file in github_downloads("https://api.github.com/repos/playit-cloud/playit-agent/releases/latest"):
        if "signed" in file and not "unsigned" in file: playit_filename = str(file.split('/')[-1])
    open("start_tunnel.cmd","w+").write(f'@echo off\ntitle Minecraft Java Playit.gg Tunnel [ {name} - {version} ] Keep me running to allow players to join your server!\n{playit_filename}\npause')

    time.sleep(3); print_read_me(); print(clr(f"\n  > To allow players to connect to your server you first need to create a tunnel.\n\n  > Follow the steps on {magenta}imgur{white} and complete the one-time setup.\n\n  > If it does not open, please go to [ https://imgur.com/a/W30s7bw ] and [ https://playit.gg/manage ] manually.\n\n  > Opening in 10s..."))
    time.sleep(10); os.system("start https://imgur.com/a/W30s7bw")
    time.sleep(10); os.system("start https://playit.gg/manage")
    print(clr("\n  > To start your server, run start_server.cmd\n\n  > To start your tunnel so people can connect over the internet, run start_tunnel.cmd"))
    wait = input(clr("\n  > After you have read the above and created a tunnel, press [ ENTER ] "))
 
else:
    
    print(clr("\n  > As you have not selected playit.gg as a host, To allow players to connect to your server over the internet, follow this tutorial on port-forwarding."))
    if input(clr("\n  > Open port forwarding tutorial on youtube? [ y / n ]: ") + magenta).lower() == "y": os.system("start https://youtu.be/X75GbRaGzu8")

# start server and shutdown server for optimizing the below settings

server_properties_config = {
    "simulation-distance=10": "simulation-distance=4",
    "motd=A Minecraft Server": f"motd=\\u00A7a---\\u00A76>\\u00A7b\\u00A7l {name} \\u00A76<\\u00A7a---\\u00A7r\\n   \\u00A76\\u00A7l\\u00A7m-----\\u00A79\\u00A78\\u00A7l[\\u00A75 Made with \\u00A7ddank\\u00A7f.\\u00A7dserverbuilder \\u00A78\\u00A7l]\\u00A76\\u00A7l\\u00A7m-----",
    "server-name=Unknown Server": f"server-name={name}",
    # "view-distance=10": "view-distance=8",
    # resource-pack-prompt=
    # resource-pack=
    # resource-pack-sha1=
}

purpur_config = {
    "use-alternate-keepalive: false": "use-alternate-keepalive: true",
    "aggressive-towards-villager-when-lagging: true": "aggressive-towards-villager-when-lagging: false",
    "brain-ticks: 1": "brain-ticks: 2",
    "lobotomize\n          enabled: false": "lobotomize\n          enabled: true",
    "teleport-if-outside-border: false": "teleport-if-outside-border: true",
}

spigot_config = {
    "merge-radius:\n      item: 2.5\n      exp: 3.0": "merge-radius:\n      item: 3.5\n      exp: 4.0",
    # "mob-spawn-range: 8": "mob-spawn-range: 2",
    # "entity-activation-range\n      animals: 32\n      monsters: 32\n      raiders: 48\n      misc: 16\n      water: 16\n      villagers: 32\n      flying-monsters: 32": "entity-activation-range\n      animals: 16\n      monsters: 24\n      raiders: 48\n      misc: 8\n      water: 8\n      villagers: 16\n      flying-monsters: 32"
}

paper_world_defaults_config = {
    "prevent-moving-into-unloaded-chunks: false": "prevent-moving-into-unloaded-chunks: true",
    "alt-item-despawn-rate:\n      enabled: false\n      items:\n        cobblestone: 300": "alt-item-despawn-rate:\n      enabled: true\n      items:\n        cobblestone: 300\n        netherrack: 300\n        sand: 300\n        red_sand: 300\n        gravel: 300\n        dirt: 300\n        grass: 300\n        pumpkin: 300\n        melon_slice: 300\n        kelp: 300\n        bamboo: 300\n        sugar_cane: 300\n        twisting_vines: 300\n        weeping_vines: 300\n        oak_leaves: 300\n        spruce_leaves: 300\n        birch_leaves: 300\n        jungle_leaves: 300\n        acacia_leaves: 300\n        dark_oak_leaves: 300\n        mangrove_leaves: 300\n        cactus: 300\n        diorite: 300\n        granite: 300\n        andesite: 300\n        scaffolding: 600",
    "redstone-implementation: VANILLA": "redstone-implementation: ALTERNATE_CURRENT",
    "optimize-explosions: false": "optimize-explosions: true",
    # "max-auto-save-chunks-per-tick: 24": "max-auto-save-chunks-per-tick: 8",
}

pufferfish_config = {
    "dab:\n  enabled: false": "dab:\n  enabled: true",
    "inactive-goal-selector-throttle: false": "inactive-goal-selector-throttle: true",
}

essentials_config = {
    "nickname-prefix: '~'": "nickname-prefix: ''",
    "ignore-colors-in-max-nick-length: false": "ignore-colors-in-max-nick-length: true",
    'custom-join-message: "none"': 'custom-join-message: "&8&l[&a+&8&l]&a&l {PLAYER}"',
    'custom-quit-message: "none"': 'custom-quit-message: "&8&l[&c-&8&l]&c&l {PLAYER}"',
    "format: '<{DISPLAYNAME}> {MESSAGE}'": "format: '&6[&a{DISPLAYNAME}&6] ➤ &b{MESSAGE}'",
    "announce-format: '&dWelcome {DISPLAYNAME}&d to the server!'": "announce-format: '&dWelcome &6&l{DISPLAYNAME}&d to the server!'",
}

while not os.path.exists("server.properties") or not os.path.exists("purpur.yml") or not os.path.exists("config/paper-world-defaults.yml") or not os.path.exists("spigot.yml") or not os.path.exists("bukkit.yml"):
    cls(); input(clr("\n  > Start the server once ( it will stop automatically on the first run ) to generate config files to be optimized\n\n  > Start your server using start_server.cmd / start_server.sh\n\n  > After your server has stopped, press [ ENTER ] "))
    try:
        purpur = open("purpur.yml", "r").read()
        spigot = open("spigot.yml", "r").read()
        pufferfish = open("pufferfish.yml", "r").read()
        server_properties = open("server.properties", "r").read()
        essentials = open("plugins/Essentials/config.yml", "r").read()
        paper_world_defaults = open("config/paper-world-defaults.yml", "r").read()

        for setting in purpur_config: purpur = purpur.replace(setting, purpur_config[setting])
        for setting in spigot_config: spigot = spigot.replace(setting, spigot_config[setting])
        for setting in pufferfish_config: pufferfish = pufferfish.replace(setting, pufferfish_config[setting])
        for setting in essentials_config: essentials = essentials.replace(setting, essentials_config[setting])
        for setting in server_properties_config: server_properties = server_properties.replace(setting, server_properties_config[setting])
        for setting in paper_world_defaults_config: paper_world_defaults = paper_world_defaults.replace(setting, paper_world_defaults_config[setting])
        if cracked: server_properties = server_properties.replace("online-mode=true","online-mode=true")

        open("purpur.yml", "w", encoding='utf-8').write(purpur)
        open("spigot.yml", "w", encoding='utf-8').write(spigot)
        open("pufferfish.yml", "w", encoding='utf-8').write(pufferfish)
        open("server.properties", "w", encoding='utf-8').write(server_properties)
        open("plugins/Essentials/config.yml", "w", encoding='utf-8').write(essentials)
        open("config/paper-world-defaults.yml", "w", encoding='utf-8').write(paper_world_defaults)
        break

    except Exception as exp:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(clr(f"\n  > Error: {str(exp)} | {exc_type} | Line: {exc_tb.tb_lineno}",2))
        time.sleep(5)

# done!

title("dank.serverbuilder [ complete! ]")
complete = "\n\n\n\n ___  ___ _ ____   _____ _ __                 \n/ __|/ _ \\ '__\\ \\ / / _ \\ '__|                \n\\__ \\  __/ |   \\ V /  __/ |                   \n|___/\\___|_|    \\_/ \\___|_|                   \n\n                     _   _                    \n  ___ _ __ ___  __ _| |_(_) ___  _ __         \n / __| '__/ _ \\/ _` | __| |/ _ \\| '_ \\        \n| (__| | |  __/ (_| | |_| | (_) | | | |       \n \\___|_|  \\___|\\__,_|\\__|_|\\___/|_| |_|       \n\n                           _      _         _ \n  ___ ___  _ __ ___  _ __ | | ___| |_ ___  / \\\n / __/ _ \\| '_ ` _ \\| '_ \\| |/ _ \\ __/ _ \\/  /\n| (_| (_) | | | | | | |_) | |  __/ ||  __/\\_/ \n \\___\\___/|_| |_| |_| .__/|_|\\___|\\__\\___\\/   \n                    |_|                       \n\n"
cls(); print(align(clr_banner(complete)))
time.sleep(5); os.system("start https://allmylinks.com/sir-dankenstein")

