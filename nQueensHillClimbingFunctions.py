import random
import time


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
            return (found_solution, steps, current_cost)
        current_cost = new_cost


def evaluate_move(board, col, new_row, original_row):
    new_board = board[:]
    new_board[col] = new_row
    new_cost = heuristic_func(new_board)
    if new_cost == 0:
        return (new_board, new_cost, True)
    return (new_board, new_cost, False)


def parallel_hill_climbing(start_board, pool):
    board = start_board[:]
    steps = 0
    current_cost = heuristic_func(board)
    while True:
        found_better = False
        args = [(board, col, new_row, board[col])
                for col in range(len(board))
                for new_row in range(len(board))
                if new_row != board[col]]
        results = pool.starmap(evaluate_move, args)
        for new_board, new_cost, found_solution in results:
            if found_solution:
                return new_board, new_cost, found_solution, steps + 1
            elif new_cost < current_cost:
                board = new_board
                current_cost = new_cost
                found_better = True
                break
        steps += 1
        if not found_better:
            return board, current_cost, False, steps


def print_chess_board(board):
    n = len(board)
    print("\nOne Possible Solution:")
    for i in range(n):
        row = ['_'] * n
        row[board[i]] = 'Q'
        print('|' + '|'.join(row) + '|')
