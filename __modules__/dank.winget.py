import os
import subprocess
from rich.panel import Panel
from rich.columns import Columns
from rich.console import Console
from dankware import cls, clr, align, rm_line
from dankware import red, red_dim, green_bright

def winget_installed():
    try:
        result = subprocess.run(['winget', '--info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return bool(result.returncode == 0)
    except FileNotFoundError:
        return False

def print_banner():
    banner = "\n\n   _         _           _             _   \n _| |___ ___| |_   _ _ _|_|___ ___ ___| |_ \n| . | .'|   | '_|_| | | | |   | . | -_|  _|\n|___|__,|_|_|_,_|_|_____|_|_|_|_  |___|_|  \n                              |___|        \n\n\n"
    cls(); print(clr(align(banner),4,colours=(red, red_dim)))
    print(clr("  [ Commands ]\n\n  - search NAME (to find software, winget only)\n\n  - installed (installed software, winget only)\n\n  - updates\n\n  - clear (refresh screen)\n\n  - exit\n"))

def handle_response(cmd, results, mode):

    try:
        cmd = cmd.stdout.decode('utf-8')
        for line in cmd.splitlines():
            if line.count('-') > 5:
                cmd = cmd.split(line)[1].splitlines()[1:]
                break
    except Exception as exc:
        raise Exception(f"Error parsing response!\n\n{cmd.stdout.decode('utf-8')}") from exc
    indexes = []

    prev = ''
    for index, char in enumerate(cmd[0]):
        if prev == ' ' and char != ' ':
            indexes.append(index)
        prev = char
    for line in cmd[1:]:
        prev = ''
        for index, char in enumerate(line):
            if prev == ' ' and char != ' ' and index in indexes:
                indexes.append(index)
            prev = char

    max_count = max([indexes.count(_) for _ in sorted(list(set(indexes)))])
    indexes = [_ for _ in sorted(list(set(indexes))) if indexes.count(_) == max_count]
    indexes.insert(0,0)
    results.clear()
    index = 1

    for line in cmd:
        parts = [line[i:j] for i,j in zip(indexes, indexes[1:]+[None])]
        if '.' in parts[1].strip():
            results[index] = {'name': parts[0].strip(), 'id': parts[1].strip()} #, 'version': parts[2].strip(), 'source': parts[3].strip()}
            index += 1

    console = Console()
    user_renderables = [f"[b][bright_white]{key} [bright_red]- [bright_white]{value['name']}[/b]" for key, value in results.items()]
    results['mode'] = mode; print()
    console.print(Panel(title="[red1]> [bright_white][b]R E S U L T S[/b] [red1]<", title_align="center", renderable=Columns(user_renderables, expand=True), style="red", expand=True))

    match mode:
        case 'search':
            print(clr("\n  - Type number to install.\n"))
        case 'installed':
            print(clr("\n  - Type number to display info.\n"))
        case 'updates':
            print(clr("\n  - Type number to update.\n"))

def print_info(id):
    cmd = subprocess.run(['winget', 'show', '--id', id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cmd.returncode == 0:
        print(clr(cmd.stdout.decode('utf-8')))
    else:
        print(clr(f"\n  [ERROR]: {cmd.stderr.decode('utf-8')}\n",2))

def main():

    results = {}
    print_banner()

    while True:

        cmd = input(clr('  > ') + green_bright)

        if cmd.lower().startswith('search '):
            cmd = subprocess.run(['winget', 'search', '--accept-source-agreements', cmd[7:]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if cmd.returncode == 0:
                handle_response(cmd, results, 'search')
            else:
                print(clr(f"\n  [ERROR]: {cmd.stderr.decode('utf-8')}\n",2))

        elif cmd.lower().startswith('installed'): 
            cmd = subprocess.run(['winget', 'list', '--accept-source-agreements'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if cmd.returncode == 0:
                handle_response(cmd, results, 'installed')
            else:
                print(clr(f"\n  [ERROR]: {cmd.stderr.decode('utf-8')}\n",2))

        elif cmd.lower().startswith('updates'):
            cmd = subprocess.run(['winget', 'upgrade', '--accept-source-agreements'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if cmd.returncode == 0:
                handle_response(cmd, results, 'updates')
            else:
                print(clr(f"\n  [ERROR]: {cmd.stderr.decode('utf-8')}\n",2))

        elif cmd.isdigit():

            if results:
                cmd = int(cmd)
                if cmd in results:

                    match results['mode']:
                        case 'search':
                            if input(clr("\n  > Display info? [y/n]: ") + green_bright).lower().startswith('y'):
                                print_info(results[cmd]['id'])
                            else: rm_line(); rm_line()
                            if input(clr("\n  > Install? [y/n]: ") + green_bright).lower().startswith('y'):
                                print()
                                os.system(f"winget install --interactive --id {results[cmd]['id']}")
                                print()
                            else: rm_line()

                        case 'installed':
                            print_info(results[cmd]['id'])

                        case 'updates':
                            print()
                            os.system(f"winget upgrade --interactive --id {results[cmd]['id']}")
                            print()

                        case _: rm_line()
                else: rm_line()
            else: rm_line()

        elif cmd.lower().startswith('clear'):
            print_banner()

        elif cmd.lower().startswith('exit'):
            break

        else:
            rm_line()

if __name__ == "__main__":

    if os.name != 'nt':
        input(clr("\n  - This module only works for Windows! Press ENTER to exit... ",2))
    elif not winget_installed():
        input(clr("\n  - This module requires winget to be installed! Press ENTER to exit... ",2))
    else:
        main()

    if "DANK_TOOL_VERSION" in os.environ:
        for _ in ('main', 'winget_installed', 'print_banner', 'handle_response', 'print_info'):
            if _ in globals(): del globals()[_]
