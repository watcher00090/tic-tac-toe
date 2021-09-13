# Tests that the game outputs the correct first prompt as well 
# as the correct prompt after Player One moves for the first time. 

import driver

print("Starting a new test....")
test_id = driver.start_new_test()

out = driver.get_last_output_line()
if out != "Player one (X) to move: ":
    print("TEST FAILED")
    print("Desired output:")
    print("Player one (X) to move: '")
    print("Actual output:")
    print(out)

driver.make_move("tl")
out = driver.get_last_output_line()

if out != "Player one (X) moved to tl":
    print("TEST FAILED")
    print("Desired output:")
    print("Player one moved to: tl")
    print("Actual output:")
    print(out)

print("TEST PASSED")
driver.end_test(test_id)

print("Test environment closed.")