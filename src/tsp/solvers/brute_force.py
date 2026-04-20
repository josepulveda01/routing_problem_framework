""" Este módulo emplea distintos métodos de fuerza bruta para resolver el TSP """

from typing import Callable

import itertools
import numpy as np
import numpy.typing as npt

from src.core.random_points import random_points_generator as rpg
from src.core.metrics import taxicab
from src.core.evaluation import route_cost, route_cost_from_points, batch_route_cost

def tsp_naive(
    X : npt.NDArray[np.float64],
    distance : Callable[ [npt.NDArray[np.float64], npt.NDArray[np.float64]], float ]
) -> tuple[tuple[int, ...], float]:
    """
    Resuelve el TSP por fuerza bruta recalculando distancias.
    
    Evalúa todas las permutaciones posibles fijando el nodo 0 como inicio para reducir
    la complejidad de n! a (n-1)!.
    
    A partir de un conjunto de puntos X = {X_1,X_2,...,X_n}, se codifica cada 

    Args:
        X (npt.NDArray[np.float64]): Puntos de shape (n, d) en R^d.
        distance (Callable[ [npt.NDArray[np.float64], npt.NDArray[np.float64]], float ]):
            Función de distancia.

    Returns:
        tuple[tuple[int, ...], float]:
            - Mejor ruta (tupla de índices)
            - Costo mínimo
    """
    
    n = X.shape[0] # X.shape = (n,d) para n vectores en R^d
    
    best_cost = float("inf")
    best_path = None
    
    for perm in itertools.permutations(range(1, n)):
        path = (0,) + perm

        cost = 0.0
        for i in range(n - 1):
            cost += distance(X[path[i]], X[path[i + 1]])
        cost += distance(X[path[-1]], X[path[0]])

        if cost < best_cost:
            best_cost = cost
            best_path = path
    
    assert best_path is not None # opcional
    return best_path + (best_path[0],), best_cost

if __name__== "__main__":
    X = rpg(5)
    tsp = tsp_naive(X, taxicab)
    print(tsp)
    
    
def tsp_matrix(
    D: npt.NDArray[np.float64]
) -> tuple[tuple[int,...], float]:
    """
    Resuelve el TSP por fuerza bruta utilizando la matriz de distancias.

    Args
        D (npt.NDArray[np.float64]): Matriz de distancias con shape (n, n).

    Returns:
        tuple[tuple[int, ...], float]:
            - Mejor ruta (tupla de índices)
            - Costo mínimo
    """
    
    n = D.shape[0] # X.shape = (n,d) para n vectores en R^d
    
    best_cost = float("inf")
    best_path = None
    
    for perm in itertools.permutations(range(1, n)):
        path = (0,) + perm

        cost = 0.0
        for i in range(n - 1):
            cost += D[path[i], path[i + 1]]

        cost += D[path[-1], path[0]]

        if cost < best_cost:
            best_cost = cost
            best_path = path

    assert best_path is not None
    return best_path, best_cost


def tsp_vectorized(
    D: npt.NDArray[np.float64]
) -> tuple[tuple[int, ...], float]:
    """
    Resuelve el TSP evaluando todas las permutaciones de forma vectorizada.
    
    NOTA:
    - Complejidad en memoria: O( (n-1)! * n )
    - Recomendado para n <= 10
    
    Args:
        D (npt.NDArray[np.float64]): Matriz de distancias (n, n)

    Returns:
        tuple[tuple[int, ...], float]:
            - Mejor ruta (cerrada)
            - Costo mínimo
    """
    
    n = D.shape[0]
    if n < 2:
        raise ValueError("Se requieren al menos 2 nodos para TSP")


    # array ((n-1)!, n-1) con las permutaciones de (1,2,...,n-1)
    perms = np.array(
        list(itertools.permutations(range(1, n))),
        dtype=int
    )

    # array ((n-1)!, n) con las permutaciones, iniciando con 0
    start = np.zeros((perms.shape[0], 1), dtype=int)
    paths = np.concatenate([start, perms], axis=1)

    # array ((n-1)!, n+1) con las permutaciones, iniciando y terminando con 0
    paths_closed = np.concatenate(
        [paths, paths[:, [0]]],
        axis=1
    )

    # Obtener pares (i -> j)
    from_nodes = paths_closed[:, :-1]   # [ [0,1,2,3,...,n-2,n-1], ... ]
    to_nodes   = paths_closed[:, 1:]    # [ [1,2,3,...,n-1,0], ... ]

    # Matriz ( (n-1)!, n) = (#rutas, #aristas) de trayectorias
    T = D[from_nodes, to_nodes]
    # T = [ [ D[0,1],...,D[n-2,n-1],D[n-1,0] ], ... ]
    
    costs = T.sum(axis=1) # costos por trayectorias

    # Mejor solución
    idx = int(np.argmin(costs))

    best_path = tuple(paths_closed[idx])
    best_cost = float(costs[idx])

    return best_path, best_cost

##### TESTING #####

if __name__== "__main__":
    X = rpg(5)
    #print(X)
    x = itertools.permutations(range(1, 5))
    print(x, "/n")
    print(y:=list(x))
    print(np.array(y).shape)