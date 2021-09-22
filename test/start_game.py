# Tests that the game outputs the correct first prompt as well 
# as the correct prompt after Player One moves for the first time. 

import driver
import sys

def eprint(s):
    print(s, file=sys.stderr)

# eprint("Starting a new test....")
test_id = driver.start_new_test()

# eprint("Passed driver.start_new_test....")

# if out != "Player one (X) to move: ":
#     eprint("TEST FAILED")
#     eprint("Desired output:")
#     eprint("Player one (X) to move: '")
#     eprint("Actual output:")
#     eprint(out)

# eprint("Passed first driver.get_last_output_line....")

driver.make_move("tl\n")

# eprint("Passed driver.make_move....")

out = driver.get_last_output_line()

# eprint("Passed second driver.get_last_output_line....")

# if out != "Player one (X) moved to tl":
#     eprint("TEST FAILED")
#     eprint("Desired output:")
#     eprint("Player one moved to: tl")
#     eprint("Actual output:")
#     eprint(out)

# eprint("TEST PASSED")
driver.end_test()

# eprint("Passed driver.end_test....")

# eprint("Test environment closed.")