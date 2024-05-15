import os
from rich.align import Align
from dankware import cls, clr
from rich.console import Console
from translatepy import Translator

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

    # banner

    cls()
    os.chdir(os.path.dirname(__file__))
    banner = "\n\n                                                          __    _______ _______ _______ \n.--------.---.-.-----.-----.-----.----.---.-.--.--.-----.|  |  |   |   |   _   |     __|\n|        |  _  |__ --|__ --|  _  |   _|  _  |  |  |  -__||  |__|       |       |__     |\n|__|__|__|___._|_____|_____|___  |__| |___._|\\___/|_____||__|__|__|_|__|___|___|_______|\n                           |_____|                                                      \n"
    Console().print(Align.center(banner), style="blink red", highlight=False)
    print(clr(f"\n  - {translate('Credits to massgravel team!')}"))
    input(clr(f"\n  > {translate('Hit [ ENTER ] to begin Microsoft-Activation-Script...')} "))

    # main

    cls(); print(clr(f"\n  - {translate('Exit inside the MAS window to return to the menu...')}"))
    os.system('powershell -Command "irm https://massgrave.dev/get | iex"')

if __name__ == "__main__":
    main()

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('main', 'translate', 'translator'):
            if _ in globals(): del globals()[_]
