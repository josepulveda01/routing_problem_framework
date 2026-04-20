import numpy as np
import numpy.typing as npt

from src.core.evaluation import route_cost


def two_opt_naive(
    route: tuple[int, ...],
    D: npt.NDArray[np.float64],
    max_iter: int = 100
) -> tuple[tuple[int, ...], float]:
    """
    Implementación de 2-opt naive para el TSP.
    
    Recomputa el costo de ruta para cada intercambio.
    Útil como baseline para benchmarking en 2-opt.
    """

    n = len(route)
    route = list(route)

    best_cost = route_cost(tuple(route), D)
    improved = True
    iteration = 0

    while improved and iteration < max_iter:
        improved = False
        iteration += 1

        for i in range(1, n - 1):
            for j in range(i + 1, n):
                
                # salta aristas adyacentes
                if j == i + 1:
                    continue

                # swap de aristas + reversión
                new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                new_cost = route_cost(tuple(new_route), D)

                if new_cost < best_cost:
                    route = new_route
                    best_cost = new_cost
                    improved = True

    return tuple(route), best_cost


def two_opt(
    route: tuple[int, ...],
    D: npt.NDArray[np.float64],
    max_iter: int = 100
) -> tuple[tuple[int, ...], float]:
    """
    Implementación de 2-opt para el TSP.
    
    A diferencia del caso naive, mejora el rendimiento mediante intercambio de aristas
    y evaluación delta.
    """

    n = len(route)
    route = list(route)
    
    def compute_delta(i: int, j: int) -> float:
        a, b = route[i - 1], route[i]
        c, d = route[j], route[j + 1]
        
        removed = D[a, b] + D[c, d]
        added = D[a, c] + D[b, d]   
        
        return added - removed

    improved = True
    iteration = 0

    while improved and iteration < max_iter:
        improved = False
        iteration += 1

        for i in range(1, n - 1):
            for j in range(i + 1, n-1):

                if j == i + 1:
                    continue

                delta = compute_delta(i, j)
                if delta < 0:
                    route[i:j + 1] = reversed(route[i:j + 1])
                    improved = True

    final_route = tuple(route)
    final_cost = route_cost(final_route, D)

    return final_route, final_cost
