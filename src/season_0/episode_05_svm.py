import numpy as np

from numpy_utils import accuracy, standardize_apply, standardize_fit, train_test_split


def make_binary_data(n_samples: int = 600, seed: int = 42):
    rng = np.random.default_rng(seed)
    n = n_samples // 2
    c0 = rng.normal(loc=[-2.0, -1.5], scale=1.0, size=(n, 2))
    c1 = rng.normal(loc=[2.0, 1.5], scale=1.0, size=(n, 2))
    X = np.vstack([c0, c1])
    y = np.hstack([np.full(n, -1, dtype=np.int64), np.full(n, 1, dtype=np.int64)])
    return X, y


def fit_linear_svm(X: np.ndarray, y: np.ndarray, lr: float = 0.01, lambda_reg: float = 0.01, epochs: int = 1000):
    n_samples, n_features = X.shape
    w = np.zeros(n_features)
    b = 0.0

    for _ in range(epochs):
        for i in range(n_samples):
            margin = y[i] * (X[i] @ w + b)
            if margin >= 1:
                w -= lr * (2 * lambda_reg * w)
            else:
                w -= lr * (2 * lambda_reg * w - y[i] * X[i])
                b -= lr * (-y[i])
    return w, b


def predict(X: np.ndarray, w: np.ndarray, b: float):
    scores = X @ w + b
    return np.where(scores >= 0, 1, -1)


def main():
    X, y = make_binary_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_ratio=0.2, seed=42)

    mean, std = standardize_fit(X_train)
    X_train = standardize_apply(X_train, mean, std)
    X_test = standardize_apply(X_test, mean, std)

    w, b = fit_linear_svm(X_train, y_train, lr=0.003, lambda_reg=0.02, epochs=80)
    preds = predict(X_test, w, b)
    acc = accuracy(y_test, preds)

    print("\nSeason 2 / Ep 05 - Linear SVM (NumPy)")
    print("Weights:", np.round(w, 4), "bias:", round(b, 4))
    print(f"Accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()
