import time
import tracemalloc

def solve_dfs(n):
    # Tracking sets to achieve O(1) conflict lookups
    cols = set()
    diag1 = set()  # Row - Col constant
    diag2 = set()  # Row + Col constant
    board = [-1] * n
    solutions = []

    def backtrack(row):
        # Stop after finding the first valid solution to measure baseline speed
        if len(solutions) > 0:
            return
        if row == n:
            solutions.append(board.copy())
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            # Place queen and update state
            board[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            # Revert state changes
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return solutions[0] if solutions else None

if __name__ == "__main__":
    # Benchmark tests for the required lower dimensions
    for test_n in [10, 30]:
        print(f"--- Running Exhaustive DFS Baseline for N = {test_n} ---")
        
        tracemalloc.start()
        start_time = time.time()
        
        result = solve_dfs(test_n)
        
        end_time = time.time()
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        execution_time = end_time - start_time
        peak_kb = peak_memory / 1024.0
        
        if result:
            print(f"Success: Valid configuration found!")
            print(f"Execution Latency: {execution_time:.6f} seconds")
            print(f"Peak Memory Demand: {peak_kb:.2f} KB\n")
        else:
            print("Failed to converge.\n")