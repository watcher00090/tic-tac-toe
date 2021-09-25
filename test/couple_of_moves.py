import driver
import sys

print("Starting a new test....")
test_id = driver.start_new_test()
print("Test has been started.")

print("Making the first move...")
driver.make_move("tl\n")
print("Successfully made the first move!")

print("Making the second move...")
driver.make_move("tr\n")
print("Successfully made the second move!")

print("Making the third move...")
driver.make_move("mi\n")
print("Successfully made the third move!")

print("Ending the test now...")
driver.end_test()
print("The test has been ended.")
