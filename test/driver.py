import subprocess
import os
import time
import sys
from subprocess import TimeoutExpired

ingameinputRE = r"Player (one|two) \((X|O)\) to move\: (.+)$"
endgameinputRE = r"Type 'n' to start a new game, or 'q' or 'quit' to quit\: (.+)$"
pidlineRE = r"\s*\w+\s+(\d*).*^$"
curr_lineidx = None
output_lines = None
ARTIFACTS_DATAPATH = os.getenv('ARTIFACTS_DATAPATH')
CODE_PATH = os.getenv('CODE_PATH')
OUTPUT_FILE = None
TEST_START_HEADER = "------------------------------------------------\n"
tic_tac_toe_proc = None
PROC_COMMUNICATION_TIMEOUT = 15

def print(s):
    print(s, file=sys.stdout)

def start_new_test() -> int:
    global OUTPUT_FILE
    global tic_tac_toe_proc
    global output_lines
    global curr_lineidx

    test_id = time.time_ns() # Epoch time in nanoseconds
    print(f"Starting a test with ID {test_id}...")

    OUTPUT_FILE = open(os.path.join(f"{ARTIFACTS_DATAPATH}", "errors.log"), mode = 'a') # Append to the file if it already exists
    OUTPUT_FILE.write(TEST_START_HEADER)

    output_lines = []
    curr_lineidx = 0

    print("Running the tic-tac-toe game as a subprocess...")
    paths = ["bin", "tic-tac-toe"]

    tic_tac_toe_proc = subprocess.Popen(os.path.join(os.path.join(f"{CODE_PATH}", "bin"), "tic-tac-toe"), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    time.sleep(5)
    print("The tic-tac-toe process has been started!")

def end_test(): 
    print("Ending the test...")
    tic_tac_toe_proc.kill()
    out, errs = tic_tac_toe_proc.communicate()
    print(f"The output after killing the tic-tac-toe process was {out}")
    print(f"The errors after killing the tic-tac-toe process were {errs}")

# Return the last output line. Return None if no such line exists. Otherwise return the line.
def get_last_output_line():
    global curr_lineidx
    global output_lines
    print("Getting the last output line...")
    if curr_lineidx <= len(output_lines)-1:
        ret = output_lines[curr_lineidx]
        curr_lineidx += 1
        print(f"Last output line = {ret}")
        return ret
    else:
        print(f"Last output line = {None}")
        return None

def make_move(move: str):
    global OUTPUT_FILE
    global output_lines
    try:
        stdout_data, stderr_data = tic_tac_toe_proc.communicate(input=move, timeout=PROC_COMMUNICATION_TIMEOUT)
        OUTPUT_FILE.write(stderr_data)
        OUTPUT_FILE.write(stdout_data)

        stderr_chunks = stderr_data.splitlines()
        stdout_chunks = stdout_data.splitlines()
        for stderr_chunk in stderr_chunks:
            output_lines.append(stderr_chunk)
        for stdout_chunk in stdout_chunks:
            output_lines.append(stdout_chunk)

    except TimeoutExpired:
        print("ERROR, unable to communicate with the tic-tac-toe-process within the specified timeout. Killing the process now...")
        tic_tac_toe_proc.kill()
        out, errs = tic_tac_toe_proc.communicate()
        print(f"The output after killing the tic-tac-toe process was: {out}")
        print(f"The errors after killing the tic-tac-toe process were: {errs}")