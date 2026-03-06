import numpy as np

from numpy_utils import mse, train_test_split


def make_regression_data(n_samples: int = 500, noise_std: float = 0.8, seed: int = 42):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n_samples, 3))
    true_w = np.array([3.5, -2.0, 1.25])
    bias = 4.0
    y = X @ true_w + bias + rng.normal(0, noise_std, size=n_samples)
    return X, y


def fit_linear_regression_normal_eq(X: np.ndarray, y: np.ndarray):
    Xb = np.hstack([np.ones((len(X), 1)), X])
    w = np.linalg.pinv(Xb.T @ Xb) @ Xb.T @ y
    return w


def predict_linear(X: np.ndarray, w: np.ndarray):
    Xb = np.hstack([np.ones((len(X), 1)), X])
    return Xb @ w


def main():
    X, y = make_regression_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_ratio=0.2, seed=42)

    w = fit_linear_regression_normal_eq(X_train, y_train)
    preds = predict_linear(X_test, w)
    loss = mse(y_test, preds)

    print("\nSeason 2 / Ep 00 - Linear Regression")
    print("Learned weights [bias, w1, w2, w3]:", np.round(w, 4))
    print(f"MSE: {loss:.4f}")


if __name__ == "__main__":
    main()
