import os
import subprocess

# Inject standard System32 paths on Windows
if os.name == "nt":
    system32 = os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "System32")
    powershell_dir = os.path.join(system32, "WindowsPowerShell", "v1.0")
    paths = os.environ.get("PATH", "").split(os.pathsep)
    for path_dir in (system32, powershell_dir, os.environ.get("SystemRoot", "C:\\Windows")):
        if path_dir and path_dir not in paths:
            paths.append(path_dir)
    os.environ["PATH"] = os.pathsep.join(paths)

import time
from subprocess import CalledProcessError

from dankware import clr, cls
from rich.align import Align
from rich.console import Console
from translatepy import Translator


def resolve_cmd(cmd):
    if os.name == 'nt':
        if os.path.isabs(cmd) or not cmd.endswith(('.exe', '')):
            return cmd
        win_dir = os.environ.get('SystemRoot', 'C:\\Windows')
        candidates = []
        if cmd.lower() in ('taskkill', 'taskkill.exe'):
            candidates = [os.path.join(win_dir, 'System32', 'taskkill.exe')]
        elif cmd.lower() in ('powershell', 'powershell.exe'):
            candidates = [os.path.join(win_dir, 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe')]
        elif cmd.lower() in ('runas', 'runas.exe'):
            candidates = [os.path.join(win_dir, 'System32', 'runas.exe')]
        for c in candidates:
            if os.path.isfile(c):
                return c
    return cmd

def run_command(command_list, check=True, capture=False, suppress_output=False):
    if not command_list:
        return
        
    command_list = list(command_list)
    command_list[0] = resolve_cmd(command_list[0])
    
    # Check if we should bypass runas (e.g. if we are not admin)
    if command_list[0].lower().endswith('runas.exe') or command_list[0] == 'runas':
        is_admin = False
        if os.name == 'nt':
            import ctypes
            try:
                is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                pass
        
        if not is_admin:
            # Bypass runas and run the command payload directly
            cmd_payload = command_list[-1]
            if os.name == 'nt':
                command_list = ["cmd.exe", "/c", cmd_payload]
            else:
                command_list = cmd_payload.split()
            command_list[0] = resolve_cmd(command_list[0])

    try:
        stdout_pipe = subprocess.DEVNULL if suppress_output else None
        stderr_pipe = subprocess.DEVNULL if suppress_output else None
        subprocess.run(
            command_list,
            check=check,
            text=True,
            stdout=stdout_pipe,
            stderr=stderr_pipe,
            capture_output=capture,
        )
    except (FileNotFoundError, PermissionError) as exc:
        # Fallback if runas wrapper failed
        if command_list[0].lower().endswith('runas.exe') or command_list[0] == 'runas':
            cmd_payload = command_list[-1]
            fallback_cmd = ["cmd.exe", "/c", cmd_payload] if os.name == 'nt' else cmd_payload.split()
            fallback_cmd[0] = resolve_cmd(fallback_cmd[0])
            try:
                subprocess.run(
                    fallback_cmd,
                    check=check,
                    text=True,
                    stdout=stdout_pipe,
                    stderr=stderr_pipe,
                    capture_output=capture,
                )
                return
            except Exception as fallback_exc:
                raise fallback_exc
        
        if isinstance(exc, FileNotFoundError):
            raise FileNotFoundError(f"Command not found: '{command_list[0]}'. Make sure it's in your system PATH.") from exc
        raise exc


def translate(text):
    if DANK_TOOL_LANG:
        try:
            global translator
            # Lazy initialize the Translator to avoid blocking the module at startup
            if translator is None:
                translator = Translator()
            text = translator.translate(text, DANK_TOOL_LANG, "en").result
        except:
            pass
    return text


def main():
    global DANK_TOOL_LANG, translator

    # check if translator is enabled (dank.tool.exe)

    try:
        DANK_TOOL_LANG = os.environ["DANK_TOOL_LANG"]
        if DANK_TOOL_LANG == "en":
            DANK_TOOL_LANG = ""
        else:
            translator = None
    except:
        DANK_TOOL_LANG = ""

    # banner

    banner1 = "\n\n .oooooo..o          amd64fox's      .   ooooooo  ooooo \nd8P'    `Y8                        .o8    `8888    d8'  \nY88bo.      oo.ooooo.   .ooooo.  .o888oo    Y888..8P    \n `\"Y8888o.   888' `88b d88' `88b   888       `8888'     \n     `\"Y88b  888   888 888   888   888      .8PY888.    \noo     .d8P  888   888 888   888   888 .   d8'  `888b   \n8\"\"88888P'   888bod8P' `Y8bod8P'   \"888\" o888o  o88888o \n             888                                        \n            o888o                                       \n"
    banner2 = '\nMP""""""`MM          oo                     dP   oo .8888b          \nM  mmmmm..M                                 88      88   "          \nM.      `YM 88d888b. dP .d8888b. .d8888b. d8888P dP 88aaa  dP    dP \nMMMMMMM.  M 88\'  `88 88 88\'  `"" 88ooood8   88   88 88     88    88 \nM. .MMM\'  M 88.  .88 88 88.  ... 88.  ...   88   88 88     88.  .88 \nMb.     .dM 88Y888P\' dP `88888P\' `88888P\'   dP   dP dP     `8888P88 \nMMMMMMMMMMM 88                                                  .88 \n            dP                                              d8888P  \n\n\n'

    cls()
    console = Console(highlight=False)
    console.print(Align.center(banner1), style="blink green3")
    console.print(Align.center("+"), style="blink red")
    console.print(Align.center(banner2), style="blink dark_orange")
    print(clr(f"\n  - {translate('Credits to amd64fox & spicetify contributors!')}"))
    input(clr(f"\n  > {translate('Hit [ ENTER ] to begin installation...')} "))

    # main

    cls()
    print(clr(f"\n  - {translate('terminating Spotify...')}\n"))
    run_command(
        ["taskkill", "/f", "/t", "/im", "spotify.exe"],
        check=False,
        suppress_output=True,
    )

    # Spicetify restore

    print(clr(f"\n  - {translate('restoring Spotify...')}\n"))
    run_command(["runas", "/trustlevel:0x20000", "spicetify restore"], check=False)

    # SpotX

    # translated = translate("installing SpotX...\n\n  [ RECOMMENDED SETTINGS ]\n  - Install Over\n  - Disable Podcasts\n  - Block Updates")
    # print(clr(f"\n  - {translated}"))
    print(clr(f"\n  - {translate('SpotX is currently being detected as a virus by windows defender, it is a false positive, the easiest way to fix this is to TEMPORARILY disable real-time protection in windows defender!')}\n"))
    run_command(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "iex \"& { $(iwr -useb 'https://raw.githubusercontent.com/SpotX-Official/spotx-official.github.io/main/run.ps1') } -confirm_uninstall_ms_spoti -confirm_spoti_recomended_over -podcasts_off -block_update_on -start_spoti -new_theme -adsections_off -lyrics_stat spotify\"",
        ],
        check=True,
    )

    input(clr(f"  > {translate('Hit [ ENTER ] if you are signed in to Spotify...')} "))

    print(clr(f"\n  - {translate('terminating Spotify...')}\n"))
    run_command(
        ["taskkill", "/f", "/t", "/im", "spotify.exe"],
        check=False,
        suppress_output=True,
    )

    # Spicetify

    print(clr(f"\n  - {translate('installing Spicetify-CLI...')}\n"))
    run_command(
        [
            "runas",
            "/trustlevel:0x20000",
            'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -UseBasicParsing https://raw.githubusercontent.com/spicetify/cli/main/install.ps1 | iex"',
        ],
        check=True,
    )
    input(clr(f"  > {translate('Hit [ ENTER ] only after the new window has closed...')} "))

    translated = translate("[ SUGGESTED EXTENSIONS / THEMES ]\n  - Extension: Beautiful Lyrics\n  - Extension: Cat-Jam Synced\n  - Theme: Lucid")
    print(clr(f"\n  {translated}"))

    print(clr(f"\n  - {translate('Sleeping for 5 seconds...')}\n"))
    time.sleep(5)


try:
    main()
except CalledProcessError:
    print(
        clr(
            f"\n  - {translate('Known error occurred! Your system is unique, I need you to join my discord server and help me fix this error!')} ",
            2,
        )
    )
    input(clr(f"  > {translate('Hit [ ENTER ] to go back to the main menu')}... "))
