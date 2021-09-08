import subprocess
import os
import time
import signal
import sys
import re
from pathlib import Path
from copy import deepcopy

ingameinputRE = r"Player (one|two) \((X|O)\) to move\: (.+)$"
endgameinputRE = r"Type 'n' to start a new game, or 'q' or 'quit' to quit\: (.+)$"

if Path("/tmp/tic-tac-toe-pipe").exists():
    os.system("rm /tmp/tic-tac-toe-pipe")

ret = os.system("bash -c \"mkfifo /tmp/tic-tac-toe-pipe\"")
if ret != 0:
    sys.exit(f"ERROR: Attempting to make the FIFO returned the error {ret}")

(pid, fd) = os.forkpty()
if pid == 0: #child
    print("child process executing...")

    ret = os.system("bash -c \"cat /tmp/tic-tac-toe-pipe | /home/ubuntu/tic-tac-toe/bin/tic-tac-toe  2> /tmp/errors.log > /tmp/errors.log\"")
    if ret != 0:
        sys.exit(f"ERROR: Attempting to run the program fed by the pipe produced the error {ret}")

else: #parent
    print("Parent process executing...")
    print("Attempting to drive the tic-tac-toe game through the parent process...")

    ret = os.system("bash -c 'echo -e \"tl\\nmi\\ntc\\ncl\\ntr\\nq\" >> /tmp/tic-tac-toe-pipe'")
    if ret != 0:
        sys.exit(f"ERROR: Attempting to write a move to the tic-tac-toe game produced the error {ret}")

    print("Command sequence fed into the pipe successfully!")

    time.sleep(5)

    # wait for the child process to complete
    status = os.wait()

    f = open("/tmp/errors.log")
    
    lines = f.readlines()

    linesCopy = []

    for line in lines:
        #print("Line{}: {}".format(count, line.rstrip("\n")))
        result        = re.match(ingameinputRE, line)
        secondresult  = re.match(endgameinputRE, line)
        if result != None:
            linesCopy.append(f"Player {result.group(1)} ({result.group(2)}) to move:\n")
            linesCopy.append(f"{result.group(3)}\n")
        elif secondresult != None:
            linesCopy.append(f"Type 'n' to start a new game, or 'q' or 'quit' to quit:\n")
            linesCopy.append(f"{secondresult.group(1)}\n")
        else:
            linesCopy.append(deepcopy(line))
        
    num = 1
    for line in linesCopy:
        print("Line {}: {}".format(num, line.rstrip("\n")))
        num += 1
