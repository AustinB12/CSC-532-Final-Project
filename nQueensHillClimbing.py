import random
import copy
from board import Board
from queen import Queen


def heuristic_func(board):
    curr_cost = 0
    queens = board.queens
    n_queens = len(queens)
    for i in range(n_queens):
        r1 = queens[i].row
        c1 = queens[i].col
        for j in range(i+1, n_queens):
            r2 = queens[j].row
            c2 = queens[j].col
            if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                curr_cost += 1
    return curr_cost


def hill_climbing(board, max_iterations):
    current_board = board

    current_conflicts = heuristic_func(board)

    for _ in range(max_iterations):
        if current_conflicts == 0:
            print("Solution found!")
            return current_board

        # pick a random queen
        queens = current_board.queens
        random_queen_index = random.randint(0, len(current_board.queens) - 1)

        random_queen = queens[random_queen_index]

        best_board_step = None
        best_step_conflicts = None
        # Move the queen to the lowest conflict position within a radius of 1 of its original location
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                new_row = random_queen.row + i
                new_col = random_queen.col + j

                if new_row < 0 or new_row >= current_board.size or new_col < 0 or new_col >= current_board.size:
                    continue

                new_board = copy.deepcopy(current_board)
                new_queen = Queen(new_row, new_col)
                new_board.queens[random_queen_index] = new_queen

                new_conflicts = heuristic_func(new_board)

                if new_conflicts < current_conflicts:
                    best_board_step = new_board
                    best_step_conflicts = new_conflicts
        if best_board_step is None:
            print("Local minimum found.")
        elif best_step_conflicts < current_conflicts:
            current_board = best_board_step
            current_conflicts = best_step_conflicts
            print("Found better position for queen with less conflicts:",
                  current_conflicts, best_step_conflicts)

            print("==========")
            board.print()
            print("==========")
            best_board_step.print()
            print("==========")

    return current_board


def main():
    board_size = 8
    max_iterations = 100
    max_restarts = 100
    num_of_queens = 8

    queens = []
    for _ in range(num_of_queens):
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        curr_queen = Queen(row, col)
        queens.append(curr_queen)

    board = Board(board_size, queens)
    board2 = hill_climbing(board, max_iterations)

    print("Initial board:")
    board.print()
    print("Final board:")
    board2.print()

    print("Initial conflicts:", heuristic_func(board),
          "Final conflicts:", heuristic_func(board2))


main()
