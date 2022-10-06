import os
import time
from dankware import title, cls, clr, clr_banner, align

def main():
    
    title("dank.spotx-windows"); banner = '\n\n\n .oooooo..o          amd64fox\'s      .   ooooooo  ooooo \nd8P\'    `Y8                        .o8    `8888    d8\'  \nY88bo.      oo.ooooo.   .ooooo.  .o888oo    Y888..8P    \n `"Y8888o.   888\' `88b d88\' `88b   888       `8888\'     \n     `"Y88b  888   888 888   888   888      .8PY888.    \noo     .d8P  888   888 888   888   888 .   d8\'  `888b   \n8""88888P\'   888bod8P\' `Y8bod8P\'   "888" o888o  o88888o \n             888                                        \n            o888o                                       \n                                                        \n'
    cls(); print(align(clr_banner(banner)))
    wait = input(clr("\n  > Hit [ ENTER ] to begin installation..."))
    while True:
        cls()
        try: os.system('powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12}"; "& {(Invoke-WebRequest -UseBasicParsing \'https://raw.githubusercontent.com/SpotX-CLI/SpotX-Win/main/Install.ps1\').Content | Invoke-Expression} -confirm_uninstall_ms_spoti -confirm_spoti_recomended_over -podcasts_off -cache_off -block_update_on -start_spoti"'); break
        except Exception as exc: wait = input(clr(f"\n  > ERROR: {str(exc)}\n\n  > Failed to launch! Make sure you are connected to the Internet! Press [ENTER] to try again... ",2))
    time.sleep(5)

if __name__ == "__main__": main()