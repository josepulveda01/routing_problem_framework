import numpy as np
import numpy.typing as npt

def random_points_generator(
    n: int = 1,
    d: int = 2,
    seed: int | None = None
) -> npt.NDArray[np.float64]:
    """ Genera n puntos aleatorios uniformes en [0,1)^d
    
    Args:
        n (int): número de puntos, debe ser >= 0
        d (int): dimensión de cada punto, debe ser >= 1
        seed (int | None): semilla para reproducibilidad
    
    Returns:
        npt.NDArray[np.float64]: array de forma (n, d) con valores en [0,1)
    
    Raises:
        TypeError: si n o d no son enteros
        ValueError: si n < 0 o d < 1
    """
    if not isinstance(n, int) or not isinstance(d, int):
        raise TypeError("n y d deben ser enteros")
    if n < 0 or d < 1:
        raise ValueError("n >= 0 y d >= 1")
    
    rng = np.random.default_rng(seed)
    return rng.random((n, d))


# ----- TESTING ------

if __name__ == "__main__":
    # Genera 5 puntos en R^3
    print(f"\n5 puntos en R^2: \n {random_points_generator(n=5, d=3, seed=42)}\n")
    
    # Genera 3 puntos en R^5
    print(f"3 puntos en R^5: \n {random_points_generator(n=3, d=5, seed=42)}\n")
    