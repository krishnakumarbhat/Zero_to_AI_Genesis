import numpy as np


class PrioritizedReplay:
    def __init__(self, alpha: float = 0.6):
        self.alpha = alpha
        self.items = []
        self.priorities = []

    def add(self, transition, td_error: float, eps: float = 1e-6):
        p = abs(td_error) + eps
        self.items.append(transition)
        self.priorities.append(p)

    def sample(self, batch_size: int = 4, seed: int = 42):
        rng = np.random.default_rng(seed)
        probs = np.array(self.priorities) ** self.alpha
        probs = probs / probs.sum()
        idx = rng.choice(len(self.items), size=batch_size, replace=False, p=probs)
        return [self.items[i] for i in idx], probs[idx], idx


def c51_projection(next_dist, rewards, dones, gamma=0.99, vmin=-10, vmax=10, atoms=51):
    z = np.linspace(vmin, vmax, atoms)
    dz = z[1] - z[0]
    proj = np.zeros_like(next_dist)

    for j in range(atoms):
        tz = rewards + gamma * (1 - dones) * z[j]
        tz = np.clip(tz, vmin, vmax)
        bj = (tz - vmin) / dz
        l = int(np.floor(bj))
        u = int(np.ceil(bj))
        if l == u:
            proj[l] += next_dist[j]
        else:
            proj[l] += next_dist[j] * (u - bj)
            proj[u] += next_dist[j] * (bj - l)
    proj = proj / (proj.sum() + 1e-12)
    return z, proj


class NoisyLinear:
    def __init__(self, in_dim: int, out_dim: int, seed: int = 42):
        rng = np.random.default_rng(seed)
        self.W = rng.normal(0, 0.1, (out_dim, in_dim))
        self.b = np.zeros(out_dim)
        self.W_sigma = np.full((out_dim, in_dim), 0.05)
        self.b_sigma = np.full(out_dim, 0.05)
        self.rng = rng

    def forward(self, x: np.ndarray):
        eps_w = self.rng.normal(0, 1, self.W.shape)
        eps_b = self.rng.normal(0, 1, self.b.shape)
        return (self.W + self.W_sigma * eps_w) @ x + (self.b + self.b_sigma * eps_b)


def main():
    memory = PrioritizedReplay(alpha=0.7)
    td_errors = [0.05, 1.2, 0.3, 2.4, 0.8, 0.02]
    for i, e in enumerate(td_errors):
        memory.add((f"s{i}", f"a{i}"), e)
    samples, probs, idx = memory.sample(batch_size=3)

    next_dist = np.ones(51) / 51
    z, proj = c51_projection(next_dist, rewards=1.5, dones=0.0)

    noisy = NoisyLinear(in_dim=4, out_dim=2)
    y = noisy.forward(np.array([0.5, -0.2, 0.1, 1.0]))

    print("\nSeason 6 / Ep 03 - Rainbow Components")
    print("PER sampled indices:", idx)
    print("PER sampled probs:", np.round(probs, 4))
    print("Distributional RL projected expectation:", round(float((z * proj).sum()), 4))
    print("NoisyNet linear output:", np.round(y, 4))


if __name__ == "__main__":
    main()
