import datetime
import os
import subprocess
import sys
import winreg
import zipfile

from dankware import clr, cls, err, export_registry_keys, get_path, is_admin, red, rm_line
from psutil import process_iter
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table
from translatepy import Translator


def translate(text):
    if DANK_TOOL_LANG:
        try:
            text = translator.translate(text, DANK_TOOL_LANG, "en").result
        except:
            pass
    return text


browsers_config = {
    "Chrome": {
        "exe_name": "chrome.exe",
        "app_path_reg": r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
        "data_path": r"%LOCALAPPDATA%\Google\Chrome\User Data",
        "data_folder_name": "User Data",
        "reg_export_key": r"Software\Google\Chrome\PreferenceMACs",
        "reg_export_name": "chrome.reg",
        "transfer_instructions": "\n  - [INSTRUCTIONS TO TRANSFER]: \n\n  - Transfer {zip_name} to another computer\n  - Install Chrome\n  - Exit Chrome\n  - Open windows explorer\n  - Paste path [%LOCALAPPDATA%\\Google\\Chrome]\n  - Delete the [User Data] folder\n  - Move extracted [User Data] folder to [%LOCALAPPDATA%\\Google\\Chrome]\n  - Run [chrome.reg]\n  - Transfer Complete!"
    },
    "Firefox": {
        "exe_name": "firefox.exe",
        "app_path_reg": r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe",
        "data_path": r"%APPDATA%\Mozilla\Firefox\Profiles",
        "data_folder_name": "Profiles",
        "reg_export_key": None,
        "reg_export_name": None,
        "transfer_instructions": "\n  - [INSTRUCTIONS TO TRANSFER]: \n\n  - Transfer {zip_name} to another computer\n  - Install Firefox\n  - Exit Firefox\n  - Open windows explorer\n  - Paste path [%APPDATA%\\Mozilla\\Firefox]\n  - Delete the [Profiles] folder\n  - Move extracted [Profiles] folder to [%APPDATA%\\Mozilla\\Firefox]\n  - Transfer Complete!"
    },
    "Opera": {
        "exe_name": "opera.exe",
        "app_path_reg": r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\opera.exe",
        "data_path": r"%APPDATA%\Opera Software\Opera Stable",
        "data_folder_name": "Opera Stable",
        "reg_export_key": None,
        "reg_export_name": None,
        "transfer_instructions": "\n  - [INSTRUCTIONS TO TRANSFER]: \n\n  - Transfer {zip_name} to another computer\n  - Install Opera\n  - Exit Opera\n  - Open windows explorer\n  - Paste path [%APPDATA%\\Opera Software]\n  - Delete the [Opera Stable] folder\n  - Move extracted [Opera Stable] folder to [%APPDATA%\\Opera Software]\n  - Transfer Complete!"
    },
    "Brave": {
        "exe_name": "brave.exe",
        "app_path_reg": r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\brave.exe",
        "data_path": r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data",
        "data_folder_name": "User Data",
        "reg_export_key": None,
        "reg_export_name": None,
        "transfer_instructions": "\n  - [INSTRUCTIONS TO TRANSFER]: \n\n  - Transfer {zip_name} to another computer\n  - Install Brave\n  - Exit Brave\n  - Open windows explorer\n  - Paste path [%LOCALAPPDATA%\\BraveSoftware\\Brave-Browser]\n  - Delete the [User Data] folder\n  - Move extracted [User Data] folder to [%LOCALAPPDATA%\\BraveSoftware\\Brave-Browser]\n  - Transfer Complete!"
    }
}


def browser_installed(reg_path):
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            winreg.QueryValueEx(key, "Path")
        return True
    except FileNotFoundError:
        return False


