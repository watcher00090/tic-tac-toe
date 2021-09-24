package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
	//	"os/signal"
	//	"syscall"
	//	"bytes"
)

var w *bufio.Writer = bufio.NewWriter(os.Stdout)

var boardbase = "   \u2506   \u2506   " +
	"-----------" +
	"   \u2506   \u2506   " +
	"-----------" +
	"   \u2506   \u2506   "

var board map[string]string = map[string]string{
	"tl": "",
	"tc": "",
	"tr": "",
	"cl": "",
	"cc": "",
	"cr": "",
	"bl": "",
	"bc": "",
	"br": "",
}

func changePlayer(player string) string {
	if player == "one" {
		return "two"
	} else {
		return "one"
	}
}

func changeToken(token string) string {
	if token == "X" {
		return "O"
	} else {
		return "X"
	}
}

func niceify(in string) string {
	move := strings.ToLower(in)
	if move == "lt" {
		return "tl"
	}
	if move == "ct" {
		return "tc"
	}
	if move == "rt" {
		return "tr"
	}
	if move == "lc" {
		return "cl"
	}
	if move == "m" || move == "mi" || move == "c" {
		return "cc"
	}
	if move == "rc" {
		return "cr"
	}
	if move == "lb" {
		return "bl"
	}
	if move == "cb" {
		return "bc"
	}
	if move == "rb" {
		return "br"
	}
	return move
}

func isValidMove(move string) bool {
	return move == "tl" || move == "tc" || move == "tr" || move == "cl" || move == "cc" || move == "cr" || move == "bl" || move == "bc" || move == "br"
}

func toDisplayString(s string) string {
	if s == "" {
		return " "
	} else {
		return s
	}
}

func clearBoard() {
	board["tl"] = ""
	board["tc"] = ""
	board["tr"] = ""
	board["cl"] = ""
	board["cc"] = ""
	board["cr"] = ""
	board["bl"] = ""
	board["bc"] = ""
	board["br"] = ""
}

func hasWon(board map[string]string, token string) bool {
	return board["tl"] == token && board["tc"] == token && board["tr"] == token ||
		board["cl"] == token && board["cc"] == token && board["cr"] == token ||
		board["bl"] == token && board["bc"] == token && board["br"] == token ||
		board["tl"] == token && board["cc"] == token && board["br"] == token ||
		board["tr"] == token && board["cc"] == token && board["bl"] == token ||
		board["tl"] == token && board["cl"] == token && board["bl"] == token ||
		board["tc"] == token && board["cc"] == token && board["bc"] == token ||
		board["tr"] == token && board["cr"] == token && board["br"] == token
}

func printBoard(board map[string]string) {
	writeToStdout("\n %s ┆ %s ┆ %s \n"+
		"-----------\n"+
		" %s ┆ %s ┆ %s \n"+
		"-----------\n"+
		" %s ┆ %s ┆ %s \n\n",
		toDisplayString(board["tl"]),
		toDisplayString(board["tc"]),
		toDisplayString(board["tr"]),
		toDisplayString(board["cl"]),
		toDisplayString(board["cc"]),
		toDisplayString(board["cr"]),
		toDisplayString(board["bl"]),
		toDisplayString(board["bc"]),
		toDisplayString(board["br"]),
	)
}
func writeToStdout(a ...interface{}) (int, error) {
	n, err := fmt.Fprintln(w, a...)
	w.Flush()
	return n, err
}

