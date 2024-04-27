import numpy as np
import math


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
