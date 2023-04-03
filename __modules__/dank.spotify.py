import os
import time
from dankware import title, cls, clr, align

def main():
    
    title("𝚍𝚊𝚗𝚔.𝚜𝚙𝚘𝚝𝚒𝚏𝚢")
    banner1 = '\n\n\n .oooooo..o          amd64fox\'s      .   ooooooo  ooooo \nd8P\'    `Y8                        .o8    `8888    d8\'  \nY88bo.      oo.ooooo.   .ooooo.  .o888oo    Y888..8P    \n `"Y8888o.   888\' `88b d88\' `88b   888       `8888\'     \n     `"Y88b  888   888 888   888   888      .8PY888.    \noo     .d8P  888   888 888   888   888 .   d8\'  `888b   \n8""88888P\'   888bod8P\' `Y8bod8P\'   "888" o888o  o88888o \n             888                                        \n            o888o                                       \n                                                        \n'
    banner2 = '\n\nMP""""""`MM          oo                     dP   oo .8888b          \nM  mmmmm..M                                 88      88   "          \nM.      `YM 88d888b. dP .d8888b. .d8888b. d8888P dP 88aaa  dP    dP \nMMMMMMM.  M 88\'  `88 88 88\'  `"" 88ooood8   88   88 88     88    88 \nM. .MMM\'  M 88.  .88 88 88.  ... 88.  ...   88   88 88     88.  .88 \nMb.     .dM 88Y888P\' dP `88888P\' `88888P\'   dP   dP dP     `8888P88 \nMMMMMMMMMMM 88                                                  .88 \n            dP                                              d8888P  \n'
    
    cls(); print(align(clr(banner1,4)) + align(clr('+')) + align(clr(banner2,4)))
    input(clr("\n  > Hit [ ENTER ] to begin installation..."))
    while True:
        cls()
        try:
            os.system('powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12}"; "& {(Invoke-WebRequest -UseBasicParsing \'https://raw.githubusercontent.com/amd64fox/SpotX/main/Install.ps1\').Content | Invoke-Expression} -confirm_uninstall_ms_spoti -confirm_spoti_recomended_over -podcasts_off -cache_on -block_update_on -start_spoti -new_theme -adsections_off -lyrics_stat spotify"; "& iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex"')
            os.system('start cmd.exe @cmd /k "spicetify restore backup apply"')
            break
        except: input(clr(f"\n  > Failed to launch! Make sure you are connected to the internet! Press [ENTER] to try again... ",2))
    time.sleep(5)

if __name__ == "__main__": main()
