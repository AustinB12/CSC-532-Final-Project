import random
import math
import time
import numpy as np
import multiprocessing as mp
from board import Board
from queen import Queen

max_iterations = 10000000000
initial_temperature = 1000.0
cooling_rate = 0.95
number_of_solutions_to_try = 6


def acceptance_probability(old_cost, new_cost, temperature):
    """Calculate the acceptance probability based on the cost difference and temperature."""
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)


def solve_puzzle(board):
    """Solve the n-queens problem using simulated annealing."""
    current_board = board
    current_cost = current_board.cost()

    temp = initial_temperature
    iteration = 0

    while iteration < max_iterations and current_cost > 0:
        new_board = current_board.generate_neighbor()
        new_cost = new_board.cost()

        ap = acceptance_probability(current_cost, new_cost, temp)

        if ap > random.random():
            current_board = new_board
            current_cost = new_cost

        temp *= cooling_rate
        iteration += 1

    return current_board


def generate_random_board(size):

    available_cols = [i for i in range(size)]
    queens = []

    for row_value in range(size):
        # Choose a col to put it in
        picked_col = random.choice(available_cols)
        curr_queen = Queen(row_value, picked_col)
        queens.append(curr_queen)
        available_cols.remove(picked_col)

    return Board(size, queens)


def simulated_annealing_single(size):
    # Constants:
    max_iterations = 10000000000
    initial_temperature = 1000.0
    cooling_rate = 0.95

    boards = [generate_random_board(size) for _ in range(number_of_solutions_to_try)]

    times = []
    start_time = time.perf_counter()
    for board in boards:

        solve_puzzle(board)

        # times.append(end_time - start_time)
    end_time = time.perf_counter()

    print(f"Total Time for {size} queens: {end_time - start_time}")

def simulated_annealing_multi(size):
    # Constants:
    max_iterations = 10000000000
    initial_temperature = 1000.0
    cooling_rate = 0.95

    boards = [generate_random_board(size) for _ in range(number_of_solutions_to_try)]

    total_start = time.perf_counter()
    with mp.Pool() as pool:
        results = pool.map(solve_puzzle, boards)

        # curr = 10
        # for i in results:
        #     print(f"Size: {curr}\tCost: {i.cost()}")
        #     curr += 1
    total_end = time.perf_counter()
    print(f"Total Time for {size} queens: {total_end - total_start}")


def main():
    # Constants:
    max_iterations = 10000000000
    initial_temperature = 1000.0
    cooling_rate = 0.95


    for i in range(10, 16):
        # simulated_annealing_single(i)
        simulated_annealing_multi(i)


if __name__ == "__main__":
    main()
