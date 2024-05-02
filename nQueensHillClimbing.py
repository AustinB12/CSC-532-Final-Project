from nQueensHillClimbingFunctions import random_board_generator, hill_climbing, parallel_hill_climbing, print_chess_board
import time
import multiprocessing
from tqdm import tqdm


def run_single_core_hill_climbing(n_queens, num_iterations):
    results = []
    total_start_time = time.perf_counter()  # Start the total time measurement
    for _ in tqdm(range(num_iterations), desc="Single-core Progress"):
        start_board = random_board_generator(n_queens)
        start_time = time.perf_counter()
        found_solution, steps, cost = hill_climbing(start_board)
        duration = time.perf_counter() - start_time
        results.append((duration, found_solution, steps))
    total_duration = time.perf_counter() - total_start_time  # Total time taken
    return results, total_duration


def run_multi_core_hill_climbing(n_queens, num_iterations):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    results = []
    total_start_time = time.perf_counter()  # Start the total time measurement
    for _ in tqdm(range(num_iterations), desc="Multi-core Hill Climbing Progress"):
        start_board = random_board_generator(n_queens)
        start_time = time.perf_counter()
        board, cost, found_solution, steps = parallel_hill_climbing(
            start_board, pool)
        duration = time.perf_counter() - start_time
        results.append((duration, found_solution, steps))
    pool.close()
    total_duration = time.perf_counter() - total_start_time  # Total time taken
    return results, total_duration


def run_multi_single_core_hill_climbing(n_queens, num_iterations):
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    async_results = []
    total_start_time = time.perf_counter()  # Start the total time measurement
    for _ in tqdm(range(num_iterations), desc="Multi-core Execution of Single-Core Hill Climbing"):
        board = random_board_generator(n_queens)
        start_time = time.perf_counter()
        result = pool.apply_async(hill_climbing, (board,))
        async_results.append((result, start_time))

    pool.close()
    pool.join()

    results = []
    for result, start_time in async_results:
        found_solution, steps, _ = result.get()
        duration = time.perf_counter() - start_time
        results.append((duration, found_solution, steps))
    total_duration = time.perf_counter() - total_start_time  # Total time taken
    return results, total_duration


def analyze_results(results):
    durations = [result[0] for result in results]
    successes = [1 for result in results if result[1]]
    steps = [result[2] for result in results if result[1]]
    average_duration = sum(durations) / len(durations) if durations else 0
    success_rate = (len(successes) / len(results)) * 100 if results else 0
    average_steps = sum(steps) / len(successes) if successes else 0
    return average_duration, success_rate, average_steps


def main():
    n_queens = 8
    num_boards = 15000  # Number of different configurations to try

    print()
    # Single-core processing
    print("Starting Single-Core Hill Climbing...")
    single_results, single_total_time = run_single_core_hill_climbing(
        n_queens, num_boards)
    single_duration, single_success_rate, single_steps = analyze_results(
        single_results)
    print(f"Single-Core - Average Duration: {single_duration} seconds, Total Time: {
          single_total_time} seconds, Success Rate: {single_success_rate}%, Average Steps: {single_steps}")

    # Multi-core processing
    print("Starting Multi-Core Hill Climbing...")
    multi_results, multi_total_time = run_multi_core_hill_climbing(
        n_queens, num_boards)
    multi_duration, multi_success_rate, multi_steps = analyze_results(
        multi_results)
    print(f"Multi-Core - Average Duration: {multi_duration} seconds, Total Time: {
          multi_total_time} seconds, Success Rate: {multi_success_rate}%, Average Steps: {multi_steps}")

    # Multi-core execution of single-core processes
    print("Starting Multi-core Execution of Single-Core Hill Climbing Processes...")
    multi_single_results, multi_single_total_time = run_multi_single_core_hill_climbing(
        n_queens, num_boards)
    multi_single_duration, multi_single_success_rate, multi_single_steps = analyze_results(
        multi_single_results)
    print(f"Multi-Core Single-Core Processes - Average Duration: {multi_single_duration} seconds, Total Time: {
          multi_single_total_time} seconds, Success Rate: {multi_single_success_rate}%, Average Steps: {multi_single_steps}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
