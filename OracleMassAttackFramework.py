#Coded by Oracle
#Usage ./OracleMassAttackFramework.py -p script.py -t 100

import threading
import subprocess
from queue import Queue
import argparse

print("""
.___________. __    __   _______      ______   .______          ___       ______  __       _______ 
|           ||  |  |  | |   ____|    /  __  \  |   _  \        /   \     /      ||  |     |   ____|
`---|  |----`|  |__|  | |  |__      |  |  |  | |  |_)  |      /  ^  \   |  ,----'|  |     |  |__   
    |  |     |   __   | |   __|     |  |  |  | |      /      /  /_\  \  |  |     |  |     |   __|  
    |  |     |  |  |  | |  |____    |  `--'  | |  |\  \----./  _____  \ |  `----.|  `----.|  |____ 
    |__|     |__|  |__| |_______|    \______/  | _| `._____/__/     \__\ \______||_______||_______|
""")
print("Oracle's Mass Attack Framework")

def run_script(ip, script_path):
    subprocess.run(['python', script_path, ip])

def read_ips_and_run(num_threads, script_path):
    ips = Queue()
    with open("ips.txt") as f:
        for ip in f:
            ips.put(ip.strip())
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(ips, script_path))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def worker(ips, script_path):
    while True:
        ip = ips.get()
        if ip is None:
            break
        run_script(ip, script_path)
        ips.task_done()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Threaded script execution')
    parser.add_argument('-p', '--path', type=str, required=True, help='path of script to run')
    parser.add_argument('-t', '--threads', type=int, default=10, help='number of threads')
    args = parser.parse_args()
    script_path = args.path
    num_threads = args.threads
    read_ips_and_run(num_threads, script_path)
