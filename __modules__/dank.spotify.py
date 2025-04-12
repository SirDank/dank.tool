import os
import time
import subprocess
from rich.align import Align
from rich.console import Console
from dankware import cls, clr
from translatepy import Translator

def run_command(command_list, check=True, capture=False, suppress_output=False, retry=False):
    max_attempts = 3 if retry else 1
    attempt = 0

    while attempt < max_attempts:
        attempt += 1
        try:
            stdout_pipe = subprocess.DEVNULL if suppress_output else None
            stderr_pipe = subprocess.DEVNULL if suppress_output else None
            # Use capture_output=True only if capture=True to avoid potential memory issues with large output
            result = subprocess.run(
                command_list,
                check=check,
                text=True,
                stdout=stdout_pipe,
                stderr=stderr_pipe,
                capture_output=capture
            )
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Command not found: '{command_list[0]}'. Make sure it's in your system PATH.") from exc
        except subprocess.CalledProcessError as e:
            if retry and attempt < max_attempts:
                input(clr(f"  > [{command_list}] Command failed. Hit [ENTER] to retry... "))
                continue
            raise subprocess.CalledProcessError(
                returncode=e.returncode,
                cmd=e.cmd,
                output=e.output,
                stderr=e.stderr
            )
        except Exception as e:
            if retry and attempt < max_attempts:
                input(clr(f"  > [[{command_list}]] Command failed. Hit [ENTER] to retry... "))
                continue
            raise RuntimeError(f"An unexpected error occurred running command: {e}") from e

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

    banner1 = '\n\n .oooooo..o          amd64fox\'s      .   ooooooo  ooooo \nd8P\'    `Y8                        .o8    `8888    d8\'  \nY88bo.      oo.ooooo.   .ooooo.  .o888oo    Y888..8P    \n `"Y8888o.   888\' `88b d88\' `88b   888       `8888\'     \n     `"Y88b  888   888 888   888   888      .8PY888.    \noo     .d8P  888   888 888   888   888 .   d8\'  `888b   \n8""88888P\'   888bod8P\' `Y8bod8P\'   "888" o888o  o88888o \n             888                                        \n            o888o                                       \n'
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
    run_command(['taskkill', '/f', '/t', '/im', 'spotify.exe'], check=False, suppress_output=True)

    # Spicetify restore

    print(clr(f"\n  - {translate('restoring Spotify...')}\n"))
    run_command(['runas', '/trustlevel:0x20000', 'spicetify restore'], check=False)

    # SpotX

    translated = translate('installing SpotX...\n\n  [ RECOMMENDED SETTINGS ]\n  - Install Over\n  - Disable Podcasts\n  - Block Updates')
    print(clr(f"\n  - {translated}"))
    run_command(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', 'iex "& { $(iwr -useb \'https://raw.githubusercontent.com/SpotX-Official/spotx-official.github.io/main/run.ps1\') } -new_theme"'], check=True, retry=True)

    input(clr(f"  > {translate('Hit [ ENTER ] if you are signed in to Spotify...')} "))

    print(clr(f"\n  - {translate('terminating Spotify...')}\n"))
    run_command(['taskkill', '/f', '/t', '/im', 'spotify.exe'], check=False, suppress_output=True)

    # Spicetify

    print(clr(f"\n  - {translate('installing Spicetify-CLI...')}\n"))
    run_command(['runas', '/trustlevel:0x20000', 'powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -UseBasicParsing https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex"'], check=True, retry=True)

    input(clr(f"  > {translate('Hit [ ENTER ] after installing Spicetify...')} "))

    print(clr(f"\n  - {translate('applying Spicetify...')}\n"))
    run_command(['runas', '/trustlevel:0x20000', 'spicetify restore backup apply'], check=True, retry=True)

    input(clr(f"  > {translate('Hit [ ENTER ] after applying Spicetify...')} "))

    translated = translate("[ SUGGESTED EXTENSIONS / THEMES ]\n  - Extension: Beautiful Lyrics\n  - Theme: Bloom (darkmono)")
    print(clr(f"\n  {translated}"))
    print(clr(f"\n  - {translate('Sleeping for 5 seconds...')}\n"))
    time.sleep(5)

main()
