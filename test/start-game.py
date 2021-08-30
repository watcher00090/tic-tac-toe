import subprocess
import os
import time

proc = subprocess.Popen(["/home/ubuntu/tic-tac-toe/bin/tic-tac-toe"], shell=True)
time.sleep(3)
pid = proc.pid

os.system("mkfifo /tmp/tic-tac-toe-input")
os.system("cat > /tmp/tic-tac-toe-input")
os.system("echo $! > /tmp/tic-tac-toe-input-pid")
os.system("cat /tmp/tic-tac-toe-input | home/ubuntu/tic-tac-toe/bin/tic-tac-toe")

time.sleep(3)