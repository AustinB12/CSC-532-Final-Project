import random
import math
import time
import numpy as np
from board import Board
from queen import Queen


# def cost(queens):
#     """Calculate the number of pairs of queens that are attacking each other."""
#     n = len(queens)
#     total_attacks = 0
#     for i in range(n):
#         for j in range(i + 1, n):
#             if queens[i] == queens[j] or abs(queens[i] - queens[j]) == abs(i - j):
#                 total_attacks += 1
#     return total_attacks


# def neighbor(queens):
#     """Generate a neighboring solution by randomly moving one queen."""
#     n = len(queens)
#     new_queens = queens[:]
#     i = random.randint(0, n - 1)
#     j = random.randint(0, n - 1)
#     new_queens[i] = j
#     return new_queens


def acceptance_probability(old_cost, new_cost, temperature):
    """Calculate the acceptance probability based on the cost difference and temperature."""
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)


def simulated_annealing(board, max_iterations, initial_temperature, cooling_rate):
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


# Constants:
max_iterations = 10000000000
initial_temperature = 1000.0
cooling_rate = 0.95

for game_size in range(10, 21):
    
    times = []
    
    for iteration in range(50):
        available_cols = [i for i in range(game_size)]

        queens = []

        for row_value in range(game_size):
            # Choose a col to put it in
            picked_col = random.choice(available_cols)

            curr_queen = Queen(row_value, picked_col)
            queens.append(curr_queen)
            available_cols.remove(picked_col)

        # Create our game board
        b = Board(game_size, queens)

        # print("START")
        # b.print()

        start_time = time.perf_counter()
        solution = simulated_annealing(b, max_iterations, initial_temperature, cooling_rate)
        end_time = time.perf_counter()
        
        times.append(end_time - start_time)

    # print("END")
    # solution.print()
    print(f"{game_size}\t{sum(times)/len(times)}\t{"Solved" if solution.cost() == 0 else "Unsolved"}")
    times = []
