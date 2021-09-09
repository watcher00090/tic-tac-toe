# Tests that the game outputs the correct first prompt as well 
# as the correct prompt after Player One moves for the first time. 

def start_game(driver):
    out = driver.get_last_output_line()
    if out != "Player one (X) to move: ":
        print("TEST FAILED")
        print("Desired output:")
        print("Player one (X) to move: '")
        print("Actual output:")
        print(out)
        return False

    driver.make_move("tl")
    out = driver.get_last_output_line()

    if out != "Player one (X) moved to tl":
        print("TEST FAILED")
        print("Desired output:")
        print("Player one moved to: tl")
        print("Actual output:")
        print(out)
        return False

    print("TEST PASSED")
    return True