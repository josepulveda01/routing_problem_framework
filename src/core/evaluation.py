"""
evaluation.py

Funciones para evaluar rutas en TSP/VRP.

Este módulo define una API consistente para:
- calcular costo de rutas
- validar rutas
- trabajar con matrices de distancia o puntos + métrica

Convenciones:
- Las rutas son SECUENCIAS ABIERTAS: (0, 2, 1, 3)
- El cierre del ciclo se maneja en la evaluación (cycle=True)

Esto evita duplicación de lógica en solvers.
"""

from typing import Callable, Iterable

import numpy as np
import numpy.typing as npt


def validate_route(route: Iterable[int], n: int) -> npt.NDArray[np.int_]:
    """
    Valida y normaliza una ruta.

    Args:
        route (Iterable[int]): iterable de índices. Ejemplo: (0,1,2,...,n)
        n(int): número de nodos

    Returns:
        np.ndarray con dtype int

    Raises:
        ValueError si la ruta no es válida
    """
    route_arr = np.asarray(route, dtype=int)

    if route_arr.ndim != 1:
        raise ValueError("La ruta debe ser un array 1D")

    if len(route_arr) != n:
        raise ValueError(f"La ruta debe tener longitud {n}")

    if not np.array_equal(np.sort(route_arr), np.arange(n)):
       raise ValueError("La ruta debe ser una permutación de los nodos")

    return route_arr


def route_cost(
    route: Iterable[int],
    D: npt.NDArray[np.float64],
    cycle: bool = True
) -> float:
    """
    Calcula el costo de una ruta usando matriz de distancias.

    Args:
        route: secuencia de nodos (ruta abierta)
        D: matriz de distancias (n, n)
        cycle: si True, cierra el ciclo

    Returns:
        costo total
    """
    if D.ndim != 2 or D.shape[0] != D.shape[1]:
        raise ValueError("D debe ser una matriz cuadrada")
    
    n = D.shape[0]
    r = validate_route(route, n)

    # aristas consecutivas
    from_nodes = r[:-1]
    to_nodes = r[1:]
    cost = float(np.sum(D[from_nodes, to_nodes])) 
    # D[from, to]_i = D[ r_i, r_{i+1} ]

    if cycle:
        cost += float(D[r[-1], r[0]])

    return cost


def route_cost_from_points(
    route: Iterable[int],
    X: npt.NDArray[np.float64],
    distance: Callable[[npt.NDArray[np.float64], npt.NDArray[np.float64]], float],
    cycle: bool = True
) -> float:
    """
    Calcula costo de ruta directamente desde puntos (sin matriz).

    Más lento que usar D, pero útil para testing o casos pequeños.
    """
    n = X.shape[0]
    r = validate_route(route, n)

    cost = 0.0
    for i in range(n - 1):
        cost += distance(X[r[i]], X[r[i + 1]])

    if cycle:
        cost += distance(X[r[-1]], X[r[0]])

    return cost


def batch_route_cost(
    routes: npt.NDArray[np.int_],
    D: npt.NDArray[np.float64],
    cycle: bool = True
) -> npt.NDArray[np.float64]:
    """
    Calcula costos de múltiples rutas en paralelo.

    Args:
        routes: shape (k, n)
        D: matriz de distancias

    Returns:
        array de shape (k,)
    """
    if routes.ndim != 2:
        raise ValueError("routes debe tener shape (k, n)")

    k, n = routes.shape

    if D.ndim != 2 or D.shape[0] != D.shape[1]:
        raise ValueError("D debe ser una matriz cuadrada")

    if D.shape[0] != n:
        raise ValueError("Dimensiones incompatibles entre routes y D")

    from_nodes = routes[:, :-1] # paths[i,j],   0<=j<=n-2
    to_nodes = routes[:, 1:]    # paths[i,j+1]  0<=j<=n-2

    T = D[from_nodes, to_nodes]
    # D[from,to]_ij = D[from_ij, to_ij] = D[paths[i,j], paths[i,j+1]]
    # 0 <= i <= k,  0 <= j <= n-2
    
    costs = T.sum(axis=1)

    if cycle:
        costs += D[routes[:, -1], routes[:, 0]]

    return costs.astype(np.float64)


def is_valid_route(route: Iterable[int], n: int) -> bool:
    """Versión no-exception para validación."""
    try:
        validate_route(route, n)
        return True
    except ValueError:
        return False