def backup(browser, compression_level):
    config = browsers_config.get(browser)
    if not config:
        return

    path_to_backup = os.path.expandvars(config["data_path"])

    # check if browser is installed

    if not browser_installed(config["app_path_reg"]):
        cls()
        print(clr(f"\n  - {translate(browser + ' possibly not installed!')}", 2))

    # set path to backup

    if not os.path.exists(path_to_backup):
        print(clr(f"\n  - {translate('Invalid Path')}: {path_to_backup}\n", 2))
        while True:
            path_to_backup = input(clr(f"  > {translate('Input user data folder path')}: "))
            rm_line()
            # Basic validation to make sure the expected data folder name is in the path
            if os.path.exists(path_to_backup) and config["data_folder_name"] in path_to_backup:
                break

    # check if browser is running

    while True:
        cls()
        browser_running = False
        for proc in process_iter(["name"]):
            if proc.info["name"] == config["exe_name"]:
                browser_running = True
                break
        if browser_running:
            input(clr(f"\n  > {translate(browser + ' is running! Terminate it and press [ENTER]...')} ", 2))
        else:
            break

    # export registry keys (if any)

    if config["reg_export_key"]:
        cls()
        print(clr(f"\n  - {translate('Exporting registry keys...')}"))
        export_registry_keys("HKEY_CURRENT_USER", config["reg_export_key"], export_path=config["reg_export_name"])

    # compress files

    print(clr(f"\n  - {translate('Compressing... (this might take a few minutes)')}\n"))

    files_to_zip = []
    for root, dirs, files in os.walk(path_to_backup):
        for file in files:
            files_to_zip.append(os.path.join(root, file))
    num_source_files = len(files_to_zip)

    now = datetime.datetime.now()
    zip_name = f"{browser.lower()}_{now.strftime('%d-%m-%Y')}_{now.strftime('%I-%M-%S-%p')}.zip"

    raw_instructions = config["transfer_instructions"].replace("{zip_name}", zip_name)
    instructions = translate(raw_instructions)

    with open("instructions.txt", "w", encoding="utf-8") as file:
        file.write(instructions)

    width = os.get_terminal_size().columns
    job_progress = Progress("{task.description}", SpinnerColumn(), BarColumn(bar_width=width), TextColumn("[progress.percentage][bright_green]{task.percentage:>3.0f}%"), "[bright_cyan]ETA", TimeRemainingColumn(), TimeElapsedColumn())
    overall_task = job_progress.add_task("[bright_green]Compressing", total=num_source_files)
    progress_table = Table.grid()
    progress_table.add_row(Panel.fit(job_progress, title="[bright_white]Jobs", border_style="red", padding=(1, 2)))

    with Live(progress_table, refresh_per_second=10):
        with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED, True, compression_level, strict_timestamps=False) as zipf:
            for file_path in files_to_zip:
                rel_path = os.path.relpath(file_path, path_to_backup)
                zipf.write(file_path, os.path.join(config["data_folder_name"], rel_path))
                job_progress.update(overall_task, advance=1)

            if config["reg_export_name"]:
                zipf.write(config["reg_export_name"], config["reg_export_name"])

            zipf.write("instructions.txt", "instructions.txt")

    # cleanup

    print(clr(f"\n  - {translate('Cleaning...')}"))
    if config["reg_export_name"] and os.path.exists(config["reg_export_name"]):
        os.remove(config["reg_export_name"])
    if os.path.exists("instructions.txt"):
        os.remove("instructions.txt")
    subprocess.run(["explorer.exe", os.getcwd()])
    cls()
    input(clr(instructions + f"\n\n  > {translate('Press [ENTER] once you have read the steps...')} "))


def main():
    global DANK_TOOL_LANG, translator

    # check if translator is enabled (dank.tool.exe)

    try:
        DANK_TOOL_LANG = os.environ["DANK_TOOL_LANG"]
        if DANK_TOOL_LANG == "en":
            DANK_TOOL_LANG = ""
        else:
            translator = Translator()
    except:
        DANK_TOOL_LANG = ""

    # banner, check if admin

    cls()
    try:
        if not is_admin():
            raise RuntimeError(clr("Not executed as administrator! Exporting browser data and registry keys requires admin privileges!"))
    except Exception as exc:
        sys.exit(clr(err((type(exc), exc, exc.__traceback__)), 2))

    # folders

    try:
        os.chdir(get_path("Documents"))
    except:
        os.chdir("C:\\")
    if not os.path.isdir("dank.browser-backup"):
        os.mkdir("dank.browser-backup")
    os.chdir("dank.browser-backup")

    # user input

    browsers = list(browsers_config.keys())
    to_print = "  - Supported Browsers: \n"
    for _, browser in enumerate(browsers):
        to_print += f"\n  - [{_ + 1}] {browser}"

    banner = "\n\n\n   _         _     _                                 _           _           \n _| |___ ___| |_  | |_ ___ ___ _ _ _ ___ ___ ___ ___| |_ ___ ___| |_ _ _ ___ \n| . | .'|   | '_|_| . |  _| . | | | |_ -| -_|  _|___| . | .'|  _| '_| | | . |\n|___|__,|_|_|_,_|_|___|_| |___|_____|___|___|_|     |___|__,|___|_,_|___|  _|\n                                                                        |_|  \n\n"
    Console().print(Align.center(banner), style="blink red", highlight=False)
    print(clr(to_print))

    print("")
    while True:
        choice = input(clr(f"  > {translate('Enter choice')}: ") + red)
        if choice.isdigit() and int(choice) > 0 and int(choice) <= int(len(browsers)):
            choice = browsers[int(choice) - 1]
            break
        rm_line()

    print("")
    while True:
        compression_level = input(clr(f"  > {translate('Compression level (Fast/Best)')} [1/2]: ") + red).lower()
        match compression_level:
            case "1" | "fast":
                compression_level = 0
                break
            case "2" | "best":
                compression_level = 9
                break
        rm_line()

    # backup

    backup(choice, compression_level)


main()
