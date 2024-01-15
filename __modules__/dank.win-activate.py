import os
from translatepy import Translator
from dankware import title, cls, clr, align
from dankware import white, white_normal, red, red_normal, red_dim

def translate(text):

    if DANK_TOOL_LANG:
        try: text = translator.translate(text, source_language='en', destination_language=DANK_TOOL_LANG)
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
    
    title("𝚍𝚊𝚗𝚔.𝚠𝚒𝚗-𝚊𝚌𝚝𝚒𝚟𝚊𝚝𝚎")
    os.chdir(os.path.dirname(__file__))
    banner = "\n\n     __          __           _                   __  _           __     \n ___/ /__ ____  / /__ _    __(_)__  _______ _____/ /_(_)  _____ _/ /____ \n/ _  / _ `/ _ \\/  '_/| |/|/ / / _ \\/___/ _ `/ __/ __/ / |/ / _ `/ __/ -_)\n\\_,_/\\_,_/_//_/_/\\_(_)__,__/_/_//_/    \\_,_/\\__/\\__/_/|___/\\_,_/\\__/\\__/ \n                                                                         \n\n"

    cls(); print(clr(align(banner),4,colours=[white, white_normal, red, red_normal, red_dim]))
    print(clr(f"\n  - Credits to massgravel team!"))
    input(clr(f"\n  > {translate('Hit [ ENTER ] to begin Microsoft-Activation-Script')}... "))
    
    # main
    
    cls(); print(clr(f"\n  - {translate('Exit inside the MAS window to return to the menu')}..."))
    os.system('powershell -Command "irm https://massgrave.dev/get | iex"')

if __name__ == "__main__":
    main()
    
    if "DANK_TOOL_VERSION" in os.environ:
        del main, translate, translator
