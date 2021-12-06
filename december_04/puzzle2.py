#!/usr/bin/env python3

"""
--- Day 4: Giant Squid ---
--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
"""

INPUT_FILE = "./input.txt"
BOARD_SIZE = 5


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


# Read the input and prepare the variables holding the data
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

# Initially we have each board in our scope
active_boards = [x for x in range(len(boards))]

final_score = None

# Process the input
for number in numbers_drawn:

    new_active_boards = []
    for i in active_boards:

        board_is_active = True
        position = find_number_in_board(number, boards[i])
        if position:
            (row, column) = position
            marked_boards[i][row][column] = True
            remaining_board_sum[i] -= number
            if board_has_just_won(marked_boards[i], row, column):

                board_is_active = False

                # Is this the only board left?
                if len(active_boards) == 1:
                    final_score = remaining_board_sum[i] * number
                    break

        if board_is_active:
            new_active_boards.append(i)

    if final_score:
        break

    active_boards = new_active_boards

print(
    f"\nFinal score of the final winning board (Remaining sum * drawn number): {final_score}"
)
