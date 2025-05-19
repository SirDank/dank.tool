import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from dankware import align, fade, cls, clr, yellow_bright, cyan, magenta, green_bright, white_bright

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

Sublime Text 4.1.9.2 Build 4192 Patcher

"""

NOP = 0x90
offsets_and_values = {
    0x000035FE: 0x01,
    0x0000361D: 0x95,
    0x0000361E: 0x9E,
    0x0000361F: 0x57,
    0x00080F00: NOP, 0x00080EFF: NOP, 0x00080F01: NOP, 0x00080F02: NOP, 0x00080F03: NOP, 0x00080F04: NOP, 0x00080F05: NOP, 0x00080F06: NOP, 0x00080F07: NOP, 0x00080F08: NOP, 0x00080F09: NOP, 0x00080F0A: NOP, 0x00080F0B: NOP, 0x00080F0C: NOP, 0x00080F0D: NOP, 0x00080F0E: NOP, 0x00080F0F: NOP, 0x00080F10: NOP, 0x00080F11: NOP, 0x00080F12: NOP, 0x00080F13: NOP, 0x00080F14: NOP, 0x00080F15: NOP, 0x00080F16: NOP, 0x00080F17: NOP, 0x00080F18: NOP, 0x00080F19: NOP, 0x00080F1A: NOP, 0x00080F1B: NOP, 0x00080F1C: NOP, 0x00080F1D: NOP, 0x00080F1E: NOP, 0x00080F1F: NOP, 0x00080F20: NOP, 0x00080F21: NOP, 0x00080F22: NOP, 0x00080F23: NOP, 0x00080F24: NOP, 0x00080F25: NOP, 0x00080F26: NOP, 0x00080F27: NOP, 0x00080F28: NOP, 0x00080F29: NOP, 0x00080F2A: NOP, 0x00080F2B: NOP, 0x00080F2C: NOP, 0x00080F2D: NOP, 0x00080F2E: NOP, 0x00080F2F: NOP, 0x00080F30: NOP, 0x00080F31: NOP, 0x00080F32: NOP, 0x00080F33: NOP, 0x00080F34: NOP, 0x00080F35: NOP, 0x00080F36: NOP, 0x00080F37: NOP, 0x00080F38: NOP, 0x00080F39: NOP,
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
    0x0057C8C8: 0x65,
    0x001BFB05: 0x00
}

def is_patched(data):
    for offset, value in offsets_and_values.items():
        if offset >= len(data) or data[offset] != value:
            return False
    return True

def patch_exe(file_path):
    os.chdir(os.path.dirname(file_path))
    file_name = 'sublime_text.exe'
    with open(file_path, 'rb') as f:
        data = f.read()

    if not is_patched(data):

        if not os.path.isfile(f'{file_name}.bak'):
            shutil.copy(file_name, f'{file_name}.bak')

        print(clr(f"[*] Patching: {file_name}...", colour_two=yellow_bright))
        print(clr(f"[*] File size: {len(data)} bytes", colour_two=cyan))

        patched_data = bytearray(data)
        for offset, value in offsets_and_values.items():
            if offset < len(patched_data):
                patched_data[offset] = value
                print(clr(f"[+] Patched {magenta}{hex(offset)}{white_bright} with {magenta}{hex(value)}", colour_two=magenta))

        while True:
            try:
                with open(file_path, 'wb') as f:
                    f.write(patched_data)
                    break
            except PermissionError:
                input(clr("[!] Error: Sublime text is running! Press [ ENTER ] to terminate it and try again... ",2))
                os.system("taskkill /f /im sublime_text.exe >nul 2>&1")
        print(clr(f"[+] Patch applied successfully! Output saved to: {file_path}", colour_two=green_bright))

    else:
        print(clr("[!] This file is already patched!", colour_two=green_bright))

    input(clr("\n  > Press [ ENTER ] to return to the main menu... ", colour_two=cyan))

def main():
    cls()
    print(align(fade(BANNER, "green2yellow-v")))
    # replace with file_selector() after update
    root = Tk()
    root.withdraw()
    if '__compiled__' in globals() and "DANK_TOOL_VERSION" in os.environ:
        root.iconbitmap(os.path.join(os.path.dirname(__file__), "dankware.ico"))
    while True:
        print(clr("[*] Opening file selector...", colour_two=yellow_bright))
        input_file = askopenfilename(title='Select sublime_text.exe', filetypes=[('Sublime', 'sublime_text.exe')], initialdir=('C:\\Program Files\\Sublime Text' if os.path.isdir('C:\\Program Files\\Sublime Text') else None), initialfile='sublime_text.exe').replace("/", "\\")
        if input_file.endswith('sublime_text.exe'):
            patch_exe(input_file)
            break

main()
