import os
import shutil
import requests
from translatepy import Translator
from dankware import title, cls, clr, align, rm_line
from dankware import white_normal, white_bright, red, red_normal, red_dim

def translate(text):
    if DANK_TOOL_LANG:
        try: text = translator.translate(text, source_language='en', destination_language=DANK_TOOL_LANG).result
        except: pass
    return text

def print_read_me():
    read_me = '\n\n:::::::::  ::::::::::     :::     :::::::::       ::::    ::::  ::::::::::\n:+:    :+: :+:          :+: :+:   :+:    :+:      +:+:+: :+:+:+ :+:       \n+:+    +:+ +:+         +:+   +:+  +:+    +:+      +:+ +:+:+ +:+ +:+       \n+#++:++#:  +#++:++#   +#++:++#++: +#+    +:+      +#+  +:+  +#+ +#++:++#  \n+#+    +#+ +#+        +#+     +#+ +#+    +#+      +#+       +#+ +#+       \n#+#    #+# #+#        #+#     #+# #+#    #+#      #+#       #+# #+#       \n###    ### ########## ###     ### #########       ###       ### ##########\n\n\n'
    cls(); print(align(read_me.replace(":",f"{white_normal}:").replace("+",f"{white_bright}+").replace("#",f"{red_normal}#")))

def file_downloader(url):
    file_name = url.split('/')[-1]
    while True:
        try:
            data = requests.get(url, headers={'User-Agent': 'dank.tool', 'Content-Type': 'application/json'}, timeout=3, allow_redirects=True).content
            with open(file_name,"wb") as _:
                _.write(data)
            break
        except Exception as exc:
            input(clr(f"\n  > {translate(f'Failed to download {file_name}! {exc} | Press ENTER to try again')}... ",2))
            rm_line(); rm_line()

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

    title("𝚍𝚊𝚗𝚔.𝚊𝚌𝚛𝚘𝚙𝚘𝚕𝚒𝚜")
    banner = '\n\n __                        __   __   __   __   __          __  \n|  \\  /\\  |\\ | |__/   /\\  /  ` |__) /  \\ |__) /  \\ |    | /__` \n|__/ /~~\\ | \\| |  \\ ./~~\\ \\__, |  \\ \\__/ |    \\__/ |___ | .__/ \n\n\n'
    cls(); print(clr(align(banner),4,colours=(red, red_dim)))
    print(clr("\n  - Credits to u/Verix- from r/GenP | Based on Acropolis v24.1"))
    print(clr(f"\n  - {translate('Uninstall Adobe Acrobat before proceeding')}!"))
    input(clr(f"\n  > {translate('Hit [ ENTER ] to begin installation')}... "))

    # folder

    cls()
    os.chdir(os.path.expandvars('%TEMP%'))
    if not os.path.isdir('dank.acropolis'):
        os.mkdir('dank.acropolis')
    os.chdir('dank.acropolis')

    # download installer

    if not os.path.isdir('Adobe Acrobat'):
        if not os.path.isfile('Acrobat_DC_Web_x64_WWMUI.zip'):
            print(clr(f"\n  - {translate('Downloading Acrobat Installer')}..."))
            file_downloader("https://trials.adobe.com/AdobeProducts/APRO/Acrobat_HelpX/win32/Acrobat_DC_Web_x64_WWMUI.zip")
        shutil.unpack_archive("Acrobat_DC_Web_x64_WWMUI.zip")

    # download patches

    if not os.path.isdir('Patches'):
        os.mkdir('Patches')
    os.chdir('Patches')
    patched_files = ('Acrobat.dll', 'acrodistdll.dll', 'acrotray.exe')
    for file in patched_files:
        if not os.path.isfile(file):
            print(clr(f"\n  - {translate(f'Downloading Patched {file}')}..."))
            file_downloader(f"https://github.com/SirDank/dank.tool/raw/main/__assets__/dank.acropolis/{file}")
    os.chdir('..')

    # banner, run installer

    print_read_me()
    print(clr(f"\n  - {translate('Keep default settings, do not change anything')}!"))
    #print(clr(f"\n  - {translate('Remember to uncheck Adobe Genuine Service (AGS) if you see it')}!"))
    print(clr(f"\n  - {translate('Click [ Install ] and then click [ Finish ]')}!"))
    input(clr(f"\n  > {translate('Hit [ ENTER ] to start installer')}... "))
    os.system('"Adobe Acrobat\\setup.exe" /quiet')

    # apply patches

    cls(); print(clr(f"\n  - {translate('Applying Patches')}..."))
    os.chdir('Patches')
    for file in patched_files:
        try: shutil.copy(file, f"C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\{file}")
        except:
            print(clr(f"\n  - {translate('Failed! Please manually copy and replace the file')}!\n\n  - [ {os.path.join(os.getcwd(), file)} ] > [ C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\{file} ]",2))
            input(clr(f"\n  > {translate('Hit [ ENTER ] after replacing the file')}... "))
    os.chdir('../..')

    # disable updater

    print(clr(f"\n  - {translate('Disabling Adobe Updater')}...\n"))
    os.system('sc config "AdobeARMservice" start= disabled')
    os.system('sc stop "AdobeARMservice"')

    # cleanup

    print(clr(f"\n  - {translate('Cleaning')}..."))
    shutil.rmtree('dank.acropolis')

    # banner

    print_read_me()
    print(clr(f"\n  - {translate('Open Adobe Acrobat, Go to: Menu > Preferences > Updater')}"))
    print(clr(f"\n  - {translate('Uncheck [ Automatically install updates ]')}"))
    input(clr(f"\n  > {translate('Hit [ ENTER ] after disabling automatic updates')}... "))

if __name__ == "__main__":
    main()

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('main', 'file_downloader', 'print_read_me', 'translate', 'translator'):
            if _ in globals(): del globals()[_]
