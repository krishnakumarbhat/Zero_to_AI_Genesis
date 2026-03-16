import numpy as np

from rl_utils import KArmedBandit, discounted_return


def run_epsilon_greedy(steps: int = 400, epsilon: float = 0.1, seed: int = 42):
    rng = np.random.default_rng(seed)
    env = KArmedBandit(k=10, seed=seed)

    q = np.zeros(10)
    n = np.zeros(10)
    rewards = []

    for _ in range(steps):
        if rng.random() < epsilon:
            a = int(rng.integers(0, 10))
        else:
            a = int(np.argmax(q))
        r = env.step(a)
        n[a] += 1
        q[a] += (r - q[a]) / n[a]
        rewards.append(r)
    return q, rewards, env.true_means


def run_ucb(steps: int = 400, c: float = 1.5, seed: int = 42):
    rng = np.random.default_rng(seed)
    env = KArmedBandit(k=10, seed=seed)

    q = np.zeros(10)
    n = np.zeros(10)
    rewards = []

    for t in range(1, steps + 1):
        bonus = c * np.sqrt(np.log(t + 1) / (n + 1e-9))
        a = int(np.argmax(q + bonus))
        r = env.step(a)
        n[a] += 1
        q[a] += (r - q[a]) / n[a]
        rewards.append(r)
    return q, rewards, env.true_means


def main():
    gamma = 0.97
    q_eps, rewards_eps, truth_eps = run_epsilon_greedy()
    q_ucb, rewards_ucb, truth_ucb = run_ucb()

    g_eps = discounted_return(rewards_eps, gamma)
    g_ucb = discounted_return(rewards_ucb, gamma)

    print("\nSeason 6 / Ep 00 - Exploration Foundations")
    print("Objective: maximize discounted return G_t = sum_k gamma^k R_{t+k+1}")
    print(f"epsilon-greedy top arm est: {np.argmax(q_eps)}, true best: {np.argmax(truth_eps)}")
    print(f"UCB top arm est: {np.argmax(q_ucb)}, true best: {np.argmax(truth_ucb)}")
    print(f"Discounted return epsilon-greedy: {g_eps:.2f}")
    print(f"Discounted return UCB: {g_ucb:.2f}")


if __name__ == "__main__":
    main()
