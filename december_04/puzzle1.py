#!/usr/bin/env python3

"""
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards on which it appears.
(Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked,
that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time.
It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input).

For example:
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners,
but the boards are marked as follows (shown here adjacent to each other to save space):
 22  13  17 *11*  0        3  15   0   2  22        14  21  17  24  *4*
  8   2  23  *4* 24       *9* 18  13  17  *5*       10  16  15  *9* 19
 21  *9* 14  16  *7*      19   8  *7* 25  23        18   8  23  26  20
  6  10   3  18  *5*      20 *11* 10  24  *4*       22 *11* 13   6  *5*
  1  12  20  15  19       14  21  16  12   6         2   0  12   3  *7*

After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:
 22  13 *17**11* *0*       3  15  *0* *2* 22       *14**21**17* 24  *4*
  8  *2**23* *4* 24       *9* 18  13 *17* *5*       10  16  15  *9* 19
*21* *9**14* 16  *7*      19   8  *7* 25 *23*       18   8 *23* 26  20
  6  10   3  18  *5*      20 *11* 10  24  *4*       22 *11* 13   6  *5*
  1  12  20  15  19       14 *21* 16  12   6        *2* *0* 12   3  *7*

Finally, 24 is drawn:
 22  13 *17**11* *0*       3  15  *0* *2* 22       *14**21**17**24* *4*
  8  *2**23* *4**24*      *9* 18  13 *17* *5*       10  16  15  *9* 19
*21* *9**14* 16  *7*      19   8  *7* 25 *23*       18   8 *23* 26  20
  6  10   3  18  *5*      20 *11* 10 *24* *4*       22 *11* 13   6  *5*
  1  12  20  15  19       14 *21* 16  12   6        *2* *0* 12   3  *7*

At this point, the third board wins because it has at least one complete row or column of marked numbers
(in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers
on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won,
24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first.
What will your final score be if you choose that board?
"""


def find_number_in_board(number, board):
    """
    Check whether a given number can be found in a board.
    Returns (row, column) in case the number can be found, None otherwise.
    """
    for i, row in enumerate(board):
        try:
            column = row.index(number)
            return (i, column)
        except:
            pass

    return None


def board_has_just_won(marked_board, row, column):
    """
    Checks whether a given board has reached the "bingo" state by
    verifying the specified row and/or column: in case either of them contains
    five "True" values, the board has won.
    """
    global BOARD_SIZE

    winner_candidate = [x for x in marked_board[row] if x]
    if len(winner_candidate) == BOARD_SIZE:
        return True

    winner_candidate = [tmp_row[column] for tmp_row in marked_board if tmp_row[column]]
    if len(winner_candidate) == BOARD_SIZE:
        return True

    return False


def print_board(board):
    """
    Prints the board
    """
    print(f"\nBoard:")
    for i in range(BOARD_SIZE):
        print(board[i])


def print_board_markers(marked_board):
    """
    Prints the board markers
    """
    print(f"\nBoard markers:")
    for i in range(BOARD_SIZE):
        print(["X" if x else "-" for x in marked_board[i]])


# Read the input and prepare the variables holding the data
INPUT_FILE = "./input.txt"
BOARD_SIZE = 5
numbers_drawn = None
boards = []  # Original data (3D)
marked_boards = []  # Flags (3D) for the numbers being already marked (=drawn)
remaining_board_sum = []  # Register for the remaining sum on the board not yet marked

with open(INPUT_FILE, "r") as infile:
    numbers_drawn = [int(x) for x in infile.readline().strip().split(",")]

    while infile.readline():
        board = []
        marked_board = []
        remaining_board_sum.append(0)

        for i in range(BOARD_SIZE):
            row = [int(x) for x in infile.readline().strip().split()]
            board.append(row)
            marked_board.append([False for x in range(BOARD_SIZE)])
            remaining_board_sum[-1] += sum(row)

        boards.append(board)
        marked_boards.append(marked_board)

# Process the input
final_score = None
for number in numbers_drawn:
    for i, board in enumerate(boards):

        position = find_number_in_board(number, board)
        if position:
            (row, column) = position
            marked_boards[i][row][column] = True
            remaining_board_sum[i] -= number
            if board_has_just_won(marked_boards[i], row, column):
                print(f"\nBoard #{i} has just won!")
                print_board(board)
                print_board_markers(marked_boards[i])
                final_score = remaining_board_sum[i] * number
                break

    if final_score:
        break

print(f"\nFinal score (Remaining sum * drawn number): {final_score}")
