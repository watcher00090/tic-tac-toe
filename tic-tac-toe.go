package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"

	//	"time"
	"os/exec"
	//	"os/signal"
	//	"syscall"
	//	"bytes"
)

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

func niceify(move string) string {
	move = strings.ToLower(move)
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
	fmt.Printf("\n %s ┆ %s ┆ %s \n"+
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

func main() {
	var player = "one"
	var token = "X"
	var move string
	var move_orig string
	numMoves := 0
	var err error
	var in string
	var input string
	var input_prompt_msg string

	var expectingMove = true // when the user can make a move or submit a command, exactly one of the following is true: expectingMove, continueOrExit
	var continueOrExit = false
	var alreadyPrintedPrompt = false

	input_prompt_msg = fmt.Sprintf("Player %s (%s) to move: ", player, token)

	for {
		if !alreadyPrintedPrompt {
			fmt.Print(input_prompt_msg)
		}

		bytes, ioutil_err := ioutil.ReadAll(os.Stdin)
		if len(bytes) == 0 || ioutil_err != nil {
			time.Sleep(5 * time.Second)
			alreadyPrintedPrompt = true
			continue
		}

		//fmt.Printf("in = %s.\n", in)
		in = strings.Trim(string(bytes), "\n\r\t ")
		// if err != nil {
		// 	if strings.ToUpper(err.Error()) == "EOF" {
		// 		time.Sleep(5 * time.Second)
		// 		alreadyPrintedPrompt = true
		// 		continue
		// 	} else {
		// 		panic(fmt.Sprintf("ERROR: ReadLine returned the error: %s\n", err.Error()))
		// 	}
		// }

		if (expectingMove && continueOrExit) || (!expectingMove && !continueOrExit) {
			panic("ERROR, exactly one of expectingMove and continueOrExit should be true!")
		}

		// fmt.Printf("in = %s.\n", in)

		if expectingMove {

			move = in
			move_orig = move
			move = niceify(move)

			if move == "help" {
				fmt.Println("\nMove commands: \n" +
					"tl, lt (top left)\n" +
					"tc, ct (top center)\n" +
					"tr, rt (top right)\n" +
					"cl, lc (center left)\n" +
					"m, mi, cc, or c (center)\n" +
					"cr, rc (center right)\n" +
					"bl, lb (bottom left)\n" +
					"bc, cb (bottom center)\n" +
					"br, rb (bottom right)\n")
				alreadyPrintedPrompt = false
			} else if move == "board" {
				printBoard(board)
				alreadyPrintedPrompt = false
			} else if !isValidMove(move) {
				fmt.Println("Error, invalid move command. Please try again.")
				fmt.Println("\nMove commands: \n" +
					"tl, lt (top left)\n" +
					"tc, ct (top center)\n" +
					"tr, rt (top right)\n" +
					"cl, lc (center left)\n" +
					"m, mi, cc, or c (center)\n" +
					"cr, rc (center right)\n" +
					"bl, lb (bottom left)\n" +
					"bc, cb (bottom center)\n" +
					"br, rb (bottom right)\n")
				alreadyPrintedPrompt = false
			} else {

				if board[move] != "" {
					fmt.Println("Error, the square you attempted to move to is already occupied! Please choose a different square and try again.")
					alreadyPrintedPrompt = false
					continue
				}

				board[move] = token
				numMoves++
				fmt.Print(fmt.Sprintf("Player %s (%s) moved to: %s\n", player, token, move_orig))

				printBoard(board)

				has_won := hasWon(board, token)

				if has_won || (!has_won && numMoves == 9) {
					expectingMove = false
					continueOrExit = true
					if has_won {
						fmt.Printf("Player %s (%s) has won the game!\n", player, token)
					} else {
						fmt.Printf("Draw!\n")
					}
					input_prompt_msg = "Type 'n' to start a new game, or 'q' or 'quit' to quit: "
					alreadyPrintedPrompt = false
				} else {
					player = changePlayer(player)
					token = changeToken(token)

					input_prompt_msg = fmt.Sprintf("Player %s (%s) to move: ", player, token)
					alreadyPrintedPrompt = false
				}
			}

		} else if continueOrExit {

			input = in
			input = strings.ToLower(input)

			if input == "q" || input == "exit" || input == "quit" {
				_, err_2 := fmt.Fprintln(os.Stdout, "Exiting", "the", "game...")
				exec.Command("echo 3 | sudo tee /proc/sys/vm/drop_caches")
				fmt.Println("Exited successfully.")
				// time.Sleep(5)
				if err_2 == nil {
					os.Exit(0)
				} else {
					fmt.Println("ERROR: Outputting a message prior to exiting produced the error: " + err.Error())
					os.Exit(1)
				}
			} else if input == "n" || input == "new game" || input == "new" {
				fmt.Println("Starting new game....")
				clearBoard()
				player = "one"
				token = "X"
				numMoves = 0
				expectingMove = true
				continueOrExit = false
				input_prompt_msg = fmt.Sprintf("Player %s (%s) to move: ", player, token)
				alreadyPrintedPrompt = false
			} else {
				fmt.Println("Invalid instruction, please try again...")
			}
		}
	}
}
