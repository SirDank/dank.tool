import socket
import requests
from mcstatus import JavaServer
from dankware import multithread, chdir, clr, cls, title, clr_banner, align, random_ip, magenta

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
            to_print = f"{ip} | {status.version.name} | {status.players.online} online | {int(status.latency)}ms | {response['city']} | {response['connection']['org']} | {response['connection']['domain']} | {status.description}".replace('\n','|')
            for _ in ['§0', '§1', '§2', '§3', '§4', '§5', '§6', '§7', '§8', '§9', '§a', '§b', '§c', '§d', '§e', '§f', '§l', '§n', '§o', '§m', '§k', '§r']: to_print = to_print.replace(_,'')
            print(clr(f"  > {to_print}\n"))
            open('servers.txt','a').write(f"\n{to_print}")
        except Exception as exc:
            exc = str(exc)
            err_found = False
            
            for err in ["timed out", "unreachable", "refused", "not valid", "invalid", "closed", "did not", "aborted", "failed", "no route", "No route", "Broken pipe"]:
                if err in exc:
                    err_found = True; break
            
            if not err_found:
                open('servers.txt','a').write(f"\n{ip} | {exc}")
                print(f"{ip} | {exc}\n")

# generates random valid ip

def generate():

    while True:
        ip = random_ip()
        if ip in ips or ip in scanned: continue
        ips.append(ip); break

def main():
    
    global ips, scanned

    title("dank.minecraft-server-scanner"); banner = '\n\n     _             _                                                              \n    | |           | |                                                             \n  _ | | ____ ____ | |  _   ____   ____ ___ ___  ____ ____ ____  ____   ____  ____ \n / || |/ _  |  _ \\| | / ) |    \\ / ___|___)___)/ ___) _  |  _ \\|  _ \\ / _  )/ ___)\n( (_| ( ( | | | | | |< ( _| | | ( (___   |___ ( (__( ( | | | | | | | ( (/ /| |    \n \\____|\\_||_|_| |_|_| \\_|_)_|_|_|\\____)  (___/ \\____)_||_|_| |_|_| |_|\\____)_|    \n                                                                                  \n'
    socket.setdefaulttimeout(1)

    exec_mode = "script"; exec(chdir(exec_mode))
    try: open('scanned.txt','x')
    except: pass
    try: open('servers.txt','x')
    except: pass
    scanned = sorted(list(set(open('scanned.txt','r').read().splitlines())))
    servers = sorted(list(set(open('servers.txt','r').read().splitlines())))
    open('servers.txt','w').write('\n'.join(servers))

    while True:
        cls(); print(align(clr_banner(banner)))
        threads = input(clr("\n  > The scanned.txt file stores the ips that have been scanned, and thus will not be scanned again.\n\n  > Delete this file to reset scanned ips.\n\n  > Start with [ 100 threads ] just to see the performance impact on your computer.\n\n  > Should be smooth upto 500, you might notice some performance impact after this point!\n\n  > Start with 50000 IPs, will take a few seconds to generate.\n\n  > The scanned.txt is only updated after the scan is complete.\n\n  > Threads: ") + magenta)
        if threads.isdigit(): threads = int(threads)
        else: continue
        ips_amt = input(clr("\n  > Amount of IPs to scan: ") + magenta)
        if ips_amt.isdigit(): ips_amt = int(ips_amt); break

    cls(); print(clr(f"\n  > Generating {ips_amt} ips...\n"))
    ips = []; temp_ips_amt = ips_amt 
    while temp_ips_amt >= 500:
        multithread(generate, 500, progress_bar=False)
        temp_ips_amt -= 500
    if temp_ips_amt > 0: multithread(generate, temp_ips_amt, progress_bar=False)

    ips = list(set(ips))
    cls(); print(clr(f"\n  > Checking {ips_amt} ips...\n"))
    multithread(check, threads, ips)
    
    scanned = sorted(list(set(scanned + ips)))
    open('scanned.txt','w').write('\n'.join(scanned))
    #cls(); print(clr(f"\n > Scanning Complete! Sleeping 5s...")); time.sleep(5)
    
if __name__ == "__main__": 
    main()
