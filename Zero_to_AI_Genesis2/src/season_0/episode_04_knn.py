import numpy as np

from numpy_utils import accuracy, standardize_apply, standardize_fit, train_test_split


def make_multiclass_data(n_samples: int = 600, seed: int = 42):
    rng = np.random.default_rng(seed)
    n = n_samples // 3
    c0 = rng.normal(loc=[-2.0, -1.0], scale=0.9, size=(n, 2))
    c1 = rng.normal(loc=[2.0, 2.0], scale=0.9, size=(n, 2))
    c2 = rng.normal(loc=[-2.0, 2.5], scale=0.9, size=(n, 2))
    X = np.vstack([c0, c1, c2])
    y = np.hstack([np.zeros(n, dtype=np.int64), np.ones(n, dtype=np.int64), np.full(n, 2, dtype=np.int64)])
    return X, y


def knn_predict(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, k: int = 5):
    preds = []
    for x in X_test:
        d = np.sqrt(((X_train - x) ** 2).sum(axis=1))
        nn_idx = np.argsort(d)[:k]
        vote = np.bincount(y_train[nn_idx]).argmax()
        preds.append(vote)
    return np.array(preds, dtype=np.int64)


def main():
    X, y = make_multiclass_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_ratio=0.2, seed=42)

    mean, std = standardize_fit(X_train)
    X_train = standardize_apply(X_train, mean, std)
    X_test = standardize_apply(X_test, mean, std)

    preds = knn_predict(X_train, y_train, X_test, k=7)
    acc = accuracy(y_test, preds)

    print("\nSeason 2 / Ep 04 - KNN (NumPy)")
    print(f"Accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()
