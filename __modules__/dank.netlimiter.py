import os
import requests
from translatepy import Translator
from dankware import cls, clr, align, rm_line, red, red_dim

def translate(text):
    if DANK_TOOL_LANG:
        try: text = translator.translate(text, DANK_TOOL_LANG, 'en').result
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

    # init

    os.chdir(os.path.dirname(__file__))
    if not os.path.isdir('netlimiter'):
        os.mkdir('netlimiter')
    os.chdir('netlimiter')

    session = requests.Session()
    headers = {"User-Agent": f"dank.tool {os.environ['DANK_TOOL_VERSION']}"}
    banner = "\n\n     __     _     __ _           _ _                   ___           \n  /\\ \\ \\___| |_  / /(_)_ __ ___ (_) |_ ___ _ __       / _ \\_ __ ___  \n /  \\/ / _ \\ __|/ / | | '_ ` _ \\| | __/ _ \\ '__|____ / /_)/ '__/ _ \\ \n/ /\\  /  __/ |_/ /__| | | | | | | | ||  __/ | |_____/ ___/| | | (_) |\n\\_\\ \\/ \\___|\\__\\____/_|_| |_| |_|_|\\__\\___|_|       \\/    |_|  \\___/ \n\n\n"
    cls(); print(clr(align(banner),4,colours=(red, red_dim)))
    print(clr(f"\n  - {translate('Credits to Baseult!')}"))

    # main

    if os.path.isfile(r"C:\Program Files\Locktime Software\NetLimiter\NetLimiter.dll"):
        print(clr(f"\n  - {translate('NetLimiter found!')}"))
    else:
        print(clr(f"\n  - {translate('NetLimiter not found!')}\n\n  - {translate('Downloading NetLimiter...')}"))
        url = 'https://download.netlimiter.com' + session.get("https://www.netlimiter.com/download").content.decode().split('https://download.netlimiter.com',1)[1].split('"',1)[0]
        data = session.get(url, headers=headers).content
        with open('netlimiter.exe', 'wb') as file:
            file.write(data)

        os.system('netlimiter.exe')
        input(clr(f"\n  > {translate('Press [ ENTER ] after installing NetLimiter...')} "))

    sha = session.get("https://api.github.com/repos/Baseult/NetLimiterCrack/commits?path=NetLimiter%20Crack.exe&page=1&per_page=1", headers=headers).json()[0]['sha']

    def get_patcher():
        data = session.get("https://github.com/Baseult/NetLimiterCrack/raw/main/NetLimiter%20Crack.exe", headers=headers).content
        print(clr(f"\n  - {translate('NetLimiter-Patcher downloaded successfully!')}"))
        while True:
            try:
                with open('netlimiter-patcher.exe', 'wb') as file:
                    file.write(data)
                print(clr(f"\n  - {translate('NetLimiter-Patcher saved successfully!')}"))
                break
            except Exception as exc:
                input(clr(f"\n  > {translate('Failed to save NetLimiter-Patcher!')} {exc} | {translate('Press [ ENTER ] to try again...')} ",2))
                rm_line(); rm_line()

    if os.path.isfile('netlimiter-patcher.exe'):
        with open('sha.txt', 'r', encoding='utf-8') as file:
            _sha = file.read()
        if _sha == sha:
            print(clr(f"\n  - {translate('NetLimiter-Patcher is up-to-date!')}"))
        else:
            print(clr(f"\n  - {translate('Updating NetLimiter-Patcher...')}"))
            get_patcher()
            with open('sha.txt', 'w', encoding='utf-8') as file:
                file.write(sha)
    else:
        print(clr(f"\n  - {translate('Downloading NetLimiter-Patcher...')}"))
        get_patcher()
        with open('sha.txt', 'w', encoding='utf-8') as file:
            file.write(sha)

    input(clr(f"\n  > {translate('Hit [ ENTER ] to start NetLimiter-Patcher...')} "))
    cls(); print(clr(f"\n  - {translate('Close the patcher to return to the menu...')}"))
    os.system('netlimiter-patcher.exe')

if __name__ == "__main__":
    main()

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('main', 'translate', 'translator'):
            if _ in globals(): del globals()[_]
