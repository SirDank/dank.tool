import os
import time
from translatepy import Translator
from dankware import title, cls, clr, align
from dankware import white, white_normal, green, green_normal, green_dim, yellow, yellow_normal, yellow_dim

def translate(text):

    if DANK_TOOL_LANG:
        try: text = translator.translate(text, source_language='en', destination_language=DANK_TOOL_LANG).result
        except: pass
    return text

def main():
    
    global DANK_TOOL_LANG, translator
    
    # check if translator is enabled (dank.tool.exe)

    try:
        DANK_TOOL_LANG = os.environ['DANK_TOOL_LANG']
        if DANK_TOOL_LANG == 'en':
            DANK_TOOL_LANG = ''
        else:
            translator = Translator()
    except:
        DANK_TOOL_LANG = ''
        
    # banner
    
    title("𝚍𝚊𝚗𝚔.𝚜𝚙𝚘𝚝𝚒𝚏𝚢")
    banner1 = '\n\n\n .oooooo..o          amd64fox\'s      .   ooooooo  ooooo \nd8P\'    `Y8                        .o8    `8888    d8\'  \nY88bo.      oo.ooooo.   .ooooo.  .o888oo    Y888..8P    \n `"Y8888o.   888\' `88b d88\' `88b   888       `8888\'     \n     `"Y88b  888   888 888   888   888      .8PY888.    \noo     .d8P  888   888 888   888   888 .   d8\'  `888b   \n8""88888P\'   888bod8P\' `Y8bod8P\'   "888" o888o  o88888o \n             888                                        \n            o888o                                       \n                                                        \n'
    banner2 = '\n\nMP""""""`MM          oo                     dP   oo .8888b          \nM  mmmmm..M                                 88      88   "          \nM.      `YM 88d888b. dP .d8888b. .d8888b. d8888P dP 88aaa  dP    dP \nMMMMMMM.  M 88\'  `88 88 88\'  `"" 88ooood8   88   88 88     88    88 \nM. .MMM\'  M 88.  .88 88 88.  ... 88.  ...   88   88 88     88.  .88 \nMb.     .dM 88Y888P\' dP `88888P\' `88888P\'   dP   dP dP     `8888P88 \nMMMMMMMMMMM 88                                                  .88 \n            dP                                              d8888P  \n'
    
    cls(); print(align(clr(banner1,4,colours=[white, white_normal, green, green_normal, green_dim]) + align(clr('+')) + align(clr(banner2,4,colours=[white, white_normal, yellow, yellow_normal, yellow_dim]))))
    print(clr(f"\n  - {translate('NOTE: If you have never installed Spotify before, this will install it for you but you will need to sign in manually. In only this case you will need to re-run this module to complete the spicetify installation')}."))
    input(clr(f"\n  > {translate('Hit [ ENTER ] to begin installation')}... "))
    
    # main
    
    cls()
    print(clr(f"\n  - {translate('terminating Spotify')}...\n"))
    os.system('taskkill /f /im spotify.exe >nul 2>&1')
    print(clr(f"\n  - {translate('restoring Spotify')}...\n"))
    os.system('spicetify restore')
    print(clr("\n  - installing SpotX...\n\n  [ RECOMMENDED SETTINGS ]\n  - Install Over\n  - Disable Podcasts\n  - Enable Auto-Clear Cache (30d)\n  - Block Updates"))
    os.system('powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString(\'https://raw.githubusercontent.com/SpotX-Official/SpotX/main/run.ps1\'))} -confirm_uninstall_ms_spoti -confirm_spoti_recomended_over -podcasts_off -cache_on -block_update_on -start_spoti -new_theme -adsections_off -lyrics_stat spotify"')
    input(clr(f"  > {translate('Hit [ ENTER ] if you are signed in to Spotify')}... "))
    print(clr(f"\n  - {translate('terminating Spotify')}...\n"))
    os.system('taskkill /f /im spotify.exe >nul 2>&1')
    print(clr(f"\n  - {translate('installing Spicetify-CLI... (N to start installation)')}\n"))
    os.system('powershell -Command "& Invoke-WebRequest -UseBasicParsing https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex"')
    #print(clr(f"\n  - {translate('installing Spicetify-Marketplace')}...\n"))
    #os.system('powershell -Command "& iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1 | iex"')
    print(clr(f"\n  - {translate('applying Spicetify')}...\n"))
    os.system('spicetify restore backup apply')
    print(clr("\n  [ SUGGESTED EXTENSIONS / THEMES ]\n  - Extension: Beautiful Lyrics\n  - Theme: Bloom\n  - Theme: Retroblur (dream)"))
    print(clr(f"\n  - {translate('Sleeping for 5 seconds')}...\n"))
    time.sleep(5)
    #os.system('start cmd.exe @cmd /k "spicetify backup apply && timeout 5 && exit"')

if __name__ == "__main__":
    main()

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('main', 'translate', 'translator'):
            if _ in globals(): del _
