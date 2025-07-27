import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from dankware import align, clr, cls, cyan, fade, green_bright, magenta, white_bright, yellow_bright

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
# fmt: off
offsets_and_values = {
    0x00030170: 0x00,
    0x000A94D0: NOP, 0x000A94D1: NOP, 0x000A94D2: NOP, 0x000A94D3: NOP, 0x000A94D4: NOP, 0x000A94D5: NOP, 0x000A94D6: NOP, 0x000A94D7: NOP, 0x000A94D8: NOP, 0x000A94D9: NOP, 0x000A94DA: NOP, 0x000A94DB: NOP, 0x000A94DC: NOP, 0x000A94DD: NOP, 0x000A94DE: NOP, 0x000A94DF: NOP, 0x000A94E0: NOP, 0x000A94E1: NOP, 0x000A94E2: NOP, 0x000A94E3: NOP, 0x000A94E4: NOP, 0x000A94E5: NOP, 0x000A94E6: NOP, 0x000A94E7: NOP, 0x000A94E8: NOP, 0x000A94E9: NOP, 0x000A94EA: NOP, 0x000A94EB: NOP, 0x000A94EC: NOP, 0x000A94ED: NOP, 0x000A94EE: NOP, 0x000A94EF: NOP, 0x000A94F0: NOP, 0x000A94F1: NOP, 0x000A94F2: NOP, 0x000A94F3: NOP, 0x000A94F4: NOP, 0x000A94F5: NOP, 0x000A94F6: NOP, 0x000A94F7: NOP, 0x000A94F8: NOP, 0x000A94F9: NOP, 0x000A94FA: NOP, 0x000A94FB: NOP, 0x000A94FC: NOP, 0x000A94FD: NOP, 0x000A94FE: NOP, 0x000A94FF: NOP, 0x000A9500: NOP, 0x000A9501: NOP, 0x000A9502: NOP, 0x000A9503: NOP, 0x000A9504: NOP, 0x000A9505: NOP, 0x000A9506: NOP, 0x000A9507: NOP, 0x000A9508: NOP, 0x000A9509: NOP, 0x000A950A: NOP, 0x000A950B: NOP, 0x000A950C: NOP, 0x000A950D: NOP, 0x000A950E: NOP, 0x000A950F: NOP,
    0x001C6CCD: 0x02,
    0x001C6CE4: 0x00,
    0x001C6CFB: 0x00,
}
# fmt: on


def is_patched(data):
    for offset, value in offsets_and_values.items():
        if offset >= len(data) or data[offset] != value:
            return False
    return True


def patch_exe(file_path):
    os.chdir(os.path.dirname(file_path))
    file_name = "sublime_text.exe"
    with open(file_path, "rb") as f:
        data = f.read()

    if not is_patched(data):
        if not os.path.isfile(f"{file_name}.bak"):
            shutil.copy(file_name, f"{file_name}.bak")

        print(clr(f"[*] Patching: {file_name}...", colour_two=yellow_bright))
        print(clr(f"[*] File size: {len(data)} bytes", colour_two=cyan))

        patched_data = bytearray(data)
        for offset, value in offsets_and_values.items():
            if offset < len(patched_data):
                patched_data[offset] = value
                print(clr(f"[+] Patched {magenta}{hex(offset)}{white_bright} with {magenta}{hex(value)}", colour_two=magenta))

        while True:
            try:
                with open(file_path, "wb") as f:
                    f.write(patched_data)
                    break
            except PermissionError:
                input(clr("[!] Error: Sublime text is running! Press [ ENTER ] to terminate it and try again... ", 2))
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
    if "__compiled__" in globals() and "DANK_TOOL_VERSION" in os.environ:
        root.iconbitmap(os.path.join(os.path.dirname(__file__), "dankware.ico"))
    while True:
        print(clr("[*] Opening file selector...", colour_two=yellow_bright))
        input_file = askopenfilename(title="Select sublime_text.exe", filetypes=[("Sublime", "sublime_text.exe")], initialdir=("C:\\Program Files\\Sublime Text" if os.path.isdir("C:\\Program Files\\Sublime Text") else None), initialfile="sublime_text.exe").replace("/", "\\")
        if input_file.endswith("sublime_text.exe"):
            patch_exe(input_file)
            break


main()
