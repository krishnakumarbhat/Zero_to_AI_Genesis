import math

import numpy as np
import torch
from torch import nn


def make_series(n_points=1200):
    x = np.linspace(0, 40 * math.pi, n_points)
    y = np.sin(x) + np.random.normal(0, 0.1, size=n_points)
    return y.astype(np.float32)


def make_windows(series, window=30):
    X, y = [], []
    for i in range(len(series) - window):
        X.append(series[i : i + window])
        y.append(series[i + window])
    X = np.array(X)[:, :, None]
    y = np.array(y)[:, None]
    return torch.tensor(X), torch.tensor(y)


class LSTMRegressor(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=1, hidden_size=32, batch_first=True)
        self.head = nn.Linear(32, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.head(out[:, -1, :])


def main():
    series = make_series()
    X, y = make_windows(series)
    X_train, y_train = X[:900], y[:900]
    X_test, y_test = X[900:], y[900:]

    model = LSTMRegressor()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    for _ in range(15):
        pred = model(X_train)
        loss = loss_fn(pred, y_train)
        opt.zero_grad()
        loss.backward()
        opt.step()

    with torch.no_grad():
        test_loss = loss_fn(model(X_test), y_test).item()

    print("\nSeason 3 / Ep 02 - LSTM on Synthetic Sine Wave")
    print(f"Test MSE: {test_loss:.6f}")


if __name__ == "__main__":
    main()
