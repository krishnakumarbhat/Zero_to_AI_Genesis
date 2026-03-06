import numpy as np

from numpy_utils import accuracy, train_test_split


def make_multiclass_data(n_samples: int = 600, seed: int = 42):
    rng = np.random.default_rng(seed)
    n = n_samples // 3
    c0 = rng.normal(loc=[-2.0, -1.5], scale=0.8, size=(n, 2))
    c1 = rng.normal(loc=[2.2, 1.8], scale=0.8, size=(n, 2))
    c2 = rng.normal(loc=[-2.0, 2.5], scale=0.8, size=(n, 2))
    X = np.vstack([c0, c1, c2])
    y = np.hstack(
        [
            np.zeros(n, dtype=np.int64),
            np.ones(n, dtype=np.int64),
            np.full(n, 2, dtype=np.int64),
        ]
    )
    return X, y


def gini(y: np.ndarray):
    if len(y) == 0:
        return 0.0
    counts = np.bincount(y)
    p = counts / len(y)
    return 1.0 - np.sum(p**2)


def majority_class(y: np.ndarray):
    return int(np.bincount(y).argmax())


class SimpleDecisionTree:
    def __init__(self, max_depth: int = 4, min_samples_split: int = 10, feature_subsample: int | None = None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.feature_subsample = feature_subsample
        self.tree = None

    def _best_split(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        feature_ids = np.arange(n_features)
        if self.feature_subsample is not None and self.feature_subsample < n_features:
            rng = np.random.default_rng()
            feature_ids = rng.choice(feature_ids, size=self.feature_subsample, replace=False)

        best = {"gain": -1.0, "feature": None, "threshold": None}
        parent_impurity = gini(y)

        for f in feature_ids:
            thresholds = np.unique(X[:, f])
            for t in thresholds:
                left = X[:, f] <= t
                right = ~left
                if left.sum() == 0 or right.sum() == 0:
                    continue
                impurity = (left.sum() / n_samples) * gini(y[left]) + (right.sum() / n_samples) * gini(y[right])
                gain = parent_impurity - impurity
                if gain > best["gain"]:
                    best = {"gain": gain, "feature": int(f), "threshold": float(t)}
        return best

    def _build(self, X: np.ndarray, y: np.ndarray, depth: int):
        if depth >= self.max_depth or len(np.unique(y)) == 1 or len(y) < self.min_samples_split:
            return {"leaf": True, "class": majority_class(y)}

        split = self._best_split(X, y)
        if split["feature"] is None or split["gain"] <= 1e-12:
            return {"leaf": True, "class": majority_class(y)}

        f = split["feature"]
        t = split["threshold"]
        left_mask = X[:, f] <= t
        right_mask = ~left_mask

        return {
            "leaf": False,
            "feature": f,
            "threshold": t,
            "left": self._build(X[left_mask], y[left_mask], depth + 1),
            "right": self._build(X[right_mask], y[right_mask], depth + 1),
        }

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.tree = self._build(X, y, 0)
        return self

    def _predict_one(self, x: np.ndarray, node: dict):
        if node["leaf"]:
            return node["class"]
        if x[node["feature"]] <= node["threshold"]:
            return self._predict_one(x, node["left"])
        return self._predict_one(x, node["right"])

    def predict(self, X: np.ndarray):
        return np.array([self._predict_one(x, self.tree) for x in X], dtype=np.int64)


class SimpleRandomForest:
    def __init__(self, n_trees: int = 25, max_depth: int = 4, min_samples_split: int = 10):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees: list[SimpleDecisionTree] = []

    def fit(self, X: np.ndarray, y: np.ndarray):
        rng = np.random.default_rng(42)
        n_samples, n_features = X.shape
        feature_subsample = max(1, int(np.sqrt(n_features)))

        self.trees = []
        for _ in range(self.n_trees):
            idx = rng.integers(0, n_samples, size=n_samples)
            Xb, yb = X[idx], y[idx]
            tree = SimpleDecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                feature_subsample=feature_subsample,
            )
            tree.fit(Xb, yb)
            self.trees.append(tree)
        return self

    def predict(self, X: np.ndarray):
        votes = np.array([tree.predict(X) for tree in self.trees])
        out = []
        for i in range(X.shape[0]):
            out.append(np.bincount(votes[:, i]).argmax())
        return np.array(out, dtype=np.int64)


def main():
    X, y = make_multiclass_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_ratio=0.2, seed=42)

    tree = SimpleDecisionTree(max_depth=4, min_samples_split=8)
    tree.fit(X_train, y_train)
    tree_acc = accuracy(y_test, tree.predict(X_test))

    forest = SimpleRandomForest(n_trees=35, max_depth=5, min_samples_split=8)
    forest.fit(X_train, y_train)
    forest_acc = accuracy(y_test, forest.predict(X_test))

    print("\nSeason 2 / Ep 02 - Decision Trees & Random Forest")
    print(f"Decision Tree Accuracy: {tree_acc:.4f}")
    print(f"Random Forest Accuracy: {forest_acc:.4f}")


if __name__ == "__main__":
    main()
