import time
import tracemalloc

class TimeoutException(Exception):
    pass

def solve_dfs_with_timeout(n, time_limit=60):
    cols, diag1, diag2 = set(), set(), set()
    board = [-1] * n
    start_clock = time.time()

    def backtrack(row):
        # Force terminate if execution takes longer than the allowed threshold
        if time.time() - start_clock > time_limit:
            raise TimeoutException("Time Limit Exceeded (60s Limit Crossed)")
        if row == n:
            return board.copy()

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            board[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            res = backtrack(row + 1)
            if res:
                return res

            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
        return None

    return backtrack(0)

if __name__ == "__main__":
    # Stress test the exact solver on high-dimensional boards
    for test_n in [50, 100, 500]:
        print(f"--- Running Exhaustive DFS with Timeout for N = {test_n} ---")
        tracemalloc.start()
        start_time = time.time()
        
        try:
            result = solve_dfs_with_timeout(test_n, time_limit=60)
            end_time = time.time()
            _, peak_memory = tracemalloc.get_traced_memory()
            print(f"Success! Time: {end_time - start_time:.6f}s, RAM: {peak_memory/1024:.2f} KB")
        except TimeoutException as e:
            print(f"Status: {e}")
            _, peak_memory = tracemalloc.get_traced_memory()
            print(f"Peak Memory Used Before Timeout: {peak_memory/1024:.2f} KB")
        finally:
            tracemalloc.stop()
        print("-" * 50)