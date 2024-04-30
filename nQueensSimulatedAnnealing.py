import random
import math
import time
import numpy as np
import multiprocessing as mp
from board import Board
from queen import Queen


def acceptance_probability(old_cost, new_cost, temperature):
    """Calculate the acceptance probability based on the cost difference and temperature."""
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)


def solve_puzzle(board, max_iterations, initial_temperature, cooling_rate):
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


def simulated_annealing(size):
    # Constants:
    max_iterations = 10000000000
    initial_temperature = 1000.0
    cooling_rate = 0.95

    boards = [generate_random_board(size) for _ in range(5)]

    times = []
    for board in boards:
        start_time = time.perf_counter()

        result = solve_puzzle(board, max_iterations, initial_temperature, cooling_rate)

        end_time = time.perf_counter()

        times.append(end_time - start_time)

    return sum(times) / len(times)


def main():
    # Constants:
    max_iterations = 10000000000
    initial_temperature = 1000.0
    cooling_rate = 0.95


    # ======== Multiprocessor ========
    # total_start = time.perf_counter()
    # with mp.Pool() as pool:
    #     results = pool.map(simulated_annealing, range(10, 15))

    #     curr = 10
    #     for i in results:
    #         print(f"Size: {curr}\tTime: {i}")
    #         curr += 1
    # total_end = time.perf_counter()
    # print(f"Total Time: {total_end - total_start}")
    # ======== Multiprocessor ========

    # ======== Single Process ========
    total_start = time.perf_counter()
    for game_size in range(10, 15):

        times = []

        boards = [
                generate_random_board(game_size)
            for _ in range(5)
        ]

        for b in boards:
            start_time = time.perf_counter()
            solve_puzzle(b, max_iterations, initial_temperature, cooling_rate)
            end_time = time.perf_counter()

            times.append(end_time - start_time)

        print(f"{game_size}\t{sum(times)/len(times)}")
        times = []
    total_end = time.perf_counter()
    print(f"Total Time: {total_end - total_start}")
    # ======== Single Process ========


if __name__ == "__main__":
    main()
