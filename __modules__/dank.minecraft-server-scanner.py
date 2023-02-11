import os
import time
import json
import socket
import requests
from mcstatus import JavaServer
from dankware import multithread, clr, cls, title, align, magenta, rm_line, random_ip

'''

for the future of this script

Goals: masscan port scans

https://github.com/MyKings/python-masscan
https://github.com/Arryboom/MasscanForWindows
https://github.com/rezonmain/mc-server-scanner/blob/main/src/iprange.py
https://github.com/ObscenityIB/creeper/blob/main/creeper.sh
https://raw.githubusercontent.com/robertdavidgraham/masscan/master/data/exclude.conf
https://github.com/Footsiefat/Minecraft-Server-Scanner

'''

# checks if ip has a server running on port 25565

def check(ip):

    if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((ip,25565)) == 0:
        try:
            server = JavaServer(ip, 25565)
            status = server.status()
            #try: query = server.query(); query_response = f"| {query.software}"
            #except: query_response = ""
            response = requests.get(f"http://ipwho.is/{ip}").json()
            to_print = f"{ip} | {status.version.name} | {status.players.online} online | {int(status.latency)}ms | {response['city']} | {response['connection']['org']} | {response['connection']['domain']} | {status.description}".replace('\n','|').replace('ü','u')
            for _ in ['§0', '§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§a', '§b', '§c', '§d', '§e', '§f', '§l', '§n', '§o', '§m', '§k', '§r']: to_print = to_print.replace(_,'')
            print(clr(f"  > {to_print}\n"))
            open('servers.txt','a',encoding='utf-8').write(f"\n{to_print}")
        except Exception as exc:
            exc = str(exc)
            err_found = False
            
            for err in ["timed out", "unreachable", "refused", "not valid", "invalid", "closed", "did not", "aborted", "failed", "no route", "No route", "Broken pipe"]:
                if err in exc:
                    err_found = True; break
            
            if not err_found:
                open('servers.txt','a',encoding='utf-8').write(f"\n{ip} | {exc}")
                print(f"{ip} | {exc}\n")

# generates random valid ip

def generate():

    while True:
        ip = random_ip()
        if ip in ips.keys() or ip in scanned.keys(): continue
        ips[ip] = ""; break

def main():
    
    global ips, scanned

    title("𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚜𝚌𝚊𝚗𝚗𝚎𝚛"); banner = '\n\n     _             _                                                              \n    | |           | |                                                             \n  _ | | ____ ____ | |  _   ____   ____ ___ ___  ____ ____ ____  ____   ____  ____ \n / || |/ _  |  _ \\| | / ) |    \\ / ___|___)___)/ ___) _  |  _ \\|  _ \\ / _  )/ ___)\n( (_| ( ( | | | | | |< ( _| | | ( (___   |___ ( (__( ( | | | | | | | ( (/ /| |    \n \\____|\\_||_|_| |_|_| \\_|_)_|_|_|\\____)  (___/ \\____)_||_|_| |_|_| |_|\\____)_|    \n                                                                                  \n'
    socket.setdefaulttimeout(1)

    #exec_mode = "script"; exec(chdir(exec_mode))
    os.chdir(os.path.join(os.environ['USERPROFILE'],'Documents'))
    try: os.mkdir('dank.mc-server-scanner')
    except: pass
    os.system(f'explorer.exe "dank.mc-server-scanner"')
    os.chdir('dank.mc-server-scanner')
    try: open('scanned.txt','x').close()
    except: pass
    try: open('servers.txt','x').close()
    except: pass
    cls(); print(clr("\n  > Loading scanned.txt..."))
    try: scanned = json.loads(open('scanned.txt','r').read())
    except: scanned = {}

    while True:
        cls(); print(align(clr(banner,4)))
        threads = input(clr("\n  > The scanned.txt file stores the ips that have been scanned, and thus will not be scanned again.\n\n  > Delete this file to reset scanned ips.\n\n  > Start with [ 100 threads ] just to see the performance impact on your computer.\n\n  > Should be smooth upto 500, you might notice some performance impact after this point!\n\n  > Start with 50000 IPs, will take a few seconds to generate.\n\n  > The scanned.txt is only updated after the scan is complete.\n\n  > Threads: ") + magenta)
        if threads.isdigit(): threads = int(threads)
        else: continue
        ips_amt = input(clr("\n  > Amount of IPs to scan: ") + magenta)
        if ips_amt.isdigit(): ips_amt = int(ips_amt); break

    gen_rem = ips_amt
    while gen_rem > 0:
        
        ips = {}
        generated = 0
        gen_rate = 500 # threads to generate at
        gen_amt = 50000 # max generate / check amount
        if not gen_rem >= gen_amt: gen_amt = gen_rem
        
        # multithreaded generator
        
        cls(); print(clr(f"\n  > Generating {gen_amt} ips...\n"))
        while generated < gen_amt:
            while True:
                try:
                    if gen_amt >= gen_rate:
                        multithread(generate, gen_rate, progress_bar=False); generated += gen_rate
                    else:
                        multithread(generate, gen_amt, progress_bar=False); generated += gen_amt
                    break
                except KeyboardInterrupt: input(clr(f"\n  > Failed to generate ips! Try not to use [COPY] or [PASTE]! Press [ENTER] to try again... ",2)); rm_line()
                
        # multithreaded checker

        while True:
            try: 
                cls(); print(clr(f"\n  > Checking {len(ips)} ips...\n"))
                multithread(check, threads, list(ips.keys())); break
            except KeyboardInterrupt: input(clr(f"\n  > Failed to check ips! Try not to use [COPY] or [PASTE]! Press [ENTER] to try again... ",2)); rm_line()
        
        # saving scanned ips
    
        cls(); print(clr("\n  > Saving scanned.txt..."))
        for ip in ips: scanned[ip] = ""
        print(clr(f"\n  > Totally Scanned {len(scanned)} IPs!"))
        open('scanned.txt','w').write(str(scanned).replace("'",'"').replace(",",",\n"))
        time.sleep(5)
        
        gen_rem -= gen_amt
    
if __name__ == "__main__": main()
