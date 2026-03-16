import numpy as np


def make_expert_data(n=300, seed=42):
    rng = np.random.default_rng(seed)
    s = rng.uniform(-2, 2, size=(n, 2))
    a = (s[:, 0] + 0.5 * s[:, 1] > 0).astype(np.int64)
    return s, a


def softmax_logits(logits):
    z = logits - logits.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def behavioral_cloning(s, a, epochs=200, lr=0.1):
    W = np.zeros((2, 2))
    b = np.zeros(2)
    y = np.eye(2)[a]

    for _ in range(epochs):
        logits = s @ W + b
        p = softmax_logits(logits)
        grad_logits = (p - y) / len(s)
        W -= lr * (s.T @ grad_logits)
        b -= lr * grad_logits.sum(axis=0)
    return W, b


def gail_like_discriminator(expert_sa, agent_sa, epochs=200, lr=0.05):
    x = np.vstack([expert_sa, agent_sa])
    y = np.hstack([np.ones(len(expert_sa)), np.zeros(len(agent_sa))])
    w = np.zeros(x.shape[1])

    for _ in range(epochs):
        z = x @ w
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        grad = x.T @ (p - y) / len(x)
        w -= lr * grad
    return w


def offline_cql_update(Q, dataset, alpha=0.1, gamma=0.95, lr=0.2):
    for (s, a, r, s2) in dataset:
        td_target = r + gamma * np.max(Q[s2])
        td = td_target - Q[s, a]

        lse = np.log(np.sum(np.exp(Q[s])))
        cql_penalty_grad = np.exp(Q[s]) / np.sum(np.exp(Q[s]))

        Q[s, a] += lr * td
        Q[s] -= lr * alpha * cql_penalty_grad
    return Q


def main():
    s_exp, a_exp = make_expert_data()
    W, b = behavioral_cloning(s_exp, a_exp)
    pred = np.argmax(s_exp @ W + b, axis=1)
    bc_acc = np.mean(pred == a_exp)

    rng = np.random.default_rng(7)
    s_agent = rng.uniform(-2, 2, size=(300, 2))
    a_agent = rng.integers(0, 2, size=300)
    expert_sa = np.hstack([s_exp, a_exp[:, None]])
    agent_sa = np.hstack([s_agent, a_agent[:, None]])
    d_w = gail_like_discriminator(expert_sa, agent_sa)

    Q = np.zeros((6, 2))
    dataset = [(0, 0, 0.5, 1), (1, 1, 0.1, 2), (2, 0, 0.8, 3), (3, 1, -0.2, 4), (4, 0, 1.0, 5)]
    for _ in range(80):
        Q = offline_cql_update(Q, dataset, alpha=0.2)

    print("\nSeason 6 / Ep 06 - Imitation + Offline RL")
    print("Behavioral cloning accuracy:", round(float(bc_acc), 4))
    print("GAIL-like discriminator weight norm:", round(float(np.linalg.norm(d_w)), 4))
    print("Offline CQL-style Q-values at state 0:", np.round(Q[0], 4))


if __name__ == "__main__":
    main()
