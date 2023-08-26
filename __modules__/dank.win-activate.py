import os
from dankware import title, cls, clr, align
from dankware import white, white_normal, red, red_normal, red_dim

def main():
    
    title("𝚍𝚊𝚗𝚔.𝚠𝚒𝚗-𝚊𝚌𝚝𝚒𝚟𝚊𝚝𝚎")
    os.chdir(os.path.dirname(__file__))
    banner = "\n\n     __          __           _                   __  _           __     \n ___/ /__ ____  / /__ _    __(_)__  _______ _____/ /_(_)  _____ _/ /____ \n/ _  / _ `/ _ \\/  '_/| |/|/ / / _ \\/___/ _ `/ __/ __/ / |/ / _ `/ __/ -_)\n\\_,_/\\_,_/_//_/_/\\_(_)__,__/_/_//_/    \\_,_/\\__/\\__/_/|___/\\_,_/\\__/\\__/ \n                                                                         \n\n"

    cls(); print(clr(align(banner),4,colours=[white, white_normal, red, red_normal, red_dim]))
    input(clr("\n  > Hit [ ENTER ] to begin Microsoft-Activation-Script... "))
    while True:
        cls()
        try:
            print(clr("\n  > Exit inside the MAS window to return to the menu..."))
            os.system('powershell -Command "irm https://massgrave.dev/get | iex"')
            #data = requests.get("https://raw.githubusercontent.com/massgravel/Microsoft-Activation-Scripts/master/MAS/All-In-One-Version/MAS_AIO.cmd").content.decode()
            #open("MAS_AIO.cmd", "w").write(data)
            #os.system("MAS_AIO.cmd")
            break
        except: input(clr(f"\n  > Failed to launch! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))

if __name__ == "__main__":
    main()
    
    if "DANK_TOOL_VERSION" in os.environ:
        del main
