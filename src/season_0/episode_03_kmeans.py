import numpy as np


def make_blobs_numpy(n_samples: int = 500, seed: int = 42):
    rng = np.random.default_rng(seed)
    centers = np.array([[-4.0, -3.5], [4.5, 4.0], [-4.0, 4.5], [4.5, -3.0]])
    points_per = n_samples // len(centers)
    X = []
    for c in centers:
        X.append(rng.normal(loc=c, scale=0.9, size=(points_per, 2)))
    X = np.vstack(X)
    return X


def pairwise_distances(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    return np.sqrt(((X[:, None, :] - Y[None, :, :]) ** 2).sum(axis=2))


def kmeans(X: np.ndarray, k: int = 4, max_iter: int = 100, seed: int = 42):
    rng = np.random.default_rng(seed)
    centers = X[rng.choice(len(X), size=k, replace=False)].copy()

    for _ in range(max_iter):
        d = pairwise_distances(X, centers)
        labels = d.argmin(axis=1)

        new_centers = np.array(
            [X[labels == j].mean(axis=0) if np.any(labels == j) else centers[j] for j in range(k)]
        )
        if np.allclose(new_centers, centers, atol=1e-5):
            centers = new_centers
            break
        centers = new_centers
    return labels, centers


def silhouette_score_numpy(X: np.ndarray, labels: np.ndarray) -> float:
    n = len(X)
    unique = np.unique(labels)
    D = pairwise_distances(X, X)
    s = np.zeros(n)

    for i in range(n):
        own = labels[i]
        own_mask = labels == own
        own_mask[i] = False

        if own_mask.sum() == 0:
            a = 0.0
        else:
            a = D[i, own_mask].mean()

        b = np.inf
        for c in unique:
            if c == own:
                continue
            c_mask = labels == c
            if c_mask.sum() > 0:
                b = min(b, D[i, c_mask].mean())

        s[i] = (b - a) / max(a, b, 1e-12)

    return float(np.mean(s))


def main():
    X = make_blobs_numpy(n_samples=500)
    labels, centers = kmeans(X, k=4)
    score = silhouette_score_numpy(X, labels)

    print("\nSeason 2 / Ep 03 - KMeans Clustering")
    print("Centers:\n", np.round(centers, 3))
    print(f"Silhouette score: {score:.4f}")


if __name__ == "__main__":
    main()
