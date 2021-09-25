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

STDIN_PIPE_READ_END  = None
STDIN_PIPE_WRITE_END  = None
STDOUT_PIPE_READ_END = None
STDOUT_PIPE_WRITE_END = None
STDERR_PIPE_READ_END = None
STDERR_PIPE_WRITE_END = None 

STDIN_PIPE_READ_END_FILEHANDLE = None
STDIN_PIPE_WRITE_END_FILEHANDLE = None
STDOUT_PIPE_READ_END_FILEHANDLE = None
STDOUT_PIPE_WRITE_END_FILEHANDLE = None
STDERR_PIPE_READ_END_FILEHANDLE = None
STDERR_PIPE_WRITE_END_FILEHANDLE = None


def start_new_test() -> int:
    global OUTPUT_FILE
    global tic_tac_toe_proc
    global output_lines
    global curr_lineidx

    global STDIN_PIPE_READ_END 
    global STDIN_PIPE_WRITE_END
    global STDOUT_PIPE_READ_END
    global STDOUT_PIPE_WRITE_END
    global STDERR_PIPE_READ_END
    global STDERR_PIPE_WRITE_END

    global STDIN_PIPE_READ_END_FILEHANDLE
    global STDIN_PIPE_WRITE_END_FILEHANDLE
    global STDOUT_PIPE_READ_END_FILEHANDLE
    global STDOUT_PIPE_WRITE_END_FILEHANDLE
    global STDERR_PIPE_READ_END_FILEHANDLE
    global STDERR_PIPE_WRITE_END_FILEHANDLE

    test_id = time.time_ns() # Epoch time in nanoseconds
    print(f"Starting a test with ID {test_id}...")

    OUTPUT_FILE = open(os.path.join(f"{ARTIFACTS_DATAPATH}", "errors.log"), mode = 'a') # Append to the file if it already exists
    OUTPUT_FILE.write(TEST_START_HEADER)

    STDIN_PIPE_READ_END, STDIN_PIPE_WRITE_END   = os.pipe()
    STDOUT_PIPE_READ_END, STDOUT_PIPE_WRITE_END = os.pipe()
    STDERR_PIPE_READ_END, STDERR_PIPE_WRITE_END = os.pipe()

    # The final 0 is to disable buffering
    STDIN_PIPE_READ_END_FILEHANDLE   = os.fdopen(STDIN_PIPE_READ_END, 'r', 0)
    STDIN_PIPE_WRITE_END_FILEHANDLE  = os.fdopen(STDIN_PIPE_WRITE_END, 'rw', 0)
    STDOUT_PIPE_READ_END_FILEHANDLE  = os.fdopen(STDOUT_PIPE_READ_END, 'r', 0)
    STDOUT_PIPE_WRITE_END_FILEHANDLE = os.fdopen(STDOUT_PIPE_WRITE_END, 'rw', 0)
    STDERR_PIPE_READ_END_FILEHANDLE  = os.fdopen(STDERR_PIPE_READ_END, 'r', 0)
    STDERR_PIPE_WRITE_END_FILEHANDLE = os.fdopen(STDERR_PIPE_WRITE_END, 'rw', 0)

    output_lines = []
    curr_lineidx = 0

    print("Running the tic-tac-toe game as a subprocess...")
    paths = ["bin", "tic-tac-toe"]

    tic_tac_toe_proc = subprocess.Popen(os.path.join(os.path.join(f"{CODE_PATH}", "bin"), "tic-tac-toe"), 
        stdin=STDIN_PIPE_READ_END_FILEHANDLE, 
        stdout=STDOUT_PIPE_WRITE_END_FILEHANDLE, 
        stderr=STDERR_PIPE_WRITE_END_FILEHANDLE, 
        text=True
    )
    time.sleep(5)
    print("The tic-tac-toe process has been started!")

def end_test(): 
    global STDIN_PIPE_READ_END 
    global STDIN_PIPE_WRITE_END
    global STDOUT_PIPE_READ_END
    global STDOUT_PIPE_WRITE_END
    global STDERR_PIPE_READ_END
    global STDERR_PIPE_WRITE_END
    global STDIN_PIPE_READ_END_FILEHANDLE
    global STDIN_PIPE_WRITE_END_FILEHANDLE
    global STDOUT_PIPE_READ_END_FILEHANDLE
    global STDOUT_PIPE_WRITE_END_FILEHANDLE
    global STDERR_PIPE_READ_END_FILEHANDLE
    global STDERR_PIPE_WRITE_END_FILEHANDLE

    print("Closing the input and output pipes for the tic-tac-toe process...")

    os.close(STDIN_PIPE_READ_END)
    os.close(STDIN_PIPE_WRITE_END)
    os.close(STDOUT_PIPE_READ_END)
    os.close(STDOUT_PIPE_WRITE_END)
    os.close(STDERR_PIPE_READ_END)
    os.close(STDERR_PIPE_WRITE_END)

    STDIN_PIPE_READ_END = None
    STDIN_PIPE_WRITE_END = None
    STDOUT_PIPE_READ_END = None
    STDOUT_PIPE_WRITE_END = None
    STDERR_PIPE_READ_END = None
    STDERR_PIPE_WRITE_END = None

    STDIN_PIPE_READ_END_FILEHANDLE = None
    STDIN_PIPE_WRITE_END_FILEHANDLE = None
    STDOUT_PIPE_READ_END_FILEHANDLE = None
    STDOUT_PIPE_WRITE_END_FILEHANDLE = None
    STDERR_PIPE_READ_END_FILEHANDLE = None
    STDERR_PIPE_WRITE_END_FILEHANDLE = None

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

    global STDIN_PIPE_READ_END_FILEHANDLE
    global STDIN_PIPE_WRITE_END_FILEHANDLE
    global STDOUT_PIPE_READ_END_FILEHANDLE
    global STDOUT_PIPE_WRITE_END_FILEHANDLE
    global STDERR_PIPE_READ_END_FILEHANDLE
    global STDERR_PIPE_WRITE_END_FILEHANDLE

    STDIN_PIPE_WRITE_END_FILEHANDLE.write(move)
    stdout_str = STDOUT_PIPE_READ_END_FILEHANDLE.readline()
    stderr_str = STDOUT_PIPE_READ_END_FILEHANDLE.readline()
    OUTPUT_FILE.write(stderr_str)
    OUTPUT_FILE.write(stdout_str)

        # stderr_chunks = stderr_str.splitlines()
        # stdout_chunks = stdout_str.splitlines()
        # for stderr_chunk in stderr_chunks:
        #     output_lines.append(stderr_chunk)
        # for stdout_chunk in stdout_chunks:
        #     output_lines.append(stdout_chunk)

    # except TimeoutExpired:
    #     print("ERROR, unable to communicate with the tic-tac-toe-process within the specified timeout. Killing the process now...")
    #     tic_tac_toe_proc.kill()
    #     out, errs = tic_tac_toe_proc.communicate()
    #     print(f"The output after killing the tic-tac-toe process was: {out}")
    #     print(f"The errors after killing the tic-tac-toe process were: {errs}")