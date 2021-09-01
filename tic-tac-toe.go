package main

import (
	"fmt"
	"os"
	"strings"
	"bufio"
)

var boardbase = "   ┆   ┆   " +
	"-----------" +
	"   ┆   ┆   " +
	"-----------" +
	"   ┆   ┆   "

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
	reader := bufio.NewReader(os.Stdin)
	var err error
	var in []byte
	var input string

	for true {
		fmt.Print(fmt.Sprintf("Player %s (%s) to move: ", player, token))
		//fmt.Scanln(&move)
		in, _, err =  reader.ReadLine()
		if err != nil {
			fmt.Println("ERROR: ReadLine returned the error: " + err.Error())
		}

		move = string(in)
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
		} else if move == "board" {
			printBoard(board)
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
		} else {

			if board[move] != "" {
				fmt.Println("Error, the square you attempted to move to is already occupied! Please choose a different square and try again.")
				continue
			}

			board[move] = token
			numMoves++
			fmt.Print(fmt.Sprintf("Player %s (%s) moved to: %s\n", player, token, move_orig))

			printBoard(board)

			has_won := hasWon(board, token)

			if has_won || (!has_won && numMoves == 9) {
				if has_won {
					fmt.Printf("Player %s (%s) has won the game!\n", player, token)
				} else {
					fmt.Printf("Draw!\n")
				}
				for true {
					fmt.Print("Type 'n' to start a new game, or 'q' or 'quit' to quit: ")
					in, _, err =  reader.ReadLine()
					if err != nil {
						panic("ERROR: ReadLine returned the error: " + err.Error())
					}
					input = string(in)
					input = strings.ToLower(input)

					if input == "q" || input == "exit" || input == "quit" {
						fmt.Println("Exiting the game...")
						os.Exit(0)
					} else if input == "n" || input == "new game" || input == "new" {
						fmt.Println("Starting new game....")
						clearBoard()
						player = "one"
						token = "X"
						numMoves = 0
						break
					} else {
						fmt.Println("Invalid instruction, please try again...")
					}
				}
			} else {
				player = changePlayer(player)
				token = changeToken(token)
			}
		}
	}
}
