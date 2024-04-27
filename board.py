import numpy as np
import random
from queen import Queen


class Board:
    def __init__(self, size, queens=[]):
        self.size = size
        self.queens = queens

        # Board starts as 2d matrix of zeros
        self.board = np.zeros((size, size), dtype=int)

        if len(queens) != 0:
            for queen in queens:
                # Flip spot from 0 to 1, to indicate a Queen occupies the location
                self.board[queen.row][queen.col] = 1

    def cost(self):
        total_moves = 0

        for i in range(len(self.queens)):

            queen1 = self.queens[i]
            for j in range(len(self.queens)):
                if i == j:
                    # don't compare a queen to itself
                    continue
                queen2 = self.queens[j]

                q1_sum = queen1.col + queen1.row
                q2_sum = queen2.col + queen2.row

                row_diff = abs(queen1.row - queen2.row)
                col_diff = abs(queen1.col - queen2.col)

                if (
                    queen1.col == queen2.col  # same col
                    or queen1.row == queen2.row  # same row
                    or q1_sum == q2_sum  # diagonal check
                    or row_diff == col_diff  # also diagonal check
                ):
                    total_moves += 1

        return total_moves

    def generate_neighbor(self):

        new_queens = self.queens[:]

        index_of_queen_to_move = random.randint(0, len(self.queens) - 1)

        new_spot_is_accepted = False

        new_row = -1
        new_col = -1

        while new_spot_is_accepted == False:
            new_row = random.randint(0, self.size - 1)
            new_col = random.randint(0, self.size - 1)

            new_spot_is_accepted = True

            for i in self.queens:
                if i.row == new_row and i.col == new_col:
                    new_spot_is_accepted = False

        # Get rid of original queen we selected
        new_queens.pop(index_of_queen_to_move)

        # Add new queen with new coordinates
        new_queens.append(Queen(new_row, new_col))

        # # Reset board queens
        # self.queens = new_queens

        # self.board = np.zeros((self.size, self.size), dtype=int)
        # for queen in self.queens:
        #     # Flip spot from 0 to 1, to indicate a Queen occupies the location
        #     self.board[queen.row][queen.col] = 1

        # return new board
        return Board(self.size, new_queens)

    def print(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    print("Q", end=" ")
                else:
                    if i % 2 == 0:
                        if j % 2 == 0:
                            print("▨", end=" ")
                        else:
                            print("▢", end=" ")
                    else:
                        if j % 2 == 0:
                            print("▢", end=" ")
                        else:
                            print("▨", end=" ")
            print()
