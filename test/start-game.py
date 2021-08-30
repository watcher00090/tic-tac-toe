import subprocess
import os
import time

proc = subprocess.Popen(["/home/ubuntu/tic-tac-toe/bin/tic-tac-toe"], shell=True)
time.sleep(3)
pid = proc.pid
print('pid = ', pid)

print("Sending data to STDIN of the TTY controlling the tic-tac-toe process...")
os.system(f"echo tr > /proc/{pid}/fd/0")
time.sleep(3)