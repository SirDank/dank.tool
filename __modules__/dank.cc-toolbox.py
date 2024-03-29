import os
from translatepy import Translator
from dankware import cls, clr, align
from dankware import red, red_dim

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

    os.chdir(os.path.dirname(__file__))
    banner = "\n\n _____         _____               _           _ _           \n|   __|___ ___|  _  |  ___ ___ ___| |_ ___ ___| | |_ ___ _ _ \n|  |  | -_|   |   __|_|  _|  _|___|  _| . | . | | . | . |_'_|\n|_____|___|_|_|__|  |_|___|___|   |_| |___|___|_|___|___|_,_|\n\n\n"

    cls(); print(clr(align(banner),4,colours=(red, red_dim)))
    print(clr(f"\n  - {translate('Credits to r/GenP team!')}"))
    input(clr(f"\n  > {translate('Hit [ ENTER ] to start CC-ToolBox')}... "))

    # main

    cls(); os.system('powershell -Command "irm dank-site.onrender.com/GenP/cc-toolbox-ps | iex"')

if __name__ == "__main__":
    main()

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('main', 'translate', 'translator'):
            if _ in globals(): del globals()[_]
