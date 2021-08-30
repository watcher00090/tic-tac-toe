import subprocess
import os
import time
import signal


if os.path.exists("/tmp/tic-tac-toe-input"):
    os.remove("/tmp/tic-tac-toe-input")

if os.path.exists("/tmp/tic-tac-toe-input-pid"):
    file = open('/tmp/tic-tac-toe-input-pid', 'r')
    lines = file.readLines()
    pid = lines[0]
    file.close()
    os.kill(pid, signal.SIGTERM) #or signal.SIGKILL 
    os.remove("/tmp/tic-tac-toe-input-pid")

os.system("mkfifo /tmp/tic-tac-toe-input")
time.sleep(5)

pid = os.Popen("cat > /tmp/tic-tac-toe-input").pid
time.sleep(5)

os.system(f"echo {pid} > /tmp/tic-tac-toe-input-pid")
time.sleep(5)

os.system("cat /tmp/tic-tac-toe-input | /home/ubuntu/tic-tac-toe/bin/tic-tac-toe")
time.sleep(5)