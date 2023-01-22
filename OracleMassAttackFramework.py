import threading
import subprocess
from queue import Queue
import argparse
import ipaddress
import validators

#Coded by Oracle
#Usage ./OracleMassAttackFramework.py -p script.py -t 100
#Usage with extra arguements: ./OracleMassAttackFramework.py -p script.py -t 100 -p 8080
#You do not have to use IPs, you can use URLs if you want to as well, additionally, feel free to use subnets.


print("""
.___________. __    __   _______      ______   .______          ___       ______  __       _______ 
|           ||  |  |  | |   ____|    /  __  \  |   _  \        /   \     /      ||  |     |   ____|
`---|  |----`|  |__|  | |  |__      |  |  |  | |  |_)  |      /  ^  \   |  ,----'|  |     |  |__   
    |  |     |   __   | |   __|     |  |  |  | |      /      /  /_\  \  |  |     |  |     |   __|  
    |  |     |  |  |  | |  |____    |  `--'  | |  |\  \----./  _____  \ |  `----.|  `----.|  |____ 
    |__|     |__|  |__| |_______|    \______/  | _| `._____/__/     \__\ \______||_______||_______|
""")
print("Oracle's Mass Attack Framework")
print("pwn the planet. :)")


def run_script(ip, script_path, *args):
    subprocess.run(['python', script_path, ip, *args])


def initiate_thread(num_threads, script_path, *args):
    ips = Queue()
    with open("ips.txt") as f:
        for ip in f:
            try:
                ip = ipaddress.ip_address(ip.strip())
            except ValueError:
                try:
                    subnet = ipaddress.ip_network(ip.strip())
                    for address in subnet:
                        ips.put(address)
                except ValueError:
                    if validators.url(ip):
                        ips.put(ip)
                    else:
                        print(f"{ip.strip()} is not a valid IP address, URL, or subnet.")
            else:
                ips.put(ip)
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(ips, script_path, *args))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def worker(ips, script_path, *args):
    while True:
        ip = ips.get()
        if ip is None:
            break
        run_script(ip, script_path, *args)
        ips.task_done()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Threaded script execution')
    parser.add_argument('-p', '--path', type=str, required=True, help='path of script to run')
    parser.add_argument('-t', '--threads', type=int, default=10, help='number of threads')
    parser.add_argument('args', nargs='*', help='additional arguments')
    args = parser.parse_args()
    script_path = args.path
    num_threads = args.threads
    additional_args = args.args
    initiate_thread(num_threads, script_path, *additional_args)
