import subprocess
import os
import time

proc = subprocess.Popen(["C:\workspace\\go-jenkins\\bin\\tic-tac-toe.exe"], shell=True)
time.sleep(3)
pid = proc.pid
print('pid = ', pid)