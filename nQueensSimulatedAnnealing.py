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


# Example usage:
n = 5  # Board size
max_iterations = 1000
initial_temperature = 1000.0
cooling_rate = 0.95

queens = []

num_of_queens = 4

available_cols = [i for i in range(n)]

for i in range(num_of_queens):
    picked_col = random.choice(available_cols)
    curr_queen = Queen(i, picked_col)

    queens.append(curr_queen)

    available_cols.remove(picked_col)

b = Board(n, queens)

print("START")
b.print()

start = time.perf_counter()
solution = simulated_annealing(b, max_iterations, initial_temperature, cooling_rate)
end = time.perf_counter()


print("END")
solution.print()
print("Time: ", end - start)
