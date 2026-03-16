import numpy as np

from numpy_utils import accuracy, standardize_apply, standardize_fit, train_test_split


def make_binary_data(n_samples: int = 600, seed: int = 42):
    rng = np.random.default_rng(seed)
    n = n_samples // 2
    class0 = rng.normal(loc=[-1.5, -1.0], scale=0.9, size=(n, 2))
    class1 = rng.normal(loc=[1.5, 1.0], scale=0.9, size=(n, 2))
    X = np.vstack([class0, class1])
    y = np.hstack([np.zeros(n, dtype=np.int64), np.ones(n, dtype=np.int64)])
    return X, y


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -40, 40)))


def fit_logistic_regression(X: np.ndarray, y: np.ndarray, lr: float = 0.1, epochs: int = 1200):
    Xb = np.hstack([np.ones((len(X), 1)), X])
    w = np.zeros(Xb.shape[1], dtype=np.float64)

    for _ in range(epochs):
        p = sigmoid(Xb @ w)
        grad = (Xb.T @ (p - y)) / len(X)
        w -= lr * grad
    return w


def predict_proba(X: np.ndarray, w: np.ndarray):
    Xb = np.hstack([np.ones((len(X), 1)), X])
    return sigmoid(Xb @ w)


def predict(X: np.ndarray, w: np.ndarray):
    return (predict_proba(X, w) >= 0.5).astype(np.int64)


def main():
    X, y = make_binary_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_ratio=0.2, seed=42)

    mean, std = standardize_fit(X_train)
    X_train = standardize_apply(X_train, mean, std)
    X_test = standardize_apply(X_test, mean, std)

    w = fit_logistic_regression(X_train, y_train)
    preds = predict(X_test, w)
    acc = accuracy(y_test, preds)

    print("\nSeason 2 / Ep 01 - Logistic Regression")
    print("Learned weights [bias, w1, w2]:", np.round(w, 4))
    print(f"Accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()
