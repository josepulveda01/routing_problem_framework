import time

from src.data.instances import generate_instance
from src.tsp.solvers.nearest_neighbor import (
    nearest_neighbor,
    nearest_neighbor_random_start,
    nearest_neighbor_all_starts,
    two_opt
)

from src.benchmark.db import (
    get_connection,
    init_db,
    insert_instance,
    insert_run
)


SIZES = [10, 20, 50, 100]
SEEDS = range(30)

SOLVERS = {
    "nn": nearest_neighbor,
    "nn_rs": nearest_neighbor_random_start,
    "nn_as": nearest_neighbor_all_starts,
    "two_opt": two_opt
}


def create_instance(n, seed):
    return generate_instance(n, seed)


def run_solver(solver, D):
    start = time.perf_counter()
    route, cost = solver(D)
    end = time.perf_counter()

    return route, cost, (end - start) * 1000


def log(n, solver, seed, cost, time_ms):
    print(f"[n={n}] {solver} | seed={seed} | cost={cost:.4f} | {time_ms:.3f} ms")


def run_benchmark(conn):
    for n in SIZES:
        for seed in SEEDS:

            coords, D = create_instance(n, seed)
            instance_id = insert_instance(conn, n, seed)

            for solver_name, solver in SOLVERS.items():

                try:
                    route, cost, time_ms = run_solver(solver, D)

                    insert_run(
                        conn,
                        instance_id,
                        solver_name,
                        seed,
                        cost,
                        time_ms,
                        route
                    )

                    log(n, solver_name, seed, cost, time_ms)

                except Exception as e:
                    print(f"[ERROR] {solver_name} | n={n} | seed={seed} -> {e}")


def main():
    conn = get_connection()
    init_db(conn)

    print("Starting TSP benchmark...\n")

    run_benchmark(conn)

    conn.close()

    print("\nBenchmark completed.")


if __name__ == "__main__":
    main()
