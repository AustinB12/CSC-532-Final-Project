# compare_hill_climbing.py
from nQueensHillClimbingFunctions import random_board_generator, hill_climbing, print_chess_board
import time
import multiprocessing
from tqdm import tqdm


def run_single_core_hill_climbing(n_queens, num_iterations):
    results = []
    for _ in tqdm(range(num_iterations), desc="Single-core Progress"):
        start_board = random_board_generator(n_queens)
        start_time = time.perf_counter()
        board, cost, found_solution, steps = hill_climbing(start_board)
        duration = time.perf_counter() - start_time
        results.append((duration, found_solution, steps))
    return results


def run_multi_core_hill_climbing(n_queens, num_iterations):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    start_time = time.perf_counter()
    async_results = [pool.apply_async(hill_climbing, (random_board_generator(
        n_queens),)) for _ in tqdm(range(num_iterations), desc="Multi-core Progress")]
    pool.close()
    pool.join()
    end_time = time.perf_counter()
    results = [result.get() for result in async_results]
    total_duration = end_time - start_time
    return [(total_duration / num_iterations, found_solution, steps) for (board, cost, found_solution, steps) in results]


def analyze_results(results):
    durations = [result[0] for result in results]
    successes = [1 for result in results if result[1]]
    steps = [result[2] for result in results if result[1]]
    average_duration = sum(durations) / len(results) if durations else 0
    success_rate = (len(successes) / len(results)) * 100 if results else 0
    average_steps = sum(steps) / len(successes) if successes else 0
    return average_duration, success_rate, average_steps


def main():
    n_queens = 16
    num_boards = 10000  # Number of different configurations to try

    # Measure total time for single-core processing
    start_time = time.perf_counter()
    print("Starting Single-Core Hill Climbing...")
    single_results = run_single_core_hill_climbing(n_queens, num_boards)
    single_duration, single_success_rate, single_steps = analyze_results(
        single_results)
    total_single_duration = time.perf_counter() - start_time
    print(f"Single-Core - Total Duration: {total_single_duration} seconds, Average Duration: {
          single_duration} seconds, Success Rate: {single_success_rate}, Average Steps: {single_steps}")

    # Measure total time for multi-core processing
    start_time = time.perf_counter()
    print("Starting Multi-Core Hill Climbing...")
    multi_results = run_multi_core_hill_climbing(n_queens, num_boards)
    multi_duration, multi_success_rate, multi_steps = analyze_results(
        multi_results)
    total_multi_duration = time.perf_counter() - start_time
    print(f"Multi-Core - Total Duration: {total_multi_duration} seconds, Average Duration: {
          multi_duration} seconds, Success Rate: {multi_success_rate}, Average Steps: {multi_steps}")


if __name__ == "__main__":
    main()
