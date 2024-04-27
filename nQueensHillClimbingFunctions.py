# hill_climbing_functions.py
import random
import time
import multiprocessing


def random_board_generator(n):
    board = list(range(n))
    random.shuffle(board)
    return board


def heuristic_func(board):
    n = len(board)
    current_cost = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                current_cost += 1
    return current_cost


def next_board_simple_hill_climbing(board):
    n = len(board)
    current_cost = heuristic_func(board)
    for col in range(n):
        original_row = board[col]
        for new_row in range(n):
            if new_row != original_row:
                board[col] = new_row
                new_cost = heuristic_func(board)
                if new_cost == 0:
                    return board, new_cost, True
                if new_cost < current_cost:
                    return board, new_cost, False
                board[col] = original_row
    return board, current_cost, False


def hill_climbing(start_board):
    board = start_board
    steps = 0
    current_cost = heuristic_func(board)
    while True:
        board, new_cost, found_solution = next_board_simple_hill_climbing(
            board)
        steps += 1
        if new_cost == 0 or new_cost >= current_cost:
            return board, new_cost, found_solution, steps
        current_cost = new_cost


def print_chess_board(board):
    n = len(board)
    print("\nOne Possible Solution:")
    for i in range(n):
        row = ['_'] * n
        row[board[i]] = 'Q'
        print('|' + '|'.join(row) + '|')
