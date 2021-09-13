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
pidlineRE = r"\s*\w+\s+(\d*).*^$"
curr_lineidx = 0
queue_is_empty = False
queued_line = None
ARTIFACTS_DATAPATH = os.getenv('ARTIFACTS_DATAPATH')
CODE_PATH = os.getenv('CODE_PATH')

def eprint(s):
    print(s, file=sys.stderr)

def start_new_test() -> int:
    test_id = time.time() # Epoch time
    eprint(f"Starting a test with ID {test_id}...")

    if Path(f"{ARTIFACTS_DATAPATH}/tic-tac-toe-pipe").exists():
        os.system(f"rm {ARTIFACTS_DATAPATH}/tic-tac-toe-pipe")

    if Path(f"{ARTIFACTS_DATAPATH}/errors_formatted.log").exists():
        os.system(f"ERROR: {ARTIFACTS_DATAPATH}/errors_formatted.log already exists! Exiting the script.")
        sys.exit()

    os.system(f"touch {ARTIFACTS_DATAPATH}/errors_formatted.log")

    ret = os.system(f"bash -c \"mkfifo {ARTIFACTS_DATAPATH}/tic-tac-toe-pipe\"")
    if ret != 0:
        sys.exit(f"ERROR: Attempting to make the FIFO returned the error {ret}")

    (pid, _) = os.forkpty()
    if pid == 0: #child
        eprint("Starting the tic-tac-toe game in the child process...")

        ret = os.system(f"bash -c \"cat {ARTIFACTS_DATAPATH}/tic-tac-toe-pipe | {CODE_PATH}/bin/tic-tac-toe 2> {ARTIFACTS_DATAPATH}/errors.log > {ARTIFACTS_DATAPATH}/errors.log\"")
        if ret != 0:
            sys.exit(f"ERROR: Attempting to run the tic-tac-toe game fed by the pipe produced the error {ret}")

    else: #parent
        eprint("Attempting to drive the tic-tac-toe game through the parent process...")

        #ret = os.system("bash -c 'echo -e \"tl\\nmi\\ntc\\ncl\\ntr\\nq\" >> /tmp/tic-tac-toe-pipe'")

        time.sleep(5)

        # wait for the child process to complete
        status = os.wait()

        f = open(f"{ARTIFACTS_DATAPATH}/errors.log")
        
        lines = f.readlines()

        linesCopy = []

        for line in lines:
            #eprint("Line{}: {}".format(count, line.rstrip("\n")))
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
            eprint("Line {}: {}".format(num, line.rstrip("\n")))
            num += 1

    return 42

def end_test(test_id: int): 
    eprint("Ending the test with id: " + test_id)
    os.system(f"ps -ef | grep tic-tac-toe | grep -v 'grep' >> {ARTIFACTS_DATAPATH}/tic-tac-toe-process-line")
    f = open(f"{ARTIFACTS_DATAPATH}/tic-tac-toe-process-line")
    lines = f.readlines()
    main_line = lines[0]
    result = re.match(pidlineRE, main_line)
    if result != None:
        pid = result.group(1)
        eprint(f"Matched the tic-tac-toe line: Found a tic-tac-toe process running with pid {pid}!")
        eprint("Ending the process now...")
        os.kill(pid, 9)
        eprint("The tic-tac-toe process has been terminated.")
        if Path(f"{ARTIFACTS_DATAPATH}/tic-tac-toe-pipe").exists():
            os.system(f"rm {ARTIFACTS_DATAPATH}/tic-tac-toe-pipe")

def get_last_output_line() -> str:
    global queue_is_empty
    global queued_line

    if not queue_is_empty:
        queue_is_empty = True
        ret = deepcopy(queued_line)
        queued_line = None
        return ret

    # Read the last line of the file and return the next output line, queueing up a line if necessary
    else:

        f = open(f"{ARTIFACTS_DATAPATH}/errors.log")
        f_formatted = open(f"{ARTIFACTS_DATAPATH}/errors_formatted.log", 'w+')
        lines = f.readlines()

        line = lines[-1]
        result        = re.match(ingameinputRE, line)
        secondresult  = re.match(endgameinputRE, line)
        if result != None:
            ret = f"Player {result.group(1)} ({result.group(2)}) to move:"
            second_line = f"{result.group(3)}"

            queue_is_empty = False
            queued_line = deepcopy(second_line)

            return ret

        elif secondresult != None:
            ret = (f"Type 'n' to start a new game, or 'q' or 'quit' to quit:")
            second_line = f"{secondresult.group(1)}"

            queue_is_empty = False
            queued_line = deepcopy(second_line)

            return ret

        else:
            return line 

def make_move(move: str):
    eprint(f"Attempting to make the move: {move}")
    ret = os.system(f"bash -c 'echo -e \"{move}\" >> {ARTIFACTS_DATAPATH}/tic-tac-toe-pipe'")
    if ret != 0:
        sys.exit(f"ERROR: Attempting to write a move to the tic-tac-toe game produced the error {ret}")
    eprint("Move successfully fed into the tic-tac-toe game!")