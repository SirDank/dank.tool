import sys
import os
import logging
from colorama import init, Fore, Back, Style
import time
from dankware import align, fade

offsets_and_values = {
        0x000035FE: 0x01,
        0x0000361D: 0x95,
        0x0000361E: 0x9E,
        0x0000361F: 0x57,
        0x0057C8B6: 0x70,
        0x0057C8B7: 0x61,
        0x0057C8B8: 0x74,
        0x0057C8B9: 0x63,
        0x0057C8BA: 0x68,
        0x0057C8BB: 0x65,
        0x0057C8BC: 0x64,
        0x0057C8BD: 0x20,
        0x0057C8BE: 0x62,
        0x0057C8BF: 0x79,
        0x0057C8C0: 0x20,
        0x0057C8C1: 0x30,
        0x0057C8C2: 0x78,
        0x0057C8C3: 0x6D,
        0x0057C8C4: 0x72,
        0x0057C8C5: 0x70,
        0x0057C8C6: 0x65,
        0x0057C8C7: 0x70,
        0x0057C8C8: 0x65
}

BANNER = """
 .d8888b.                                                                     
d88P  Y88b                                                                    
888    888                                                                    
888    888 888  888 88888b.d88b.  888d888 88888b.   .d88b.  88888b.   .d88b.  
 888    888 `Y8bd8P' 888 "888 "88b 888P"   888 "88b d8P  Y8b 888 "88b d8P  Y8b 
 888    888   X88K   888  888  888 888     888  888 88888888 888  888 88888888 
 Y88b  d88P .d8""8b. 888  888  888 888     888 d88P Y8b.     888 d88P Y8b.     
  "Y8888P"  888  888 888  888  888 888     88888P"   "Y8888  88888P"   "Y8888  
                                           888               888               
                                           888               888               
                                           888               888               
[>] Sublime Text 4.1.9.2 Build 4192 patcher
"""

# Initialize colorama
init(autoreset=True)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')


def patch_exe(input_file, output_file=None):
    output_file = output_file or f"{os.path.splitext(input_file)[0]}_patched.exe"
    try:
        logging.info(Fore.YELLOW + Back.BLACK + Style.BRIGHT + f"[*] Starting patching: {os.path.basename(input_file)}...")
        with open(input_file, 'rb') as f:
            data = f.read()
        patched_data = bytearray(data)
        logging.info(Fore.CYAN + f"[*] File size: {len(data)} bytes")
        
        for offset, value in offsets_and_values.items():
            if offset < len(patched_data):
                patched_data[offset] = value
                logging.info(Fore.MAGENTA + f"[+] Patched {hex(offset)} with {hex(value)}")
        
        with open(output_file, 'wb') as f:
            f.write(patched_data)
        
        logging.info(Fore.GREEN + Back.BLACK + Style.BRIGHT + f"[+] Patch applied successfully! Output saved to: {output_file}")
        logging.info(Fore.YELLOW + f"[*] Returning to the main menu...")
        time.sleep(1)

    except Exception as e:
        logging.error(Fore.RED + f"[-] Error: {e}")
    
    input(Fore.CYAN + "Press Enter to return to the main menu...")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(align(fade(BANNER, "green2yellow-v")))
    # RESET FORE
    input_file = input(Fore.CYAN + "Enter the input file path: " + Fore.RESET)
    output_file = input(Fore.CYAN + "Enter the output file path (or press Enter to use the default): " + Fore.RESET)

    patch_exe(input_file, output_file if output_file else None)

if __name__ == "__main__":
    main()