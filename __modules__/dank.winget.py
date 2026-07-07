import os
import subprocess
import tempfile

import requests
from dankware import clr, cls, github_file_selector, green_bright, rm_line
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel


def winget_installed():
    try:
        result = subprocess.run(
            ["winget", "--info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return bool(result.returncode == 0)
    except OSError:
        return False


def install_winget():
    file_name = "Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle"
    url = github_file_selector("microsoft/winget-cli", "add", [".msixbundle"])[0]
    print(clr("\n  - Downloading..."))
    os.chdir(tempfile.gettempdir())

    # ⚡ Bolt Optimization: Stream the msixbundle download (often >100MB) directly to disk
    # This prevents loading the entire payload into RAM at once, massively reducing memory consumption.
    with requests.get(
        url,
        headers={
            "User-Agent": ("dank.tool" if "DANK_TOOL_VERSION" not in os.environ else f"dank.tool {os.environ['DANK_TOOL_VERSION']}"),
            "Content-Type": "application/json",
        },
        timeout=180,
        allow_redirects=True,
        stream=True,
    ) as response:
        response.raise_for_status()
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    print(clr("\n  - Downloaded!"))
    subprocess.run([file_name], check=False)
    input(clr("\n  - Hit [ ENTER ] after you have installed winget... "))


def print_banner():
    cls()
    banner = "\n\n   _         _           _             _   \n _| |___ ___| |_   _ _ _|_|___ ___ ___| |_ \n| . | .'|   | '_|_| | | | |   | . | -_|  _|\n|___|__,|_|_|_,_|_|_____|_|_|_|_  |___|_|  \n                              |___|        \n\n\n"
    Console().print(Align.center(banner), style="blink red", highlight=False)
    print(clr("  [ Commands ]\n\n  - search <NAME OF SOFTWARE>\n\n  - installed (list of installed software)\n\n  - updates\n\n  - update-all\n\n  - clear (refresh screen)\n\n  - exit\n"))


def handle_response(cmd, results, mode):
    results.clear()
    results["mode"] = mode

    # Bolt Optimization: Accept a pre-decoded and pre-split array instead of repeating the operation
    if not isinstance(cmd, list):
        cmd = cmd.stdout.decode("utf-8").splitlines()

    cmd = [line for line in cmd if line.strip()]
    if not cmd:
        return

    table_header_idx = -1
    for i, line in enumerate(cmd):
        if line.count("-") > 3:
            table_header_idx = i - 1
            break

    if table_header_idx == -1 or table_header_idx >= len(cmd):
        return

    header_line = cmd[table_header_idx]
    cmd = cmd[table_header_idx + 2:]

    columns = header_line.split()[:3]
    if len(columns) < 2:
        return

    indexes = [0]
    for char in (word[0] for word in columns[1:] if word):
        if char in header_line:
            index = header_line.index(char)
            if index > 0 and header_line[index - 1] == " ":
                indexes.append(index)

    if len(indexes) < 2:
        return

    index = 1
    for line in cmd:
        parts = [line[i:j] for i, j in zip(indexes, indexes[1:] + [None])]
        if len(parts) > 1 and parts[1].strip() and "." in parts[1].strip():
            results[index] = {
                "name": parts[0].strip(),
                "id": parts[1].strip(),
            }
            index += 1

    console = Console()
    user_renderables = [f"[b][bright_white]{key} [bright_red]- [bright_white]{value['name']}[/b]" for key, value in results.items() if key != "mode"]
    print()
    if user_renderables:
        console.print(
            Panel(
                title="[red1]> [bright_white][b]R E S U L T S[/b] [red1]<",
                title_align="center",
                renderable=Columns(user_renderables, expand=True),
                style="red",
                expand=True,
            )
        )

        match mode:
            case "search":
                print(clr("\n  - Type number to install ( Supports multiple ex: 1,2,3 )\n"))
            case "installed":
                print(clr("\n  - Type number to display info ( Supports multiple ex: 1,2,3 )\n"))
            case "updates":
                print(clr("\n  - Type number to update ( Supports multiple ex: 1,2,3 )\n"))
    else:
        print(clr("  - No packages or updates found!\n"))


def print_info(id):
    cmd = subprocess.run(
        ["winget", "show", "--id", id],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cmd.returncode == 0:
        print(clr(cmd.stdout.decode("utf-8")))
    else:
        print(clr(f"\n  [ERROR]: {cmd.stdout.decode('utf-8')}", 2))


def process_winget_output(cmd_result, results, mode):
    if cmd_result.returncode == 0:
        output_lines = cmd_result.stdout.decode("utf-8").splitlines()
        if len(output_lines) > 0:
            handle_response(output_lines, results, mode)
        else:
            print(
                clr(
                    "\n  [KNOWN ERROR]: Please report this issue on GitHub / Discord Support Ticket to help fix it!",
                    2,
                )
            )
    else:
        print(clr(f"\n  [ERROR]: {cmd_result.stdout.decode('utf-8')}", 2))


def handle_search(cmd_input, results):
    cmd_result = subprocess.run(
        ["winget", "search", "--accept-source-agreements", cmd_input[7:]],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    process_winget_output(cmd_result, results, "search")


def handle_installed(results):
    cmd_result = subprocess.run(
        ["winget", "list", "--accept-source-agreements"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    process_winget_output(cmd_result, results, "installed")


def handle_updates(choice, results):
    cmd_result = subprocess.run(
        ["winget", "upgrade", "--accept-source-agreements"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cmd_result.returncode == 0:
        output_lines = cmd_result.stdout.decode("utf-8").splitlines()
        if len(output_lines) > 0:
            if not choice.startswith("update-all"):
                handle_response(output_lines, results, "updates")
            else:
                handle_response(output_lines, results, "update-all")
                max_items = len(results) - 1
                for index in range(1, max_items + 1):
                    print(clr(f"\n  - [{index}/{max_items}] Updating {results[index]['name']}...\n"))
                    subprocess.run(["winget", "upgrade", "--interactive", "--id", results[index]["id"]], check=False)
                print()
        else:
            print(
                clr(
                    "\n  [KNOWN ERROR]: Please report this issue on GitHub / Discord Support Ticket to help fix it!",
                    2,
                )
            )
    else:
        print(clr(f"\n  [ERROR]: {cmd_result.stdout.decode('utf-8')}", 2))


def handle_numeric_selection(cmd_input, results):
    if not results:
        rm_line()
        return

    for selected in cmd_input.split(","):
        selected = int(selected)
        if selected in results:
            match results["mode"]:
                case "search":
                    if input(clr("\n  > Display info? [y/n]: ") + green_bright).lower().startswith("y"):
                        print()
                        print_info(results[selected]["id"])
                    else:
                        rm_line()
                        rm_line()
                    if input(clr("\n  > Install? [y/n]: ") + green_bright).lower().startswith("y"):
                        print()
                        subprocess.run(["winget", "install", "--interactive", "--id", results[selected]["id"]], check=False)
                        print()
                    else:
                        rm_line()

                case "installed":
                    print_info(results[selected]["id"])

                case "updates":
                    print()
                    subprocess.run(["winget", "upgrade", "--interactive", "--id", results[selected]["id"]], check=False)
                    print()

                case _:
                    rm_line()
        else:
            rm_line()


def main():
    results = {}
    print_banner()

    while True:
        cmd_input = input(clr("  > ") + green_bright)
        cmd_lower = cmd_input.lower()

        if cmd_lower.startswith("search "):
            handle_search(cmd_input, results)
        elif cmd_lower.startswith("installed"):
            handle_installed(results)
        elif cmd_lower.startswith("updates") or cmd_lower.startswith("update-all"):
            handle_updates(cmd_lower, results)
        elif cmd_lower.startswith("clear"):
            print_banner()
        elif cmd_lower.startswith("exit"):
            break
        elif all(_.isdigit() for _ in cmd_input.strip().split(",")) and cmd_input.strip() != "":
            handle_numeric_selection(cmd_input.strip(), results)
        else:
            rm_line()


if os.name != "nt" or "WINELOADER" in os.environ:
    input(
        clr(
            "\n  - This module only works for Windows! Press [ ENTER ] to exit... ",
            2,
        )
    )
elif not winget_installed():
    input(clr("\n  - This module requires winget to be installed! Press [ ENTER ] to download and install... "))
    install_winget()
    main()
else:
    main()
