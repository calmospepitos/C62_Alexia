import numpy as np

class Similarity:
    def compute(self, u: np.ndarray, v: np.ndarray) -> float:
        """Calculer la similarité (ou la distance) entre deux vecteurs. Les sous-classes doivent surcharger cette méthode."""
        raise NotImplementedError("Les sous-classes doivent implémenter compute().")

class DotProduct(Similarity):
    def compute(self, u: np.ndarray, v: np.ndarray) -> float:
        return np.dot(u, v)

class LeastSquares(Similarity):
    def compute(self, u: np.ndarray, v: np.ndarray) -> float:
        return np.sum((u - v)**2)

class CityBlock(Similarity):
    def compute(self, u: np.ndarray, v: np.ndarray) -> float:
        return np.sum(np.abs(u - v))
