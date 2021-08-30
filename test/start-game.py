import subprocess
import os
import time

proc = subprocess.Popen(["/home/ubuntu/tic-tac-toe/bin/tic-tac-toe"], shell=True)
time.sleep(3)
pid = proc.pid

os.system(f'echo "tr\\n" > /proc/{pid}/fd/0')
time.sleep(3)