import random
import numpy as np
import time

class KMeans:
    def __init__(self, k, max_iter=100):
        self.k = k
        self.max_iter = max_iter
        self.migrations = []
        self.partition_sizes = []

    def fit(self, data: dict[int, np.ndarray]):
        """
        data: mapping mot_id -> cooccurrence vector (np.ndarray)
        Affiche pour chaque itération le temps, le nombre de migrations et la taille de chaque partition.
        """
        self.data = data
        self.ids = list(data.keys())
        X = np.stack([data[i] for i in self.ids])  # shape (V, D)
        V, D = X.shape

        # Initialisation aléatoire des centroïdes
        init_idx = random.sample(range(V), self.k)
        self.centroids = X[init_idx].astype(float)
        self.assignments = np.full(V, -1, dtype=int)

        for it in range(1, self.max_iter + 1):
            start = time.time()
            # Étape d'affectation
            distances = np.linalg.norm(X[:, None, :] - self.centroids[None, :, :], axis=2)
            new_assign = np.argmin(distances, axis=1)

            # Compter les migrations
            migrations = int((new_assign != self.assignments).sum())
            self.migrations.append(migrations)

            # Tailles des partitions
            sizes = np.bincount(new_assign, minlength=self.k)
            self.partition_sizes.append(sizes)

            elapsed = time.time() - start
            print(f"Itération {it} : {elapsed:.2f} secondes. {migrations} migrations.")
            for c, size in enumerate(sizes):
                print(f"Partition {c}\t: {size}.0 mots")
            print("\n" + "*"*40 + "\n")

            # Convergence
            if migrations == 0:
                break

            self.assignments = new_assign
            # Étape de mise à jour des centroïdes
            for c in range(self.k):
                members = X[self.assignments == c]
                if len(members) > 0:
                    self.centroids[c] = members.mean(axis=0)

        return self.assignments

    def top_n(self, n: int) -> dict[int, list[tuple[int, float]]]:
        """
        Pour chaque cluster, retourne une liste de tuples (mot_id, distance) des n mots les plus proches du centroïde.
        """
        results: dict[int, list[tuple[int, float]]] = {}
        for c in range(self.k):
            idxs = np.where(self.assignments == c)[0]
            dists = []
            for idx in idxs:
                mid = self.ids[idx]
                vec = self.data[mid]
                dist = np.linalg.norm(vec - self.centroids[c])
                dists.append((mid, dist))
            dists.sort(key=lambda x: x[1])
            results[c] = dists[:n]
        return results