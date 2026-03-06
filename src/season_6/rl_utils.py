import numpy as np


class KArmedBandit:
    def __init__(self, k: int = 10, seed: int = 42):
        rng = np.random.default_rng(seed)
        self.true_means = rng.normal(0.0, 1.0, size=k)
        self.rng = rng

    def step(self, action: int) -> float:
        return float(self.rng.normal(self.true_means[action], 1.0))


class GridWorld:
    def __init__(self, size: int = 5, max_steps: int = 40):
        self.size = size
        self.start = (0, 0)
        self.goal = (size - 1, size - 1)
        self.max_steps = max_steps
        self.reset()

    @property
    def n_states(self):
        return self.size * self.size

    @property
    def n_actions(self):
        return 4

    def state_to_idx(self, s):
        return s[0] * self.size + s[1]

    def idx_to_state(self, idx: int):
        return idx // self.size, idx % self.size

    def reset(self):
        self.state = self.start
        self.steps = 0
        return self.state_to_idx(self.state)

    def step(self, action: int):
        r, c = self.state
        if action == 0:
            r = max(0, r - 1)
        elif action == 1:
            r = min(self.size - 1, r + 1)
        elif action == 2:
            c = max(0, c - 1)
        else:
            c = min(self.size - 1, c + 1)

        self.state = (r, c)
        self.steps += 1

        done = self.state == self.goal or self.steps >= self.max_steps
        reward = 10.0 if self.state == self.goal else -1.0
        return self.state_to_idx(self.state), reward, done


def epsilon_greedy(Q_row: np.ndarray, epsilon: float, rng: np.random.Generator) -> int:
    if rng.random() < epsilon:
        return int(rng.integers(0, len(Q_row)))
    return int(np.argmax(Q_row))


def discounted_return(rewards: list[float], gamma: float) -> float:
    g = 0.0
    pow_g = 1.0
    for r in rewards:
        g += pow_g * r
        pow_g *= gamma
    return float(g)
