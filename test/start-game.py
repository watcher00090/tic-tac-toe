import subprocess
import os
import time
import signal
import sys


os.system("rm /tmp/tic-tac-toe-pipe")
os.system("rm /tmp/tic-tac-toe-pipe-helper-pid")

#if os.path.exists("/tmp/tic-tac-toe-pipe-helper-pid"):
#    file = open('/tmp/tic-tac-toe-pipe-helper-pid', 'r')
#    lines = file.readLines()
#    pid = lines[0]
#    file.close()
#    os.kill(pid, signal.SIGTERM) #or signal.SIGKILL 
#    os.remove("/tmp/tic-tac-toe-pipe-helper-pid")

#os.system("touch /tmp/tic-tac-toe-pipe-helper-pid")

ret = os.system("bash -c \"mkfifo /tmp/tic-tac-toe-pipe\"")
if ret != 0:
    sys.exit(f"ERROR: Attempting to make the FIFO returned the error {ret}")

#ret = os.system("bash -c \"nohup cat > /tmp/tic-tac-toe-pipe-helper-pid 1> /tmp/stdout.log 2> /tmp/stderr.log &\"")
#if ret != 0:
#    sys.exit(f"ERROR: Attempting to create a dummy writer returned the error {ret}")


(pid, fd) = os.forkpty()
if pid == 0: #child
    print("child process executing...")

    ret = os.system("bash -c \"cat /tmp/tic-tac-toe-pipe | /home/ubuntu/tic-tac-toe/bin/tic-tac-toe  2> /tmp/errors.log > /tmp/errors.log\"")
    if ret != 0:
        sys.exit(f"ERROR: Attempting to run the program fed by the pipe produced the error {ret}")

else: #parent
    print("parent process executing...")
    print("Attempting to drive the tic-tac-toe game through the parent process...")

    ret = os.system("bash -c 'echo -e \"tl\\nmi\\ntc\\ncl\\ntr\\nq\" >> /tmp/tic-tac-toe-pipe'")
    if ret != 0:
        sys.exit(f"ERROR: Attempting to write a move to the tic-tac-toe game produced the error {ret}")

    print("command sequence fed into the pipe successfully!")

    time.sleep(5)

    # wait for the child process to complete
    status = os.wait()

    # converts to the command: bash -c 'echo -e "tl\nmi\ntc\ncl\ntr" >> /tmp/tic-tac-toe-pipe'
#    ret = os.system("bash -c 'echo -e \"tl\\nmi\\ntc\\ncl\\ntr\" >> /tmp/tic-tac-toe-pipe'")
#    if ret != 0:
#        sys.exit(f"ERROR: Attempting to write a move to the tic-tac-toe game produced the error {ret}")

#    print("Move sequence fed in successfully!")

    # while True:
    #    time.sleep(5)

    #ret = os.system("bash -c \"echo tr >> /tmp/tic-tac-toe-pipe\"")
    #if ret != 0:
    #    sys.exit(f"ERROR: Attempting to write a move to the tic-tac-toe game produced the error {ret}")
    #time.sleep(3)
    #print("Second move fed in")

    #print("removing the pipe...")
    #os.system("rm /tmp/tic-tac-toe-pipe")
    #print("the pipe has been removed...")
