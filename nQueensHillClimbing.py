import random
import time


def random_board_generator(n):
    """Generates a random board configuration for n queens."""
    board = list(range(n))
    random.shuffle(board)
    return board


def heuristic_func(board):
    """Calculates the number of pairs of queens that are attacking each other."""
    n = len(board)
    current_cost = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                current_cost += 1
    return current_cost


def next_board_simple_hill_climbing(board):
    """Finds a neighboring board with a lower heuristic value and checks for solution."""
    n = len(board)
    current_cost = heuristic_func(board)
    for col in range(n):
        original_row = board[col]
        # Try each possible row
        for new_row in range(n):
            if new_row == original_row:
                continue  # Skip if it's the original position
            board[col] = new_row
            new_cost = heuristic_func(board)
            if new_cost == 0:
                return board, new_cost  # Return immediately if a solution is found
            if new_cost < current_cost:
                return board, new_cost  # Return a better state
            board[col] = original_row  # Revert if no improvement
    return board, current_cost  # Return the same board if no better neighbor is found


def print_chess_board(board):
    """Prints the board."""
    n = len(board)
    print("\n")
    for i in range(n):
        row = ['_'] * n
        row[board[i]] = 'Q'
        print('|' + '|'.join(row) + '|')


def main():
    n_queens = 8
    if n_queens <= 3 and n_queens != 1:
        print("No arrangement is possible")
        return

    max_instance = 100
    instance = 0
    solution_found = False

    start_time = time.time()
    while instance < max_instance:
        instance += 1
        board = random_board_generator(n_queens)
        print_chess_board(board)
        current_cost = heuristic_func(board)

        while True:
            board, new_cost = next_board_simple_hill_climbing(board)
            if new_cost == 0 or new_cost >= current_cost:  # Check for solution or no improvement
                break
            current_cost = new_cost

        if new_cost == 0:  # Solution found
            print("\nOne Possible Solution:")
            print_chess_board(board)
            break

    print(f"\nRuntime: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
