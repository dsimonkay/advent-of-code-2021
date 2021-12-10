#!/usr/bin/env python3

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
