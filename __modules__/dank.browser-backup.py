import os
import sys
import time
import shutil
import winreg
import datetime
import pyminizip
from psutil import process_iter
from dankware import title, cls, clr, err, align, magenta, rm_line, is_admin, export_registry_keys

from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn

def chrome_installed():
    try:
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            winreg.QueryValueEx(key, "Path")
        return True
    except FileNotFoundError:
        return False

def backup(browser, password, compression_level):

    if browser == "Chrome":
        
        path_to_backup = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        
        if not chrome_installed():
            cls(); print(clr("\n  > Chrome possibly not installed!",2))
        
        if not os.path.exists(path_to_backup):
            print(clr(f"\n  > Invalid Path: {path_to_backup}\n",2))
            while True:
                path_to_backup = input(clr("  > Input user data folder path: ")); rm_line()
                if os.path.exists(path_to_backup) and r"Google\Chrome\User Data" in path_to_backup: break
        
        while True:
            cls(); chrome_running = False
            for proc in process_iter(['name']):
                if proc.info['name'] == 'chrome.exe':
                    chrome_running = True; break
            if chrome_running: input(clr("\n  > Chrome is running! Terminate it and press [ENTER]... ",2))
            else: break

        cls(); print(clr("\n  > Exporting registry keys..."))
        export_registry_keys('HKEY_CURRENT_USER', r'Software\Google\Chrome\PreferenceMACs')
        
        print(clr("\n  > Compressing... (this might take a few minutes)\n"))
        source_files = ["export.reg"]
        prefixes = [""]

        for root, dirs, files in os.walk(path_to_backup):
            for file in files:
                filepath = os.path.join(root, file)
                prefix = str("User Data" + filepath.split("User Data")[1]).replace(f"\\{file}",'')
                source_files.append(filepath)
                prefixes.append(prefix)

        now = datetime.datetime.now()
        zip_name = f'chrome_[{now.strftime("%d-%m-%Y")}]_[{now.strftime("%I-%M-%S-%p")}].zip'
        
        width = os.get_terminal_size().columns
        job_progress = Progress("{task.description}", SpinnerColumn(), BarColumn(bar_width=width), TextColumn("[deep_pink1][progress.percentage][bright_cyan]{task.percentage:>3.0f}%"), TimeRemainingColumn())
        overall_task = job_progress.add_task("[bright_green]Compressing", total=int(len(source_files)))
        progress_table = Table.grid()
        progress_table.add_row(Panel.fit(job_progress, title="[bright_red]Jobs", border_style="magenta1", padding=(1, 2)))

        with Live(progress_table, refresh_per_second=10):
                while not job_progress.finished:
                    time.sleep(0.1)
                    pyminizip.compress_multiple(source_files, prefixes, zip_name, password, compression_level, lambda x: job_progress.update(overall_task, advance=1))

        print(clr("\n  > Cleaning..."))
        #if os.path.exists("User Data"): shutil.rmtree("User Data", ignore_errors=True)
        if os.path.exists("export.reg"): os.remove("export.reg")

        os.system(f'explorer.exe "{os.getcwd()}"')
    
        cls(); input(clr(f'\n  > [STEPS TO TRANSFER]: \n\n  - Transfer {zip_name} to another computer\n  - Unzip with the password "{password}"\n  - Install chrome\n  - Exit chrome\n  - Open windows explorer\n  - Paste path [%LOCALAPPDATA%\\Google\\Chrome]\n  - Delete the [User Data] folder\n  - Move extracted [User Data] folder to [%LOCALAPPDATA%\\Google\\Chrome]\n  - Run [export.reg]\n  - Transfer Complete!\n\n  > Press [ENTER] once you have read the steps... '))
    
    #elif browser == "Firefox"
    #elif browser == "Opera":
    #elif browser == "Brave":  

def main():

    cls(); title("𝚍𝚊𝚗𝚔.𝚋𝚛𝚘𝚠𝚜𝚎𝚛-𝚋𝚊𝚌𝚔𝚞𝚙"); banner = "\n\n                                                                             \n   _         _     _                                 _           _           \n _| |___ ___| |_  | |_ ___ ___ _ _ _ ___ ___ ___ ___| |_ ___ ___| |_ _ _ ___ \n| . | .'|   | '_|_| . |  _| . | | | |_ -| -_|  _|___| . | .'|  _| '_| | | . |\n|___|__,|_|_|_,_|_|___|_| |___|_____|___|___|_|     |___|__,|___|_,_|___|  _|\n                                                                        |_|  \n\n"
    try:
        if not is_admin(): raise RuntimeError(clr("Current user is not an administrator! Exporting browser data and registry keys requires admin privileges!"))
    except: sys.exit(clr(err(sys.exc_info()),2))
    
    try: os.chdir(os.path.join(os.environ['USERPROFILE'],'Documents'))
    except: os.chdir("C:\\")
    try: os.mkdir('dank.browser-backup')
    except: pass
    os.chdir('dank.browser-backup')
    
    browsers = ['Chrome']
    to_print = "\n  > Supported Browsers: \n"
    for _ in range(len(browsers)): to_print += f"\n  - [{_+1}] {browsers[_]}"
    to_print += "\n"
    
    print(align(clr(banner,4)) + clr(to_print))
    
    while True:
        choice = input(clr("  > Enter choice: ") + magenta)
        if choice.isdigit() and int(choice) > 0 and int(choice) <= int(len(browsers)):
            choice = browsers[int(choice)-1]; break
        else: rm_line()
    
    print("")
    while True:
        password = input(clr("  > Enter backup password: ") + magenta)
        if password: break
        else: rm_line()
        
    print("")
    while True:
        compression_level = input(clr("  > Compression level (Fast/Best) [1/2]: ") + magenta).lower()
        if compression_level in ['1', 'fast']:
            compression_level = 0; break
        elif compression_level in ['2', 'best']:
            compression_level = 10; break
        else: rm_line()

    backup(choice, password, compression_level)

if __name__ == "__main__": main()
