"""
metrics.py

Este módulo proporciona diferentes métricas para calcular distancias entre vectores en R^d.
Las implementaciones utilizan 'scipy.spatial.distance', aprovechando su optimización en C
para cálculos más eficientes y precisos.

Funciones actuales:
- minkowski(x, y, p): distancia de Minkowski con parámetro p >= 1.
- taxicab(x, y): distancia Manhattan o taxicab (caso p=1 de Minkowski).
- euclidean(x, y): distancia euclídea (caso p=2 de Minkowski).
- uniform(x, y): distancia uniforme o Chebyshev (coincide con p = ∞ en Minkowski).

Todas las funciones validan que los vectores tengan la misma dimensión y lanzan un error en caso contrario.
El módulo está diseñado para poder incorporar nuevas métricas en el futuro.

Ejemplo de uso:
    >>> x = [1, 2, 3]
    >>> y = [4, 0, 3]
    >>> euclidean(x, y)
    3.605551275463989
"""
import numpy as np

from typing import Callable
import numpy.typing as npt

from numpy.typing import ArrayLike
from scipy.spatial import distance

def check_shape(x: ArrayLike, y: ArrayLike):
    x_arr = np.asarray(x).ravel()
    y_arr = np.asarray(y).ravel()
    if x_arr.shape != y_arr.shape:
        raise ValueError("x e y deben tener la misma dimensión")
    

def minkowski(x: ArrayLike, y: ArrayLike, p: float=2) -> float:
    r""" Distancia de Minkowski entre dos vectores en R^d:
    
    d_p(x, y) = ( Σ_i |x_i - y_i|^p )^(1/p), con p >= 1
    
    Args:
        x (ArrayLike) : primer vector.
        y (ArrayLike) : segundo vector.
        p (float) : parámetro de la métrica, debe ser mayor o igual a 1.
    
    Returns (float):
        distancia de Minkowski entre los dos vectores.
        
    Raises:
        ValueError: si los vectores no tienen la misma dimensión o si p < 1.

    """
    if p<1:
        raise ValueError(f"La función no es una métrica si p<1 (valor actual: p={p})")
    check_shape(x,y)
    return distance.minkowski(x,y,p)


def taxicab(x: ArrayLike, y: ArrayLike) -> float:
    r""" Distancia Manhattan (taxicab) entre dos vectores en R^d:
    
    $ d_1(x,y) = \sum_{i=1}^d |x_i - y_i| $ 
    
    Args:
        x (ArrayLike) : primer vector.
        y (ArrayLike) : segundo vector.
    
    Returns (float):
        distancia Manhattan entre los dos vectores.
        
    Raises:
        ValueError: si los vectores no tienen la misma dimensión.
    """
    
    check_shape(x,y)
    return distance.cityblock(x,y)


def euclidean(x: ArrayLike, y: ArrayLike) -> float:
    r""" Distancia euclídea entre dos vectores en R^d:
    
    $ d_2(x,y) = \sqrt{ \sum_{i=1}^d |x_i - y_i|^2 } $ 
    
    Args:
        x (ArrayLike) : primer vector.
        y (ArrayLike) : segundo vector.
    
    Returns (float):
        distancia euclídea entre los dos vectores.
        
    Raises:
        ValueError: si los vectores no tienen la misma dimensión.
    """
    
    check_shape(x,y)
    return distance.euclidean(x,y)


def uniform(x: ArrayLike, y: ArrayLike) -> float:
    r""" Distancia uniforme (Chebyshev) entre dos vectores en R^d:
    
    $ d_\infty(x,y) = max_{i=1,\dots,n} |x_i - y_i|  $ 
    
    Args:
        x (ArrayLike) : primer vector
        y (ArrayLike) : segundo vector
    
    Returns (float):
        distancia uniforme (Chebyshev) entre los dos vectores
        
    Raises:
        ValueError: si los vectores no tienen la misma dimensión.
    """
    
    check_shape(x,y)
    return distance.chebyshev(x,y)


def distance_matrix(
    X: npt.NDArray[np.float64],
    distance : Callable[[npt.NDArray[np.float64], npt.NDArray[np.float64]], float],
) -> npt.NDArray[np.float64]:
    
    n = X.shape[0]
    D = np.zeros((n,n), dtype=np.float64)
    
    # La matriz de distancias es simétrica con 0's en su diagonal
    for i in range(n):
        for j in range(i+1,n):
            d = distance(X[i],X[j])
            D[i,j] = d
            D[j,i] = d
            
    return D

# ----- TESTING ---- 

import random
from random_points import random_points_generator

if __name__ == "__main__":
    points = random_points_generator(n=2)
    x = np.round(points[0],3)
    y = np.round(points[1],3)
    p = np.round(random.uniform(0,5),3)
    
    print(f"\nx={x}")
    print(f"y={y}")
    print(f"p={p}\n")
    
    metrics = [minkowski, taxicab, euclidean, uniform]
    for metric in metrics:
        if metric == minkowski:
            print(f"minkowski(x,y) = {minkowski(x,y,p)} (p={p})")
        else:
            print(f"{metric.__name__}(x,y) = {metric(x,y)}")
    