func main() {
	var player = "one"
	var token = "X"
	var move string
	var move_orig string
	var numMoves = 0
	var err error
	var in string
	var input string
	var input_prompt_msg string
	var move_command string

	var expectingMove = true // when the user can make a move or submit a command, exactly one of the following is true: expectingMove, continueOrExit
	var continueOrExit = false
	var shouldPrintInputPrompt = true
	var input_commands_chan chan string

	input_prompt_msg = fmt.Sprintf("Player %s (%s) to move: ", player, token)

	// The elements are the commands that the user has submitted
	input_commands_chan = make(chan string)

	// Thread that registers all input from stdin
	go func(input_commands_chan chan string) {
		for { // Continuously poll Stdin to check for new user input
			fmt.Println("Trying to fetch data from stdin...")
			//bytes, ioutil_err := io.ReadAll(os.Stdin)

			var input_str string
			n, io_err := fmt.Scanf("%s", &input_str)
			if err != nil {
				panic(err)
			}

			fmt.Println("Fetched data from stdin...")
			if n == 0 { // no data inputted
				shouldPrintInputPrompt = true
			} else if io_err != nil { // I/O error
				panic(fmt.Sprintf("ERROR: After calling ReadAll(stdin) in the input thread, the following error was returned: %s\n", io_err.Error()))
			} else { // Write the first line of the input string to the input commands channel
				//lines := strings.Split(input_str, "\n")
				//first_command := lines[0]
				input_commands_chan <- input_str
				writeToStdout("Sent a move command to the game logic thread.")
			}
			// Sleep for 50 milliseconds before polling again
			time.Sleep(time.Millisecond * 50)
		}
	}(input_commands_chan)

	// Continously poll the input_commands_chan checking for new commands and if so respond accordingly
	for {
		// Print the prompt if we haven't already
		if shouldPrintInputPrompt {
			writeToStdout(input_prompt_msg)
		}

		writeToStdout("Polling the input commands channel....")

		// Wait until a move command is submitted
		move_command = <-input_commands_chan

		// Remove spaces and whitespace from the input
		in = strings.Trim(string(move_command), "\n\r\t ")

		if (expectingMove && continueOrExit) || (!expectingMove && !continueOrExit) {
			panic("ERROR: Exactly one of expectingMove and continueOrExit should be true. We goofed, sorry. Exiting now...")
		}

		if expectingMove {

			move = niceify(in)

			if move == "help" || move == "h" || move == "info" || move == "i" {

				writeToStdout("\nMove commands: \n" +
					"tl, lt (top left)\n" +
					"tc, ct (top center)\n" +
					"tr, rt (top right)\n" +
					"cl, lc (center left)\n" +
					"m, mi, cc, or c (center)\n" +
					"cr, rc (center right)\n" +
					"bl, lb (bottom left)\n" +
					"bc, cb (bottom center)\n" +
					"br, rb (bottom right)\n")
				shouldPrintInputPrompt = true

			} else if move == "board" || move == "print" || move == "p" {

				printBoard(board)
				shouldPrintInputPrompt = true

			} else if !isValidMove(move) {

				writeToStdout("Error, invalid move command. Please try again.")
				writeToStdout("\nMove commands: \n" +
					"tl, lt (top left)\n" +
					"tc, ct (top center)\n" +
					"tr, rt (top right)\n" +
					"cl, lc (center left)\n" +
					"m, mi, cc, or c (center)\n" +
					"cr, rc (center right)\n" +
					"bl, lb (bottom left)\n" +
					"bc, cb (bottom center)\n" +
					"br, rb (bottom right)\n")
				shouldPrintInputPrompt = true

			} else {
				// Make the move, update the game state
				if board[move] != "" {
					writeToStdout("Error, the square you attempted to move to is already occupied! Please choose a different square and try again.")
					shouldPrintInputPrompt = true
					continue
				}

				board[move] = token
				numMoves++
				writeToStdout(fmt.Sprintf("Player %s (%s) moved to: %s", player, token, move_orig))

				printBoard(board)

				has_won := hasWon(board, token)

				if has_won || (!has_won && numMoves == 9) {

					expectingMove = false
					continueOrExit = true
					if has_won {
						writeToStdout(fmt.Sprintf("Player %s (%s) has won the game!", player, token))
					} else {
						writeToStdout("Draw!")
					}
					input_prompt_msg = "Type 'n' to start a new game, or 'q' or 'quit' to quit: "
					shouldPrintInputPrompt = true

				} else {

					player = changePlayer(player)
					token = changeToken(token)

					input_prompt_msg = fmt.Sprintf("Player %s (%s) to move: ", player, token)
					shouldPrintInputPrompt = true

				}
			}

		} else if continueOrExit {

			input = in
			input = strings.ToLower(input)

			if input == "q" || input == "exit" || input == "quit" {
				_, err_2 := writeToStdout("Exiting", "the", "game...")
				// exec.Command("echo 3 | sudo tee /proc/sys/vm/drop_caches")
				writeToStdout("Exited successfully.")
				// time.Sleep(5)
				if err_2 == nil {
					os.Exit(0)
				} else {
					writeToStdout("ERROR: Printing a message prior to exiting produced the error: " + err.Error())
					os.Exit(1)
				}
			} else if input == "n" || input == "new game" || input == "new" {
				writeToStdout("Starting new game....")
				clearBoard()
				player = "one"
				token = "X"
				numMoves = 0
				expectingMove = true
				continueOrExit = false
				input_prompt_msg = fmt.Sprintf("Player %s (%s) to move: ", player, token)
				shouldPrintInputPrompt = true
				writeToStdout("Got here")
			} else {
				writeToStdout("Invalid instruction, please try again...")
			}
		}
		// Sleep for 50 milliseconds before polling again
		time.Sleep(time.Millisecond * 50)
	}
}
