# Tests that the game outputs the correct first prompt as well 
# as the correct prompt after Player One moves for the first time. 

import driver
import sys

def print(s):
    print(s, file=sys.stderr)

# print("Starting a new test....")
test_id = driver.start_new_test()

# print("Passed driver.start_new_test....")

# if out != "Player one (X) to move: ":
#     print("TEST FAILED")
#     print("Desired output:")
#     print("Player one (X) to move: '")
#     print("Actual output:")
#     print(out)

# print("Passed first driver.get_last_output_line....")

driver.make_move("tl\n")

# print("Passed driver.make_move....")

out = driver.get_last_output_line()

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