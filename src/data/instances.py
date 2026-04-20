import numpy as np

def generate_instance(n: int, seed: int):
    rng = np.random.default_rng(seed)

    coords = rng.random((n, 2))  # puntos en [0,1]^2

    # matriz de distancias euclidianas
    diff = coords[:, None, :] - coords[None, :, :]
    D = np.sqrt((diff ** 2).sum(axis=2))

    return coords, D
