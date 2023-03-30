import os
import time
import json
import socket
import requests
from mcstatus import JavaServer, BedrockServer
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

# checks if ip has a server running on the specified port

def check_java(ip):

    if socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((ip,port)) == 0:
        save_server(ip)
    
def check_bedrock(ip):
    
    try:
        socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(bytes.fromhex("01" + "000000000000000000" + "ffff00fefefefefdfdfdfd12345678" + "0000000000000000"), (ip, port))
        save_server(ip)
    except: pass

def save_server(ip):
    
    try:
        if server_type == "java": server = JavaServer(ip,port)
        else: server = BedrockServer(ip,port)
        status = server.status()
        #try: query = server.query(); query_response = f"| {query.software}"
        #except: query_response = ""
        response = requests.get(f"http://ipwho.is/{ip}").json()
        to_print = f"{ip} | {'java' if server_type == 'java' else 'bedrock'} | {status.version.name} | {status.players.online} online | {int(status.latency)}ms | {response['city']} | {response['connection']['org']} | {response['connection']['domain']} | {status.description}".replace('\n','|').replace('ü','u')
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

def generate_ip():

    while True:
        ip = random_ip()
        if ip in ips.keys() or ip in scanned.keys(): continue
        ips[ip] = ""; break

def main():
    
    global ips, scanned, server_type, port

    title("𝚍𝚊𝚗𝚔.𝚖𝚒𝚗𝚎𝚌𝚛𝚊𝚏𝚝-𝚜𝚎𝚛𝚟𝚎𝚛-𝚜𝚌𝚊𝚗𝚗𝚎𝚛"); banner = '\n\n     _             _                                                              \n    | |           | |                                                             \n  _ | | ____ ____ | |  _   ____   ____ ___ ___  ____ ____ ____  ____   ____  ____ \n / || |/ _  |  _ \\| | / ) |    \\ / ___|___)___)/ ___) _  |  _ \\|  _ \\ / _  )/ ___)\n( (_| ( ( | | | | | |< ( _| | | ( (___   |___ ( (__( ( | | | | | | | ( (/ /| |    \n \\____|\\_||_|_| |_|_| \\_|_)_|_|_|\\____)  (___/ \\____)_||_|_| |_|_| |_|\\____)_|    \n                                                                                  \n'
    socket.setdefaulttimeout(1)
    
    # change directory

    #exec_mode = "script"; exec(chdir(exec_mode))
    try: os.chdir(os.path.join(os.environ['USERPROFILE'],'Documents'))
    except: os.chdir("C:\\")
    try: os.mkdir('dank.mc-server-scanner')
    except: pass
    os.system(f'explorer.exe "dank.mc-server-scanner"')
    os.chdir('dank.mc-server-scanner')
    
    # create and load files
    
    ###
    if os.path.isfile("scanned.txt"): os.rename('scanned.txt', 'java_scanned.txt')
    ###

    try: open('java_scanned.txt','x').close()
    except: pass
    try: open('bedrock_scanned.txt','x').close()
    except: pass
    try: open('servers.txt','x').close()
    except: pass
    
    ###
    try:
        if os.path.isfile('java_scanned.json'):
            tmp = open('java_scanned.json','r').read()
            os.remove('java_scanned.json')
            if "{" in tmp:
                tmp = sorted(list(set(json.loads(tmp).keys())))
                open('java_scanned.txt','w').write('\n'.join(tmp))
    except:
        open('java_scanned.txt','w').write("")

    try:
        if os.path.isfile('bedrock_scanned.json'):
            tmp = open('bedrock_scanned.json','r').read()
            os.remove('bedrock_scanned.json')
            if "{" in tmp:
                tmp = sorted(list(set(json.loads(tmp).keys())))
                open('bedrock_scanned.txt','w').write('\n'.join(tmp))
    except:
        open('bedrock_scanned.txt','w').write("")
        
    tmp = None
    ###
    
    #cls(); print(clr("\n  > Loading scanned.txt..."))

    # get user input

    cls(); print(align(clr(banner,4)))
    print(clr("\n  > The scanned.txt files store the ips that have been scanned, and thus will not be scanned again.\n\n  > Delete this file to reset scanned ips.\n\n  > Start with [ 100 threads ] just to see the performance impact on your computer.\n\n  > Should be smooth upto 500, you might notice some performance impact after this point!\n\n  > Start with 50000 IPs, will take a few seconds to generate.\n\n  > The scanned.txt file is only updated after the scan is complete."))
    
    print("")
    while True:
        server_type = input(clr("  > Server Type [java/bedrock]: ") + magenta)
        if server_type == "java":
            scanned = open('java_scanned.txt','r').read().splitlines()
            scanned = {key: "" for key in scanned}
            port = 25565
            break
        elif server_type == "bedrock":
            scanned = open('bedrock_scanned.txt','r').read().splitlines()
            scanned = {key: "" for key in scanned}
            port = 19132
            break
        else: rm_line()
        
    print("")
    while True:
        threads = input(clr("  > Threads: ") + magenta)
        if threads.isdigit(): threads = int(threads); break
        else: rm_line()
        
    print("")
    while True:
        ips_amt = input(clr("  > Amount of IPs to scan: ") + magenta)
        if ips_amt.isdigit(): ips_amt = int(ips_amt); break
        else: break
        
    # disclaimer
 
    cls(); input(clr("\n  [IMPORTANT]\n\n  > Try not to use [COPY] or [PASTE] when the scanner is running!\n\n  > All the servers are saved to servers.txt!\n\n  > Press [ ENTER ] to start the scanner..."))
    cls()

    # generate and check ips on multiple threads in batches
    
    gen_rate = 5000 # threads to generate at | higher = faster
    gen_amt = 50000 # max generate / check amount
    gen_rem = ips_amt
    while gen_rem > 0:
        
        ips = {}
        generated = 0
        if not gen_rem >= gen_amt: gen_amt = gen_rem
        
        # multithreaded generator
        
        #cls()
        print(clr(f"\n  > Generating {gen_amt} unique ips..."))
        while generated < gen_amt:
            while True:
                try:
                    if gen_amt >= gen_rate:
                        multithread(generate_ip, gen_rate, progress_bar=False); generated += gen_rate
                    else:
                        multithread(generate_ip, gen_amt, progress_bar=False); generated += gen_amt
                    break
                except KeyboardInterrupt: input(clr(f"\n  > Failed to generate ips! Try not to use [COPY] or [PASTE]! Press [ENTER] to try again... ",2)); rm_line()
                
        # multithreaded checker

        while True:
            try: 
                #cls()
                print(clr(f"\n  > Checking {len(ips)} unique ips...\n"))
                if server_type == "java": multithread(check_java, threads, list(ips.keys())); break
                else: multithread(check_bedrock, threads, list(ips.keys())); break
            except KeyboardInterrupt: input(clr(f"\n  > Failed to check ips! Try not to use [COPY] or [PASTE]! Press [ENTER] to try again... ",2)); rm_line()
        
        # saving scanned ips
    
        #cls()
        print(clr(f"\n  > Saving {server_type}_scanned.txt..."))
        for ip in ips: scanned[ip] = ""
        print(clr(f"\n  > Totally Scanned {len(scanned)} IPs!"))
        try: open(f'{server_type}_scanned.txt','w').write('\n'.join(sorted(list(set(scanned.keys())))))
        except MemoryError: 
            print(clr(f"\n  > Resetting {server_type}_scanned.txt due to MemoryError...",2))
            open(f'{server_type}_scanned.txt','w').write('')
        time.sleep(5)
        
        gen_rem -= gen_amt
    
if __name__ == "__main__": main()
