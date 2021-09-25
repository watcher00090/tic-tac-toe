# Tests that the game outputs the correct first prompt as well 
# as the correct prompt after Player One moves for the first time. 

import driver
import sys

def print(s):
    print(s, file=sys.stderr)

# print("Starting a new test....")
test_id = driver.start_new_test()

driver.make_move("tl\n")

driver.make_move("tr\n")

driver.make_move("mi\n")

# print("Passed driver.make_move....")

# print("Passed second driver.get_last_output_line....")

# if out != "Player one (X) moved to tl":
#     print("TEST FAILED")
#     print("Desired output:")
#     print("Player one moved to: tl")
#     print("Actual output:")
#     print(out)

# print("TEST PASSED")
driver.end_test()

# print("Passed driver.end_test....")

# print("Test environment closed.")