import numpy as np


class Board:
    def __init__(self, size, queens=[]):
        self.size = size

        # Board starts as 2d matrix of zeros
        self.board = np.zeros((size, size), dtype=int)

        if len(queens) != 0:
            for queen in queens:
                # Flip spot from 0 to 1, to indicate a Queen occupies the location
                self.board[queen.row][queen.col] = 1

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
