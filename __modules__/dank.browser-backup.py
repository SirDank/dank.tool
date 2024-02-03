import os
import sys
import winreg
import zipfile
import datetime
from psutil import process_iter
from translatepy import Translator
from dankware import white, white_normal, red, red_normal, red_dim
from dankware import title, cls, clr, err, align, rm_line, is_admin, export_registry_keys, get_path

from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn, TimeElapsedColumn

def translate(text):

    if DANK_TOOL_LANG:
        try: text = translator.translate(text, source_language='en', destination_language=DANK_TOOL_LANG).result
        except: pass
    return text

def chrome_installed():
    try:
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            winreg.QueryValueEx(key, "Path")
        return True
    except FileNotFoundError:
        return False

def backup(browser, compression_level):

    if browser == "Chrome":

        path_to_backup = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")

        # check if chrome is installed

        if not chrome_installed():
            cls(); print(clr(f"\n  - {translate('Chrome possibly not installed')}!",2))

        # set path to backup

        if not os.path.exists(path_to_backup):
            print(clr(f"\n  - {translate('Invalid Path')}: {path_to_backup}\n",2))
            while True:
                path_to_backup = input(clr(f"  > {translate('Input user data folder path')}: ")); rm_line()
                if os.path.exists(path_to_backup) and r"Google\Chrome\User Data" in path_to_backup: break

        # check if chrome is running

        while True:
            cls(); chrome_running = False
            for proc in process_iter(['name']):
                if proc.info['name'] == 'chrome.exe':
                    chrome_running = True; break
            if chrome_running: input(clr("\n  > Chrome is running! Terminate it and press [ENTER]... ",2))
            else: break

        # export registry keys

        cls(); print(clr(f"\n  - {translate('Exporting registry keys')}..."))
        export_registry_keys('HKEY_CURRENT_USER', r'Software\Google\Chrome\PreferenceMACs', export_path='chrome.reg')

        # compress files

        print(clr(f"\n  - {translate('Compressing... (this might take a few minutes)')}\n"))

        num_source_files = 0
        for root, dirs, files in os.walk(path_to_backup):
            for file in files:
                num_source_files += 1

        now = datetime.datetime.now()
        zip_name = f'chrome_{now.strftime("%d-%m-%Y")}_{now.strftime("%I-%M-%S-%p")}.zip'
        instructions = f'\n  - [INSTRUCTIONS TO TRANSFER]: \n\n  - Transfer {zip_name} to another computer\n  - Install chrome\n  - Exit chrome\n  - Open windows explorer\n  - Paste path [%LOCALAPPDATA%\\Google\\Chrome]\n  - Delete the [User Data] folder\n  - Move extracted [User Data] folder to [%LOCALAPPDATA%\\Google\\Chrome]\n  - Run [chrome.reg]\n  - Transfer Complete!'
        with open('instructions.txt', 'w', encoding='utf-8') as _:
            _.write(instructions)

        width = os.get_terminal_size().columns
        job_progress = Progress("{task.description}", SpinnerColumn(), BarColumn(bar_width=width), TextColumn("[progress.percentage][bright_green]{task.percentage:>3.0f}%"), "[bright_cyan]ETA", TimeRemainingColumn(), TimeElapsedColumn())
        overall_task = job_progress.add_task("[bright_green]Compressing", total=num_source_files)
        progress_table = Table.grid()
        progress_table.add_row(Panel.fit(job_progress, title="[bright_white]Jobs", border_style="bright_red", padding=(1, 2)))

        with Live(progress_table, refresh_per_second=10):
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, True, compression_level, strict_timestamps=False) as zipf:
                for root, dirs, files in os.walk(path_to_backup):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, path_to_backup)
                        zipf.write(file_path, os.path.join("User Data", rel_path))
                        job_progress.update(overall_task, advance=1)
                zipf.write("chrome.reg", "chrome.reg")
                zipf.write("instructions.txt", "instructions.txt")

        # cleanup

        print(clr("\n  - Cleaning..."))
        os.remove("chrome.reg")
        os.remove("instructions.txt")
        os.system(f'explorer.exe "{os.getcwd()}"')
        cls(); input(clr(instructions + '\n\n  > Press [ENTER] once you have read the steps... '))

    #elif browser == "Firefox"
    #elif browser == "Opera":
    #elif browser == "Brave":

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

    # banner, check if admin

    cls(); title("𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙"); banner = "\n\n                                                                             \n   _         _     _                                 _           _           \n _| |___ ___| |_  | |_ ___ ___ _ _ _ ___ ___ ___ ___| |_ ___ ___| |_ _ _ ___ \n| . | .'|   | '_|_| . |  _| . | | | |_ -| -_|  _|___| . | .'|  _| '_| | | . |\n|___|__,|_|_|_,_|_|___|_| |___|_____|___|___|_|     |___|__,|___|_,_|___|  _|\n                                                                        |_|  \n\n"
    try:
        if not is_admin(): raise RuntimeError(clr("Not executed as administrator! Exporting browser data and registry keys requires admin privileges!"))
    except: sys.exit(clr(err(sys.exc_info()),2))

    # folders

    try: os.chdir(get_path('Documents'))
    except: os.chdir("C:\\")
    try: os.makedirs('dank.browser-backup')
    except FileExistsError: pass
    os.chdir('dank.browser-backup')

    # user input

    browsers = ['Chrome']
    to_print = "  - Supported Browsers: \n"
    for _, browser in enumerate(browsers):
        to_print += f"\n  - [{_+1}] {browser}"

    print(align(clr(banner,4,colours=(white, white_normal, red, red_normal, red_dim))))
    print(clr(to_print))

    print("")
    while True:
        choice = input(clr("  > Enter choice: ") + red)
        if choice.isdigit() and int(choice) > 0 and int(choice) <= int(len(browsers)):
            choice = browsers[int(choice)-1]; break
        else: rm_line()

    #print("")
    #while True:
    #    password = input(clr("  > Enter backup password: ") + red)
    #    if password: break
    #    else: rm_line()

    print("")
    while True:
        compression_level = input(clr(f"  > {translate('Compression level (Fast/Best)')} [1/2]: ") + red).lower()
        if compression_level in ('1', 'fast'):
            compression_level = 0; break
        elif compression_level in ('2', 'best'):
            compression_level = 9; break
        else: rm_line()

    # backup

    backup(choice, compression_level)

if __name__ == "__main__":
    main()

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('chrome_installed', 'backup', 'main', 'translate', 'translator'):
            if _ in globals(): del globals()[_]
