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

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

# Ensure that stdout is unbuffered
sys.stdout = Unbuffered(sys.stdout)

STDIN_PIPE  = "STDIN_PIPE"
OUTPUT_PIPE = "OUTPUT_PIPE"

STDIN_PIPE_READ_END_FD= None
STDIN_PIPE_WRITE_END_FD= None
OUTPUT_PIPE_READ_END_FD= None
OUTPUT_PIPE_WRITE_END_FD= None

def start_new_test() -> int:
    global OUTPUT_FILE
    global tic_tac_toe_proc
    global output_lines
    global curr_lineidx

    global STDIN_PIPE
    global OUTPUT_PIPE

    global STDIN_PIPE_READ_END_FD
    global STDIN_PIPE_WRITE_END_FD
    global OUTPUT_PIPE_READ_END_FD
    global OUTPUT_PIPE_WRITE_END_FD

    test_id = time.time_ns() # Epoch time in nanoseconds
    print(f"Starting a test with ID {test_id}...")

    OUTPUT_FILE = open(os.path.join(f"{ARTIFACTS_DATAPATH}", "errors.log"), mode = 'a') # Append to the file if it already exists
    OUTPUT_FILE.write(TEST_START_HEADER)

    STDIN_PIPE = f"{ARTIFACTS_DATAPATH}/stdin_pipe"
    OUTPUT_PIPE = f"{ARTIFACTS_DATAPATH}/output_pipe"
    os.system(f"mkfifo {STDIN_PIPE}")
    os.system(f"mkfifo {OUTPUT_PIPE}")

    STDIN_PIPE_READ_END_FD  = os.open(STDIN_PIPE, os.O_RDONLY)
    STDIN_PIPE_WRITE_END_FD = os.open(STDIN_PIPE, os.O_WRONLY)
    OUTPUT_PIPE_READ_END_FD = os.open(OUTPUT_PIPE, os.O_RDONLY)
    OUTPUT_PIPE_WRITE_END_FD= os.open(OUTPUT_PIPE, os.O_WRONLY)

    output_lines = []
    curr_lineidx = 0

    print("Running the tic-tac-toe game as a subprocess...")
    paths = ["bin", "tic-tac-toe"]

    tic_tac_toe_proc = subprocess.Popen(os.path.join(os.path.join(f"{CODE_PATH}", "bin"), "tic-tac-toe"), 
        stdin=STDIN_PIPE_READ_END_FD, 
        stdout=OUTPUT_PIPE_WRITE_END_FD, 
        # stderr=OUTPUT_PIPE_WRITE_END_FILEHANDLE, 
        text=True
    )
    time.sleep(5)
    print("The tic-tac-toe process has been started!")

def end_test(): 
    global STDIN_PIPE_READ_END_FD
    global STDIN_PIPE_WRITE_END_FD
    global OUTPUT_PIPE_READ_END_FD
    global OUTPUT_PIPE_WRITE_END_FD

    print("Closing the input and output pipes for the tic-tac-toe process...")

    os.close(STDIN_PIPE_READ_END_FD)
    os.close(STDIN_PIPE_WRITE_END_FD)
    os.close(OUTPUT_PIPE_READ_END_FD)
    os.close(OUTPUT_PIPE_WRITE_END_FD)

    STDIN_PIPE_READ_END_FD   = None
    STDIN_PIPE_WRITE_END_FD  = None
    OUTPUT_PIPE_READ_END_FD  = None
    OUTPUT_PIPE_WRITE_END_FD = None

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
    print(f"Trying to make a move....")

    global OUTPUT_FILE
    global output_lines

    global STDIN_PIPE_READ_END_FD
    global STDIN_PIPE_WRITE_END_FD
    global OUTPUT_PIPE_READ_END_FD
    global OUTPUT_PIPE_WRITE_END_FD

    os.write(STDIN_PIPE_WRITE_END_FD, move.encode('utf-8'))
    print(f"Successfully pushed the move into the pipe...")
    last_line = OUTPUT_PIPE_READ_END_FD.readline()
    print(f"Successfully got the next line of output from the output pipe...")
    OUTPUT_FILE.write(last_line)
    print(f"Successfully wrote the next line of output to the output file....")
    
    output_lines.append(last_line)

        # stderr_chunks = stderr_str.splitlines()
        # stdout_chunks = stdout_str.splitlines()
        # for stderr_chunk in stderr_chunks:
        #     output_lines.append(stderr_chunk)
        # for stdout_chunk in stdout_chunks:
        #     output_lines.append(stdout_chunk)