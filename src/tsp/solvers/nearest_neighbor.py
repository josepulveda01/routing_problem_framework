""" Nearest Neighbor heuristic para TSP """

import numpy as np
import numpy.typing as npt

from src.core.evaluation import route_cost


def nearest_neighbor(
    D: npt.NDArray[np.float64],
    start_node: int = 0
) -> tuple[tuple[int, ...], float]: 
    """
    Heurística Nearest Neighbor para TSP a partir de la matriz de distancias.
    Este método funciona para grafos, en general, y no solo para puntos en R^d

    Construye una ruta greedily eligiendo siempre el nodo más cercano
    no visitado.

    Args:
        D (npt.NDArray[np.float64]): matriz de distancias (n, n)
        start (int): nodo inicial

    Returns:
        tuple[tuple[int, ...], float]:
            - ruta abierta (permutación de nodos)
            - costo total (ciclo evaluado vía route_cost)
    """

    if D.ndim != 2 or D.shape[0] != D.shape[1]:
        raise ValueError("D debe ser una matriz cuadrada")

    n = D.shape[0]

    if not (0 <= start_node < n):
        raise ValueError("start fuera de rango")

    visited = np.zeros(n, dtype=bool)
    visited[start_node] = True

    route = [start_node]
    current_node = start_node

    for _ in range(n - 1):
        # distancias desde el nodo actual
        node_distances = D[current_node]

        # ignorar nodos ya visitados
        masked_distances = node_distances.copy()
        masked_distances[visited] = np.inf

        # elegir el más cercano
        next_node = int(np.argmin(masked_distances))

        route.append(next_node)
        visited[next_node] = True
        current_node = next_node

    route_tuple = tuple(route)
    traveled_distance = route_cost(route_tuple, D)

    return route_tuple, traveled_distance


import numpy as np
import numpy.typing as npt
from src.core.evaluation import route_cost


def nearest_neighbor_random_start(
    D: npt.NDArray[np.float64]
) -> tuple[tuple[int, ...], float]:

    n = D.shape[0]
    start_node = int(np.random.randint(0,n))

    return nearest_neighbor(D, start_node)


def nearest_neighbor_all_starts(
    D: npt.NDArray[np.float64],
) -> tuple[tuple[int, ...], float]:

    n = D.shape[0]

    best_route = None
    best_cost = np.inf

    for start_node in range(n):
        route, cost = nearest_neighbor(D, start_node)

        if cost < best_cost:
            best_cost = cost
            best_route = route

    return best_route, best_cost